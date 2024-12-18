# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.Group import Group
from orionpy.orioncore.Groups import Groups

# =============================================================================
# CLASS
# =============================================================================


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.groups = Groups()

        self.group_org = {
            "name": "org",
            "title": "Organisateur",
            "properties": {"builtinRole": "org"},
        }

        self.group_public = {
            "name": "public",
            "title": "Public",
            "properties": {"builtinRole": "public"},
        }

        self.group_lists = {
            "results": [
                {"id": "gr1_id", "title": "group 1"},
                {"id": "gr2_id", "title": "group 2"},
                {"id": "gr3_id", "title": "group 3"},
            ],
            "nextStart": -1,
        }

        self.portal = {"id": "123456789ABCDE"}
        responses.add(
            responses.GET,
            self.groups.url_manager.subject_list_url("groups"),
            json=self.group_lists,
            status=200,
        )

        responses.add(
            responses.GET,
            self.groups.url_manager.self_url(),
            json=self.portal,
            status=200,
        )

        responses.add(
            responses.GET,
            self.groups.url_manager.subject_information_url("groups", "org"),
            json=self.group_org,
            status=200,
        )

        responses.add(
            responses.GET,
            self.groups.url_manager.subject_information_url("groups", "public"),
            json=self.group_public,
            status=200,
        )

    @responses.activate
    def test_update(self):
        self.groups._update()
        self.assertEqual(5, len(self.groups._elements))

        group_def = self.group_lists["results"][0]
        group_test = Group(group_def["title"], group_def["id"])
        self.assertEqual(
            group_test.__str__(), self.groups._elements[group_def["title"]].__str__()
        )

    @responses.activate
    def test_get_with_id(self):
        group_def = self.group_lists["results"][1]
        group_test = Group(group_def["title"], group_def["id"])
        group_result = self.groups.get_with_id("gr2_id")
        self.assertIsInstance(group_result, Group)
        self.assertEqual(group_test.__str__(), group_result.__str__())
        self.assertIsNone(self.groups.get_with_id("wrong"))

    @responses.activate
    def test_all(self):
        self.assertEqual(5, len(self.groups.all()))

    @responses.activate
    def test_get(self):
        group_def = self.group_lists["results"][1]
        group_test = Group(group_def["title"], group_def["id"])
        group_result = self.groups.get("  group 2  ")
        self.assertIsInstance(group_result, Group)
        self.assertEqual(group_test.__str__(), group_result.__str__())
        self.assertIsNone(self.groups.get("wrong"))
