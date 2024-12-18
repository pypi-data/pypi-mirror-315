# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.Group import Group
from orionpy.orioncore.resources.CadastreResource import CadastreResource
from orionpy.orioncore.resources.Resource import RightLevel

# =============================================================================
# CLASS
# =============================================================================


class TestCadastreResource(unittest.TestCase):
    def setUp(self):
        self.resource = CadastreResource(
            {
                "_id": "rId",
                "definition": {
                    "filterByCommunesId": "fId",
                    "parcellesLayerReferenceIds": ["pId"],
                    "serviceReference": "Service_MapServer",
                },
            }
        )
        self.group = Group("Group name", "groupId")
        url = self.resource._url_builder.cadastre_configuration_url(self.group.get_id())
        responses.add(responses.POST, url, status=200)

        # For the calls to _get_current_rights
        current_rights = {
            "rights": [
                {"action": RightLevel.PUBLIC_ACCESS.name, "filteredDimensions": ["fid"]}
            ]
        }
        url = self.resource._url_builder.cadastre_rights_url(self.group.get_id())
        responses.add(responses.GET, url, json=current_rights, status=200)

    def test_set_associated_filter(self):  # TODO test
        pass

    @responses.activate
    def test_get_right_structure(self):
        rights = self.resource._get_right_structure(self.group)
        self.assertEqual(rights["rights"][0]["action"], RightLevel.PUBLIC_ACCESS.name)
        self.assertEqual(rights["rights"][0]["filteredDimensions"][0], "fid")

    def test_update_right(self):  # TODO test
        pass

    def test_update_right_from_string(self):  # TODO test
        pass

    def test_is_right_good(self):
        self.assertEqual(self.resource._is_right_good("nominatif"), True)
        self.assertEqual(self.resource._is_right_good("public"), True)
        self.assertEqual(self.resource._is_right_good("noaccess"), True)
        self.assertEqual(self.resource._is_right_good("nominatiff"), False)
        self.assertEqual(self.resource._is_right_good(""), False)

    def test_can_modify(self):  # TODO test
        pass
