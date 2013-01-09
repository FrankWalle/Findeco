#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of Findeco.
#
# Findeco is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Findeco. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User
from ..path_helpers import get_favorite_if_slot, get_ordered_children_for
from ..models import Node, NodeOrder, Vote

class HelpersTest(TestCase):
    def setUp(self):
        self.root = Node()
        self.root.node_type = 'structureNode'
        self.root.save()
        self.slot1 = Node()
        self.slot1.node_type = 'slot'
        self.slot1.save()
        self.slot1_order = NodeOrder()
        self.slot1_order.parent = self.root
        self.slot1_order.child = self.slot1
        self.slot1_order.position = 0
        self.slot1_order.save()
        self.text1 = Node()
        self.text1.node_type = 'textNode'
        self.text1.save()
        text1_order = NodeOrder()
        text1_order.parent = self.slot1
        text1_order.child = self.text1
        text1_order.position = 1
        text1_order.save()
        self.slot2 = Node()
        self.slot2.node_type = 'slot'
        self.slot2.save()
        slot2_order = NodeOrder()
        slot2_order.parent = self.root
        slot2_order.child = self.slot2
        slot2_order.position = 1
        slot2_order.save()
        self.text3 = Node()
        self.text3.node_type = 'textNode'
        self.text3.save()
        self.slot2.append_child(self.text3)
        self.text4 = Node()
        self.text4.node_type = 'textNode'
        self.text4.save()
        self.slot2.append_child(self.text4)
        self.slot3 = Node()
        self.slot3.node_type = 'slot'
        self.slot3.save()
        slot3_order = NodeOrder()
        slot3_order.parent = self.root
        slot3_order.child = self.slot3
        slot3_order.position = 2
        slot3_order.save()
        self.text5 = Node()
        self.text5.node_type = 'textNode'
        self.text5.save()
        self.slot3.append_child(self.text5)
        self.text6 = Node()
        self.text6.node_type = 'textNode'
        self.text6.save()
        self.slot3.append_child(self.text6)
        max = User()
        max.username = "Max"
        max.save()
        v1 = Vote()
        v1.user = max
        v1.save()
        v1.nodes.add(self.text5)
        v1.save()

    def test_get_favorite_if_slot(self):
        n = get_favorite_if_slot(self.root)
        self.assertEqual(n, self.root)
        n = get_favorite_if_slot(self.slot1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.text1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.slot2)
        self.assertEqual(n, self.text4)
        n = get_favorite_if_slot(self.slot3)
        self.assertEqual(n, self.text5)

    def test_get_ordered_children_for(self):
        list = get_ordered_children_for(self.slot3)
        self.assertSequenceEqual(list, [self.text5,self.text6])