#!/usr/bin/env python
"""

"""

import numpy as np
import pdb

def sar_observation_operator(x, polarisation):

    """
    For the sar_observation_operator a simple Water Cloud Model (WCM) is used
    We assume that the WCM is given by

    -----------------------------------------------------
    tau = exp(-2*B*V/cos(theta))
    sigma_veg = A*V**E*cos(theta)*(1-tau)
    sigma_soil = 10**((C+D*SM)/10)
    sigma_0 = sigma_veg + tau*sigma_soil

    A, B, C, D, E are parameters determined by fitting of the model
    V is a vegetation descriptor e.g. LAI, LWAI, VWM
    SM is the soil moisture [m^3/m^3]
    sigma_veg is the volume component of the backscatter [m^3/m^3]
    sigma_soil is the surface component of the backscatter [m^3/m^3]
    tau is the two way attenuation through the canopy (unitless)
    sigma_0 is the total backscatter in [m^3/m^3]
    ----------------------------------------------------

    Input
    -----
    polarisation: considered polarisation as string
    x: 2D array where every row is the set of parameters for one pixel

    Output
    ------
    sigma_0: predicted backscatter for each individual parameter set
    grad: gradient for each individual parameter set and each parameter determined by 2D input array x. The gradient should thus have the same size and shape as x
    sigma_veg: predicted volume component of sigma_0
    sigma_surf: predicted surface component of sigma_0
    tau: predicted two-way attenuation through the canopy
    """

    # x 2D array where every row is the set of parameters for one pixel
    x = np.atleast_2d(x)

    # conversion of incidence angle to radiant
    # the incidence angle itself should probably implemented in x)
    theta = np.deg2rad(23.)

    # Simpler definition of cosine of theta
    mu = np.cos(theta)

    # the model parameters (A, B, C, D, E) for different polarisations
    parameters = {'VV': [0.0846, 0.0615, -14.8465, 15.907, 0.], 'VH': [0.0795, 0.1464, -14.8332, 15.907, 0.]}

    # Select model parameters
    try:
        A, B, C, D, E = parameters[polarisation]
    except KeyError:
        raise ValueError('Only VV and VH polarisations available!')

    # Calculate Model
    tau = np.exp(-2 * B / mu * x[0, :])
    sigma_veg = A * (x[0, :] ** E) * mu * (1 - tau)
    sigma_surf = 10 ** ((C + D * x[1, :]) / 10.)

    sigma_0 = sigma_veg + tau * sigma_surf

    # Calculate Gradient (grad has same dimension as x)
    grad = x*0
    n_elems = x.shape[1]
    for i in range(n_elems):
        tau_value = np.exp(-2 * B / mu * x[0, i])
        grad[0, i] = A * E * mu * (x[0, i] ** (E - 1)) * (1 - tau_value) + \
            2 * A * B * (x[0, i] ** E) * tau_value - (\
            (2 ** (1/10. * (C + D * x[1, i]) + 1)) * \
            (5 ** (1/10. * (C + D * x[1, i])) * B * tau_value) \
            ) / mu
        grad[1, i] = D * np.log(10) * tau_value * 10 ** (1/10. * (C + D * x[1, i]) - 1)


    # returned values are linear scaled not dB!!!
    # return sigma_0, grad, sigma_veg, sigma_surf, tau
    return sigma_0, grad



    # # Calculate Gradient without conversion of sigma_soil from dB to linear
    # grad = x*0
    # n_elems = x.shape[0]
    # for i in range(n_elems):
    #     tau = np.exp(-2 * B / mu * x[i, 0])
    #     grad[i, 0] = 2 * A * B * x[i, 0] * tau - \
    #         A * mu * tau + \
    #         A * mu - \
    #         2 * B * C * tau / mu - \
    #         2 * B * D * x[i, 1] * tau / mu
    #     grad[i, 1] = D * tau


