#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Lewis Kunik - University of Utah
# Contact: lewis.kunik@utah.edu
#
# Created on Tue Oct 24 2023
#
#

#########################################
# Import packages
#########################################
#%%
# File system packages
import os  # operating system library
import sys
import glob
from pathlib import Path
import copy
import re

# runtime packages
import warnings
import rasterio.errors
warnings.filterwarnings('ignore', category=rasterio.errors.NotGeoreferencedWarning)
import gc

# numerical/data management packages
import math
import numpy as np
import xarray as xr  # for multi dimensional data
import rioxarray as rxr
import pandas as pd
import xesmf as xe
import struct
from rasterio.enums import Resampling

# shapefile/geospatial packages

# time and date packages
import time
from datetime import datetime as dt  # date time library
from datetime import timedelta

# plotting packages
from matplotlib import pyplot as plt  # primary plotting module
from shapely.geometry import mapping
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter as FFmt  # need this for formatting plot ticks
import cartopy.crs as ccrs  #
from cartopy.io import img_tiles  # cartopy's implementation of webtiles
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature


#########################################
# Define Global Filepaths
#########################################
#%%

GCOM_basedir = "/uufs/chpc.utah.edu/common/home/lin-group28/ltk/GCOM-C/RSRF/raw_h5/"
out_basedir = '/uufs/chpc.utah.edu/common/home/lin-group28/ltk/GCOM-C/RSRF/CV-MVC/pre-fill/QCfilt_basic/'
plot_basedir = '/uufs/chpc.utah.edu/common/home/lin-group19/ltk/GCOM-C/plots/maps/CV-MVC/pre-fill/QCfilt_basic/'




#########################################
# Define Global functions
#########################################

def floor(value, decimal_digits):
  scale = (10**decimal_digits)
  return  np.floor(value * scale)/scale

def ceil(value, decimal_digits):
  scale = (10**decimal_digits)
  return  np.ceil(value * scale)/scale


def binary(str_in, num_bits = 16):

    bit_format=f'0{num_bits}b'
    if np.isnan(str_in):
        return num_bits*'1'
    else:
        return format(int(str_in), bit_format)

binary_v = np.vectorize(binary)

def get_bits(str, start_bit, end_bit):
    if start_bit == 0:
        str_split = [*str][-(end_bit+1):]
    else:
        str_split = [*str][-(end_bit+1):-(start_bit)]
    return ''.join(str_split)

get_bits_v = np.vectorize(get_bits)


tanh_v = np.vectorize(np.tanh)

arccos_v = np.vectorize(np.arccos)

def rad_to_deg(rad):
   return rad*180/math.pi

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def td_min(td):
    return td.seconds//60

def td_sec(td):
    return td.seconds%60


def get_GCOM_files_filedates(GCOM_sitedir):
    GCOM_files = []
    GCOM_filedates = []
    GCOM_siteyear_dirs = sorted(glob.glob(os.path.join(GCOM_sitedir, '*/'))) # get list of year directories for this tile

    # siteyear_dir = GCOM_siteyear_dirs[0]
    for siteyear_dir in GCOM_siteyear_dirs:
        YYYY = os.path.basename(os.path.normpath(siteyear_dir))
        print(f'getting files from year {YYYY}')
        sitemonth_dirs = sorted(glob.glob(os.path.join(siteyear_dir, '*/'))) # get list of month directories for this tile-year
        # sitemonth_dir = sitemonth_dirs[0]
        for sitemonth_dir in sitemonth_dirs:
            MM = os.path.basename(os.path.normpath(sitemonth_dir))
            siteday_dirs = sorted(glob.glob(os.path.join(sitemonth_dir, '*/'))) # get list of day directories for this tile-year-month
            # siteday_dir = siteday_dirs[0]
            for siteday_dir in siteday_dirs:
                DD = os.path.basename(os.path.normpath(siteday_dir))
                local_files = sorted(glob.glob(os.path.join(siteday_dir, f'GC1SG1_{YYYY}{MM}{DD}D*.h5')))
                if len(local_files) > 0:
                    filedate = dt.strptime(f'{YYYY}{MM}{DD}', '%Y%m%d').date()
                    GCOM_files.append(local_files[0]) # get list of files for this tile-year-month-day
                    GCOM_filedates.append(filedate)

    return GCOM_files, GCOM_filedates



