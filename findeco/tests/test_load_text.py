#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
import json
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from findeco.api_validation import errorResponseValidator
from node_storage import get_root_node
from node_storage.factory import create_slot, create_user, create_textNode, create_vote, create_structureNode

class LoadTextTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.structureNode1 = create_structureNode('LangerWahlprogrammTitel', authors=[self.hans])
        self.slot11 = create_slot('Transparenz')
        self.textnode11 = create_textNode('Traaaansparenz', authors=[self.hans])
        self.slot11.append_child(self.textnode11)
        self.slot12 = create_slot('Bildung')
        self.textnode12 = create_textNode('Biiildung', authors=[self.hans])
        self.slot12.append_child(self.textnode12)
        self.slot13 = create_slot('Datenschutz')
        self.textnode13 = create_textNode('Daaatenschutz', authors=[self.hans])
        self.slot13.append_child(self.textnode13)
        self.structureNode1.append_child(self.slot11)
        self.structureNode1.append_child(self.slot12)
        self.structureNode1.append_child(self.slot13)
        self.slot1.append_child(self.structureNode1)

        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode('LangerGrundsatzTitel', authors=[self.hugo])
        self.slot2.append_child(self.textnode2)

        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode('Langweilig3', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.slot3.append_child(self.textnode33)
        create_vote(self.hans, [self.textnode33])

        self.top_slots = [self.slot1, self.slot2, self.slot3]
        self.child_slots = [self.slot11, self.slot12, self.slot13]
        self.short_titles = ['Wahlprogramm', 'Grundsatzprogramm', 'Organisatorisches']
        self.full_titles = ['LangerWahlprogrammTitel', 'LangerGrundsatzTitel','Langweilig3']
        self.authors = [[self.hans], [self.hugo], [self.hans, self.hugo]]

    def test_url_gives_correct_text(self):
        response = self.client.get(reverse('load_text', kwargs=dict(path="Wahlprogramm.1/Transparenz.1")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        print(data)

    def test_on_illegal_path_gives_error_response(self):
        illegal_paths = ['Wahlprogramm.1/foo', 'Wahlprogramm.1/foo.1.pro', 'Wahlprogramm.1/foo.1.pro.2']
        for p in illegal_paths:
            response = self.client.get(reverse('load_text', kwargs=dict(path=p)))
            parsed = json.loads(response.content)
            self.assertTrue(errorResponseValidator.validate(parsed))
            self.assertEqual(parsed['errorResponse']['errorTitle'], "IllegalPath")