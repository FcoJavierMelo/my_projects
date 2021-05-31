import streamlit as st
import cv2
import matplotlib.pyplot as plt
from keras.preprocessing import image
from skimage.io import imread
from tempfile import NamedTemporaryFile
import tensorflow as tf
from tensorflow import keras
from efficientnet.tfkeras import EfficientNetB7
import numpy as np
import pandas as pd
import plotly.express as px


def df_predictions(predictions, modelos):
    lista_modelos = []
    lista_values = []
    p = predictions[0]

    for index, predict in enumerate(p.T):
        lista_modelos.append(list(modelos.keys())[list(modelos.values()).index(index)])
        lista_values.append(round(predict * 100, 3))

    df = pd.DataFrame({'modelo': lista_modelos, 'probabilidad': lista_values})

    return df

def image_convert(temp_file, target_size):
    imagen = image.load_img(temp_file.name, target_size=target_size)
    imagen = image.img_to_array(imagen)
    imagen = imagen / 255
    imagen = np.expand_dims(imagen, axis=0)

    return np.vstack([imagen])


def model_from_image():

    modelos = {'Audi E-tron 2019': 0,
               'BMW i3 2018': 1,
               'Ford Mustang Mach-E 2020': 2,
               'Honda e 2020': 3,
               'ID3': 4,
               'ID4': 5,
               'Lucid Air': 6,
               'Nissan Leaf 2018': 7,
               'Porsche Taycan': 8,
               'Renault Zoe 2020': 9,
               'Tesla Model 3': 10}

    buffer = st.file_uploader("Carga una imagen", type=['jpg'])
    temp_file = NamedTemporaryFile(delete=False)
    if buffer is not None:
        temp_file.write(buffer.getvalue())
        imagen = image.load_img(temp_file.name)
        st.image(imagen)
        images_EfficientNetB7 = image_convert(temp_file, (224,224))
        images_ResNet50 = image_convert(temp_file, (250, 250))

        model_EfficientNetB7 = tf.keras.models.load_model('../models/EfficientNetB7.h5')

        predictions_EfficientNetB7 = model_EfficientNetB7.predict(images_EfficientNetB7)

        model_ResNet50 = tf.keras.models.load_model('../models/modelo_ResNet50_2.h5')

        predictions_ResNet50 = model_ResNet50.predict(images_ResNet50)

        df_EfficientNetB7 = df_predictions(predictions_EfficientNetB7, modelos)

        df_ResNet50 = df_predictions(predictions_ResNet50, modelos)

        fig = px.bar(df_EfficientNetB7, x="probabilidad", y="modelo", orientation='h')

        fig.update_layout(title='Resultados modelo EfficientNetB7')

        st.plotly_chart(fig)

        fig = px.bar(df_ResNet50, x="probabilidad", y="modelo", orientation='h')

        fig.update_layout(title='Resultados modelo ResNet50')

        st.plotly_chart(fig)
