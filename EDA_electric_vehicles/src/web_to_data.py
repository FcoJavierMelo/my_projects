import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO


def data_lifetime_from_web():
    response = requests.get("https://www.iea.org/data-and-statistics/charts/comparative-life-cycle-greenhouse-gas"
                            "-emissions-over-ten-year-lifetime-of-an-average-mid-size-car-by-powertrain-2018")

    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find('div', class_='m-chart-block')

    data_aux = StringIO(data.get_attribute_list('data-chart-csv')[0].replace("\\", ""))

    df = pd.read_csv(data_aux, sep=",", quotechar='"')

    df.rename(columns={"Unnamed: 0": "Type"}, inplace=True)

    df.to_csv('../Datos/Coches/emissions_lifetime_cars.csv', index=False)


def row_text_convert(row_text, title=False):
    row_text = row_text.replace('%', '')
    row_text = row_text.replace('N/A', '0')

    if row_text != '':
        if row_text.find('[') == -1:
            row_text = row_text.strip()
        else:
            row_text = row_text[:row_text.find('[')].strip()
    else:
        if title:
            row_text = 'Column'
        else:
            row_text = '0'

    return row_text


def wikipedia_html_table_to_dataframe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    data = []
    table = soup.find('table', attrs={'class': 'sortable wikitable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        titles = row.find_all('th')
        data.append([row_text_convert(title.text, title=True) for title in titles])  # Get rid of empty values

        values = row.find_all('td')
        data.append([row_text_convert(value.text) for value in values])  # Get rid of empty values

    df = pd.DataFrame(data[1:-1], columns=data[0])

    df.dropna(inplace=True)

    df.drop(['Column'], axis=1, inplace=True, errors="ignore")

    df = df.reset_index(drop=True)

    df.to_csv('../Datos/Coches/plugin-cars-sales.csv', index=False)


def evcars_html_table_to_dataframe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    data = []
    table = soup.find('table', attrs={'class': 'aligncenter'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        cols = [ele.text.strip() if ele.text != '' else 'Column' for ele in cols]
        print(cols)
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    df = pd.DataFrame(data[1:], columns=data[0])

    df.drop(['Column'], axis=1, inplace=True)

    return df


df_evcars2020 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2020-ev-phev/")
df_evcars2020.to_csv('../Datos/Coches/ev-cars-sales-2020.csv', index=False)

df_evcars2019 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2019-ev-phev/")
df_evcars2019.to_csv('../Datos/Coches/ev-cars-sales-2019.csv', index=False)

df_evcars2018 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2018-ev-phev/")
df_evcars2018.to_csv('../Datos/Coches/ev-cars-sales-2018.csv', index=False)

df_evcars2017 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2017-ev-phev/")
df_evcars2017.to_csv('../Datos/Coches/ev-cars-sales-2017.csv', index=False)

df_evcars2016 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2016-ev-phev/")
df_evcars2016.to_csv('../Datos/Coches/ev-cars-sales-2016.csv', index=False)

df_evcars2015 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2015-ev-phev/")
df_evcars2015.to_csv('../Datos/Coches/ev-cars-sales-2015.csv', index=False)

df_evcars2014 = evcars_html_table_to_dataframe("https://carsalesbase.com/european-sales-2014-ev-and-phev-segment/")
df_evcars2014.to_csv('../Datos/Coches/ev-cars-sales-2014.csv', index=False)

data_lifetime_from_web()

wikipedia_html_table_to_dataframe("https://en.wikipedia.org/wiki/Electric_car_use_by_country")
