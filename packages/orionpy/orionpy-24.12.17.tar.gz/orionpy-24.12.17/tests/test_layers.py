# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Layers import Layers

# =============================================================================
# CLASS
# =============================================================================


class TestLayers(unittest.TestCase):
    def setUp(self):
        self.layers = Layers("Serv_MapServer")

        self.service_def = {
            "definition": {
                "capabilities": "Create,Query,Update",
                "isManaged": True,
                "layers": [
                    {
                        "id": 0,
                        "name": "lay0",
                        "parentLayerId": -1,
                        "defaultVisibility": True,
                        "subLayerIds": None,
                        "minScale": 0,
                        "maxScale": 0,
                    },
                    {
                        "id": 1,
                        "name": "lay1",
                        "parentLayerId": -1,
                        "defaultVisibility": True,
                        "subLayerIds": None,
                        "minScale": 2000,
                        "maxScale": 0,
                    },
                ],
            }
        }
        responses.add(
            responses.GET,
            self.layers.url_manager.resource_definition_url("Serv_MapServer"),
            json=self.service_def,
            status=200,
        )

    @responses.activate
    def test_update(self):
        self.layers._update()
        self.assertEqual(
            len(self.layers._elements), len(self.service_def["definition"]["layers"])
        )

    @responses.activate
    def test_get_id(self):
        self.layers._update()
        self.assertEqual(self.layers.get_id("lay0"), "0")
        self.assertIsNone(self.layers.get_id("WRONG"))
