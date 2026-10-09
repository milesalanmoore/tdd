"""Combine forest fire emissions and GDP data by country and year

    * get_data - returns rows (and optionally the header) of a CSV file
    * get_column_index - returns the position of a column name in a header
    * get_fire_gdp_year_data - returns [year, forest_fires, gdp] per year
"""


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    pass


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
