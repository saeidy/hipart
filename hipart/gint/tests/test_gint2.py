# -*- coding: utf-8 -*-
# HiPart is a program to analyze the electronic structure of molecules with
# fuzzy-atom partitioning methods.
# Copyright (C) 2007 - 2012 Toon Verstraelen <Toon.Verstraelen@UGent.be>
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
#--


from hipart.gint.tests.utils import setup_gaussian

from hipart.gint import GaussianBasis, gint2_nai_dmat, gint2_nai_S_S, \
    reorder_dmat

from molmod.io import FCHKFile
from molmod import angstrom

import numpy, shutil
from nose.tools import assert_raises


ref_data_h_sto3g_pot = numpy.array([
    [0.0, 0.0, 0.1, 4.093585398681],
    [0.0, 0.0, 0.3, 0.735799318055],
    [0.0, 0.0, 0.5, 0.22127781768],
    [0.0, 0.0, 0.7, 0.074899054133],
    [0.0, 0.0, 0.9, 0.026753454579],
    [0.0, 0.0, 1.1, 0.009972987563],
    [0.0, 0.0, 1.3, 0.003796220644],
    [0.0, 0.0, 1.5, 0.001428250591],
    [0.0, 0.0, 1.7, 0.000515694308],
    [0.0, 0.0, 1.9, 0.000175125083],
    [0.352326199645, -1.08546276319, 1.976991856, 0.000017984595],
    [1.25436683018, -0.217346976668, -0.871646334866, 0.001153040181],
    [-0.957002321789, -0.512937147175, 1.0427486273, 0.001390286941],
    [1.41126124545, -0.836402729349, -0.409710665699, 0.000540859302],
    [1.20238210907, 0.691132305708, -2.0404187327, 0.000005399526],
    [-1.6129930801, 0.85290566018, -0.032146667224, 0.000264855369],
    [-0.548491749792, -1.61416187871, -0.292826338472, 0.000440979474],
    [0.131987372541, 0.2706767489, 0.368981911725, 0.252935104791],
    [0.158093550045, -2.74244800526, 0.15125114888, 0.000000734598],
    [0.240250681611, -1.01981571127, 1.48630738657, 0.000274253676],
])

def test_pot_h_sto3g():
    tmpdir, fn_fchk = setup_gaussian("h_sto3g")
    fchk = FCHKFile(fn_fchk)
    shutil.rmtree(tmpdir)
    basis = GaussianBasis.from_fchk(fchk)
    # real test for the output
    dmat = fchk.fields["Total SCF Density"]
    points = ref_data_h_sto3g_pot[:,:3]*angstrom
    radius = numpy.sqrt((points**2).sum(axis=1))
    ref_data_h_sto3g_pot[:,3] -= 1/radius
    potential = -basis.call_gint_grid(gint2_nai_dmat, dmat, points)
    assert(abs(potential-ref_data_h_sto3g_pot[:,3]).max() < 1e-8)
    # test error mechanism
    basis.shell_types[0] = 102
    assert_raises(ValueError, basis.call_gint_grid, gint2_nai_dmat, dmat, points*angstrom)
    basis.shell_types[0] = -763
    assert_raises(ValueError, basis.call_gint_grid, gint2_nai_dmat, dmat, points*angstrom)


def test_gint2_nai_S_S():
    from scipy.special import erf
    a = numpy.zeros(3)
    a_a = 3.42525091E+00
    out1 = numpy.zeros(1, float)
    for z in 0.1, 0.5, 0.7, 1.0, 2.0, 5.0:
        c = numpy.array([0.0, 0.0, z])
        gint2_nai_S_S(a, a_a, a, a_a, c, out1)
        out2 = erf(numpy.sqrt(2*a_a)*z)/z
        assert(abs(out1[0] - out2) < 1e-10)


