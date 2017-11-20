#!/usr/bin/env python
"""Optical observation operator.
Just a thin wrapper around PROSPECT+SAIL bindings.
"""
try:
    from prosail import run_prosail
except ImportError:
    raise ImportError("You need the PROSAIL Python bindings from "
                      "http://github.com/jgomezdans/prosail/!")

__author__ = "J Gomez-Dans"
__copyright__ = "Copyright 2017 J Gomez-Dans"
__version__ = "1.0 (09.03.2017)"
__license__ = "GPLv3"
__email__ = "j.gomez-dans@ucl.ac.uk"


def optical_forward_operator(x, sza, vza, raa, version="PROSAIL_D",
                             hspot=0.01):
    """A generic wrapper to the PROSPECT+SAIL operators. Uses either PROSPECT D
    or PROSPECT 5"""
    if not version.upper() in ["PROSAIL_D", "PROSAIL_5"]:
        raise ValueError("Can only deal with SAIL + PROSPECT D or 5!")

    if version.upper() == "PROSAIL_D":
        # Using prospect D
        n, ant, cab, car, cbrown, cw, cm, lai, ala, rsoil, psoil = x
        rho_canopy = run_prosail(n, cab, car,  cbrown, cw, cm, lai, ala, hspot,
                                 sza, vza, raa, ant=ant, prospect_version="D",
                                 rsoil=rsoil, psoil=psoil)

    elif version.upper() == "PROSAIL_5":
        n, cab, car, cbrown, cw, cm, lai, ala, rsoil, psoil = x
        rho_canopy = run_prosail(n, cab, car,  cbrown, cw, cm, lai, ala, hspot,
                                 sza, vza, raa, prospect_version="5",
                                 rsoil=rsoil, psoil=psoil)
    return rho_canopy
