"""Download the data and plot forest fire emissions against GDP

    snakemake --cores 1

makes doc/fire_gdp.png (every country in one figure) and one
doc/countries/{country}.png per country.
"""

# Data file name (without .csv) -> download URL
DATA_URLS = {
    'Agrofood_co2_emission':
        'https://docs.google.com/uc?export=download'
        '&id=1AsXP_OGs1O_TDeXiZjk3fYV1SrG4vwXF',
    'IMF_GDP':
        'https://docs.google.com/uc?export=download'
        '&id=19YEPysdnK7VCXuAe9Og9pwYkNT5CbQzr',
}

# File name -> country name as written in both data files. The first six are
# from Assignment 6; the rest are the other countries in the top 14 for total
# forest fire emissions that also have GDP data.
COUNTRIES = {
    'Brazil': 'Brazil',
    'DR_Congo': 'Democratic Republic of the Congo',
    'Russia': 'Russian Federation',
    'Australia': 'Australia',
    'Canada': 'Canada',
    'USA': 'United States of America',
    'Central_African_Republic': 'Central African Republic',
    'Zambia': 'Zambia',
    'Mozambique': 'Mozambique',
    'Angola': 'Angola',
    'Myanmar': 'Myanmar',
    'Tanzania': 'United Republic of Tanzania',
    'Bolivia': 'Bolivia (Plurinational State of)',
    'Cambodia': 'Cambodia',
    'Indonesia': 'Indonesia',
    'India': 'India',
}

CO2_FILE = 'data/Agrofood_co2_emission.csv'
GDP_FILE = 'data/IMF_GDP.csv'


def quote(names):
    """Quote each name so names with spaces stay one shell argument."""
    return ' '.join(f'"{name}"' for name in names)


wildcard_constraints:
    dataset='|'.join(DATA_URLS),
    country='|'.join(COUNTRIES)


rule all:
    input:
        'doc/fire_gdp.png',
        expand('doc/countries/{country}.png', country=COUNTRIES)


rule get_inputs:
    output:
        'data/{dataset}.csv'
    params:
        url=lambda wildcards: DATA_URLS[wildcards.dataset]
    shell:
        """
        curl --fail -L "{params.url}" -o {output}
        """


rule plot_country:
    input:
        co2=CO2_FILE,
        gdp=GDP_FILE,
        script='src/plot_fire_gdp.py',
        lib='src/fire_gdp.py'
    output:
        'doc/countries/{country}.png'
    params:
        name=lambda wildcards: quote([COUNTRIES[wildcards.country]])
    shell:
        """
        python {input.script} \
            --co2_file {input.co2} \
            --gdp_file {input.gdp} \
            --countries {params.name} \
            --out {output}
        """


rule plot_all_countries:
    input:
        co2=CO2_FILE,
        gdp=GDP_FILE,
        script='src/plot_fire_gdp.py',
        lib='src/fire_gdp.py'
    output:
        'doc/fire_gdp.png'
    params:
        names=quote(COUNTRIES.values())
    shell:
        """
        python {input.script} \
            --co2_file {input.co2} \
            --gdp_file {input.gdp} \
            --countries {params.names} \
            --out {output}
        """
