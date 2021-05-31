import streamlit as st
from PIL import Image


def intro():
    img = Image.open("../img/portada.jpg")
    st.image(img, use_column_width='auto')

    st.markdown('''## Objetivo del estudio
### En este EDA se va a analizar la irrupción del coche electrico desde dos puntos de vista:
### 
 * Impacto medioambiental
 * Evolución de las ventas
### 
### Los datos se centraran en el mercado europeo por varios motivos:
### 
 * Mercado mas heterogeneo que el de USA o China
 * Mayor variedad en la oferta de vehiculos electricos
 * Regulación de emisiones a nivel de la EU
### 
### Se manejan las siguientes hipotesis: 
 1- El coche electrico ayuda a rebajar las emisisones, sobre todo con energia renovable  
  
 2- Las ventas estan empezando un punto de inflexión  
### 
Sigue a un joven Elon Musk (antes de pasar por Turquia) en este emocionante viaje
''')

    with st.beta_expander("Ver imagen"):
        img = Image.open("../img/young_elon.jpg")
        st.image(img, use_column_width='auto')
