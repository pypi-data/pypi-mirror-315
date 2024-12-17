#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (c) 2021 Dafne-Imaging Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from test.testDL import testSegmentation
from test.testDL import testClassification

#testSegmentation('models/thigh.model', 'testImages/thigh_test.dcm')
#testSegmentation('models/leg.model', 'testImages/leg_test.dcm')

testClassification('models/classifier.model', 'testImages/thigh_test.dcm')
testClassification('models/classifier.model', 'testImages/leg_test.dcm')