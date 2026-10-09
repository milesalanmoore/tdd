import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import fire_gdp  # noqa: E402


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
