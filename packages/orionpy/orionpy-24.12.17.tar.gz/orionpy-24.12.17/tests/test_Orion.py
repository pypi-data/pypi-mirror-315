# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.features.Geonotes import Geonotes
from orionpy.orioncore.features.Projects import Projects
from orionpy.orioncore.Filters import Filters
from orionpy.orioncore.Groups import Groups
from orionpy.orioncore.Orion import Orion
from orionpy.orioncore.resources.Businesses import Businesses
from orionpy.orioncore.resources.Services import Services

# =============================================================================
# CLASS
# =============================================================================


class TestOrion(unittest.TestCase):
    @responses.activate
    def setUp(self):
        self.answer_token = {"token": "token_val"}
        self.url_token = "https://front.arcopole.fr/portal/sharing/rest/generateToken"
        responses.add(
            responses.POST, self.url_token, json=self.answer_token, status=200
        )
        responses.add(
            responses.GET,
            "https://front.arcopole.fr/aob-admin/app/aobconfig.json",
            json={"configs": [{"federated": True}]},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/self?f=json&token=token_val",
            json={"isSuperAdmin":True},
            status=200,
        )
        self.orion = Orion(
            "username",
            "pwd",
            "https://front.arcopole.fr",
            portal="portal",
            verify_cert=False,
        )

    def test_filters(self):
        self.assertIsInstance(self.orion.filters, Filters)

    def test_services(self):
        self.assertIsInstance(self.orion.services, Services)

    def test_businesses(self):
        self.assertIsInstance(self.orion.businesses, Businesses)

    def test_groups(self):
        self.assertIsInstance(self.orion.groups, Groups)

    def test_geonotes(self):
        self.assertIsInstance(self.orion.geonotes, Geonotes)
        print("ok")

    def test_projects(self):
        self.assertIsInstance(self.orion.projects, Projects)

    @responses.activate
    def test_generate_token(self):
        self.assertEqual(self.url_token, self.orion.url_manager.token_url())
        responses.add(
            responses.POST, self.url_token, json=self.answer_token, status=200
        )
        self.orion._generate_token("username", "pwd", self.url_token)
