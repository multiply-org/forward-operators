#!/usr/bin/env python
import os
import sys

import numpy as np

import pytest
from scipy.optimize import approx_fprime


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from multiply_forward_operators import sar_observation_operator


def test_water_cloud_bs_vv():
    x = np.atleast_2d(np.array([0.5, 2.]))
    polarisation = "VV"
    sigma, dsigma = sar_observation_operator(x, polarisation)
    assert(np.allclose(sigma, 1.975, atol=1.e-3))


def test_water_cloud_bs_vh():
    x = np.atleast_2d(np.array([0.5, 1.1]))
    polarisation = "VH"
    sigma, dsigma = sar_observation_operator(x, polarisation)
    assert(np.allclose(sigma, 1.087, atol=1.e-3))


def test_water_cloud_bs_hh():
    x = np.array([0.5, 1.1])
    polarisation = "HH"
    with pytest.raises(ValueError):
        sigma, dsigma = sar_observation_operator(x, polarisation)


def test_water_cloud_gradient_vv():
    x = np.atleast_2d(np.array([0.5, 2.]))
    polarisation = "VV"
    sigma, dsigma = sar_observation_operator(x, polarisation)

    def backscatter_gradient(t):
        return sar_observation_operator(t, polarisation)[0]

    finite_difference_gradient_approx = approx_fprime(x.squeeze(),
                                                      backscatter_gradient,
                                                      1e-6)
    assert(np.allclose(dsigma.squeeze(),
                       finite_difference_gradient_approx, atol=1e-2))


def test_water_cloud_gradient_vh():
    x = np.atleast_2d(np.array([0.5, 2.]))
    polarisation = "VH"
    sigma, dsigma = sar_observation_operator(x, polarisation)

    def backscatter_gradient(t):
        return sar_observation_operator(t, polarisation)[0]

    finite_difference_gradient_approx = approx_fprime(x.squeeze(),
                                                      backscatter_gradient,
                                                      1e-6)
    assert(np.allclose(dsigma.squeeze(),
                       finite_difference_gradient_approx, atol=1e-2))


def test_water_cloud_bs_vv_array():
    x = np.array([[0.5, 2.], [0.5, 2.], [0.5, 2.]])
    polarisation = "VV"
    sigma, dsigma = sar_observation_operator(x, polarisation)
    assert(np.allclose(sigma, np.array([1.975, 1.975, 1.975]), atol=1.e-3))


def test_water_cloud_bs_vh_array():
    x = np.array([[0.5, 1.1], [0.5, 1.1], [0.5, 1.1]])
    polarisation = "VH"
    sigma, dsigma = sar_observation_operator(x, polarisation)
    print x
    print sigma
    assert(np.allclose(sigma, np.array([1.087, 1.087, 1.087]), atol=1.e-3))
