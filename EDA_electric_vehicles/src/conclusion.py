import streamlit as st
from PIL import Image

def conclusion():
    st.markdown('''
                ## CONCLUSION 1
                ### El vehículo eléctrico y las renovables, combinación ganadora para el planeta
                ''')

    img = Image.open("../img/meme_ev_2.jpg")
    st.image(img, use_column_width='auto')

    st.markdown('''
                ## CONCLUSION 2
                ### Las ventas de eléctricos no paran de aumentar años tras año y ademas...  
                ''')

    col1, col2 = st.beta_columns(2)

    with col1:
        img = Image.open("../img/Ford.PNG")
        st.image(img, use_column_width='auto')

    with col2:
        img = Image.open("../img/Jaguar.PNG")
        st.image(img, use_column_width='auto')

    col1, col2 = st.beta_columns(2)

    with col1:
        img = Image.open("../img/volkswagen.PNG")
        st.image(img, use_column_width='auto')

    with col2:
        img = Image.open("../img/comisión.PNG")
        st.image(img, use_column_width='auto')

    st.markdown('''                    
                    #### Y nuestro amigo Elon que estará haciendo...?  
                    ''')

    with st.beta_expander("Ver imagen"):
        img = Image.open("../img/old_elon.jpg")
        st.image(img, use_column_width='auto')

    st.markdown('''                    
                ## Gracias por tu atención, [me puedes encontrar aquí](https://www.linkedin.com/in/f-javier-melo-delgado-836590131/)  
                ''')