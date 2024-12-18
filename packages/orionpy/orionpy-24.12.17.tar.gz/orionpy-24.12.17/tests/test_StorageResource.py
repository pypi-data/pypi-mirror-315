# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.StorageResource import StorageResource

# from orionpy.orioncore.Group import Group
# from orionpy.orioncore.resources.Resource import RightLevel

# =============================================================================
# CLASS
# =============================================================================


class TestStorageResource(unittest.TestCase):
    def setUp(self):
        self.resource = StorageResource(
            {
                "dimensionId": "",
                "id": "standard",
                "service": {"url": "Hosted/StatService/FeatureServer"},
                "tables": [],
                "type": "service",
            }
        )

        responses.add(
            responses.POST,
            "https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Stats/standard/__configure",
            status=200,
        )

        self.stats_status = {"mode": "Full", "operations": [], "rules": []}
        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/stats/status",
            json=self.stats_status,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/stats/synthesis",
            json={},
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/stats/clean",
            json={},
            status=200,
        )

        self.session_id = "31b9afc8-f8f2-4cb4-a6a2-9b141b2c173a"
        responses.add(
            responses.POST,
            "https://front.arcopole.fr/Orion/orion/stats/newSession",
            json={"sessionId": self.session_id},
            status=200,
        )

        responses.add(
            responses.POST,
            "https://front.arcopole.fr/Orion/orion/stats/heartBeat",
            json={"success": True, "normalInterval": 30, "maxInterval": 24},
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/stats/push",
            json={"success": True, "result": []},
            status=200,
        )

    def test_instance(self):
        self.assertTrue("standard" in str(self.resource))

    @responses.activate
    def test_update_filter(self):
        self.assertEqual("", self.resource.filter_id)

        self.resource.update_filter("new_filter")

        self.assertEqual("new_filter", self.resource.filter_id)

    @responses.activate
    def test_get_status(self):
        self.assertEqual(self.stats_status, self.resource.get_status())

    @responses.activate
    def test_create_new_session(self):
        self.assertEqual(self.session_id, self.resource.create_new_session(None))

    @responses.activate
    def test_heart_beat(self):
        self.resource.heart_beat(None)

    @responses.activate
    def test_push(self):
        self.resource.push()

    @responses.activate
    def test_synthesis(self):
        self.resource.synthesis()

    @responses.activate
    def test_clean(self):
        self.resource.clean()

    @responses.activate
    def test_disassociate_filter(self):
        self.resource.update_filter("new_filter")
        self.resource.disassociate_filter()
        self.assertEqual("", self.resource.filter_id)
