"""Scatter plot forest fire emissions against GDP, one panel per country

GDP is in each country's own currency, so countries are never pooled.
"""
import argparse
import math
import statistics
import sys

import matplotlib
import matplotlib.pyplot as plt

import fire_gdp

matplotlib.use('Agg')

COUNTRIES = ['Brazil',
             'Democratic Republic of the Congo',
             'Russian Federation',
             'Australia',
             'Canada',
             'United States of America']


def parse_args():
    parser = argparse.ArgumentParser(
        description='Plot forest fire emissions vs GDP for each country.')
    parser.add_argument('--co2_file',
                        default='data/Agrofood_co2_emission.csv',
                        help='Agrofood CO2 emission CSV')
    parser.add_argument('--gdp_file',
                        default='data/IMF_GDP.csv',
                        help='IMF GDP CSV')
    parser.add_argument('--countries',
                        nargs='+',
                        default=COUNTRIES,
                        help='Countries to plot, one panel each')
    parser.add_argument('--out',
                        required=True,
                        help='Output image file')
    return parser.parse_args()


def plot_country(ax, data, country):
    """Scatter one country's GDP (x) against forest fires (y)."""
    years, fires, gdp = zip(*data)
    ax.scatter(gdp, fires)
    ax.set_title(f'{country}\n{years[0]}-{years[-1]}, '
                 f'r = {statistics.correlation(gdp, fires):.2f}',
                 fontsize=9)
    ax.set_xlabel('GDP (millions, local currency)')
    ax.set_ylabel('Forest fire emissions (kt CO2)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def main():
    args = parse_args()

    try:
        country_data = [(c, fire_gdp.get_fire_gdp_year_data(args.co2_file,
                                                            args.gdp_file,
                                                            c))
                        for c in args.countries]
    except FileNotFoundError as e:
        print(f'Could not find {e.filename}', file=sys.stderr)
        sys.exit(1)

    # correlation needs at least two points
    for country, data in country_data:
        if len(data) < 2:
            print(f'Skipping {country}: fewer than 2 years of data',
                  file=sys.stderr)
    country_data = [(c, d) for c, d in country_data if len(d) >= 2]
    if not country_data:
        print('No country has enough data to plot', file=sys.stderr)
        sys.exit(1)

    ncols = min(3, len(country_data))
    nrows = math.ceil(len(country_data) / ncols)
    fig, axes = plt.subplots(nrows, ncols, squeeze=False,
                             figsize=(4.5 * ncols, 4 * nrows))
    for ax, (country, data) in zip(axes.flat, country_data):
        plot_country(ax, data, country)
    for ax in axes.flat[len(country_data):]:
        ax.set_visible(False)

    fig.tight_layout()
    fig.savefig(args.out, bbox_inches='tight')


if __name__ == '__main__':
    main()
