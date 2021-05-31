import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, external_stylesheets])

df_generacion = pd.read_csv('../Datos/Generacion/owid-energy-data.txt')

columns_share = []

columns_share = [col for col in df_generacion.columns if ('share_elec' in col) or ('year' in col)]

df_europe = df_generacion[(df_generacion['year']>=2012) &
                          (df_generacion['year']<=2019) &
                          (df_generacion['country'] == 'Europe')]

df_europe_share = df_europe.filter(columns_share)

df_prueba = df_generacion[(df_generacion["year"] == 2018)
                          & (df_generacion["country"] != 'World')
                          & (df_generacion["country"] != 'Europe (other)')
                          & (df_generacion["country"] != 'Europe')
                          & (df_generacion["country"] != 'Asia Pacific')
                          & (df_generacion["country"] != 'Central America')
                          & (df_generacion["country"] != 'Middle Africa')
                          & (df_generacion["country"] != 'Middle East')
                          & (df_generacion["country"] != 'North America')
                          & (df_generacion["country"] != 'Other Asia & Pacific')
                          & (df_generacion["country"] != 'Other CIS')
                          & (df_generacion["country"] != 'Other Caribbean')
                          & (df_generacion["country"] != 'Other Middle East')
                          & (df_generacion["country"] != 'Other Northern Africa')
                          & (df_generacion["country"] != 'Other South America')
                          & (df_generacion["country"] != 'Other Southern Africa')
                          & (df_generacion["country"] != 'China')
                          & (df_generacion["country"] != 'United States')]

with open('../Datos/Mapas/custom.geo.json') as fp:
    geo_world = json.load(fp)

# Instanciating necessary lists
found = []
missing = []
countries_geo = []

# For simpler acces, setting "zone" as index in a temporary dataFrame
tmp = df_prueba.set_index('country')

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

df_europe = df_prueba[df_prueba["country"].isin(found)]

fig = px.choropleth_mapbox(
    df_europe,
    geojson=geo_world_ok,
    locations='country',
    color='electricity_generation',
    color_continuous_scale='oranges',
    mapbox_style='open-street-map',
    zoom=2.4,
    center={'lat': 55, 'lon': 11},
    opacity=0.6
)

# Define layout specificities
fig.update_layout(
    margin={'r':0,'t':0,'l':0,'b':0},
    coloraxis_colorbar={
        'title':'Tw/h'
    },
    title = "Generacion electricidad Europa 2019"
)

fig_bar_europe_share = px.bar(df_europe_share,
             x='year',
             y=['fossil_share_elec','nuclear_share_elec','renewables_share_elec'],
             barmode="group")

fig_bar_europe_share.update_layout(title='top')


# Display figure
#fig.show()

image_filename = '../img/meme_ev_1.jpg'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(
    [
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                 style={
                     'height': '50%',
                     'width': '50%'
                 }
                 ),
        dbc.Row([html.Iframe(src="https://www.youtube.com/embed/yCy-a_E2I3s",
                            width="879",
                            style={'width': '100 %',
                                   'height': '400px'}
                                   #'display': 'flex',
                                   #'align - items': 'center',
                                   #'justify - content': 'center'}
                            )], justify="center", align="center", className="h-50",
                ),
        dbc.Row(dbc.Col(html.H1(children='¿Es el futuro el coche electrico?'))),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='id_Dropdown_free_paid',
                    options=[
                        {'label': 'Free', 'value': 'Free'},
                        {'label': 'Paid', 'value': 'Paid'}
                    ],
                    value=['Free', 'Paid'],
                    multi=True
                )),
                dbc.Col(dcc.RangeSlider(
                    id='id_RangeSlider_reviews',
                    count=1,
                    min=-1,
                    max=2,
                    step=1000000,
                    value=[1, 2]
                )),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(
                    id='graph-scatter',
                    figure=fig
                ))
            ]
        )
    ], style={'textAlign': 'center'}
)


# [Input('id_RangeSlider_reviews', 'value')]
# Output('graph-bar', 'figure')

'''@app.callback(
    Output('graph-scatter', 'figure'),
    Output('graph-bar', 'figure'),
    [Input('id_Dropdown_free_paid', 'value')],
    [Input('id_RangeSlider_reviews', 'value')])
def update_graphs_selector(selected_type1, selected_type2):
    filtered_df = df_scatter[df_scatter["Type"].isin(selected_type1)]

    filtered_df = filtered_df[(filtered_df["Reviews"] >= selected_type2[0]) &
                              (filtered_df["Reviews"] <= selected_type2[1])]

    filtered_df_bar = pd.DataFrame({'count': filtered_df.groupby(['Category', "Installs"])['App'].count()}
                                   ).reset_index()

    fig = px.scatter(filtered_df, x="Reviews", y="Rating", color="Category")
    fig2 = px.bar(filtered_df_bar, x="Category", y='count', color="Installs", title="Long-Form Input")

    fig.update_layout()
    fig2.update_layout()

    return fig, fig2'''


if __name__ == '__main__':
    app.run_server(debug=True)
