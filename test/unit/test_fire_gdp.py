import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import fire_gdp  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CO2_FILE = os.path.join(DATA_DIR, 'co2.csv')
GDP_FILE = os.path.join(DATA_DIR, 'gdp.csv')


class TestGetData(unittest.TestCase):

    def test_all_rows(self):
        rows = fire_gdp.get_data(CO2_FILE)
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0], ['Brazil', '2000', '10.0', '100.5'])

    def test_quoted_comma_field(self):
        rows = fire_gdp.get_data(CO2_FILE)
        self.assertEqual(rows[-1][0], 'China, Hong Kong SAR')

    def test_query(self):
        rows = fire_gdp.get_data(GDP_FILE, query_column=0,
                                 query_value='Chile')
        self.assertEqual(rows, [['Chile', '500.00', '', '', '']])

    def test_query_no_match(self):
        rows = fire_gdp.get_data(GDP_FILE, query_column=0,
                                 query_value='Peru')
        self.assertEqual(rows, [])

    def test_return_header(self):
        header, rows = fire_gdp.get_data(GDP_FILE, return_header=True)
        self.assertEqual(header, ['Country', '2000', '2001', '2002', '2003'])
        self.assertEqual(len(rows), 2)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            fire_gdp.get_data('no_such_file.csv')


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        header = ['Country', '2000', '2001']
        self.assertEqual(fire_gdp.get_column_index(header, '2001'), 2)

    def test_name_absent(self):
        header = ['Country', '2000', '2001']
        self.assertIsNone(fire_gdp.get_column_index(header, '1999'))

    def test_empty_header(self):
        self.assertIsNone(fire_gdp.get_column_index([], 'Country'))


class TestGetFireGdpYearData(unittest.TestCase):

    def test_matches_years_and_skips_missing(self):
        # 2001 has no fire value, 2003 no GDP value, 2004 is not a GDP year
        data = fire_gdp.get_fire_gdp_year_data(CO2_FILE, GDP_FILE, 'Brazil')
        self.assertEqual(data, [[2000, 100.5, 1000.0],
                                [2002, 102.5, 1200.0]])

    def test_types(self):
        year, fires, gdp = fire_gdp.get_fire_gdp_year_data(
            CO2_FILE, GDP_FILE, 'Brazil')[0]
        self.assertIsInstance(year, int)
        self.assertIsInstance(fires, float)
        self.assertIsInstance(gdp, float)

    def test_country_not_in_gdp(self):
        data = fire_gdp.get_fire_gdp_year_data(
            CO2_FILE, GDP_FILE, 'China, Hong Kong SAR')
        self.assertEqual(data, [])


if __name__ == '__main__':
    unittest.main()
