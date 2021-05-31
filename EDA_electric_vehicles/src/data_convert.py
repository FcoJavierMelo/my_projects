import pandas as pd
import json


def data_world_electric():
    df_electric = pd.read_csv('../Datos/Generacion/owid-energy-data.txt')

    return df_electric


def year_of_data(df, name_field, year_start, year_end):
    mask = (df[name_field] >= year_start) & (df[name_field] <= year_end)
    df = df[mask]

    return df


def country_of_data(df, name_field, country):
    mask = df[name_field].isin(country)
    df = df[mask]

    return df


def data_filtered(name_field_year,
                  year_start,
                  year_end,
                  name_field_country,
                  country,
                  fields_string):
    df_generacion = data_world_electric()

    df = country_of_data(df_generacion, name_field_country, country)

    df = year_of_data(df, name_field_year, year_start, year_end)

    columns = [col for col in df.columns
               if (fields_string in col) or
               (name_field_year in col) or
               (name_field_country in col)
               ]

    df = df.filter(columns)

    return df


def transform_geojson(df):
    with open('../Datos/Mapas/custom.geo.json') as fp:
        geo_world = json.load(fp)

    # Instanciating necessary lists
    found = []
    missing = []
    countries_geo = []

    # For simpler acces, setting "country" as index in a temporary dataFrame
    tmp = df.set_index('country')

    # Looping over the custom GeoJSON file
    for country in geo_world['features']:

        # Country name detection
        country_name = country['properties']['name']

        # Checking if that country is in the dataset
        if country_name in tmp.index:

            # Adding country to our "Matched/found" countries
            found.append(country_name)

            # Getting information from both GeoJSON file and dataFrame
            geometry = country['geometry']

            # Adding 'id' information for further match between map and data
            countries_geo.append({
                'type': 'Feature',
                'geometry': geometry,
                'id': country_name
            })

        # Else, adding the country to the missing countries
        else:
            missing.append(country_name)

    # Displaying metrics
    geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}

    return geo_world_ok


def emissions_lifetime_cars():
    df_lifetime = pd.read_csv('../Datos/Coches/emissions_lifetime_cars.csv')

    return df_lifetime

def cars_sales():
    df_cars_sales = pd.read_csv('../Datos/Coches/sales-cars-europe-per-year.csv')

    return df_cars_sales

def plugin_cars_sales():
    df_plugin_cars_sales = pd.read_csv('../Datos/Coches/plugin-cars-sales.csv')

    return df_plugin_cars_sales


def melt_plugin_cars_sales(df):
    df = df.melt(id_vars=['Country'],
                 value_vars=['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013'],
                 var_name='year',
                 value_name='percentage')

    df.sort_values('year')

    return df


def clean_ev_cars_sales(df):
    # nos quedamos solos con las 2 primeras columnas, que seran los modelos y el año
    df.drop(df.iloc[:, 2:], inplace=True, axis=1)

    df.rename(columns={df.columns[0]: "electric car segment"}, inplace=True)

    mask = df["electric car segment"].isin(
        ["Segment total", "Citroën Berlingo EV",
         "Peugeot Partner EV", "Nissan e-NV200",
         "Nissan e-NV200 / Evalia","Renault Kangoo ZE"]
    )

    df = df[~mask]

    columna = df.columns[1]

    df = df.astype(str)

    df[columna] = df[columna].str.replace('.000', '')
    df[columna] = df[columna].str.replace('.', '')

    df[columna] = df[columna].astype(int)

    return df


def melt_ev_cars_sales(df):
    df = df.melt(id_vars=['electric car segment'],
                 value_vars=['2020', '2019', '2018', '2017', '2016', '2015', '2014'],
                 var_name='year',
                 value_name='sales')

    df.sort_values('year')

    return df


def ev_cars_sales():
    df_ev_cars_2014 = pd.read_csv('../Datos/Coches/ev-cars-sales-2014.csv', thousands=".")
    df_ev_cars_2015 = pd.read_csv('../Datos/Coches/ev-cars-sales-2015.csv', thousands=".")
    df_ev_cars_2016 = pd.read_csv('../Datos/Coches/ev-cars-sales-2016.csv', thousands=".")
    df_ev_cars_2017 = pd.read_csv('../Datos/Coches/ev-cars-sales-2017.csv', thousands=".")
    df_ev_cars_2018 = pd.read_csv('../Datos/Coches/ev-cars-sales-2018.csv', thousands=".")
    df_ev_cars_2019 = pd.read_csv('../Datos/Coches/ev-cars-sales-2019.csv', thousands=".")
    df_ev_cars_2020 = pd.read_csv('../Datos/Coches/ev-cars-sales-2020.csv', thousands=".")

    df_ev_cars_2014 = clean_ev_cars_sales(df_ev_cars_2014)
    df_ev_cars_2015 = clean_ev_cars_sales(df_ev_cars_2015)
    df_ev_cars_2016 = clean_ev_cars_sales(df_ev_cars_2016)
    df_ev_cars_2017 = clean_ev_cars_sales(df_ev_cars_2017)
    df_ev_cars_2018 = clean_ev_cars_sales(df_ev_cars_2018)
    df_ev_cars_2019 = clean_ev_cars_sales(df_ev_cars_2019)
    df_ev_cars_2020 = clean_ev_cars_sales(df_ev_cars_2020)

    df_ev_cars_all = pd.merge(df_ev_cars_2014, df_ev_cars_2015, how="outer", on='electric car segment')
    df_ev_cars_all = pd.merge(df_ev_cars_all, df_ev_cars_2016, how="outer", on='electric car segment')
    df_ev_cars_all = pd.merge(df_ev_cars_all, df_ev_cars_2017, how="outer", on='electric car segment')
    df_ev_cars_all = pd.merge(df_ev_cars_all, df_ev_cars_2018, how="outer", on='electric car segment')
    df_ev_cars_all = pd.merge(df_ev_cars_all, df_ev_cars_2019, how="outer", on='electric car segment')
    df_ev_cars_all = pd.merge(df_ev_cars_all, df_ev_cars_2020, how="outer", on='electric car segment')

    df_ev_cars_all = melt_ev_cars_sales(df_ev_cars_all)

    df_ev_cars_all = df_ev_cars_all.dropna()

    df_ev_cars_group = df_ev_cars_all[df_ev_cars_all['sales'] > 0].groupby('year').count()[['electric car segment']]

    df_ev_cars_group["sales"] = df_ev_cars_all.groupby('year')["sales"].sum()

    df_ev_cars_group.rename(columns={'electric car segment': 'num_models'}, inplace=True)

    return df_ev_cars_all, df_ev_cars_group





