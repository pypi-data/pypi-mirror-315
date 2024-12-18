# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.Exceptions import FilteringValuesError
from orionpy.orioncore.Filter import _FDUFilter
from orionpy.orioncore.User import User

# from orionpy.orioncore.Filter import  _SQLFilter

# =============================================================================
# CLASS
# =============================================================================


class TestUser(unittest.TestCase):
    """
    Unitary tests class for User
    """

    def setUp(self):
        self.user = User(title="title", user_id="user_id")
        partitions = [{"name": "val1"}, {"name": "val2"}, {"name": "val3"}]
        # TODO use FilterFactory instead
        self.fdu_filter = _FDUFilter(
            name="filter_fdu",
            attributeName=["attr"],
            partitions=partitions,
            filter_id="fdu_id",
        )

        user_info_url = self.user._url_builder.user_info_url(self.user.get_id())
        self.user_info = {
            "title": self.user.get_name(),
            "name": self.user.get_id(),
            "perimeters": [
                {"dimension": "fid", "valeures": "a,b"},
                {"dimension": self.fdu_filter.id, "valeures": "c,d"},
            ],
        }
        responses.add(responses.GET, user_info_url, json=self.user_info, status=200)

    def test_update_filters_values(self):  # TODO tests
        pass

    def test_reset_all_filters_values(self):  # TODO tests
        pass

    def test_set_filter_values(self):
        # Error cases tests
        # Test with no value set
        self.user.set_filter_values(fdu_filter=self.fdu_filter)
        self.assertRaisesRegex(
            FilteringValuesError,
            "[ERROR] If add_all is False, you must set selected_filtering_values !",
        )
        # Test with an empty list
        self.user.set_filter_values(fdu_filter=self.fdu_filter, labels=[])
        self.assertRaisesRegex(
            FilteringValuesError,
            "[ERROR] selected_filtering_values must not be an empty list",
        )

    def test_add_filtering_values(self):  # TODO tests
        pass

    def test_remove_filtering_values(self):  # TODO tests
        pass

    def test_apply_filtering_values(self):  # TODO tests
        pass

    def test_get_filter_index(self):  # TODO tests
        pass

    @responses.activate
    def test_get_filter_values(self):
        # error case test
        self.assertIsNone(self.user._get_filter_values("fake"))

        # Test with a filter defined
        vals = self.user._get_filter_values(self.fdu_filter.get_id())
        self.assertEqual(self.user_info["perimeters"][1]["valeures"], vals)

    @responses.activate
    def test_apply_configuration(self):
        user_conf_url = self.user._url_builder.subject_configure_url(
            "users", self.user.get_id()
        )
        responses.add(responses.GET, user_conf_url, json=self.user_info, status=200)
        self.user._apply_configuration(self.user_info)

    @responses.activate
    def test_user_information_minus_filter(self):
        expected = {
            "title": self.user.get_name(),
            "name": self.user.get_id(),
            "perimeters": [{"dimension": "fid", "valeures": "a,b"}],
        }
        self.assertDictEqual(
            expected, self.user._subject_information_minus_filter(self.fdu_filter)
        )

    def test_get_user_informations(self):  # TODO tests
        pass

    def test_build_perimeters(self):
        dict_tmp = self.user._build_perimeters(self.fdu_filter, ["val1", "ERR", "val2"])
        self.assertDictEqual(dict_tmp, {"dimension": "fdu_id", "valeures": "val1,val2"})

    def test_remove_current_filter_val(self):
        list1 = [{"dimension": "id1"}, {"dimension": "id2"}]
        list2 = list(list1)
        # Tries to remove an element not defined in the list
        self.user._remove_current_filter_value(list1, "NOT_DEFINED")
        self.assertListEqual(list1, list2)

        # Removes an element already defined in the list
        self.user._remove_current_filter_value(list1, "id2")
        self.assertListEqual(list1, [{"dimension": "id1"}])

    # ----- Test methods -----

    @responses.activate
    def test_has_defined_filter_values(self):
        self.assertTrue(self.user.has_defined_filter_values(self.fdu_filter))

    def test_has_label_set_for_filter(self):  # TODO tests
        pass

    # ----- Access methods -----
    def test_get_name(self):
        self.assertEqual(self.user.get_name(), self.user.title)

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), self.user.id)

    def test_get_activated_labels(self):  # TODO tests
        pass

    def test_print_defined_filtering_values(self):  # TODO tests
        pass

    def test_toStr(self):
        self.assertEqual('User "title"; id user_id', self.user.__str__())
