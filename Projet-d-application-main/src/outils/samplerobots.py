# -*- coding: utf-8 -*-
"""
Sample robots rewritten to be compatible with the simplified Robot class.
Only geometric parameters are kept (no dynamics, no inertia, no external forces).
Each robot definition creates arrays of size NF+1, as required by Robot.
"""

from sympy import pi, var, zeros, Matrix
from server.robot import Robot
from outils import tools


def cart_pole() -> Robot:
    """
    Cart-Pole robot conforming to the simplified Robot class.
    NL = NJ = NF = 2 → arrays of size 3
    """
    robo = Robot('CartPole', NL=2, NJ=2, NF=2, is_floating=False)

    # Antecedents
    robo.ant = [-1, 0, 1]

    # Joint types (cart: P, pole: R)
    robo.sigma = [0, 1, 0]

    # DH
    robo.alpha = [0, pi/2, pi/2]
    robo.d     = [0, 0, 0]
    robo.theta = [0, pi/2, var('th2')]
    robo.r     = [0, var('r1'), 0]

    robo.gamma = [0, 0, 0]
    robo.b     = [0, 0, 0]
    robo.mu    = [0, 1, 1]

    robo.structure = tools.SIMPLE

    # Base frame
    robo.w0 = zeros(3,1)
    robo.wdot0 = zeros(3,1)
    robo.v0 = zeros(3,1)
    robo.vdot0 = zeros(3,1)

    return robo



def planar2r() -> Robot:
    """
    Planar 2R robot with only geometric data.
    NL = NJ = NF = 2 → arrays of size 3
    """
    robo = Robot('Planar2R', NL=2, NJ=2, NF=2, is_floating=False)

    # Antecedents
    robo.ant = [-1, 0, 1]

    # sigma: 2 = fixed base, then R, R
    robo.sigma = [2, 0, 0]

    # DH
    robo.gamma = [0, 0, 0]
    robo.b     = [0, 0, 0]
    robo.alpha = [0, 0, 0]
    robo.d     = [0, 0, var('L1')]
    robo.theta = [0, var('q1'), var('q2')]
    robo.r     = [0, 0, 0]

    robo.mu = [0, 1, 1]
    robo.structure = tools.SIMPLE

    # Base frame
    robo.w0 = zeros(3,1)
    robo.wdot0 = zeros(3,1)
    robo.v0 = zeros(3,1)
    robo.vdot0 = zeros(3,1)

    return robo


# ================================================================
#  SR400 (géométrique uniquement, simplifié)
# ================================================================

def sr400() -> Robot:
    """
    SR400 geometry-only version.
    Original SR400 has NL=8, NJ=9, NF=10 but relies on dynamics.
    Here we simplify: NF = NJ = NL.
    """
    robo = Robot('SR400', NL=8, NJ=8, NF=8, is_floating=False)
    # arrays size → 9

    robo.ant = [-1, 0, 1, 2, 3, 4, 5, 6, 7]

    # Simplified sigma (all revolute)
    robo.sigma = [0] * 9

    # DH alpha (simplified variant)
    robo.alpha = [
        0,
        0, -pi/2, 0, -pi/2,
        pi/2, -pi/2, -pi/2, 0
    ]

    d_var = list(var('D0:8'))
    robo.d = [0] + d_var[0:8]

    robo.theta = [0] + list(var('th1:9'))

    robo.r = [0, 0, 0, 0, var('RL4'), 0, 0, 0, 0]

    robo.b     = [0] * 9
    robo.gamma = [0] * 9
    robo.mu    = [0] + [1] * 8

    robo.structure = tools.SIMPLE

    # Base frame
    robo.w0 = zeros(3,1)
    robo.wdot0 = zeros(3,1)
    robo.v0 = zeros(3,1)
    robo.vdot0 = zeros(3,1)

    return robo


# ================================================================
#  RX90 (géométrique, conforme SYMORO)
# ================================================================

def rx90() -> Robot:
    """
    RX90 robot fully rewritten to follow the simplified Robot class.
    NL = NJ = NF = 6 → arrays of size 7
    """
    robo = Robot('RX90', NL=6, NJ=6, NF=6, is_floating=False)

    # Antecedents (simple serial chain)
    robo.ant = [-1, 0, 1, 2, 3, 4, 5]

    # σ : type of joints
    robo.sigma = [2, 0, 0, 0, 0, 0, 0]

    # DH parameters (SYMORO RX90 standard)
    robo.alpha = [0, 0, pi/2, 0, -pi/2, pi/2, -pi/2]
    robo.d     = [0, 0, 0, var('D3'), 0, 0, 0]
    robo.theta = [0] + list(var('th1:7'))
    robo.r     = [0, 0, 0, 0, var('RL4'), 0, 0]

    # SYMORO conventions
    robo.gamma = [0] * 7
    robo.b     = [0] * 7
    robo.mu    = [0, 1, 1, 1, 1, 1, 1]

    robo.structure = tools.SIMPLE

    # Base frame
    robo.w0 = zeros(3,1)
    robo.wdot0 = zeros(3,1)
    robo.v0 = zeros(3,1)
    robo.vdot0 = zeros(3,1)

    return robo