ref_data_hf_sto3g_pot = numpy.array([
    [0.0, 0.0, 0.1, 5927.015185295983],
    [0.0, 0.0, 0.3, 10.064557630176],
    [0.0, 0.0, 0.5, 1.964032321234],
    [0.0, 0.0, 0.7, 0.385293028001],
    [0.0, 0.0, 0.9, 0.051192004848],
    [0.0, 0.0, 1.1, -0.017241812874],
    [0.0, 0.0, 1.3, -0.02831794891],
    [0.0, 0.0, 1.5, -0.027192855052],
    [0.0, 0.0, 1.7, -0.024017380694],
    [0.0, 0.0, 1.9, -0.020910984424],
    [0.352326199645, -1.08546276319, 1.976991856, -0.015912161412],
    [1.25436683018, -0.217346976668, -0.871646334866, 0.023982935246],
    [-0.957002321789, -0.512937147175, 1.0427486273, -0.031639002235],
    [1.41126124545, -0.836402729349, -0.409710665699, -0.001011983657],
    [1.20238210907, 0.691132305708, -2.0404187327, 0.02294879122],
    [-1.6129930801, 0.85290566018, -0.032146667224, -0.008756329178],
    [-0.548491749792, -1.61416187871, -0.292826338472, -0.004115822971],
    [0.131987372541, 0.2706767489, 0.368981911725, 1.792662815705],
    [0.158093550045, -2.74244800526, 0.15125114888, -0.00382837605],
    [0.240250681611, -1.01981571127, 1.48630738657, -0.023038218064],
])

def test_pot_hf_sto3g():
    tmpdir, fn_fchk = setup_gaussian("hf_sto3g")
    fchk = FCHKFile(fn_fchk)
    shutil.rmtree(tmpdir)
    basis = GaussianBasis.from_fchk(fchk)
    dmat = fchk.fields["Total SCF Density"]
    reorder_dmat(dmat, basis.g03_permutation)
    points = ref_data_hf_sto3g_pot[:,:3]*angstrom
    ref_potential = ref_data_hf_sto3g_pot[:,3]
    nuc_potential = 0.0
    for i in xrange(fchk.molecule.size):
        center = fchk.molecule.coordinates[i]
        Z = fchk.molecule.numbers[i]
        radius = numpy.sqrt(((points-center)**2).sum(axis=1))
        nuc_potential += Z/radius
    ref_potential -= nuc_potential
    potential = -basis.call_gint_grid(gint2_nai_dmat, dmat, points)
    assert(abs(potential-ref_potential).max() < 1e-6)


ref_data_o2_cc_pvtz_cart_pot = numpy.array([
    [0.0, 0.0, 0.1, 1.971246175321],
    [0.0, 0.0, 0.3, 5.584079118098],
    [0.0, 0.0, 0.5, 37.501673472694],
    [0.0, 0.0, 0.7, 20.054265047189],
    [0.0, 0.0, 0.9, 3.844098145251],
    [0.0, 0.0, 1.1, 1.062428560276],
    [0.0, 0.0, 1.3, 0.321980437457],
    [0.0, 0.0, 1.5, 0.102001763361],
    [0.0, 0.0, 1.7, 0.032322797425],
    [0.0, 0.0, 1.9, 0.008990991016],
    [1.21034804944, 1.33431925871, -1.48568061514, -0.000237748327],
    [0.380907186701, 0.535526212774, -0.780217757666, 0.44483717424],
    [-0.904257874251, 1.36596259147, 0.235856329873, 0.019236467036],
    [-0.401756143828, 1.28759317986, -1.94015316532, 0.003269057603],
    [0.187244262091, 0.534106808229, -0.111489589034, 0.557180506617],
    [-0.456926257829, -0.397398227751, -0.780884131355, 0.526630653799],
    [0.634413295603, -1.06814100395, -1.34416503192, 0.011553360451],
    [-0.912912115442, -1.54821426052, -1.20810766211, 0.005807421374],
    [0.374821493462, 0.89586852407, 0.564724774034, 0.146277164719],
    [-0.56907756444, 0.677762323202, -0.907287206105, 0.104050724016],
])

