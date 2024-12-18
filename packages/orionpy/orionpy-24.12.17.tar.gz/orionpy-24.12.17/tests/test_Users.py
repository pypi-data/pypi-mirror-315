# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.User import User
from orionpy.orioncore.Users import Users

# =============================================================================
# CLASS
# =============================================================================


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.users = Users()

        self.user_lists = {
            "results": [
                {"username": "user1_id", "fullName": "user 1"},
                {"username": "user2_id", "fullName": "user 2"},
                {"username": "user3_id", "fullName": "user 3"},
                {"username": "user3_id_bis", "fullName": "user 3"},
            ],
            "nextStart": -1,
        }

        self.portal = {"id": "123456789ABCDE"}
        responses.add(
            responses.GET,
            self.users.url_manager.subject_list_url("users"),
            json=self.user_lists,
            status=200,
        )

        responses.add(
            responses.GET,
            self.users.url_manager.self_url(),
            json=self.portal,
            status=200,
        )

    @responses.activate
    def test_update(self):
        self.users._update()
        self.assertEqual(len(self.user_lists["results"]), len(self.users._elements))

        user_def = self.user_lists["results"][0]
        user_test = self._create_user(user_def["fullName"], user_def["username"])
        self.assertEqual(
            user_test.__str__(), self.users._elements[user_def["fullName"]].__str__()
        )

    @responses.activate
    def test_get_with_id(self):
        user_def = self.user_lists["results"][1]
        user_test = self._create_user(user_def["fullName"], user_def["username"])
        user_result = self.users.get_with_id("user2_id")
        self.assertIsInstance(user_result, User)
        self.assertEqual(user_test.__str__(), user_result.__str__())
        user_result = self.users.get_with_id("user3_id")
        self.assertIsInstance(user_result, User)
        user_result = self.users.get_with_id("user3_id_bis")
        self.assertIsInstance(user_result, User)
        self.assertIsNone(self.users.get_with_id("wrong"))

    @responses.activate
    def test_all(self):
        self.assertEqual(len(self.users.all()), len(self.user_lists["results"]))

    @responses.activate
    def test_get(self):
        user_def = self.user_lists["results"][1]
        user_test = self._create_user(user_def["fullName"], user_def["username"])
        user_result = self.users.get("  user 2  ")
        self.assertIsInstance(user_result, User)
        self.assertEqual(user_test.__str__(), user_result.__str__())
        self.assertIsNone(self.users.get("wrong"))

    def _create_user(self, title, username):
        return User(title, username + "(agol)")