####################################
### Set up map parameters
####################################
#%%
# use Google Satellite imagery as basemap
tiler = img_tiles.GoogleTiles(style='satellite')
crs = tiler.crs # set crs of map tiler
alpha = 0.8  # transparency 0-1
transform = ccrs.PlateCarree()  # transform specifies the crs that the data is in

### Load state boundaries
fn = shpreader.natural_earth(
   resolution='10m', category='cultural', 
   name='admin_1_states_provinces',
)

reader = shpreader.Reader(fn)
states = [x for x in reader.records() if x.attributes["admin"] == "United States of America"] # get all states in US
states_geom = cfeature.ShapelyFeature([x.geometry for x in states], ccrs.PlateCarree())

# ### Create a custom colormap
# plot_colors = ["#ffffb2", "#fd8d3c", "#f03b20", "#810f7c", "#21013B"]
# cmap = mcolors.ListedColormap(plot_colors)
# cmaplist = [cmap(i) for i in range(cmap.N)] # extract all colors from the cmap

# # create the new map
# cmap = mcolors.LinearSegmentedColormap.from_list(
#     'Custom cmap', cmaplist, cmap.N)

tiler_zoom = 5  # define a zoom level of detail
plot_extent = [-128, -106, 39, 51]  # [minx, maxx, miny, maxy], bounds for western US



def get_tile_plot_extent(dat_xr_curv):
    lat_min = float(dat_xr_curv['lat'].min())
    lat_max = float(dat_xr_curv['lat'].max())
    lon_min = float(dat_xr_curv['lon'].min())
    lon_max = float(dat_xr_curv['lon'].max())
    plot_extent =[lon_min, lon_max, lat_min, lat_max]

    # special case if some lon values cross the 180 meridian, then lon_max will be 
    # large because it extends into Russia (lon ~ +100 to +180)
    if ((lon_min < -175) & (lon_max > 100)):
        lon_neg = dat_xr_curv.lon.values.copy()
        lon_neg[lon_neg > 0] = np.nan
        plot_extent = [-179.99, np.nanmax(lon_neg), lat_min, lat_max]

    return plot_extent


def test_plot(dat_da, plot_title, zlab, plot_extent = None, plot_filename = None, plot_min = None, plot_max = None):
    if plot_extent is None:
        plot_extent = get_tile_plot_extent(dat_da)
    if plot_min is None:
        plot_min = float(dat_da.nanmin())
    if plot_max is None:
        plot_max = float(dat_da.nanmax())
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': crs}) # establish the figure, axes
    ax.set_extent(plot_extent, crs=ccrs.PlateCarree())  # PlateCarree is default lat/lon    
    ax.add_image(tiler, tiler_zoom, interpolation='none') # Add base image
    # ax.add_feature(states_geom, facecolor="none", edgecolor="black", linewidth=1) # add state boundaries to the map
    dat_da.plot(ax=ax, x='lon', y='lat', transform=transform, 
                    alpha=alpha, cmap='inferno_r',
                    vmin=plot_min, vmax=plot_max,
                    cbar_kwargs={'orientation': 'vertical',
                                            'pad': 0.05,
                                            'label': zlab,
                                            'shrink': 0.75})

    plt.title(plot_title, fontsize=18)
    plt.xlabel('lon', fontsize=15)
    plt.ylabel('lat', fontsize=14)

    if plot_filename is not None:
        if not os.path.exists(os.path.dirname(plot_filename)):
            Path(os.path.dirname(plot_filename)).mkdir(parents=True, exist_ok=True)
        plt.savefig(plot_filename, format = "png", bbox_inches = "tight")
        plt.close('all')
    else:
        plt.show()


#########################################
# Define Global Variables and constants
#########################################
#%%

# view zenith angle above which we will exclude obs for "case 2", based on "HIGHVIEW" flag here
# https://landweb.modaps.eosdis.nasa.gov/NPP/forPage/VIIRS_NPP_Surf_Refl_UserGuide_v1.1.pdf
# VZA_thresh = 45 

min_Valid_obs_for_composite = 4

# Total number of global tiles in horz and vert directions for GCOM-C SGLI
v_tile_num = 18
h_tile_num = 36
#########################################
# Begin main
#########################################
#%%


