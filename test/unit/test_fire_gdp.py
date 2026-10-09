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


if __name__ == '__main__':
    unittest.main()
