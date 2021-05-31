import streamlit as st
import plotly.express as px
import data_convert


def sales(config):
    st.markdown('''
            ## Noruega, paraíso del coche eléctrico 
            ''')

    col1, col2 = st.beta_columns(2)

    with col1:
        st.components.v1.iframe("""https://www.youtube.com/embed/mdsPvbSpB2Y""",
                                scrolling=True,
                                height=500,
                                width=500)

    with col2:
        st.components.v1.iframe("""https://www.youtube.com/embed/lzI-Ih5BARw""",
                                scrolling=True,
                                height=500,
                                width=500)

    st.markdown('''
        ## Ventas de vehículos enchufables respecto al total del mercado 
        ''')

    europe_countries = ['Norway', 'Iceland', 'Sweden', 'Netherlands', 'Finland', 'Denmark', 'Switzerland', 'Germany',
                        'Portugal', 'France', 'UK', 'Belgium', 'Austria', 'Ireland', 'Spain', 'Italy']

    df_plugin_cars_sales = data_convert.plugin_cars_sales()

    df_plugin_cars_sales = data_convert.country_of_data(df_plugin_cars_sales, 'Country', europe_countries)

    df_plugin_cars_sales = data_convert.melt_plugin_cars_sales(df_plugin_cars_sales)

    fig_plugin_cars_sales = px.line(df_plugin_cars_sales.sort_values('year'),
                                    x="year",
                                    y="percentage",
                                    color='Country',
                                    title='Porcentaje de ventas de vehiculos enchufables por pais')

    st.plotly_chart(fig_plugin_cars_sales, use_container_width=False, **{'config': config})

    df_cars_sales = data_convert.cars_sales()

    fig_cars_sales = px.line(df_cars_sales.sort_values('year'),
                             x="year",
                             y="sales",
                             title='Evolución ventas vehiculos')

    fig_cars_sales.update_layout(yaxis_range=[0, 20000000])

    df_ev_sales, df_ev_sales_group = data_convert.ev_cars_sales()

    fig_ev_cars_sales = px.line(df_ev_sales_group.sort_values('year'),
                                y="sales",
                                title='Evolución ventas vehiculos electricos')

    fig_ev_cars_sales.update_layout(yaxis_range=[0, 20000000])

    st.markdown('''
            ## Evolución de ventas del total de vehículos y de vehículos eléctricos 
            ''')

    col1, col2 = st.beta_columns(2)

    with col1:
        st.plotly_chart(fig_cars_sales, use_container_width=False, **{'config': config})

    with col2:
        st.plotly_chart(fig_ev_cars_sales, use_container_width=False, **{'config': config})

    st.markdown('''
            ## Ventas de vehículos eléctricos por modelo 
            ''')

    fig_ev_sales_model = px.bar(df_ev_sales,
                                x='year',
                                y='sales',
                                color='electric car segment',
                                barmode="stack",
                                title="Ventas por modelo")

    fig_ev_sales_model.update_xaxes(autorange="reversed")

    fig_ev_sales_model.update_layout(width=1000)

    st.plotly_chart(fig_ev_sales_model, use_container_width=False, **{'config': config})

    fig_box2 = px.box(df_ev_sales, y="sales", x='year', boxmode='overlay')

    fig_box2.update_xaxes(autorange="reversed")

    fig_strip = px.strip(df_ev_sales, x='year', y='sales', color='electric car segment')

    fig_strip.update_xaxes(autorange="reversed")

    col1, col2 = st.beta_columns(2)

    with col1:
        st.plotly_chart(fig_box2, use_container_width=False, **{'config': config})

    with col2:
        st.plotly_chart(fig_strip, use_container_width=False, **{'config': config})

    fig_scatter = px.scatter(df_ev_sales_group, x='sales', y='num_models', color=df_ev_sales_group.index)

    st.markdown('''
                ## ¿Relación entre el numero de modelos a la venta y las ventas totales? 
                ''')

    st.plotly_chart(fig_scatter, use_container_width=False, **{'config': config})
