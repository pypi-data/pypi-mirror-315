# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Table import Table
from orionpy.orioncore.resources.Tables import Tables

# =============================================================================
# CLASS
# =============================================================================


class TestTables(unittest.TestCase):
    def setUp(self):
        self.tables = Tables("Serv_MapServer")
        self.service_def = {
            "definition": {
                "capabilities": "Create,Query,Update",
                "isManaged": True,
                "tables": [{"id": 0, "name": "tab0"}, {"id": 1, "name": "tab1"}],
            }
        }

        responses.add(
            responses.GET,
            self.tables.url_manager.resource_definition_url("Serv_MapServer"),
            json=self.service_def,
            status=200,
        )

    @responses.activate
    def test_update(self):
        self.tables._update()
        tables = self.tables.all()
        self.assertEqual(len(tables), len(self.service_def["definition"]["tables"]))
        for table in tables:
            self.assertIsInstance(table, Table)
