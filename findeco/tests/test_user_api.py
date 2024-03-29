#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
import json

from node_storage.factory import create_user
from ..api_validation import errorResponseValidator, loadUserInfoResponseValidator, loadUserSettingsResponseValidator
from ..view_helpers import create_user_info, create_user_settings


class LoadUserInfoTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.herbert = create_user('herbert')
        self.hein = create_user('hein')
        self.users = [self.hans, self.herbert, self.hein]

    def test_with_valid_username_returns_correct_user_info(self):
        for u in self.users:
            response = self.client.get(reverse('load_user_info', kwargs=dict(name=u.username)))
            parsed = json.loads(response.content)
            self.assertTrue(loadUserInfoResponseValidator.validate(parsed))
            user_info = create_user_info(u)
            self.assertEqual(parsed['loadUserInfoResponse']['userInfo'], user_info)

    def test_with_invalid_username_returns_error_response(self):
        for n in ['hannes', 'harbart', 'nieh']:
            response = self.client.get(reverse('load_user_info', kwargs=dict(name=n)))
            parsed = json.loads(response.content)
            self.assertTrue(errorResponseValidator.validate(parsed))
            self.assertEqual(parsed['errorResponse']['errorTitle'], "UnknownUser")

class LoadUserSettingsTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', password="1234")
        self.herbert = create_user('herbert', password="1234")
        self.hans.profile.blocked.add(self.herbert.profile)
        self.users = [self.hans, self.herbert]

    def test_response_validates(self):
        for u in self.users:
            self.assertTrue(self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertTrue(loadUserSettingsResponseValidator.validate(parsed))

    def test_returns_correct_user_info_for_logged_in_user(self):
        for u in self.users:
            self.assertTrue(self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertEqual(parsed['loadUserSettingsResponse']['userInfo'], create_user_info(u))

    def test_returns_correct_user_settings_for_logged_in_user(self):
        for u in self.users:
            self.assertTrue(self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertEqual(parsed['loadUserSettingsResponse']['userSettings'], create_user_settings(u))

    def test_not_logged_in_returns_error_response(self):
        for u in self.users:
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertTrue(errorResponseValidator.validate(parsed))
            self.assertEqual(parsed['errorResponse']['errorTitle'], "NeedsAuthentication")
