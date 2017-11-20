#!/usr/bin/env python
import os
import sys

from distutils import dir_util

import numpy as np

from pytest import fixture

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from multiply_forward_operators import optical_forward_operator


@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for locating the test data directory and copying it
    into a temporary directory.
    Taken from  http://www.camillescott.org/2016/07/15/travis-pytest-scipyconf/
    '''
    filename = request.module.__file__
    test_dir = os.path.dirname(filename)
    data_dir = os.path.join(test_dir, 'data')
    dir_util.copy_tree(data_dir, str(tmpdir))

    def getter(filename, as_str=True):
        filepath = tmpdir.join(filename)
        if as_str:
            return str(filepath)
        return filepath

    return getter


def test_prosaild(datadir):
    n = 2.1
    cab = 40
    car = 10.
    cbrown = 0.1
    ant = 12.
    cw = 0.001
    cm = 0.001
    lai = 4.
    ala = 45.
    rsoil = 0.1
    psoil = 0.1
    sza = 30.
    hspot = 0.1
    r_fwd = np.zeros((85, 91))
    x = n, ant, cab, car, cbrown, cw, cm, lai, ala, rsoil, psoil
    for i, vza in enumerate(np.arange(0, 85, 1)):
        for j, raa in enumerate(np.arange(0, 182, 2)):
            r = optical_forward_operator(x, sza, vza, raa, version="PROSAIL_D",
                                         hspot=hspot)
            r_fwd[i, j] = r[465]

    fname = datadir("prosailD.txt")
    r_save = np.loadtxt(fname)
    assert np.allclose(r_fwd, r_save)


def test_prosail5(datadir):
    n = 2.1
    cab = 40
    car = 10.
    cbrown = 0.1
    cw = 0.001
    cm = 0.001
    lai = 4.
    ala = 45.
    rsoil = 0.1
    psoil = 0.1
    sza = 30.
    hspot = 0.1
    r_fwd = np.zeros((85, 91))
    x = n, cab, car, cbrown, cw, cm, lai, ala, rsoil, psoil
    for i, vza in enumerate(np.arange(0, 85, 1)):
        for j, raa in enumerate(np.arange(0, 182, 2)):
            r = optical_forward_operator(x, sza, vza, raa, version="PROSAIL_5",
                                         hspot=hspot)
            r_fwd[i, j] = r[465]
    fname = datadir("prosail5.txt")
    r_save = np.loadtxt(fname)
    assert np.allclose(r_fwd, r_save)
