# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.resources.Fields import Fields
from orionpy.orioncore.resources.Layer import Layer

# =============================================================================
# CLASS
# =============================================================================


class TestLayer(unittest.TestCase):
    def setUp(self):
        description = {
            "id": 0,
            "name": "lName",
            "parentLayerId": -1,
            "defaultVisibility": True,
            "subLayerIds": None,
            "minScale": 0,
            "maxScale": 0,
        }
        self.layer = Layer(
            description=description,
            parent_service_url="serv",
            capabilities="ca1,ca2",
            is_managed=True,
        )

    def test_fields(self):
        self.assertIsInstance(self.layer.fields, Fields)

    def test_can_activate_FDU(self):  # TODO test
        # First test will exit at super can_activate_fdu
        self.assertFalse(self.layer._can_activate_FDU(None, None, None))

    def test_is_group(self):  # TODO tests
        pass

    def test_has_parent_layer(self):  # TODO test
        pass

    def test_has_sub_layers(self):  # TODO test
        pass

    def test_get_sub_layers_ids(self):  # TODO test
        pass

    def test_get_parent_layer_id(self):  # TODO test
        pass

    def test_str(self):  # TODO tests for group of layers.
        self.assertEqual(
            "Layer 0; name lName; type simple layer; for Service serv.",
            self.layer.__str__(),
        )
