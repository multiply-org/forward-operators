#!/usr/bin/env python
"""

"""
import datetime
import glob
import os
from collections import namedtuple
import gdal
import numpy as np
import osr
import scipy.sparse as sp
from netCDF4 import Dataset
from dateutil import parser


WRONG_VALUE = -999.0 # TODO tentative missing value

SARdata = namedtuple('SARdata','observations uncertainty mask metadata emulator')

def reproject_image(source_img, target_img, dstSRSs=None):
    """Reprojects/Warps an image to fit exactly another image.
    Additionally, you can set the destination SRS if you want
    to or if it isn't defined in the source image."""
    g = gdal.Open(target_img)
    geo_t = g.GetGeoTransform()
    x_size, y_size = g.RasterXSize, g.RasterYSize
    xmin = min(geo_t[0], geo_t[0] + x_size * geo_t[1])
    xmax = max(geo_t[0], geo_t[0] + x_size * geo_t[1])
    ymin = min(geo_t[3], geo_t[3] + y_size * geo_t[5])
    ymax = max(geo_t[3], geo_t[3] + y_size * geo_t[5])
    xRes, yRes = abs(geo_t[1]), abs(geo_t[5])
    if dstSRSs is None:
        dstSRS = osr.SpatialReference()
        raster_wkt = g.GetProjection()
        dstSRS.ImportFromWkt(raster_wkt)
    else:
        dstSRS = dstSRSs

    g = gdal.Warp('', source_img, format='MEM',
                  outputBounds=[xmin, ymin, xmax, ymax], xRes=xRes, yRes=yRes,
                  dstSRS=dstSRS)
    if g is None:
        raise ValueError("Something failed with GDAL!")
    return g

class S1Observations(object):
    """
    """

    def __init__(self, data_folder, state_mask, emulators={'vv':'SOmething', 'vh':'Other'}):

        """
        File sorting ??? Are sorted observation_dates needed for KafKa?
        """

        # 1. Find the files
        files = glob.glob(os.path.join(data_folder, '*.nc'))
        files.sort()
        self.state_mask = state_mask
        self.dates = []
        self.date_data = {}

        for fich in files:
            fname = os.path.basename(fich)
            # TODO Maybe filter files by metadata
            # (e.g. select ascending/descending passes)
            data = Dataset(fich)
            attrs = data.ncattrs()

            # Search for date in attribute name and takes first variable that matches
            for i, s in enumerate(attrs):
                if 'date' in s.lower():
                    date = getattr(data, s)
                    break

            this_date = parser.parse(date)

            self.dates.append(this_date)
            self.date_data[this_date] = fich
        # self.observation_dates = sorted(self.observation_dates.items())

        # 2. Store the emulator(s)
        self.emulators = emulators
        self.bands_per_observation = {}
        for the_date in self.dates:
            self.bands_per_observation[the_date] = 2 # 2 bands

    def _calculate_uncertainty(self, backscatter):
        """
        Calculation of the uncertainty of Sentinel-1 input data
        Radiometric uncertainty of Sentinel-1 Sensors are within 1 and 0.5 dB
        Calculate Equivalent Number of Looks (ENL) of input dataset leads to
        uncertainty of scene caused by speckle-filtering/multi-looking
        Input
        ------
        backscatter (backscatter values)
        Output
        ------
        unc (uncertainty in dB)
        """

        # first approximation of uncertainty (1 dB)
        unc = backscatter*0.05


        # need to find a good way to calculate ENL
        # self.ENL = (backscatter.mean()**2) / (backscatter.std()**2)

        return unc


    def _get_mask (self, this_file):
        """
        Mask for selection of pixels

        Get a True/False array with the selected/unselected pixels


        Input
        ------
        this_file ?????

        Output
        ------

        """

        mask = np.ones_like(this_file, dtype=np.bool)
        mask[this_file == WRONG_VALUE] = False
        return mask

    def _get_metadata(self, this_file):
        """
        get all relevant data information from netcdf4 global attributes


        Input
        ------
        timestep

        Output
        ------
        freq
        later maybe only for S1 data
            - satellite
            - relativorbit
            - orbitdirection
        """
        dset = Dataset(this_file, 'r', format="NETCDF4")
        freq = getattr(dset, 'frequency')

        return freq

    def _get_variable_name(self, this_file, search_string):
        """
        search for part of search string in variable names of netCDF4 files and return complete string

        Input
        -------
        this_file (path and name of netCDF4 file)
        search_string (identification string that needs to be part of the variable name within the netCDF4 file)

        Output
        -------
        variable_name (complete name of variable within netCDF4 file)

        """
        dset = Dataset(this_file, 'r', format="NETCDF4")

        for i, s in enumerate(dset.variables):
            if search_string in s.lower():
                variable_name = s
                break

        assert 'variable_name' in locals(), 'ERROR: search string "'+ search_string + '" can not be found in band names of netCDF4-file'

        return variable_name



    def get_band_data(self, timestep, band):
        """
        get all relevant S1 data information for one timestep to get processing done


        Input
        ------
        timestep
        band

        Output
        ------
        sardata (namedtuple with information on observations, uncertainty, mask, metadata, emulator/used model)

        """

        if band == 0:
            polarisation = 'vv'
        elif band == 1:
            polarisation = 'vh'
        elif band == 2:
            polarisation = 'hh'

        this_file = self.date_data[timestep]

        variable_name = self._get_variable_name(this_file, polarisation)

        fname = 'NETCDF:"{:s}":{:s}'.format(this_file, variable_name)
        obs_ptr = reproject_image(fname, self.state_mask)
        observations = obs_ptr.ReadAsArray()
        uncertainty = self._calculate_uncertainty(observations)
        mask = self._get_mask(observations)
        R_mat = np.zeros_like(observations)
        R_mat = uncertainty
        R_mat[np.logical_not(mask)] = 0.
        N = mask.ravel().shape[0]
        R_mat_sp = sp.lil_matrix((N, N))
        R_mat_sp.setdiag(1./(R_mat.ravel())**2)
        R_mat_sp = R_mat_sp.tocsr()

        emulator = self.emulators[polarisation]

        variable_name = self._get_variable_name(this_file, 'theta')
        fname = 'NETCDF:"{:s}":{:s}'.format(this_file, variable_name)
        obs_ptr = reproject_image(fname, self.state_mask)
        frequency = self._get_metadata(this_file)

        metadata = {'incidence_angle': obs_ptr.ReadAsArray(), 'frequency': float(frequency)}

        sardata = SARdata(observations, R_mat_sp, mask, metadata, emulator)
        return sardata

if __name__ == "__main__":
    data_folder = "/home/tweiss/LRZ Sync+Share/Tonio"
    sentinel1 = S1Observations(data_folder,'NETCDF:"/home/tweiss/LRZ Sync+Share/Tonio/S1A_IW_SLC__1SDV_20170101T165853_20170101T165920_014641_017CE5_63E5_GC_RC_No_Su_Co_speckle.nc":theta')
