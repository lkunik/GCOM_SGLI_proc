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

import numpy as np
from datetime import datetime, timedelta


#########################################
# Define Global Filepaths
#########################################

GCOM_basedir = '/uufs/chpc.utah.edu/common/home/lin-group28/ltk/GCOM-C/RSRF/raw_h5/'

# ALL sites BELOW
site_list = ['US-NR1', 'OSBS', 'Ca-Obs', 'DEJU']



#########################################
# Define Global functions
#########################################


#########################################
# Define Global Variables and constants
#########################################

#%%
start_year = 2018
end_year = 2025
file_years = np.arange(start_year, end_year+1)


# Site coordinates, date ranges, and save paths
site_info = {
    'US-NR1': {
        'tile': 'h09v04',
        'coords': (-105.5464, 40.0329),
        'start': '2017-01-01',
        'end': '2018-12-31'
    },
    'OSBS': {
        'tile': 'h10v06',
        'coords': (-81.993431, 29.689282),
        'start': '2021-01-01',
        'end': '2022-12-31'
    },
    'Ca-Obs': {
        'tile': 'h11v03',
        'coords': (-105.1178, 53.9872),
        'start': '2018-01-01',
        'end': '2022-12-31'
    },
    'DEJU': {
        'tile': 'h11v02',
        'coords': (-145.75136, 63.88112),
        'start': '2019-01-01',
        'end': '2021-12-31'
    }
}



#########################################
# Begin main
#########################################

#%%

site_name = site_list[0]
for site_name in site_list:

    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f'Checking files for site: {site_name}')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    # Get site-specific info
    site_tile = site_info[site_name]['tile']
    site_coords = site_info[site_name]['coords']
    site_start = site_info[site_name]['start']
    site_end = site_info[site_name]['end']

    tile_files_missing = 0

    # create list of daily datetime objects from site_start to site_end (inclusive)
    start_dt = datetime.strptime(site_start, '%Y-%m-%d')
    if start_dt < datetime(start_year, 1, 1):
        start_dt = datetime(start_year, 1, 1)
    end_dt = datetime.strptime(site_end, '%Y-%m-%d')
    if end_dt > datetime(end_year, 12, 31):
        end_dt = datetime(end_year, 12, 31)
    num_days = (end_dt - start_dt).days + 1
    site_daily_datetimes = [start_dt + timedelta(days=i) for i in range(num_days)]
    for day_datetime in site_daily_datetimes:
        yyyy = day_datetime.year
        mm = day_datetime.month
        dd = day_datetime.day

        if dd == 1:
            print(f'{yyyy}-{mm:02d}')
        dat_dir = os.path.join(GCOM_basedir, site_tile, f'{yyyy}', f'{mm:02d}', f'{dd:02d}')
        # if os.path.is_empty(dat_dir):
        #     tile_files_missing += 1
        #     print(f'    No files found for date {yyyy}-{mm:02d}-{dd:02d} at site {site_name}')

        if len(glob.glob(f'{dat_dir}/GC1SG1_{yyyy}{mm:02d}{dd:02d}D*.h5')) == 0:
            tile_files_missing += 1
            print(f'    No files found for date {yyyy}-{mm:02d}-{dd:02d} at site {site_name}')

    if tile_files_missing == 0:
        print(f'site {site_name} - no files missing (all good)')
    else:
        print(f'site {site_name} - {tile_files_missing} files missing')

    

# %%