def test_pot_o2_cc_pvtz_cart():
    tmpdir, fn_fchk = setup_gaussian("o2_cc_pvtz_cart")
    fchk = FCHKFile(fn_fchk)
    shutil.rmtree(tmpdir)
    basis = GaussianBasis.from_fchk(fchk)
    dmat = fchk.fields["Total SCF Density"]
    reorder_dmat(dmat, basis.g03_permutation)
    points = ref_data_o2_cc_pvtz_cart_pot[:,:3]*angstrom
    ref_potential = ref_data_o2_cc_pvtz_cart_pot[:,3]
    nuc_potential = 0.0
    for i in xrange(fchk.molecule.size):
        center = fchk.molecule.coordinates[i]
        Z = fchk.molecule.numbers[i]
        radius = numpy.sqrt(((points-center)**2).sum(axis=1))
        nuc_potential += Z/radius
    ref_potential -= nuc_potential
    potential = -basis.call_gint_grid(gint2_nai_dmat, dmat, points)
    assert(abs(potential-ref_potential).max() < 1e-6)


ref_data_o2_cc_pvtz_pure_pot = numpy.array([
    [0.0, 0.0, 0.1, 1.970967629165],
    [0.0, 0.0, 0.3, 5.582810453891],
    [0.0, 0.0, 0.5, 37.501129979615],
    [0.0, 0.0, 0.7, 20.052490127704],
    [0.0, 0.0, 0.9, 3.841536231275],
    [0.0, 0.0, 1.1, 1.060529841566],
    [0.0, 0.0, 1.3, 0.320231603715],
    [0.0, 0.0, 1.5, 0.100514642099],
    [0.0, 0.0, 1.7, 0.031442987225],
    [0.0, 0.0, 1.9, 0.008629268923],
    [1.21034804944, 1.33431925871, -1.48568061514, -0.000235995135],
    [0.380907186701, 0.535526212774, -0.780217757666, 0.443484404126],
    [-0.904257874251, 1.36596259147, 0.235856329873, 0.019097438009],
    [-0.401756143828, 1.28759317986, -1.94015316532, 0.003276995961],
    [0.187244262091, 0.534106808229, -0.111489589034, 0.556322338245],
    [-0.456926257829, -0.397398227751, -0.780884131355, 0.525248128634],
    [0.634413295603, -1.06814100395, -1.34416503192, 0.011379054108],
    [-0.912912115442, -1.54821426052, -1.20810766211, 0.005786492404],
    [0.374821493462, 0.89586852407, 0.564724774034, 0.145519199534],
    [-0.56907756444, 0.677762323202, -0.907287206105, 0.102948159996],
])

def test_pot_o2_cc_pvtz_pure():
    tmpdir, fn_fchk = setup_gaussian("o2_cc_pvtz_pure")
    fchk = FCHKFile(fn_fchk)
    shutil.rmtree(tmpdir)
    basis = GaussianBasis.from_fchk(fchk)
    dmat = fchk.fields["Total SCF Density"]
    reorder_dmat(dmat, basis.g03_permutation)
    points = ref_data_o2_cc_pvtz_pure_pot[:,:3]*angstrom
    ref_potential = ref_data_o2_cc_pvtz_pure_pot[:,3]
    nuc_potential = 0.0
    for i in xrange(fchk.molecule.size):
        center = fchk.molecule.coordinates[i]
        Z = fchk.molecule.numbers[i]
        radius = numpy.sqrt(((points-center)**2).sum(axis=1))
        nuc_potential += Z/radius
    ref_potential -= nuc_potential
    potential = -basis.call_gint_grid(gint2_nai_dmat, dmat, points)
    assert(abs(potential-ref_potential).max() < 1e-6)
