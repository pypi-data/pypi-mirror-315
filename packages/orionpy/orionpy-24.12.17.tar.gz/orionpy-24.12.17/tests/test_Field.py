# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.resources.Field import Field

# =============================================================================
# CLASS
# =============================================================================


class TestField(unittest.TestCase):
    def setUp(self):
        description = {"name": "fName", "type": "type", "alias": "alias"}
        self.field = Field(
            description=description,
            service_url="serv",
            layer_id=5,
            capa="ca1,ca2",
            is_managed=True,
        )

    def test_str(self):
        self.assertEqual(
            "Field fName; alias alias; layer 5; service serv", self.field.__str__()
        )

    def test_activate_FDU_filter(self):
        # TODO see if can check printing
        self.field.activate_fdu_filter(None, None)

    def test_deactivate_FDU_filter(self):
        # TODO see if can check printing
        self.field.deactivate_fdu_filter(None, None)

    def test_activate_SQL_filter(self):
        # TODO see if can check printing
        self.field.activate_sql_filter(None, None)

    def test_deactivate_SQL_filter(self):
        # TODO see if can check printing
        self.field.deactivate_sql_filter(None, None)

    def test_can_change_rights(self):  # TODO tests
        # Call to super
        # group_rights = {'isInherited': True}
        # self.assertFalse(self.field._can_change_rights(group_rights, RightLevel.WRITE,
        #                                                disable_inheritance = False,
        #                                                group = None))
        # # -- Test in the good contexts --
        # group_rights = {'isInherited': False, 'rights': [{'action': 'read'}]}
        # self.assertTrue(self.field._can_change_rights(group_rights, RightLevel.ACCESS,
        #                                               disable_inheritance = False,
        #                                               group = None))
        pass

    def test_get_name(self):
        # get_name returns the alias for fields
        self.assertEqual("alias", self.field.get_name())
