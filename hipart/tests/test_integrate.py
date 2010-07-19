# HiPart is a software toolkit to analyse molecular densities with the hirshfeld partitioning scheme.
# Copyright (C) 2007 - 2010 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of HiPart.
#
# HiPart is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HiPart is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


from hipart.integrate import *
from hipart.atoms import AtomFn

import numpy


def test_int1():
    x = numpy.arange(0.0, 1.0, 1e-4)
    y = x**2
    assert(abs(integrate_equi(x,y) - 1.0/3.0) < 1e-3)


def test_gauss_potential():
    from scipy.special import erf
    r_low = 1e-5
    r_high = 10.0
    r_steps = 500
    r_factor = (r_high/r_low)**(1.0/(r_steps-1))
    rs = r_low*r_factor**numpy.arange(r_steps)
    beta = 0.5
    norm = (numpy.pi*beta**2)**(3.0/2.0)
    rhos = numpy.exp(-(rs/beta)**2)/norm
    assert(abs(integrate_log(rs, rhos*rs**2*4*numpy.pi) - 1.0) < 1e-3)
    vs = -erf(rs/beta)/rs
    vs_numer1 = -cumul_integrate_log(rs, cumul_integrate_log(rs, -rhos*4*numpy.pi*rs**2)/rs**2)

    qs = -cumul_integrate_log(rs, rhos*4*numpy.pi*rs**2)
    rs_inv = 1/rs
    vs_numer2 = cumul_integrate_log(rs_inv[::-1], qs[::-1])[::-1]

    atom_fn = AtomFn(rs, rhos, True)
    vs_numer3 = atom_fn.potential(rs)
    assert(abs(vs-vs_numer3).max() < 1e-3)