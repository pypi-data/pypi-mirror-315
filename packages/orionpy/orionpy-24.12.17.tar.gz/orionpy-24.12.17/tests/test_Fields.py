# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Fields import Fields

# =============================================================================
# CLASS
# =============================================================================


class TestFields(unittest.TestCase):
    def setUp(self):
        self.fields = Fields("serv", "1")

        self.layer_def = {
            "definition": {
                "id": 0,
                "name": "lay0",
                "capabilities": "Create,Query,Update,Delete,Uploads,Editing",
                "isManaged": True,
                "fields": [
                    {"name": "field1", "type": "Type1", "alias": "My field 1"},
                    {"name": "field2", "type": "Type2", "alias": "My field 2"},
                ],
            }
        }

        responses.add(
            responses.GET,
            self.fields.url_manager.resource_definition_url("serv/1"),
            json=self.layer_def,
            status=200,
        )

    @responses.activate
    def test_update(self):  # TODO test
        self.fields._update()
        self.assertEqual(
            len(self.fields._elements), len(self.layer_def["definition"]["fields"])
        )
