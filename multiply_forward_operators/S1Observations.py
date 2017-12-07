#!/usr/bin/env python
"""

"""

import glob
import os
from collections import namedtuple
import datetime
import xarray as xr


SARdata = namedtuple('SARdata','observations uncertainty mask metadata emulator')

class S1Observations(object):
    """
    """

    def __init__(self, data_folder='/media/tweiss/Daten/2017_MNI/coregister/speckle/normalization_db/',emulators={'VV':'SOmething', 'VH':'Other'}):

        """

        """


        # 1. Find the files
        files = glob.glob(os.path.join(data_folder, '*.nc'))
        files.sort()
        self.observation_dates = {}
        for fich in files:
            fname = os.path.basename(fich)
            splitter = fname.split('_')
            this_date = datetime.datetime.strptime(splitter[5], '%Y%m%dT%H%M%S')
            self.observation_dates[this_date] = fich

        # 2. Store the emulator(s)
        self.emulators = emulators


    def _read_backscatter(self, fname, polarisation):
        """
        Read backscatter from NetCDF4 File
        Should return a 2D array that should overlap with the "state grid"

        Input
        ------
        fname (string, filename of the NetCDF4 file, path included)
        polarisation (string, used polarisation)

        Output
        ------
        backscatter values stored within NetCDF4 file for given polarisation

        """

        backscatter = xr.open_dataset(fname)
        backscatter = backscatter['sigma0_' + polarisation]

        return backscatter



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
        self.unc = 1.

        # need to find a good way to calculate ENL
        # self.ENL = (backscatter.mean()**2) / (backscatter.std()**2)

        return self.unc


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

        pass


    def get_band_data (self, timestep, band):
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
            polarisation = 'VV'
        elif band == 1:
            polarisation = 'VH'
        this_file = self.observation_dates[timestep]
        observations = self._read_backscatter(this_file, polarisation)
        uncertainty = self._calculate_uncertainty(backscatter)
        mask = self._get_mask(this_file)
        emulator = self.emulators[polarisation]
        sardata = SARdata(observations, uncertainty, mask, None, emulator)
        return sardata




