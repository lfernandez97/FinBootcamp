import streamlit as st
import pandas as pd
import geocoder
import math 
import time
from geopy.distance import geodesic

#Funcion ordena diccionarios
def ordena_diccionario(diccionario):
        # Ordenar el diccionario de mayor a menor
        diccionario_ordenado = dict(sorted(diccionario.items(), key=lambda item: item[1], reverse=True))
        return diccionario_ordenado   


#Funcion para puntuar los tipos de cocina segun deseo del usuario
def puntuacion_cocinas(lista):
        # Solicita al usuario que califique cada opción
        st.write("Por favor, califique las opciones de cocina:")
        st.write("Escala de calificación: 1 (No me apetece) a 10 (Me encanta), Intentar No Repetir Puntuación")
        calificaciones={}

        for opcion in lista:
            calificacion = st.slider(f"Califique Tipo de Cocina '{opcion}' (1-10):", 1, 10)
            calificaciones[opcion] = calificacion / 10
            
        calificaciones_order= ordena_diccionario(calificaciones)#ordenamos el diccionario generado
        st.write("Asi quedaria el orden asignado a los tipos de cocina:")
        for opcion, calificacion in calificaciones_order.items():
                st.write(f"{opcion}: {calificacion * 10}")
        return calificaciones_order

#Funcion para los subtipos de cocina
def sub_cocina(cadena, lista, diccionario):
    primeras_tres_claves = list(diccionario.keys())[:3]
    if cadena in primeras_tres_claves:
        st.write(f"\nCalificaciones {cadena}")
        dicc_temporal = puntuacion_cocinas(lista)
        calif_cocina_ordenado = ordena_diccionario(dicc_temporal)
        lista_calif_ordenado=list(calif_cocina_ordenado.keys())
    else:
        lista_calif_ordenado=[] 
    return(lista_calif_ordenado) 

# Define el logo o imagen que deseas mostrar
logo = st.image("logo.png",use_column_width=True)


# Página 0; Código Bruto
df=pd.read_csv("df_Clean_TripAdvisor.csv")

factor=0.6 
Punt_poderada_list=[]
for x,y in zip(df["Score"], df["Num_Reviews"]):
    Punt_poderada=round(x *(1 + factor * math.log(y+ 1)),3)   
    Punt_poderada_list.append(Punt_poderada)  

df["Valoracion"]=Punt_poderada_list

reemplazo = {
    '€': 'Restaurantes baratos',
    '€€ - €€€': 'Gama media',
    '€€€€': 'Gama alta'}

df['Rango_precio'] = df['Rango_precio'].replace(reemplazo)


def main():
    # Crear las pestañas
    tabs = ["Home", "Buscador de Restaurantes", "Recomendador Inteligente", "About"]
    selected_tab = st.selectbox("Selecciona una pestaña y....  Buen Provecho!!!", tabs)

####### Contenido de la pestaña 1 "HOME"##################################
    if selected_tab == "Home":        
               st.markdown('<p style="font-size: 24px;">Sobre este Proyecto:</p>',
               unsafe_allow_html=True)
               st.write("En la actualidad nsca jgldkgldfnffdjvksdj.sjlsdj")
               






#############################################################################
###### Contenido de la pestaña 2 "BUSCADOR DE RESTAURANTES"##################
    elif selected_tab == "Buscador de Restaurantes":
        st.markdown('<p style="font-size: 24px;">Restaurantes perfectos para ti:</p>',
                    unsafe_allow_html=True)

# Filtrar el DataFrame en función de la selección de precio
        precio = st.radio("Rango  de Precio:", ["Restaurantes baratos", "Gama media", "Gama Alta"])

        if precio == "Restaurantes baratos":
            df_filtrado = df[df['Rango_precio'] == "Restaurantes baratos"]
        elif precio == "Gama media":
              df_filtrado = df[df['Rango_precio'] == "Gama media"]
        elif precio == "Gama alta":
              df_filtrado = df[df['Rango_precio'] == "Gama alta"]
        else:
             df_filtrado = df
    
        filtrar_awards = st.checkbox("Quiero que sean restaurantes con la certificacion TRAVELLER´S CHOICE")
        # Verificar la selección del usuario
        
        
        #¿Porque esta mezclado en un if y un else certificaciones y distancia?????
        
        if filtrar_awards:
            # Filtrar solo valores 1m en la columna 'Awards'
            df_filtrado2 = df_filtrado[df_filtrado['Awards'] == 1]
        else:
            df_filtrado2= df_filtrado
            distancia = st.slider("Distancia (km):", 0, 10, 1)# esto no funciona!!!!!!!!!!!!!!!!!!!!!

        # Combina la ubicación y la distancia
        comida = st.slider("Comida (1-5):", 1, 5, 3)
        servicio = st.slider("Servicio (1-5):", 1, 5, 3)
        calidad_precio = st.slider("Calidad/Precio (1-5):", 1, 5, 3)

        st.write(df_filtrado2)


#################################

    # Contenido de la pestaña 3 #RECOMENDADOR INTELIGENTE
    elif selected_tab == "Recomendador Inteligente":
          
          # Widget para el botón de recomendación
          recomienda_cocina = st.checkbox("Tengo Preferencias por el tipo de comida")
          # Si el usuario marca la casilla de recomendación
          if recomienda_cocina:
            tipo_cocina_preferida_list=[]
            lista_opciones =["Region_Latinoamerica", "Region_Asiatica", "Italiana", "Española",
                             "America Norte", "Eur Este","Eur Occidental", "Arabe", "Africana", "India"]
            dicc_calificaciones_order= puntuacion_cocinas(lista_opciones)   

            #dicc_tipos_cocina= subtipos_cocina(dicc_calificaciones_order)
            Region_Latinoamerica =["America Sur", "Asador", "Caribeña", "Mexicana", "Latina"]
            Region_Asiatica = ["Asiatica", "China", "Japonesa"]
            latin_list=sub_cocina("Region_Latinoamerica", Region_Latinoamerica, dicc_calificaciones_order)
            asia_list=sub_cocina("Region_Asiatica", Region_Asiatica, dicc_calificaciones_order )

            ###################

            lista_pref= list(dicc_calificaciones_order.keys())[0:4]
            
            for x in lista_pref:
                if x !="Region_Latinoamerica" and x!="Region_Asiatica":
                    tipo_cocina_preferida_list.append(x)
                elif x == "Region_Latinoamerica":
                    tipo_cocina_preferida_list.extend(latin_list[0:2])                
                elif x == "Region_Asiatica":
                    tipo_cocina_preferida_list.extend(asia_list[0:2])
            
           
            #st.write(tipo_cocina_preferida_list)

            ########################

            resultado=pd.DataFrame()
            dicc_df={}
            #z= int(input(f"¿Cuantas recomendaciones quiere por tipo de cocina?(1-10)"))#numero de recomendaciones por tipo de cocina
            z= 10
            for y in tipo_cocina_preferida_list:
                for x in df.columns[19:-4]:#se corresponde con las columnas tipo cocina
                    if x == y:
                        df_recomendador1 = df[df[x]==1]
                        st.write(f"El tipo de cocina Seleccionada: {y}")
                        df_ordenado = df_recomendador1.sort_values(by='Valoracion', ascending=False)
                        st.write(df_ordenado[["Nombre", "Score","Valoracion"]].head(z))
                        dicc_df[x]=df_ordenado[["Nombre", "Score","Valoracion"]].head(z)
            
            # Convertir el valor en un número entero (int)
            #    num_rest = int(num_rest)

 ###############################       
    
    # Contenido de la pestaña 4
    elif selected_tab == "About":
        st.title("Sobre Nosotros")
        st.title("Sobre esta Aplicación")
                
        st.write("Esta aplicación ha sido desarrollada como Proyecto Final de Bootcamp por las siguientes personas:")

        # Ficha de Lucas Fernández Martínez
        st.write("Nombre: Lucas Fernández Martínez")
        st.write("LinkedIn: [Perfil de LinkedIn](https://www.linkedin.com/in/lucasfdzmtz")
   
   
if __name__ == "__main__":
    main()



