#!/usr/bin/env python
"""A simple Water cloud SAR operator
"""
import numpy as np


def sar_observation_operator(x, polarisation):
    """We assume that the WCM is given by
    $$
    \begin{align}
    \sigma_0^{pp} &= A_{1}\cdot VWC\left[ 1 - \exp(-2\cdot A_2\cdot VWC/\cos\theta )\right]\\
                &+ \sigma_{soil}^{pp}\cdot \exp(-2\cdot A_2\cdot VWC/\cos\theta )\\
    \end{align}
    $$
    where for each polarisation we have two parameters: A1, A2. The model is
    in this case parameterised by two input magnitudes: the VWC and soil
    backscatter (in reality, we would have soil moisture etc instead of soil
    backscatter, but this is just an example ;D). A1 and A2 are defined per
    polarisation.

    `x` is a 2D array where each row contains
    """
    x = np.atleast_2d(x)
    theta = np.deg2rad(38.)  # Whathever the incidence angle is
    mu = 1./np.cos(theta)  # Define mu as simpler
    # the model parameters. Some made up numbers ;-)
    parameters = {"VV": [0.15, 0.01],
                  "VH": [0.14, 0.01]}
    # Select model parameters
    try:
        A1, A2 = parameters[polarisation]
    except KeyError:
        raise ValueError("Only VV and VH polarisations available!")
    sigma_0 = A1*x[:, 0]*(1 - np.exp(-2*mu*A2*x[:, 0])) + \
        x[:, 1]*np.exp(-2*mu*A2*x[:, 0])
    grad = x*0
    n_elems = x.shape[0]
    for i in xrange(n_elems):
        grad[i, 0] = A1*(1 - np.exp(-2*mu*A2*x[i, 0])) + \
            2*A1*A2*mu*x[i, 0]*np.exp(-2*mu*A2*x[i, 0]) - \
            2*A2*mu*x[i, 1]*np.exp(-2*mu*A2*x[i, 0])
        grad[i, 1] = np.exp(-2*mu*A2*x[i, 0])
    return sigma_0, grad
