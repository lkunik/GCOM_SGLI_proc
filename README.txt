GCOM-C SGLI RSRF surface reflectance data were downloaded as a sanity check
and validation/benchmark of the MCD19 data because GCOM-C has similar retrieval windows
to MODIS' bands 1, 2 and 11 (making it capable of comparing CCI and NDVI across the
different sensors/platforms). 

the data were downloaded from JAXA's ftp server (GPortal)
data are offered as h5 files - these are version 3 L2 files (L2.LAND.RSRF is the code)
Note that in step 01, data were downloaded somewhat manually using the lftp commands 
listed in 01_sample_lftp_commands.sh. But you don't need to include this in the writeup.

We downloaded tiles h09v04, h10v06, h11v03 and h11v02 but in JAXA's file naming
system these are labeled T0409, T0610, T0311 and T0211. The data are available starting
in early 2018, so we downloaded all years available that overlapped with the PhotoSpec timing

Step 02 (GCOM-C/code/02_process_GCOM-C_SGLI_RSRF_CV-MVC_pre-fill_composites_batch.py)
The data were processed to yield 16-day composites at 250m spatial resolution.
The compositing algorithm was identical to the CV-MVC algorithm used for the MCD19 composites

When performing QC filtering of the GCOM data we used the following filters to ensure good quality:
(see info here: https://suzaku.eorc.jaxa.jp/GCOM_C/data/update/Algorithm_RSRF_en.html)
Cloud filter ("probably_cloud" must not be 1; note that Clouds are already pre-filtered in L2 data)
No Sunglint contamination ("sunglint" must not be 1)
No snow cover ("snow or ice" flag must not be 1)
No high AOD ("high tau-a", i.e. >0.8, must not be 1)
No straylight detected ("stray light flag" must not be 1)
No cloud shadows ("shadow" must not be 1)


Note that NDVI and CCI are calculated in future analysis scripts which use these data.
but FYI the NDVI is calculated as:
NDVI = (GCOM_pt.VN11 - GCOM_pt.VN08) / (GCOM_pt.VN11 + GCOM_pt.VN08)

and CCI as:
CCI = (GCOM_pt.VN05 - GCOM_pt.VN08) / (GCOM_pt.VN05 + GCOM_pt.VN08)

Where VN08 (663.5-683.5 nm) is the analog to MODIS Band 1
VN11 (858.5-878.5 nm) is the analog to MODIS Band 2
VN05 (520-540 nm) is the analog to MODIS Band 11


Some details that might be relevant (but might not - including here as notes):
python's rioxarray was used to load the h5 files using open_rasterio()

sinusoidal lon/lat coordinates must be calculated from the view geometry information in the file

