# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.Filter import Filter, FilterFactory, _FDUFilter, _SQLFilter

# =============================================================================
# CLASS
# =============================================================================


class TestFilterFactory(unittest.TestCase):
    def test_buildFilter(self):
        # if no argument, returns a none
        self.assertIsNone(FilterFactory.build_filter())
        # ---- Test with arguments ----
        self.assertIsInstance(
            FilterFactory.build_filter(name="try", where_clause="where"), _SQLFilter
        )
        # attr not none
        self.assertIsInstance(
            FilterFactory.build_filter(
                name="try", attributes=["attr"], filtering_values=["val1"]
            ),
            _FDUFilter,
        )
        # attributename none
        self.assertIsNone(FilterFactory.build_filter(name="try"))

        # ---- Test with dictionary ----
        dic1 = {"whereClause": "where", "name": "name", "id": "id", "dbId": "dbId"}
        self.assertIsInstance(FilterFactory.build_filter(filter_dic=dic1), _SQLFilter)
        dic1 = {"whereClause": "", "name": "name", "id": "id", "dbId": "dbId"}
        self.assertIsNone(FilterFactory.build_filter(filter_dic=dic1), _SQLFilter)

        dic1 = {
            "name": "name",
            "id": "id",
            "dbId": "dbId",
            "attributeName": "attr",
            "properties": "prop",
            "partitions": "part",
        }
        self.assertIsInstance(FilterFactory.build_filter(filter_dic=dic1), _FDUFilter)
        # TODO tests with type_filt


class TestFilter(unittest.TestCase):
    def test_createFilter(self):
        """Test the Filter::__init__() method"""
        # Create a filter using arguments
        my_filter = Filter(name="filt1", filter_id="my_id")
        self.assertEqual("Filter filt1; id my_id", my_filter.__str__())

        # Creates a filter using a dictionary
        dic = {"name": "filt1", "properties": "", "id": "my_id"}
        my_filter = Filter(filter_dic=dic)
        self.assertEqual("Filter filt1; id my_id", my_filter.__str__())

    def test_toStr(self):
        """Test the Filter::__str__() overload"""
        # Test the conversion between a filter and a string
        my_filter = Filter(name="filt1", filter_id="my_id")
        self.assertEqual("Filter filt1; id my_id", my_filter.__str__())

        dic = {"name": "filt1", "properties": "", "id": "my_id"}
        my_filter = Filter(filter_dic=dic)
        self.assertEqual("Filter filt1; id my_id", my_filter.__str__())


class TestSQLFilter(unittest.TestCase):
    def test_createSQLFilter(self):
        """Test the _SQLFilter::__init__() method"""
        # Creation with parameters
        my_filter = _SQLFilter("filt1", " where Clause ")
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause', my_filter.__str__()
        )
        # Creation with parameters and id
        my_filter = _SQLFilter("filt1", " where Clause ", filter_id="filt_id")
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause; id filt_id',
            my_filter.__str__(),
        )
        # Creation with dictionary
        filt_dic = {
            "name": "filt1",
            "whereClause": " where Clause ", 
            "properties": "",
            "id": "filt_id",
            "dbId": "db_id",
        }
        my_filter = _SQLFilter(filter_dic=filt_dic)
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause; id filt_id',
            my_filter.__str__(),
        )
        # Creation with parameters and dictionary
        my_filter = _SQLFilter(
            name="FAKE", whereClause="FAKE", filter_id="FAKE", filter_dic=filt_dic
        )
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause; id filt_id',
            my_filter.__str__(),
        )

    def test_toStr(self):
        """Test the _SQLFilter::__str__() method"""
        # Creation with parameters
        my_filter = _SQLFilter("filt1", " where Clause ")
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause', my_filter.__str__()
        )
        # Creation with parameters and id
        my_filter = _SQLFilter("filt1", " where Clause ", filter_id="filt_id")
        self.assertEqual(
            'SQL Filter "filt1"; whereClause : where Clause; id filt_id',
            my_filter.__str__(),
        )


class TestFDUFilter(unittest.TestCase):
    def setUp(self):
        partitions = [
            {"name": "val1", "properties": {"attr1": "p11", "attr2": "p12"}},
            {"name": "val2", "properties": {"attr1": "p21", "attr2": "p22"}},
            {"name": "val3", "properties": {"attr1": "p31", "attr2": "p32"}},
        ]
        self.fdu_filter = _FDUFilter(
            name="filt1",
            attributeName=["attr1", "attr2"],
            partitions=partitions,
            filter_id="fdu_id",
        )

    def test_createFDUFilter(self):
        pass  # TODO ?

    def test_label_defined(self):
        """Test the _FDUFilter::label_defined() method"""
        self.assertTrue(self.fdu_filter.is_label_defined("val2"))
        self.assertFalse(self.fdu_filter.is_label_defined("WRONG"))

    def test_get_labels(self):
        """Test the _FDUFilter::get_labels() method"""
        self.assertListEqual(self.fdu_filter.get_labels(), ["val1", "val2", "val3"])

    def test_str_FDU(self):
        """Test the _FDUFilter::__str__() method"""
        self.assertEqual(
            "FDU Filter \"filt1\"; attribute name(s): ['attr1', 'attr2'];"
            "\n\tFiltering values = label:val1; values:p11, p12; label:val2; values:p21, p22;"
            " label:val3; values:p31, p32; id fdu_id",
            self.fdu_filter.__str__(),
        )
