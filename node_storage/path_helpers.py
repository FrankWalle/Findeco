#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
from __future__ import division, print_function, unicode_literals
from models import Node

def get_node_for_path(path):
    """
    Return the node corresponding to given path.
    """
    return Node.objects.filter(id=0)[0]

def get_favorite_if_slot(node):
    """
    Returns the favorite child if given a slot and returns node otherwise.
    """
    return None

def get_arguments_for(node, arg_type='all'):
    """
    Return a list of arguments for node.
    arg_type can be one of: 'pro', 'con', 'neut', 'all'
    """
    return []

def get_ordered_children_for(node):
    """
    Return a list of children for given node ordered by their position.
    """
    return []