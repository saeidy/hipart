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

from hipart.gint.tests.utils import setup_fchk, hf_fchk

from hipart.gint.basis import GaussianBasis
from hipart.gint.gint1_fn import gint1_fn_basis

from molmod.io import FCHKFile

import shutil, numpy


def test_load_blind():
    tmpdir, fn_fchk = setup_fchk(hf_fchk)
    fchk = FCHKFile(fn_fchk)
    basis = GaussianBasis.from_fchk(fchk)
    weights = fchk.fields["Alpha MO coefficients"][:basis.num_dof]
    output = basis.call_gint1(gint1_fn_basis, weights, numpy.zeros(3,float))
    print output
    shutil.rmtree(tmpdir)
    raise Exception