def main():

    # mark start time to keep track of elapsed
    start_total = time.time()

    GCOM_tile = sys.argv[1] # #'h10v04'
    composite_year = int(sys.argv[2]) # command line argument
    composite_period = int(sys.argv[3]) # command line argument
    QC_option = sys.argv[4] # command line argument - default = 'basic'

    GCOM_sitedir = os.path.join(GCOM_basedir, GCOM_tile)
    GCOM_files, GCOM_filedates = get_GCOM_files_filedates(GCOM_sitedir)

    out_dir = os.path.join(out_basedir, GCOM_tile)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    outfile = os.path.join(out_dir, f'GC1SG1_RSRF_{GCOM_tile}_250m_16day_CV-MVC_QCfilt_{QC_option}_{composite_year}-{str(composite_period).zfill(2)}.nc')

    plot_dir = os.path.join(plot_basedir, GCOM_tile)
    Path(plot_dir).mkdir(parents=True, exist_ok=True)

    GCOM_filedoys = [int(date.strftime('%j')) for date in GCOM_filedates]
    DOY_composite_starts = np.arange(1, 366, 16)
    GCOM_file_composite_periods = np.searchsorted(DOY_composite_starts, GCOM_filedoys, side='right') - 1


    if os.path.exists(outfile):
        print(f'Output file {os.path.basename(outfile)} already exists, skipping processing for {composite_year}-{str(composite_period).zfill(2)}')
        # sys.exit(0)


    iYYMM = [ i for i in range(len(GCOM_filedates)) if ((GCOM_filedates[i].year == composite_year) &
                                                    (GCOM_file_composite_periods[i] == composite_period)) ]
    dat_xrs = []

    if len(iYYMM) == 0:
        print(f'No files found for {composite_year}-{str(composite_period).zfill(2)}, skipping processing')
        # sys.exit(0)

    tot_gridcells_16day = 0
    tot_orig_nonNA_16day = 0


    num_iter = 0
    ii = iYYMM[num_iter] 
    for num_iter, ii in enumerate(iYYMM):
        
        file = GCOM_files[ii]
        filedate = GCOM_filedates[ii]
        print(f'Processing file {num_iter+1} of {len(iYYMM)}: {os.path.basename(file)} - date: {filedate}')

        if os.stat(file).st_size == 0:
            print(f'    File {os.path.basename(file)} is empty, skipping')
            continue
        # print(f'    loading file: {os.path.basename(file)} - 1km data')

        tile_match = re.search(r'_T(\d{4})_', file)
        tile_num = tile_match.group(1)
        v_tile = int(tile_num[:2])  # vertical tile number
        h_tile = int(tile_num[2:])  # horizontal tile number

        ### Open h5 vars using rioxarray
        try:

            # Read the visible/NIR bands using rioxarray
            # vn01_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN01')
            # vn02_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN02')
            # vn03_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN03')
            # vn04_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN04')
            vn05_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN05') # For CCI, PRI
            vn06_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN06') # For PRI
            # vn07_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN07')
            vn08_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN08') # For CCI, NDVI
            # vn09_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN09')
            vn10_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN10') 
            vn11_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/Rs_VN11') # FOR NDVI
            qa_raw = rxr.open_rasterio(f'HDF5:"{file}"://Image_data/QA_flag')
            SZA_raw = rxr.open_rasterio(f'HDF5:"{file}"://Geometry_data/Solar_zenith')
            SAZ_raw = rxr.open_rasterio(f'HDF5:"{file}"://Geometry_data/Solar_azimuth')
            VZA_raw = rxr.open_rasterio(f'HDF5:"{file}"://Geometry_data/Sensor_zenith')
            VAZ_raw = rxr.open_rasterio(f'HDF5:"{file}"://Geometry_data/Sensor_azimuth')
            # Obs_time_raw = rxr.open_rasterio(f'HDF5:"{file}"://Geometry_data/Obs_time')

            VN_maxval = 65534
            
            # vn01_raw = vn01_raw.where(vn01_raw < VN_maxval)
            # vn02_raw = vn02_raw.where(vn02_raw < VN_maxval)
            # vn03_raw = vn03_raw.where(vn03_raw < VN_maxval)
            # vn04_raw = vn04_raw.where(vn04_raw < VN_maxval)
            vn05_raw = vn05_raw.where(vn05_raw < VN_maxval)
            vn06_raw = vn06_raw.where(vn06_raw < VN_maxval)
            # vn07_raw = vn07_raw.where(vn07_raw < VN_maxval)
            vn08_raw = vn08_raw.where(vn08_raw < VN_maxval)
            # vn09_raw = vn09_raw.where(vn09_raw < VN_maxval)
            vn10_raw = vn10_raw.where(vn10_raw < VN_maxval)
            vn11_raw = vn11_raw.where(vn11_raw < VN_maxval)
            SZA_raw = SZA_raw.where(SZA_raw > 0)
            SAZ_raw = SAZ_raw.where(SAZ_raw > 0)
            VZA_raw = VZA_raw.where(VZA_raw > 0)
            VAZ_raw = VAZ_raw.where(VAZ_raw > 0)



            qa_binary = binary_v(qa_raw.values[0])
            qa_nodata_bit = get_bits_v(qa_binary, 0, 0)
            qa_land_bit = get_bits_v(qa_binary, 1, 1)
            qa_coast_bit = get_bits_v(qa_binary, 2, 2)
            # qa_sunglint_flag_bit = get_bits_v(qa_binary, 3, 3)
            qa_sunglint_mask_bit = get_bits_v(qa_binary, 4, 4)
            qa_snow_bit = get_bits_v(qa_binary, 5, 5)
            # qa_cloud_mask_bit = get_bits_v(qa_binary, 6, 6)
            qa_probably_cloud_bit = get_bits_v(qa_binary, 7, 7)
            qa_AOD_bit = get_bits_v(qa_binary, 8, 8)
            qa_straylight_bit = get_bits_v(qa_binary, 11, 11)
            qa_shadow_bit = get_bits_v(qa_binary, 12, 12)
            # qa_cloud_polarized_bit = get_bits_v(qa_binary, 13, 13)

            qa_nodata_OK = (qa_nodata_bit == '0')
            qa_nodata_OK_true_count = np.count_nonzero(qa_nodata_OK)
            print(f"qa_nodata_OK True count: {qa_nodata_OK_true_count}")

            qa_land_OK = (qa_land_bit == '1')
            qa_land_OK_true_count = np.count_nonzero(qa_land_OK)
            print(f"qa_land_OK True count: {qa_land_OK_true_count}")

            qc_coast_OK = (qa_coast_bit == '1')
            qc_coast_OK_true_count = np.count_nonzero(qc_coast_OK)
            print(f"qc_coast_OK True count: {qc_coast_OK_true_count}")

            qa_cloud_OK = (qa_probably_cloud_bit == '0')
            qa_cloud_OK_true_count = np.count_nonzero(qa_cloud_OK)
            print(f"qa_cloud_OK True count: {qa_cloud_OK_true_count}")

            qc_sunglint_OK = (qa_sunglint_mask_bit == '0')
            qc_sunglint_OK_true_count = np.count_nonzero(qc_sunglint_OK)
            print(f"qc_sunglint_OK True count: {qc_sunglint_OK_true_count}")

            qc_snow_OK = (qa_snow_bit == '0')
            qc_snow_OK_true_count = np.count_nonzero(qc_snow_OK)
            print(f"qc_snow_OK True count: {qc_snow_OK_true_count}")

            qc_AOD_OK = (qa_AOD_bit == '0')
            qc_AOD_OK_true_count = np.count_nonzero(qc_AOD_OK)
            print(f"qc_AOD_OK True count: {qc_AOD_OK_true_count}")

            qc_straylight_OK = (qa_straylight_bit == '0')
            qc_straylight_OK_true_count = np.count_nonzero(qc_straylight_OK)
            print(f"qc_straylight_OK True count: {qc_straylight_OK_true_count}")

            qc_shadow_OK = (qa_shadow_bit == '0')
            qc_shadow_OK_true_count = np.count_nonzero(qc_shadow_OK)
            print(f"qc_shadow_OK True count: {qc_shadow_OK_true_count}")


            qc_pass = qa_nodata_OK & qa_land_OK & qa_cloud_OK & qc_AOD_OK & qc_sunglint_OK & qc_snow_OK & qc_straylight_OK & qc_shadow_OK
            qc_pass_true_count = np.count_nonzero(qc_pass)
            print(f"qc_pass True count: {qc_pass_true_count}")

            del qa_binary, qa_nodata_bit, qa_land_bit, qa_coast_bit, qa_sunglint_mask_bit, qa_snow_bit, qa_probably_cloud_bit, qa_straylight_bit, qa_shadow_bit  # remove large, unused vars
            del qa_nodata_OK, qa_land_OK, qc_coast_OK, qa_cloud_OK, qc_AOD_OK, qc_sunglint_OK, qc_snow_OK, qc_straylight_OK, qc_shadow_OK # remove large, unused vars
            gc.collect() # manual garbage collection

            #########################################################
            ### Calculate lon and lat from sinusoidal projection
            #########################################################
            # Get image dimensions
            ny, nx = vn05_raw.shape[1], vn05_raw.shape[2]
            lin_tile = ny  # 4800 for Q resolution
            col_tile = nx  # 4800 for Q resolution

            # Constants for sinusoidal projection
            # degrees per pixel (180.0 / 86400 pixels from pole to pole)
            # This is 180 / (18 tiles * 4800 pixels per tile)
            d = 180/lin_tile/v_tile_num # 0.00208333333 vertical degrees/pixel
            NL = int(180 / d)  # Total pixels from south to north pole (86400)
            NP0 = int(2 * NL) # Total pixels east-west at equator (172800)


            #########################################################
            ### Apply scale and offset to convert to reflectance
            #########################################################
            # Get slope for reflectance conversion
            vn_slope_attrs = {
                # 'VN01': float(vn01_raw.attrs['Slope']),
                # 'VN02': float(vn02_raw.attrs['Slope']),
                # 'VN03': float(vn03_raw.attrs['Slope']),
                # 'VN04': float(vn04_raw.attrs['Slope']),
                'VN05': float(vn05_raw.attrs['Slope']),
                'VN06': float(vn06_raw.attrs['Slope']),
                # 'VN07': float(vn07_raw.attrs['Slope']),
                'VN08': float(vn08_raw.attrs['Slope']),
                # 'VN09': float(vn09_raw.attrs['Slope']),
                'VN10': float(vn10_raw.attrs['Slope']),
                'VN11': float(vn11_raw.attrs['Slope']),
            }
            if len(set(vn_slope_attrs.values())) != 1:
                raise ValueError(f"VN band Slope attributes differ: {vn_slope_attrs}")

            scale = vn_slope_attrs['VN05']  # something like 0.0001
            offset = float(vn05_raw.attrs['Offset']) # should be 0
            # Apply scale and offset
            # vn01_data = vn01_raw.values[0] * scale + offset
            # vn02_data = vn02_raw.values[0] * scale + offset
            # vn03_data = vn03_raw.values[0] * scale + offset
            # vn04_data = vn04_raw.values[0] * scale + offset
            vn05_data = vn05_raw.values[0] * scale + offset # Analog to MODIS band 11
            vn06_data = vn06_raw.values[0] * scale + offset # Analog to MODIS band 12
            # vn07_data = vn07_raw.values[0] * scale + offset # Analog to MODIS band 1 (view angle 1?)
            vn08_data = vn08_raw.values[0] * scale + offset # Analog to MODIS band 1 (view angle 2?)
            # vn09_data = vn09_raw.values[0] * scale + offset
            vn10_data = vn10_raw.values[0] * scale + offset # Analog to MODIS band 2 (view angle 1?)
            vn11_data = vn11_raw.values[0] * scale + offset # Analog to MODIS band 2 (view angle 2?)

            # Total pre-QC obs across all pixels for this file
            num_total_preQC = np.count_nonzero(~np.isnan(vn05_data))
            print(f'Band 5: # of non-nan values before QC = {num_total_preQC}')

            # close the file connections to free up memory
            # vn01_raw.close() 
            # vn02_raw.close()
            # vn03_raw.close()
            # vn04_raw.close()
            vn05_raw.close()
            vn06_raw.close()
            # vn07_raw.close()
            vn08_raw.close()
            # vn09_raw.close()
            vn10_raw.close()
            vn11_raw.close()
            qa_raw.close()
            SZA_raw.close()
            SAZ_raw.close()
            VZA_raw.close()
            VAZ_raw.close()
            # Obs_time_raw.close()

            # del vn01_raw, vn02_raw, vn03_raw, vn04_raw, vn07_raw, vn09_raw # remove large, unused vars
            del vn05_raw, vn06_raw, vn08_raw, vn10_raw, vn11_raw # remove large raw vars since we have the scaled data now
            gc.collect() # manual garbage collection

            #########################################################
            ### Apply basic QC filter
            #########################################################

            # vn01_data = np.where(qc_pass, vn01_data, np.nan)
            # vn02_data = np.where(qc_pass, vn02_data, np.nan)
            # vn03_data = np.where(qc_pass, vn03_data, np.nan)
            # vn04_data = np.where(qc_pass, vn04_data, np.nan)
            vn05_data = np.where(qc_pass, vn05_data, np.nan)
            vn06_data = np.where(qc_pass, vn06_data, np.nan)
            # vn07_data = np.where(qc_pass, vn07_data, np.nan)
            vn08_data = np.where(qc_pass, vn08_data, np.nan)
            # vn09_data = np.where(qc_pass, vn09_data, np.nan)
            vn10_data = np.where(qc_pass, vn10_data, np.nan)
            vn11_data = np.where(qc_pass, vn11_data, np.nan)

            num_total_postQC = np.count_nonzero(~np.isnan(vn05_data))
            print(f'Band 5: # of non-nan values after QC = {num_total_postQC}')

            SZA_scale = float(SZA_raw.attrs['Slope'])
            SZA_offset = float(SZA_raw.attrs['Offset'])
            SZA_data = SZA_raw.values[0] * SZA_scale + SZA_offset

            print(f"SZA raw min = {np.nanmin(SZA_data)}")
            print(f"SZA raw median = {np.nanmedian(SZA_data)}")
            print(f"SZA raw max = {np.nanmax(SZA_data)}")

            SAZ_scale = float(SAZ_raw.attrs['Slope'])
            SAZ_offset = float(SAZ_raw.attrs['Offset'])
            SAZ_data = SAZ_raw.values[0] * SAZ_scale + SAZ_offset

            print(f"SAZ raw min = {np.nanmin(SAZ_data)}")
            print(f"SAZ raw median = {np.nanmedian(SAZ_data)}")
            print(f"SAZ raw max = {np.nanmax(SAZ_data)}")

            VZA_scale = float(VZA_raw.attrs['Slope'])
            VZA_offset = float(VZA_raw.attrs['Offset'])
            VZA_data = VZA_raw.values[0] * VZA_scale + VZA_offset

            print(f"VZA raw min = {np.nanmin(VZA_data)}")
            print(f"VZA raw median = {np.nanmedian(VZA_data)}")
            print(f"VZA raw max = {np.nanmax(VZA_data)}")

            VAZ_scale = float(VAZ_raw.attrs['Slope'])
            VAZ_offset = float(VAZ_raw.attrs['Offset'])
            VAZ_data = VAZ_raw.values[0] * VAZ_scale + VAZ_offset

            print(f"VAZ raw min = {np.nanmin(VAZ_data)}")
            print(f"VAZ raw median = {np.nanmedian(VAZ_data)}")
            print(f"VAZ raw max = {np.nanmax(VAZ_data)}")


            # Create pixel coordinate arrays
            lin = np.arange(ny)
            col = np.arange(nx)

            # Create 2D grids
            col_2d, lin_2d = np.meshgrid(col, lin)

            # Calculate total pixel numbers from south pole and from west
            lin_total = lin_2d + (v_tile * lin_tile)
            col_total = col_2d + (h_tile * col_tile)

            # Calculate latitude and longitude using the handbook formula
            lat = 90.0 - (lin_total + 0.5) * d
            NPi = NP0 * np.cos(np.radians(lat))
            lon = (360.0 / NPi) * (col_total - NP0/2 + 0.5)

            # Clip to valid ranges
            lat = np.clip(lat, -90, 90)
            lon = np.clip(lon, -180, 180)

            # Create xarray dataset with proper coordinates
            dat_xr = xr.Dataset({
                # 'VN01': (['y', 'x'], vn01_data, {'long_name': 'Surface reflectance 375-380 nm', 'units': 'dimensionless'}),
                # 'VN02': (['y', 'x'], vn02_data, {'long_name': 'Surface reflectance 407-417 nm', 'units': 'dimensionless'}),
                # 'VN03': (['y', 'x'], vn03_data, {'long_name': 'Surface reflectance 438-448 nm', 'units': 'dimensionless'}),
                # 'VN04': (['y', 'x'], vn04_data, {'long_name': 'Surface reflectance 485-495 nm', 'units': 'dimensionless'}),
                'VN05': (['y', 'x'], vn05_data, {'long_name': 'Surface reflectance 520-540 nm', 'units': 'dimensionless'}),
                'VN06': (['y', 'x'], vn06_data, {'long_name': 'Surface reflectance 555-575 nm', 'units': 'dimensionless'}),
                # 'VN07': (['y', 'x'], vn07_data, {'long_name': 'Surface reflectance 663.5-683.5 nm', 'units': 'dimensionless'}),
                'VN08': (['y', 'x'], vn08_data, {'long_name': 'Surface reflectance 663.5-683.5 nm', 'units': 'dimensionless'}),
                # 'VN09': (['y', 'x'], vn09_data, {'long_name': 'Surface reflectance 757-769 nm', 'units': 'dimensionless'}),
                'VN10': (['y', 'x'], vn10_data, {'long_name': 'Surface reflectance 858.5-878.5 nm', 'units': 'dimensionless'}),
                'VN11': (['y', 'x'], vn11_data, {'long_name': 'Surface reflectance 858.5-878.5 nm', 'units': 'dimensionless'}),
                'SZA': (['y', 'x'], SZA_data, {'long_name': 'Solar zenith angle', 'units': 'degrees'}),
                'SAZ': (['y', 'x'], SAZ_data, {'long_name': 'Solar azimuth angle', 'units': 'degrees'}),
                'VZA': (['y', 'x'], VZA_data, {'long_name': 'View zenith angle', 'units': 'degrees'}),
                'VAZ': (['y', 'x'], VAZ_data, {'long_name': 'View azimuth angle', 'units': 'degrees'}),
            },
            coords={
                'lat': (['y', 'x'], lat),
                'lon': (['y', 'x'], lon),
                'time': filedate
            })


            # del vn01_data, vn02_data, vn03_data, vn04_data, vn07_data, vn09_data # remove large, unused vars
            del vn05_data, vn06_data, vn08_data, vn10_data, vn11_data, SZA_data, SAZ_data, VZA_data, VAZ_data # remove large raw vars since we have the scaled data now
            gc.collect() # manual garbage collection


            dat_xr.rio.write_crs(4326, inplace = True) # specify WGS84 as CRS
            dat_xr = dat_xr.assign(NDVI = (dat_xr["VN11"] - dat_xr["VN08"])/(dat_xr["VN11"] + dat_xr["VN08"]))
            test_plot(dat_xr['NDVI'], f'{str(filedate)}', 'NDVI', None,
                        #  f'test_NDVI/{Path(file).stem}_1km_NDVI_Orbit{Orbit}.png',
                        plot_min = 0, plot_max = 1)


            
            dat_xrs.append(dat_xr)




            # end_file = time.time()
            # file_elapsed = timedelta(seconds=end_file-start_file)
            # total_elapsed = timedelta(seconds=end_file-start_total)
            # time_remaining = total_elapsed * (len(iYYMM)-num_iter-1)/(num_iter+1)
            # print(f'file processing took {td_min(file_elapsed)} mins, {td_sec(file_elapsed)} seconds')
            # print(f'  estimated time remaining: {td_min(time_remaining)} mins, {td_sec(time_remaining)} seconds')

        except (OSError, RuntimeError) as e:
            print(f'    ERROR processing file {os.path.basename(file)}: {e}')
            print(f'    Skipping bad file')
            # Close any open file handles
            try:
                # vn01_raw.close() 
                # vn02_raw.close()
                # vn03_raw.close()
                # vn04_raw.close()
                vn05_raw.close()
                vn06_raw.close()
                # vn07_raw.close()
                vn08_raw.close()
                # vn09_raw.close()
                vn10_raw.close()
                vn11_raw.close()
                qa_raw.close()
                SZA_raw.close()
                SAZ_raw.close()
                VZA_raw.close()
                VAZ_raw.close()
                # Obs_time_raw.close()
            except:
                pass
            continue

    print(f'Done stacking daily files for {composite_year}-{str(composite_period).zfill(2)}. Concatenating into single dataset...')
    dat_full_ds = xr.concat(dat_xrs, dim = 'time') # concatenate along time axis
    del dat_xrs # remove large, unused vars
    gc.collect() # manual garbage collection

    #####################################
    ### Implement CV-MVC algorithm
    #####################################


    ### Step 1: pixel-wise sort by NDVI
    # define the array from which we want to sort NDVI values
    arr_sort_NDVI = -dat_full_ds.NDVI # NOTE THE NEGATIVE!!! makes it a descending sort
    sort_axis = arr_sort_NDVI.get_axis_num('time') # this gets the axis over which we want to sort
    sort_inds_NDVI = arr_sort_NDVI.argsort(axis=sort_axis) # perform the sort to get pixel-wise indices of the highest NDVI, 2nd highest NDVI, etc...
    sort_inds_NDVI = sort_inds_NDVI.rename({'time': 'NDVI_rank'}) # Replace time dim with ranking dim
    sort_inds_top2NDVI = sort_inds_NDVI.isel(NDVI_rank = [0,1]) # select only the top 2 NDVI indices
    dat_full_ds_top2NDVI = dat_full_ds.isel({'time': sort_inds_top2NDVI}) # filter the original stacked dataset for these top 2 NDVI indices

    del dat_full_ds, sort_inds_NDVI, arr_sort_NDVI
    gc.collect() # manual garbage collection

    ### Step 2: pixel-wise sort by View angle
    # pipe the NDVI-filtered dataset into this step to sort by VZA values
    arr_sort_VZA = dat_full_ds_top2NDVI.VZA # NOTE There is NO negative, makes it an ascending sort
    sort_inds_VZA = arr_sort_VZA.argsort(axis=sort_axis) # perform sort to get pixel-wise indices of lowest and 2nd lowest VZA (NOTE sort_axis should be the same axis as with NDVI.)
    sort_inds_VZA = sort_inds_VZA.rename({'NDVI_rank': 'VZA_rank'}) # replace NDVI_rank dim with VZA_rank
    sort_inds_lowVZA = sort_inds_VZA.isel(VZA_rank = 0) # get the index of the lowest VZA
    sort_inds_highVZA = sort_inds_VZA.isel(VZA_rank = 1) # get the other index
    dat_full_ds_top2NDVI_lowestVZA = dat_full_ds_top2NDVI.isel({'NDVI_rank': sort_inds_lowVZA}) # Using the NDVI-filtered stacked dataset, filter for the lowest VZA
    dat_full_ds_top2NDVI_highestVZA = dat_full_ds_top2NDVI.isel({'NDVI_rank': sort_inds_highVZA}) # For any pixels 

    del arr_sort_VZA, sort_inds_VZA, sort_inds_lowVZA, sort_inds_highVZA, dat_full_ds_top2NDVI
    gc.collect() # manual garbage collection

    ### Step 3: pixel-wise check for <2 valid NDVI vals
    # if the resulting NDVI value is nan, use the values of the next smallest VZA.
    # (If there was only 1 valid NDVI value to begin, this will recover that value)
    nan_inds_NDVI = np.isnan(dat_full_ds_top2NDVI_lowestVZA.NDVI)
    composite_ds = dat_full_ds_top2NDVI_lowestVZA.where(~nan_inds_NDVI, dat_full_ds_top2NDVI_highestVZA)

    del nan_inds_NDVI, dat_full_ds_top2NDVI_lowestVZA, dat_full_ds_top2NDVI_highestVZA
    gc.collect() # manual garbage collection


    # clean up the dataset for saving
    vars_to_drop = ['time', 'timeobs', 'Orbits', 'NDVI_rank', 'VZA_rank']
    for var_to_drop in vars_to_drop:
        if var_to_drop in composite_ds.data_vars:
            composite_ds = composite_ds.drop(var_to_drop)
    composite_dayofyear = (composite_period * 16) + 1
    dat_date = dt.strptime(f"{composite_year}{composite_dayofyear:03d}", "%Y%j")
    composite_ds = composite_ds.expand_dims(time = [dat_date])

    # define global attributes
    composite_ds.attrs['title'] = 'GCOM-C SGLI Surface reflectance and Vegetation Indices - 16-day composite using Constrained View angle - Maximum Value Composite (CV-MVC) algorithm'
    composite_ds.attrs['date_string'] = str(dat_date.date())
    composite_ds.attrs['Comment1'] = 'Original files downloaded from ftp.gportal.jaxa.jp/standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3'
    composite_ds.attrs['Comment2'] = 'h5 files loaded into python using rioxarray and converted to xarray dataset'
    composite_ds.attrs['Citation'] = 'Murakami, H. GCOM-C/SGLI Land Atmospheric Correction Algorithm. 2021. Available online: https://suzaku.eorc.jaxa.jp/  GCOM_C/data/ATBD/ver3/V3ATBD_T1A_Atmcorr_murakami.pdf'
    composite_ds.attrs['Processed_by'] = 'Lewis Kunik, lewis.kunik@utah.edu'
    composite_ds.attrs['Date_created'] = str(dt.today().date())

    # Finally, save to netcdf
    composite_ds.to_netcdf(path=outfile, format="NETCDF4")
    composite_ds.close()

    end_total = time.time()
    total_elapsed = timedelta(seconds=end_total-start_total)
    print(f'File saved. Total elapsed time = {td_min(total_elapsed)} mins, {td_sec(total_elapsed)} seconds')

    del composite_ds # remove large variables from environment to free up space
    gc.collect()

if __name__ == '__main__':
   main()
