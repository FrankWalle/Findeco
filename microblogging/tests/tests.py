#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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

from django.test import TestCase
from node_storage.factory import create_slot, create_textNode
from node_storage.factory import create_user
from ..models import create_post
from django.core.urlresolvers import reverse
import node_storage as backend
from ..models import Post
import json

class MicrobloggingTests(TestCase):
    def setUp(self):
        self.user_max = create_user("max",password="1234")
        self.user_maria = create_user("Maria")

        root = backend.get_root_node()
        slot1 = create_slot("Bla")
        root.append_child(slot1)

        self.text_node1 = create_textNode("Whatever","Testtext",[self.user_max])
        slot1.append_child(self.text_node1)

        slot2 = create_slot("Blubb")
        root.append_child(slot2)

        text_node2 = create_textNode("Whatever2","Testtext Nummer 2",[self.user_max])
        slot2.append_child(text_node2)

    def test_post_creation(self):
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla.1 gut.",self.user_max))
        posts.append(create_post("Ich finde /Blubb schlecht.", self.user_max))
        posts.append(create_post("Ich finde /Follopp schlecht.", self.user_max))

        all_posts = Post.objects.all()
        self.assertSequenceEqual(all_posts,posts)
        self.assertEqual(all_posts[0].text,'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
        self.assertEqual(all_posts[0].author,self.user_max)
        self.assertEqual(all_posts[0].id,1)
        self.assertSequenceEqual(all_posts[0].node_references.all(),[self.text_node1])

    def test_store_microblog_post(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.post(reverse('store_microblog_post', kwargs=dict(path="Bla.1")),
            dict(microBlogText="Bla bla bla. I had to say it."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)),0)
        self.assertEqual(len(Post.objects.filter(text="Bla bla bla. I had to say it.").all()),1)

    def test_load_microblogging(self):
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla.1 gut.",self.user_max))
        posts.append(create_post("Ich finde /Blubb schlecht.", self.user_max))

        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(reverse('load_microblogging',
            kwargs=dict(path="Slot_4.1/SubSlot_1.1",select_id=0,microblogging_load_type="newer")))
        self.assertEqual(response.content,'{"errorResponse": {"errorTitle": "Illegal path", "errorMessage": "Illegal path: Slot_4.1/SubSlot_1.1"}}')

        response = self.client.get(reverse('load_microblogging',
            kwargs=dict(path="Bla.1",select_id=0,microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogText'],'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
            self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogID'],19-i+1)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']),1)
            self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']),20)

        response = self.client.get(reverse('load_microblogging',
            kwargs=dict(path="Bla.1",select_id=3,microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogText'],'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
            self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogID'],19-i+4)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']),1)
            self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']),20)

        response = self.client.get(reverse('load_microblogging',
            kwargs=dict(path="Bla.1",select_id=6,microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(19):
            self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogText'],'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
            self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogID'],18-i+7)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']),1)
            self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']),19)

        response = self.client.get(reverse('load_microblogging',
            kwargs=dict(path="Blubb.1",select_id=0,microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertEqual(len(data['loadMicrobloggingResponse']),1)
        self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microBlogText'],'Ich finde <a href="/Blubb.1">Blubb.1</a> schlecht.')
        self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microBlogID'],26)
        self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(len(data['loadMicrobloggingResponse'][0]['authorGroup']),1)
        self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][0])


    def test_load_timeline(self):
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla.1 gut.",self.user_max))
        posts.append(create_post("Ich finde /Blubb schlecht.", self.user_max))

        self.assertTrue(self.client.login(username="max", password="1234"))
        response = self.client.get(reverse('load_timeline',
            kwargs=dict(name="max", select_id=0, microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogText'],
                'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
            self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogID'],19-i+1)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']),1)
            self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']),20)

        response = self.client.get(reverse('load_timeline',
            kwargs=dict(name="max", select_id=None, microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microBlogText'],
            'Ich finde <a href="/Blubb.1">Blubb.1</a> schlecht.')
        self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microBlogID'],26)
        self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(len(data['loadMicrobloggingResponse'][0]['authorGroup']),1)
        self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][0])
        for i in range(1,20):
            self.assertTrue('microBlogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogText'],
                'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
            self.assertTrue('microBlogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microBlogID'],26-i)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']),1)
            self.assertTrue('microBlogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']),20)