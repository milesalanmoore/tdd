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
    """Pair a country's forest fire emissions with its GDP by year.

    Years with a missing fire or GDP value, or that are not in the GDP
    header, are skipped.

    Parameters
    ----------
    co2_file : str
        CSV with Area (index 0), Year (index 1), and Forest fires columns
    gdp_file : str
        CSV with Country (index 0) and one column per year
    country : str
        Country name as written in both files

    Returns
    -------
    data : list of [int, float, float]
        [year, forest_fires, gdp] for each matched year
    """
    co2_header, co2_rows = get_data(co2_file, 0, country, return_header=True)
    gdp_header, gdp_rows = get_data(gdp_file, 0, country, return_header=True)
    if not gdp_rows:
        return []
    gdp_row = gdp_rows[0]
    fire_index = get_column_index(co2_header, 'Forest fires')

    data = []
    for row in co2_rows:
        year = row[1]
        fires = row[fire_index]
        gdp_index = get_column_index(gdp_header, year)
        if gdp_index is None or fires == '' or gdp_row[gdp_index] == '':
            continue
        data.append([int(year), float(fires), float(gdp_row[gdp_index])])
    return data
