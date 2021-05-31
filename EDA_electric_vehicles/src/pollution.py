import streamlit as st
from PIL import Image
import plotly.express as px
import data_convert


def pollution_bar_graphs(df, x, y, labels, title, width):
    fig = px.bar(df,
                 x=x,
                 y=y,
                 labels=labels,
                 barmode="group")

    fig.update_layout(showlegend=True,
                      width=width,
                      legend=dict(
                          font=dict(size=8),
                          orientation="h",
                          yanchor="top",
                          y=1.12,
                          xanchor="left",
                          x=0.01
                      ),
                      title=dict(
                          text=title,
                          y=0.99))

    return fig


def pollution_map_graph(df, geojson, locations, color, title, color_scale):
    fig_map = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations=locations,
        color=color,
        color_continuous_scale=color_scale,
        mapbox_style='open-street-map',
        zoom=2,
        center={'lat': 55, 'lon': 11},
        opacity=0.6
    )

    # Define layout specificities
    fig_map.update_layout(
        # margin={'r':0,'t':0,'l':0,'b':0},
        width=570,
        height=600,
        coloraxis_colorbar={
            'title': '%'
        },
        title=title
    )

    return fig_map


def pollution(config):
    st.markdown('''
    ## ¿Es el coche eléctrico 0 emisiones? 
    Es importante definir que es ser "0 emisiones", un coche eléctrico no tiene
    emisiones directas, pero la electricidad que consume para cargar sus baterías si
    puede provenir de fuentes emisoras de contaminación.
    ''')

    img = Image.open("../img/meme_ev_1.jpg")
    st.image(img, use_column_width='auto')

    st.markdown('''
    
    
        ### Contaminación en ciudades 
        
        
        ''')

    img = Image.open("../img/contaminacion_ciudades.jpg")
    st.image(img, use_column_width='auto')

    st.markdown('''
     
     
     
        Una ventaja de la no emisión directa es el impacto que tendría en las ciudades donde [cerca del 60%](
        https://es.greenpeace.org/es/noticias/desmontamos-3-falsos-mitos-sobre-contaminacion-en-las-ciudades/) de la 
        contaminación proviene del trafico. 
        
        
        Bueno, salvo para este señor....
        ''')

    st.components.v1.iframe("""https://www.youtube.com/embed/pR1olDL5Vqo""",
                            scrolling=True,
                            height=500,
                            width=500)

    st.markdown('''
        ## Generación de electricidad en Europa 
        En las siguientes gráficas podemos observar la generación total de electricidad en Europa entre 2012 y 2019 ,
        tanto en Tw/h como porcentualmente y con que tipos de fuentes se genera dicha electricidad
        ''')

    list_europe_countries = ['Austria', 'Belarus', 'Belgium',
                             'Bulgaria', 'Croatia', 'Denmark',
                             'Estonia', 'Finland', 'France',
                             'Germany', 'Greece', 'Hungary',
                             'Iceland', 'Ireland', 'Italy',
                             'Netherlands', 'Norway', 'Poland',
                             'Latvia', 'Lithuania', 'Luxembourg',
                             'Portugal', 'Romania',
                             'Slovakia', 'Slovenia', 'Spain',
                             'Sweden', 'Switzerland',
                             'Ukraine', 'United Kingdom']

    df_europe_countries_share = data_convert.data_filtered("year",
                                                           2012,
                                                           2019,
                                                           "country",
                                                           list_europe_countries,
                                                           "share")

    df_europe_share = data_convert.data_filtered("year",
                                                 2012,
                                                 2019,
                                                 "country",
                                                 ["Europe"],
                                                 "share")

    df_europe_share.rename(columns={"fossil_share_elec": "Combustibles fosiles",
                                    "nuclear_share_elec": "Nuclear",
                                    "renewables_share_elec": "Renovables"}, inplace=True)

    df_europe_elect = data_convert.data_filtered("year",
                                                 2012,
                                                 2019,
                                                 "country",
                                                 ["Europe"],
                                                 "electricity")

    '''df_europe_share.rename(columns={"fossil_share_elec": "Combustibles fosiles",
                                    "nuclear_share_elec": "Nuclear",
                                    "renewables_share_elec": "Renovables"}, inplace=True)'''

    geo_world_ok = data_convert.transform_geojson(df_europe_countries_share)

    col1, col2 = st.beta_columns(2)

    with col1:
        fig_bar_europe_elect = pollution_bar_graphs(df_europe_elect,
                                                    'year',
                                                    ['electricity_generation',
                                                     'fossil_electricity',
                                                     'nuclear_electricity',
                                                     'renewables_electricity'],
                                                    {"variable": "Tipo", "year": "anio",
                                                     "value": "Electricidad Producida Tw/h"},
                                                    "Producción electricidad en Europa",
                                                    600)

        st.plotly_chart(fig_bar_europe_elect, use_container_width=False, **{'config': config})

    with col2:
        fig_bar_europe_share = pollution_bar_graphs(df_europe_share,
                                                    'year',
                                                    ['Combustibles fosiles', 'Nuclear', 'Renovables'],
                                                    {"variable": "Tipo", "year": "anio", "value": "Porcentaje"},
                                                    "Fuentes de generación por porcentaje en Europa",
                                                    600)
        st.plotly_chart(fig_bar_europe_share, use_container_width=False, **{'config': config})

    country = st.sidebar.selectbox("Pais", list_europe_countries)

    df_country_share = df_europe_countries_share[df_europe_countries_share["country"] == country]

    df_country_share.rename(columns={"fossil_share_elec": "Combustibles fosiles",
                                     "nuclear_share_elec": "Nuclear",
                                     "renewables_share_elec": "Renovables"}, inplace=True)

    fig_bar_country_share = pollution_bar_graphs(df_country_share,
                                                 'year',
                                                 ['Combustibles fosiles', 'Nuclear', 'Renovables'],
                                                 {"variable": "Tipo", "year": "anio", "value": "Porcentaje"},
                                                 "Fuentes de generación por porcentaje en " + country,
                                                 800)

    st.markdown('''
            Filtrando por país podremos ver las diferencias en las fuentes de generación usadas.
            ''')

    st.plotly_chart(fig_bar_country_share, use_container_width=False, **{'config': config})

    st.markdown('''
            En estos mapas observamos la distribución de cada fuente de generación.
            ''')

    year = st.sidebar.selectbox("Año", range(2012, 2020))

    col1, col2, col3 = st.beta_columns(3)

    with col1:
        fig_map_fossil = pollution_map_graph(df_europe_countries_share[df_europe_countries_share["year"] == year],
                                             geo_world_ok,
                                             'country',
                                             'fossil_share_elec',
                                             'Porcentaje de combustibles fosiles ' + str(year),
                                             'oranges')

        st.plotly_chart(fig_map_fossil, use_container_width=False, **{'config': config})
    with col2:
        fig_map_nuclear = pollution_map_graph(df_europe_countries_share[df_europe_countries_share["year"] == year],
                                              geo_world_ok,
                                              'country',
                                              'nuclear_share_elec',
                                              'Porcentaje de energia nuclear ' + str(year),
                                              'blues')

        st.plotly_chart(fig_map_nuclear, use_container_width=False, **{'config': config})
    with col3:
        fig_map_renewables = pollution_map_graph(df_europe_countries_share[df_europe_countries_share["year"] == year],
                                                 geo_world_ok,
                                                 'country',
                                                 'renewables_share_elec',
                                                 'Porcentaje de energia renovable ' + str(year),
                                                 'greens')

        st.plotly_chart(fig_map_renewables, use_container_width=False, **{'config': config})

    st.markdown('''
        ## Pero ¿y la elaboración de las baterias?        
        ''')

    img = Image.open("../img/cuñado.jpg")
    st.image(img, use_column_width='auto')

    st.markdown('''
           ### Noticias en prensa sobre el mismo estudio que afirma que un diésel contamina mas que un eléctrico.        
           ''')

    img = Image.open("../img/Noticias.PNG")
    st.image(img, use_column_width='auto')

    df_lifetime = data_convert.emissions_lifetime_cars()

    fig_lifetime = px.bar(df_lifetime[df_lifetime["Type"].isin(["BEV 40", "BEV 80", "ICE"])],
                          x='Type',
                          y=['Vehicle cycle - assembly, disposal and recycling',
                             'Vehicle cycle - components and fluids',
                             'Vehicle cycle - batteries (65 kg CO2/kWh)',
                             'Additional emissions with 100 kg CO2/kWh battery manufacturing',
                             'Well-to-tank fuel cycle',
                             'Tank-to-wheel fuel cycle'
                             ],
                          labels={'value': 'Toneladas CO2', 'Type': 'Tipo vehiculo'},
                          barmode="stack",
                          title="Ciclo de vida de un vehiculo, uso de 10 años y 150.000 km")

    fig_lifetime.update_layout(width=1000)

    st.plotly_chart(fig_lifetime, use_container_width=False, **{'config': config})
