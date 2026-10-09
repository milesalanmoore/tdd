"""Combine forest fire emissions and GDP data by country and year

    * get_data - returns rows (and optionally the header) of a CSV file
    * get_column_index - returns the position of a column name in a header
    * get_fire_gdp_year_data - returns [year, forest_fires, gdp] per year
"""
import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    """Read rows from a CSV file, optionally keeping only matching rows.

    Parameters
    ----------
    file_name : str
        CSV file whose first line is a header
    query_column : int, optional
        Index of the column to match against query_value
    query_value : str, optional
        Keep only rows whose query_column equals this string
    return_header : bool
        If True, also return the header

    Returns
    -------
    rows : list of list of str
        Matching rows, or (header, rows) if return_header is True
    """
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader
                if query_column is None or row[query_column] == query_value]
    if return_header:
        return header, rows
    return rows


def get_column_index(header, column_name):
    """Find the position of a column name in a header.

    Parameters
    ----------
    header : list of str
        Column names
    column_name : str
        Name to look for

    Returns
    -------
    index : int or None
        Position of column_name, or None if it is not in header
    """
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass
