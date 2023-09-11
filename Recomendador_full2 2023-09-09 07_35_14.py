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
logo = st.image("/Users/adrianaperez/Streamlit/streamlit_venv/source/Logo.png",use_column_width=True)


# Página 0; Código Bruto
df=pd.read_csv("/Users/adrianaperez/Streamlit/streamlit_venv/source/df_Clean_TripAdvisor.csv")

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
    tab1, tab2, tab3, tab4 = st.tabs(["Home", "Buscador de Restaurantes", "Recomendador Inteligente", "About",])
    #st.subheader("Selecciona una pestaña y....  Buen Provecho!!!")

####### Contenido de la pestaña 1 "HOME"##################################
    with tab1:
    
        if tab1:
            st.title("Sobre este Proyecto")
            st.write("En la actualidad nsca")
        





#############################################################################
###### Contenido de la pestaña 2 "BUSCADOR DE RESTAURANTES"##################
    with tab2:
        
        if tab2:
            st.title("Buscador de restaurantes")
            st.subheader("Restaurantes perfectos para ti")
            precio = st.radio(label = "Precio",
                       options = ("Restaurantes baratos", "Gama media", "Gama Alta"),
                       index = 0,
                       disabled = False,
                       horizontal = True,)
            

            if precio == "Restaurantes baratos":
                df_filtrado = df[df['Rango_precio'] == "Restaurantes baratos"]
            elif precio == "Gama media":
                df_filtrado = df[df['Rango_precio'] == "Gama media"]
            elif precio == "Gama alta":
                df_filtrado = df[df['Rango_precio'] == "Gama alta"]
            else:
                df_filtrado = df

            filtrar_awards = st.checkbox("Quiero que sean restaurantes premiados")
            # Verificar la selección del usuario
            if filtrar_awards:
            # Filtrar solo valores 1m en la columna 'Awards'
                df_filtrado2 = df_filtrado[df_filtrado['Awards'] == 1]
            else:
                df_filtrado2= df_filtrado    # esto no funciona!!!!!!!!!!!!!!!!!!!!!

    
            distancia, comida,servicio,calidad_precio =st.columns([5,5,5,5])
            with distancia:
                distancia_choice= st.slider("Distancia",min_value= 1,max_value= 5,step= 1,value= 3,)
            with comida:
                comida_choice = st.slider("Comida",min_value= 1,max_value= 5,step= 1,value=3,)
            with servicio:   
                servicio = st.slider("Servicio",min_value= 1,max_value= 5,step= 1,value=3,)
            with calidad_precio:
                calidad_precio = st.slider("Calidad/Precio",min_value= 1,max_value= 5,step= 1,value=3,)


            st.write(df_filtrado2)


#################################

    # Contenido de la pestaña 3 #RECOMENDADOR INTELIGENTE
    with tab3:
        
        if tab3:
            st.write("Recomendador inteligente")
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
    with tab4:
        
        if tab4:
            st.write("Sobre nosotros")
            col1, col2 = st.columns([1,12])
            # Colocar el logo en la primera columna y el texto con enlace en la segunda columna
            with col1:
                st.image("/Users/adrianaperez/Streamlit/streamlit_venv/source/link.png",use_column_width=True)

            with col2:
                st.write("www.linkedin.com/in/adrianaperezolivares")
            col3, col4 = st.columns([1,12])
            with col3:
                st.image("/Users/adrianaperez/Streamlit/streamlit_venv/source/link.png",use_column_width=True)

            with col4:
                st.write("https://www.linkedin.com/in/lucasfdzmtz")
            col5, col6 = st.columns([1,12])
            with col5:
                st.image("/Users/adrianaperez/Streamlit/streamlit_venv/source/link.png",use_column_width=True)

            with col6:
                st.write("https://www.linkedin.com/in/lucasfdzmtz")
            col7, col8 = st.columns([1,12])
            with col7:
                st.image("/Users/adrianaperez/Streamlit/streamlit_venv/source/link.png",use_column_width=True)

            with col8:
                st.write("https://www.linkedin.com/in/lucasfdzmtz")
   
   
if __name__ == "__main__":
    main()



