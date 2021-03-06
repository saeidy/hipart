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


import hipart.llext

import numpy


__all__ = ["grid_fns", "get_grid"]


grid_fns = {}
for name in dir(hipart.llext):
    if name.startswith("ld"):
        grid_fns[int(name[2:])] = hipart.llext.__dict__[name]


def get_grid(number):
    if number not in grid_fns:
        raise ValueError("There is no Lebedev-Laikov grid with %i points." % number)
    xyz = numpy.zeros((3,number), float)
    w = numpy.zeros(number, float)
    x,y,z = xyz
    grid_fns[number](x,y,z,w,0)
    return xyz.transpose(), w
