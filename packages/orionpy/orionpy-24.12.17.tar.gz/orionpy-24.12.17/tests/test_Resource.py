# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.Filter import _FDUFilter, _SQLFilter
from orionpy.orioncore.Group import Group
from orionpy.orioncore.resources.Resource import Resource, RightLevel

# =============================================================================
# CLASS
# =============================================================================


class TestResource(unittest.TestCase):
    def setUp(self):
        self.resource = Resource(access_url="Res/serv/lay", is_managed=True)
        self.group = Group("Group name", "groupId")
        self.fdu_filter = _FDUFilter("fdu", ["attr"], filter_id="fdu_id")
        self.sql_filter = _SQLFilter("sql", "Where", filter_id="sql_id")

        url = self.resource._url_builder.resource_configuration_url(
            self.group.get_id(), self.resource.access_url
        )
        responses.add(responses.POST, url, status=200)

        # For the calls to _get_current_rights
        current_rights = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": ["fid"]}],
        }
        url = self.resource._url_builder.resource_rights_url(
            self.group.get_id(), self.resource.access_url
        )
        responses.add(responses.GET, url, json=current_rights, status=200)

    # ----- Filter activation -----

    @responses.activate
    def test_activate_FDU_filter(self):
        group_right = {"perimeters": [{"dimension": "fid"}]}
        url = self.resource._url_builder.group_information_url(self.group.id)
        responses.add(responses.GET, url, json=group_right, status=200)

        self.resource.activate_fdu_filter(self.group, self.fdu_filter)
        # TODO asserts

    @responses.activate
    def test_activate_SQL_filter(self):
        self.resource.activate_sql_filter(self.group, self.sql_filter)
        # TODO asserts

    @responses.activate
    def test_activate_filter(self):
        # Prepare data for test
        current_rights = {"rights": [{"filteredDimensions": ["fid"]}]}
        # Does the test itself.
        self.resource._activate_filter(current_rights, self.fdu_filter, self.group)
        self.assertEqual(len(current_rights["rights"][0]["filteredDimensions"]), 2)
        self.assertEqual(
            current_rights["rights"][0]["filteredDimensions"][1], self.fdu_filter.id
        )

    # ----- Filter deactivation -----

    @responses.activate
    def test_deactivate_FDU_filter(self):
        current_rights = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": ["fdu_id", "fid"]}],
        }
        url = self.resource._url_builder.resource_rights_url(
            self.group.get_id(), self.resource.access_url
        )
        responses.add(responses.GET, url, json=current_rights, status=200)
        self.resource.deactivate_fdu_filter(self.group, self.sql_filter)
        # TODO assert

    @responses.activate
    def test_deactivate_SQL_filter(self):
        current_rights = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": ["sql_id", "fid"]}],
        }
        url = self.resource._url_builder.resource_rights_url(
            self.group.get_id(), self.resource.access_url
        )
        responses.add(responses.GET, url, json=current_rights, status=200)
        self.resource.deactivate_sql_filter(self.group, self.sql_filter)
        # TODO assert

    @responses.activate
    def test_deactivate_filter(self):
        current_rights = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": ["fdu_id", "fid"]}],
        }
        url = self.resource._url_builder.resource_rights_url(
            self.group.get_id(), self.resource.access_url
        )
        responses.add(responses.GET, url, json=current_rights, status=200)
        self.resource._deactivate_filter(self.fdu_filter, self.group)
        # TODO asserts

    # ----- Access to current/parent rights -----
    @responses.activate
    def test_get_current_rights(self):
        # NB : to see the rights that will be returned, check self.setUp
        rights = self.resource._get_right_structure(self.group)
        self.assertFalse(rights["isInherited"])
        self.assertEqual(len(rights["rights"][0]["filteredDimensions"]), 1)

    @responses.activate
    def test_get_resolved_right(self):  # TODO test
        # Prepares data...
        url = self.resource._url_builder.resource_resolved_permissions_url(
            self.group.get_id(), self.resource.access_url
        )
        # for the first test
        res_rights = {"resolvedPermissions": {"write": {"permission": True}}}
        responses.add(responses.GET, url, json=res_rights, status=200)
        # For the second test
        res_rights = {"resolvedPermissions": {"read": {"permission": True}}}
        responses.add(responses.GET, url, json=res_rights, status=200)
        # For the third test
        res_rights = {"resolvedPermissions": {"wtcf": {"permission": True}}}
        responses.add(responses.GET, url, json=res_rights, status=200)

        self.assertEqual(self.resource.get_resolved_right(self.group), RightLevel.WRITE)
        self.assertEqual(self.resource.get_resolved_right(self.group), RightLevel.READ)
        self.assertEqual(
            self.resource.get_resolved_right(self.group), RightLevel.ACCESS
        )

    def test_get_parent_rights(self):  # TODO test
        pass

    def test_print_rights(self):  # TODO test
        pass

    # ----- Update level of right -----
    def test_update_right(self):  # TODO test
        pass

    @responses.activate
    def test_clear_all_rights(self):
        # TODO : assert (create a given right structure ?)
        # Prepares request.
        url = self.resource._url_builder.resource_clear_all_url(
            self.resource.access_url
        )
        responses.add(responses.POST, url, status=200)

        self.resource.clear_all_rights()

    # ----- Check validity of modification -----

    def test_is_shared_with(self):
        self.assertTrue(self.resource.is_shared_with(None))

    def test_has_parent(self):  # Tests OK
        self.resource.parent_access = "pare"
        self.assertTrue(self.resource._has_parent())
        self.resource.parent_access = ""
        self.assertFalse(self.resource._has_parent())

    def test_is_managed(self):  # Tests OK
        self.resource._is_managed = False
        self.assertFalse(self.resource.is_managed())
        self.resource._is_managed = True
        self.assertTrue(self.resource.is_managed())

    def test_has_inherited_right(self):  # TODO test
        pass

    def test_get_access_url(self):
        self.assertEqual(self.resource.get_access_url(), self.resource.access_url)

    def test_can_modify(self):  # TODO test
        # self.resource._is_managed = False
        # self.assertFalse(self.resource._can_modify(None, disable_inheritance = False))
        # self.resource._is_managed = True
        # group_rights = {'isInherited': True}
        # self.assertFalse(self.resource._can_modify(None,
        #                                            disable_inheritance = False))
        # group_rights = {'isInherited': False}
        # # TODO will not work when is_shared_with will work
        # self.assertTrue(self.resource._can_modify(group_rights, None))
        pass

    def test_can_change_rights(self):  # TODO test
        # Test with problemn in can_modify
        # group_rights = {'isInherited': True}
        # self.assertFalse(self.resource._can_change_rights(group_rights, RightLevel.WRITE,
        #                                                   disable_inheritance = False,
        #                                                   group = None))
        # # Test if Editing not in capabilities
        # self.resource.capa = ['ca1', 'ca2']
        # group_rights = {'isInherited': False}
        # self.assertFalse(self.resource._can_change_rights(group_rights, RightLevel.WRITE,
        #                                                   disable_inheritance = False,
        #                                                   group = None))
        # # Test read to read
        # group_rights = {'isInherited': False, 'rights': [{'action': 'read'}]}
        # self.assertFalse(self.resource._can_change_rights(group_rights, RightLevel.READ,
        #                                                   disable_inheritance = False,
        #                                                   group = None))
        # # Test write to write (with Editing)
        # self.resource.capa = ['ca1', 'Editing']
        # group_rights = {'isInherited': False, 'rights': [{'action': 'write'}]}
        # self.assertFalse(self.resource._can_change_rights(group_rights, RightLevel.WRITE,
        #                                                   disable_inheritance = False,
        #                                                   group = None))
        # # Test access to access
        # group_rights = {'isInherited': False, 'rights': []}
        # self.assertFalse(self.resource._can_change_rights(group_rights, RightLevel.ACCESS,
        #                                                   disable_inheritance = False,
        #                                                   group = None))
        # # -- Test in the good contexts --
        # group_rights = {'isInherited': False, 'rights': [{'action': 'read'}]}
        # self.assertTrue(self.resource._can_change_rights(group_rights, RightLevel.ACCESS,
        #                                                  disable_inheritance = False,
        #                                                  group = None))
        pass

    def test_can_activate_SQL(self):
        # Filter not of sql type
        self.assertFalse(
            self.resource._can_activate_SQL(group_rights=None, filt=None, group=None)
        )

    def test_can_activate_FDU(self):  # TODO tests
        # Test with problemn in can_modify
        # group_rights = {'isInherited': True}
        # self.assertFalse(self.resource._can_activate_FDU(group_rights, None, None))
        # # Filter not of fdu type
        # group_rights = {'isInherited': False, 'rights': []}
        # self.assertFalse(self.resource._can_activate_FDU(group_rights, filt = None, group = None))
        # # test with no read right on resource
        # f = _FDUFilter('name', ['attr'])
        # self.assertFalse(self.resource._can_activate_FDU(group_rights, filt = f, group = None))
        # # Test with a filter already applied
        # f.id = 'id'
        # group_rights = {'isInherited': False, 'rights': [{'filteredDimensions': [f.id]}]}
        # self.assertFalse(self.resource._can_activate_FDU(group_rights, filt = f, group = None))
        # # Test in good conditions
        # group_rights = {'isInherited': False, 'rights': [{'filteredDimensions': ['rand_id']}]}
        # self.assertTrue(self.resource._can_activate_FDU(group_rights, filt = f, group = None))
        pass

    @responses.activate
    def test_can_activate_filter(self):  # Nothing more to check
        # Test with problemn in can_modify
        self.resource._is_managed = False
        self.assertFalse(self.resource._can_activate_filter(None, None, None))

        self.resource._is_managed = True
        group_rights = {"isInherited": False, "rights": []}
        self.assertFalse(
            self.resource._can_activate_filter(group_rights, None, self.group)
        )

        group_rights = {
            "isInherited": False,
            "rights": [
                {"action": "read", "filteredDimensions": ["fid", self.fdu_filter.id]}
            ],
        }
        self.assertFalse(
            self.resource._can_activate_filter(
                group_rights, self.fdu_filter, self.group
            )
        )

    @responses.activate
    def test_can_deactivate_filter(self):  # TODO tests
        # Test with problemn in can_modify
        self.resource._is_managed = False
        self.assertFalse(self.resource._can_deactivate_filter(None, None, None))
        # Test with no filter to deactiate
        self.resource._is_managed = True
        group_rights = {"isInherited": False, "rights": []}
        self.assertFalse(
            self.resource._can_deactivate_filter(
                group_rights, filt=None, group=self.group
            )
        )
        # Test with filter to deactivate not defined here
        group_rights = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": ["fid"]}],
        }
        self.assertFalse(
            self.resource._can_deactivate_filter(
                group_rights, filt=self.fdu_filter, group=self.group
            )
        )
        # Test in good conditions
        group_rights = {
            "isInherited": False,
            "rights": [{"filteredDimensions": ["id", "fdu_id"]}],
        }
        self.assertTrue(
            self.resource._can_deactivate_filter(
                group_rights, filt=self.fdu_filter, group=self.group
            )
        )

    def test_prepare_rights_structure(self):  # Tests OK
        # Write -> read
        current = {"isInherited": False, "rights": [{"action": "write"}]}
        expected = {"isInherited": False, "rights": [{"action": "read"}]}
        self.assertDictEqual(
            expected, self.resource._prepare_rights_structure(current, RightLevel.READ)
        )
        # read -> write
        current = {"isInherited": False, "rights": [{"action": "read"}]}
        expected = {"isInherited": False, "rights": [{"action": "write"}]}
        self.assertDictEqual(
            expected, self.resource._prepare_rights_structure(current, RightLevel.WRITE)
        )
        # read/write --> access
        expected = {"isInherited": False, "rights": []}
        self.assertDictEqual(
            expected,
            self.resource._prepare_rights_structure(current, RightLevel.ACCESS),
        )
        # access --> read/write
        current = {"isInherited": False, "rights": []}
        expected = {
            "isInherited": False,
            "rights": [{"action": "read", "filteredDimensions": []}],
        }
        self.assertDictEqual(
            expected, self.resource._prepare_rights_structure(current, RightLevel.READ)
        )
        expected = {
            "isInherited": False,
            "rights": [{"action": "write", "filteredDimensions": []}],
        }
        self.assertDictEqual(
            expected, self.resource._prepare_rights_structure(current, RightLevel.WRITE)
        )

    # ----- Change inheritance -----

    @responses.activate
    def test_enable_inheritance(self):
        self.resource.enable_inheritance(self.group)
        # TODO asserts

    @responses.activate
    def test_disable_inheritance(self):
        self.resource.disable_inheritance(self.group)
        # TODO asserts

    @responses.activate
    def test_change_inheritance(self):
        # Test with problem in is_managed
        self.resource._is_managed = False
        self.assertFalse(self.resource._change_inheritance(None, None))
        # Test if nothing to change
        self.resource._is_managed = True
        self.assertFalse(self.resource._change_inheritance(self.group, False))
        # Test enabling inheritance
        # TODO asserts
        self.resource._change_inheritance(group=self.group, new_inheritance=True)
        # TODO test disabling inheritance

    def test_prepare_rights(self):
        # Switch to access
        group_rights = {"rights": []}
        Resource._prepare_rights(group_rights, RightLevel.ACCESS)
        self.assertListEqual(group_rights["rights"], [])

        # Empty list and switch to sth else that access
        Resource._prepare_rights(group_rights, RightLevel.READ)
        self.assertDictEqual(
            group_rights["rights"][0], {"action": RightLevel.READ.value}
        )

        # Not an empty list and switch to sth else than access
        group_rights = {"rights": [{"action": "action"}]}
        Resource._prepare_rights(group_rights, RightLevel.WRITE)
        self.assertDictEqual(
            group_rights["rights"][0], {"action": RightLevel.WRITE.value}
        )
