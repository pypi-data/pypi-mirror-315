# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Layers import Layers
from orionpy.orioncore.resources.Service import Service
from orionpy.orioncore.resources.Tables import Tables

# =============================================================================
# CLASS
# =============================================================================


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service(
            service_id="s_id",
            access_url="Serv_MapServer",
            capabilities="cap1,cap2",
            is_managed=True,
        )

    def test_layers(self):
        self.assertIsInstance(self.service.layers, Layers)

    def test_tables(self):
        self.assertIsInstance(self.service.tables, Tables)

    def test_is_shared_with(self):  # TODO test
        pass

    def test_activate_SQL_filter(self):
        # TODO check printing
        self.service.activate_sql_filter(None, None)

    def test_deactivate_SQL_filter(self):
        # TODO check printing
        self.service.deactivate_sql_filter(None, None)

    def test_apply_filter(self):
        pass  # TODO test

    def test_get_current_rights(self):
        pass  # TODO test

    def test_change_inheritance(self):
        pass  # TODO test

    def test_update_rights(self):
        pass  # TODO test

    def test_enable(self):
        pass  # TODO test

    def test_disable(self):
        pass  # TODO test

    @responses.activate
    def test_change_management(self):  # TODO test
        url = self.service._url_builder.resource_management_url(
            self.service.get_access_url()
        )
        answer = {"message": "Handling by aOB changed"}
        responses.add(responses.GET, url, json=answer, status=200)

        self.service._change_management(enable=True)
        self.assertTrue(self.service.is_managed())

        self.service._change_management(enable=False)
        self.assertFalse(self.service.is_managed())

    def test_str(self):
        """Test Service:__str() method"""
        self.assertEqual(
            "Service Serv_MapServer; id s_id; MANAGED", self.service.__str__()
        )
