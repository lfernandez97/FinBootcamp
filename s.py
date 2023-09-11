import streamlit as st
import pandas as pd
import geocoder
import math 
import time
from geopy.distance import geodesic
df=pd.read_csv("df_Clean_TripAdvisor 2023-09-05 14_24_13.csv")
def main():
    
    tab1, tab2, tab3,= st.tabs(["Home", "Resultados", "About"])
    tab1.title("Recomendador Inteligente de Restaurantes")
    tab1.header("Encuentra el restaurante perfecto")
    tab1.write("Cuéntanos lo que necesitas y encontraremos el mejor sitio")
    
    
    opciones_precio = ["Restaurantes baratos", "Gama media", "Buena comida"]
   
    
    if opciones_precio == "Restaurantes baratos":
        df = df[df['Precio'] == 'Barato']
    elif opciones_precio == "Gama media":
        df = df[df['Precio'] == 'Gama media']
    else:
        df = df[df['Precio'] == 'Buena comida']
    
    
    
    

    tab1.button("Buscar Restaurantes")

    
   
    tab2.title("Restaurantes perfectos para ti")
    tab2.write(df)
    
    
    
    tab3.title("Sobre esta Aplicación")
    
    tab3.write("Esta aplicación ha sido desarrollada como Proyecto Final de Bootcamp por las siguientes personas:")

    # Ficha de Lucas Fernández Martínez
    tab3.image("LUCAS.jpg", caption="Lucas Fernández Martínez", use_column_width=True)
    tab3.write("Nombre: Lucas Fernández Martínez")
    tab3.write("LinkedIn: [Perfil de LinkedIn](https://www.linkedin.com/in/lucasfdzmtz")

    st.experimental_set_query_params(resultados=True)

    


if __name__ == "__main__":
    main()