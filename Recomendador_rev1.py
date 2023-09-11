import streamlit as st
import pandas as pd
import geocoder
import math 
import time
from geopy.distance import geodesic
from PIL import Image
import matplotlib.pyplot as plt
import pydeck as pdk
import folium
import base64
from pdf2image import convert_from_path
from PIL import Image
import pdfplumber


st.set_page_config(page_title="Hungry Hunt",  page_icon="logodefweb.png")
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
            calificacion = st.slider(f"Preferencias por el Tipo de Cocina '{opcion}' (1-10):", min_value= 1,max_value= 10,step= 1,value= 5)
            calificaciones[opcion] = calificacion / 10
            
        calificaciones_order= ordena_diccionario(calificaciones)#ordenamos el diccionario generado
        

        # Insertar una línea divisoria personalizada
        st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)
        st.write("Una vez clasificadas sus preferencias....")
        st.write("Asi quedaria el orden asignado a los tipos de cocina:")
        st.markdown("",unsafe_allow_html=True)
        st.table(calificaciones_order)
        st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)
        return calificaciones_order

#Funcion para los subtipos de cocina
def sub_cocina(cadena, lista, diccionario):
    primeras_tres_claves = list(diccionario.keys())[:3]
    if cadena in primeras_tres_claves:
        st.write(f"\n Vemos que en sus preferidas esta la Cocina de la {cadena}, debo informarle que la Region seleccionada") 
        st.write(f"agrupa varios tipos de cocina {lista}. Debe escoger las dos que mas prefiere")
        #st.write("por favor organice de acuerdo a sus preferencias")
        dicc_temporal = puntuacion_cocinas(lista)
        calif_cocina_ordenado = ordena_diccionario(dicc_temporal)
        lista_calif_ordenado=list(calif_cocina_ordenado.keys())
    else:
        lista_calif_ordenado=[] 
    return(lista_calif_ordenado)

#Ubicación
ubicacion = geocoder.ip('me')
Latitud = ubicacion.latlng[0]
Longitud = ubicacion.latlng[1]

def create_restaurant_map(restaurant_row):
    # Crear un DataFrame con los datos del restaurante
    df_map = pd.DataFrame([restaurant_row])
    df_map = df_map.dropna()

    # Crear las capas del mapa
    layer = pdk.Layer(
        "TextLayer",
        data=df_map,
        get_position=["Longitud", "Latitud"],
        get_text="Nombre",
        get_size=16,
        get_color=[0, 0, 0, 255],  # Fondo verde
        get_background_color=[255, 255, 255, 255],  # Fondo blanco
        get_angle=0,
        pickable=True,
    )

    arrow_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position=["Longitud", "Latitud"],
        get_fill_color=[20, 255, 0, 255],  # Color de la flecha (rojo)
        get_radius=8,  # Tamaño de la flecha
        get_line_color=[0, 255, 0, 255],  # Color del borde de la flecha
        get_line_width_min_pixels=2,
    )

    # Crear el mapa con DeckGL
    map = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=df_map['Latitud'].mean(),
            longitude=df_map['Longitud'].mean(),
            zoom=16,
        ),
        layers=[layer, arrow_layer],
    )

    return map 

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



# Página 0; Código Bruto
df=pd.read_csv("df_Clean_TripAdvisor 2023-09-07 13_29_53.csv")

factor=0.6 
Punt_poderada_list=[]
for x,y in zip(df["Score"], df["Num_Reviews"]):
    Punt_poderada=round(x *(1 + factor * math.log(y+ 1)),3)   
    Punt_poderada_list.append(Punt_poderada)  

df["Valoracion"]=Punt_poderada_list

reemplazo = {
    '€': 'Restaurantes baratos',
    '€€ - €€€': 'Gama media',
    '€€€': 'Gama Alta'}

df['Rango_precio'] = df['Rango_precio'].replace(reemplazo)

distancias = []
for index, row in df.iterrows():
    ubicacion_restaurante = (row['Latitud'], row['Longitud'])
    try:
        distancia = geodesic((Latitud, Longitud), ubicacion_restaurante).kilometers
    except Exception as e:
        distancia = 1000  
    distancias.append(distancia)

df['Distancia_km'] = distancias
            # Agregar la lista de distancias al DataFrame como una nueva columna

def main():

    imagen = st.image('logo_proyecto.jpg', use_column_width=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Buscador de Restaurantes", "Recomendador Inteligente", "About","Herramienta BI"])
    
# Contenido de la Sección 1
    with tab1:
    
        if tab1:
            st.title("Sobre este Proyecto")
            st.write("En este proyecto os queremos  presentar nuestro recomendador de restaurantes de Madrid Hungry Hunt, una herramienta  desarrollada  en base a las opiniones y valoraciones de los usuarios en TripAdvisor. Este programa está diseñado para brindar a los usuarios una selección precisa en base a variables como el tipo de comida, el precio medio y las valoraciones de los usuarios de los restaurantes de  la capital española.")
            st.write(" ")
            st.write(" Para la extracción de la información utilizamos la técnica de web scraping en TripAdvisor. Hemos recopilado cerca de 10,000 filas de datos para nuestro proyecto. Estos datos incluyen información sobre el tipo de cocina, precio promedio, ubicación y las valoraciones de los usuarios. Sin embargo, esta recopilación inicial presentó una cantidad significativa de valores nulos (NaN), lo que requirió un proceso de limpieza para finalmente obtener un csv de 6354 filas. A continuación adjuntamos una copia del código en foormato pdf con el código ìntegro y explicado.")
            st.write(" ") 
            st.write(show_pdf("WebScrapping1.pdf"))
            st.write(show_pdf("WebScrapping2.pdf"))
            st.write(show_pdf("TipoCocina.pdf"))
            st.write(" ") 
            st.write("Una vez limpio el CSV, procedemos a realizar un EDA ( Exploratory Data Analysis) cuyo objectivo es entender y familiarizarse con los datos antes de realizar análisis estadísticos más avanzados o construir modelos predictivos.El EDA es una etapa crucial para comprender la naturaleza de los datos, identificar problemas potenciales y tomar decisiones informadas sobre cómo proceder en un análisis del proyecto. ")
            st.write(" ") 
            st.write(show_pdf("EDApdf.pdf"))
            st.write(" ") 
            st.write("La información obtenida de este modo es subida a esta aplicación en Streamlit (un framework oriantado a ciencia de daots), dónde el usuario procede a introducir sus preferencias de búsqueda, ya sea a través de un simple filtro, o mediante el recomendador de Inteligencia Artificial Avanzada del que se adjunta el código. ") 
            st.write(" ") 
            st.write(show_pdf("recomendador.pdf"))
            st.write(" ") 
            st.write("Como función complementariam se añade un cuadro de mandos en Power BI que permite analizar tanto la información global de la información extraída, como las opciones filtradas por el usuario.") 


        
                                    
        

# Contenido de la Sección 2
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
                df_filtrado = df[df['Rango_precio'] == "Gama Alta"]
            else:
                df_filtrado = df

            filtrar_awards = st.checkbox("Quiero que sean restaurantes premiados")

            # Verificar la selección del usuario
            if filtrar_awards:
            # Filtrar solo valores 1m en la columna 'Awards'
                df_filtrado2 = df_filtrado[df_filtrado['Awards'] == 1]
            else:
                df_filtrado2= df_filtrado    
        
            distancia, comida,servicio,calidad_precio =st.columns([5,5,5,5])
            with distancia:
                distancia_choice= st.slider("Distancia",min_value= 1,max_value= 5,step= 1,value= 3,)
                df_filtrado3 = df_filtrado2[df_filtrado2['Distancia_km'] >= distancia_choice]
            with comida:
                comida_choice = st.slider("Comida",min_value= 1,max_value= 5,step= 1,value=3,)
                df_filtrado4 = df_filtrado3[df_filtrado3['Score_Comida'] >= comida_choice]
            with servicio:   
                servicio_choice = st.slider("Servicio",min_value= 1,max_value= 5,step= 1,value=3,)
                df_filtrado5 = df_filtrado4[df_filtrado4['Score_Servicio'] >= servicio_choice]
            with calidad_precio:
                calidad_precio_choice = st.slider("Calidad/Precio",min_value= 1,max_value= 5,step= 1,value=3,)
                df_filtrado6 = df_filtrado5[df_filtrado5['Calidad_Precio'] >= calidad_precio_choice]
            
            columnas_mostrar = ["Nombre", "Distancia_km", "Awards", "Score_Comida", "Calidad_Precio", "Score_Servicio","Latitud","Longitud","Web_TripAdvisor"]
            num_rest2 = st.slider("Número de restaurantes a mostrar (entre 1 y 10)", min_value=1, max_value=10, value=5)

             # Asegúrate de que num_rest2 esté dentro del rango de 1 a 10
            num_rest2 = max(1, min(10, num_rest2))

                # Muestra las primeras num_rest2 filas del DataFrame
            df_show = df_filtrado6.head(num_rest2)[columnas_mostrar]
            #tab2.write(df_show)


 
            df_map = df_show
            df_map = df_map.dropna()
      

            layer = pdk.Layer(
            "TextLayer",
            data=df_map,
            get_position=["Longitud", "Latitud"],
            get_text="Nombre",
            get_size=16,
            get_color=[0, 0, 0, 255],  # Fondo verde
            get_background_color=[255, 255, 255, 255],  # Fondo blanco
            get_angle=0,
            pickable=True,)
            
            
            arrow_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map,
            get_position=["Longitud", "Latitud"],
            get_fill_color=[20, 255, 0, 255],  # Color de la flecha (rojo)
            get_radius=100,  # Tamaño de la flecha
            get_line_color=[0, 255, 0, 255],  # Color del borde de la flecha
            get_line_width_min_pixels=2,)  # Grosor mínimo del borde

            # Crear el mapa con DeckGL
            map = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                    latitude=df_map['Latitud'].mean(),
                    longitude=df_map['Longitud'].mean(),
                    zoom=12,),layers=[layer, arrow_layer],)
            
            tab2.subheader("Mapa de ubicaciones:")
            tab2.pydeck_chart(map)
            
            for index, row in df_show.iterrows():
                with st.expander(row["Nombre"]):
                    st.subheader(row["Nombre"])  # Nivel 1: Nombre del restaurante como título
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("Servicio:")
                        st.write("⭐" * int(row["Score_Servicio"]))
                    with col2:
                        st.write("Comida:")
                        st.write("⭐" * int(row["Score_Comida"]))
                    with col3:
                        st.write("Relación Calidad-Precio:")
                        st.write("⭐" * int(row["Calidad_Precio"]))

                    # Nivel 3: Distancia y enlace directo a la página de TripAdvisor
                    st.write(f"Distancia: {row['Distancia_km']} km")
                    st.write(f"Enlace a TripAdvisor:")
                    st.write(row["Web_TripAdvisor"])
                    
                    st.pydeck_chart(create_restaurant_map(row))
                    
                    # Crear un botón para exportar a CSV
            st.title("Exportar DataFrame a CSV")
            csv = df_show.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="consulta.csv">Descargar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

# Contenido de la Sección 3
   
    with tab3:        
        if tab3:
            st.title("🤖Recomendador Inteligente🤖")
            st.write("Le ofrecemos la opción de indicar sus preferencias en estilos de cocina y recomendaremos según sus gustos")
            st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)#LINEA
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
                
            st.write("Este es el orden de preferencias despues de haber hecho la selección:")
            st.table(tipo_cocina_preferida_list)
            st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)
            
            ########################

            resultado=pd.DataFrame()
            dicc_df={}
            columnas_mostrar1 = ["Nombre","Score", "Num_Reviews", "Rango_precio", "Awards", "Score_Comida", "Calidad_Precio", "Score_Servicio","Web_TripAdvisor"]           
            #preguntar por el numero e restaurtantes a mostrar
            st.subheader("Indique el Número de restaurantes que quiere ver x tipo de cocina elegida:")
            st.write("Recomendamos no más de 10 restaurantes, aunque el número máximo de esta opción es 50 por cada tipode cocina")
            z = st.number_input("",min_value=0, max_value=50, value=0)
            z = int(z)
            c=0
            
            for y in tipo_cocina_preferida_list:
                for x in df.columns[19:-4]:#se corresponde con las columnas tipo cocina
                    if x == y:
                        df_recomendador1 = df[df[x]==1]
                        st.write(f"El tipo de cocina Seleccionada: {y}")
                        df_ordenado = df_recomendador1.sort_values(by='Valoracion', ascending=False)
                        st.write(df_ordenado.head(z)[columnas_mostrar1])
                        df_show1=df_ordenado.head(z)[columnas_mostrar1]
                        dicc_df[x]=df_ordenado.head(z)[columnas_mostrar1]

                       #### EN ESTE PUNTO YA SE OBTIENE EL DF POR TIPOS DE COCINA QUE SE GUARDA EN UN DICCIONARIO             
                        st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)

                ########################### FILTROS  ###############################
                        st.write("Puede filtrar su seleccion por Rango de Precio")
                        precio = st.radio(label = "Rango de Precios", key= c,
                            options = ("Restaurantes baratos", "Gama media", "Gama alta"),
                            index = 0,
                            disabled = False,
                            horizontal = True,)
                        c+=1     

                        if precio == "Gama alta":
                            df_filter_price = df_show1[df_show1['Rango_precio'] == "Gama alta"]
                            st.write(df_filter_price)                        
                        elif precio == "Gama media":
                            df_filter_price = df_show1[df_show1['Rango_precio'] == "Gama media"]
                            st.write(df_filter_price)
                        elif precio == "Restaurantes baratos":
                            df_filter_price = df_show1[df_show1['Rango_precio'] == "Restaurantes baratos"]
                            st.write(df_filter_price)
                        else:
                            df_filter_price = df_show1 
                            st.write(df_filter_price)       
                        
                        
                        
                        
                        for index, row in df_filter_price.iterrows():
                            with st.expander(row["Nombre"]):
                                # Nivel 1: Nombre del restaurante como título
                                score= row["Score"]
                                num_reviews= row["Num_Reviews"]
                                rango_precio= row["Rango_precio"]

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.subheader(f"Puntuación: {score}")
                                with col2:
                                    st.subheader(f"Número de Reviews: {num_reviews}")
                                with col3:
                                    st.subheader(f"Rango-Precios: {rango_precio}")
                                st.markdown("<hr style='border: 1px solid #050743; background-color:#050743'>", unsafe_allow_html=True)    
                                
                                 #Nivel 2
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    score_servicio=row["Score_Servicio"]
                                    st.write(f"Servicio: {score_servicio}")
                                    st.write("⭐" * int(row["Score_Servicio"]))
                                with col2:
                                    score_food= row["Score_Comida"]
                                    st.write(f"Comida: {score_food}")
                                    st.write("⭐" * int(row["Score_Comida"]))
                                with col3:
                                    score_calidad_precio= row["Calidad_Precio"]
                                    st.write(f"Relación Calidad-Precio: {score_calidad_precio}")
                                    st.write("⭐" * int(row["Calidad_Precio"]))
                                    # Nivel 3: enlace directo a la página de TripAdvisor
                                    
                                st.write(f"Enlace a TripAdvisor:")
                                st.write(row["Web_TripAdvisor"])


# Contenido de la Sección 4
    with tab4:
        
        if tab4:
            st.title("Sobre nosotros")
            st.text("")
            
            st.write("Esta aplicación ha sido desarrollada con fines formativos como Proyecto de Final de Bootcamp de Data Science de Hack a Boss por las siguientes personas, a quien pertenecen la autoría intelectúal y corresponde la protección legal de aplicación.")
            
            st.text("")
            col1, col2 = st.columns([1,12])
            with col1:
                st.image("linkedin.png",use_column_width=True)

            with col2:
                st.write("Adriana Pérez Olivares")
                st.write("www.linkedin.com/in/adrianaperezolivares")
            col3, col4 = st.columns([1,12])
            with col3:
               st.image("linkedin.png",use_column_width=True)

            with col4:
                st.write("Iván Enrique García Reyes")
                st.write("https://es.linkedin.com/in/ivenrique")
            col5, col6 = st.columns([1,12])
            with col5:
                st.image("linkedin.png",use_column_width=True)

            with col6:
               st.write("Carlos Garrido")
               st.write("https://es.linkedin.com/in/carlosgarridomuñoz")
            col7, col8 = st.columns([1,12])
            with col7:
                st.image("linkedin.png",use_column_width=True)

            with col8:
               st.write("Lucas Fernández Martíenz")
               st.write("https://www.linkedin.com/in/lucasfdzmtz")
               
            st.text("")
            st.text("")
            
            web_url = "https://www.hackaboss.com/ad/data-science-bootcamp?utm_term=&utm_campaign=_%5BHAB%5D+-+DATA++-+Nacional+-+DSA+-+Search&utm_source=adwords&utm_medium=ppc&hsa_acc=1070315109&hsa_cam=20162534836&hsa_grp=153011258567&hsa_ad=659044950915&hsa_src=g&hsa_tgt=dsa-2065258095016&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad=1&gclid=EAIaIQobChMI747_vuGfgQMVTJNoCR0ulwQ8EAAYASAAEgLGh_D_BwE"

            # Generar el iframe para mostrar la página web
            iframe_code = f'<iframe src="{web_url}" width="800" height="600"></iframe>'

            # Mostrar el iframe en la aplicación Streamlit
            st.markdown(iframe_code, unsafe_allow_html=True)
            

    with tab5:
        if tab5:
            st.title("Análisis en Power BI")
            st.text("")
            
            st.write("En el momento actual, no existe una integración directa entre Streamlit y Power BI debido a que son herramientas independientes con enfoques y finalidades diferentes. Streamlit se utiliza para crear aplicaciones web interactivas en Python, mientras que Power BI se enfoca en la creación de informes y paneles interactivos de análisis de datos.")

            st.write("Sin embargo, es posible incrustar un informe de Power BI en una aplicación de Streamlit utilizando un componente de iframe. Esto implica publicar el informe de Power BI en la web y luego insertar su URL en un componente `st.iframe` en Streamlit. Aunque esta integración permite mostrar el informe de Power BI dentro de la aplicación de Streamlit, no habrá una interacción directa entre los datos del informe y la aplicación de Streamlit, ya que ambas plataformas operan de forma independiente.")

            st.write("En resumen, aunque actualmente no existe una integración nativa entre Streamlit y Power BI, es posible incorporar un informe de Power BI en una aplicación de Streamlit utilizando iframes y asegurándose de que el informe esté disponible en línea para su visualización.")

            st.write("Así que para importar al información obtenida del recomendador, se generó un Script en Python.")
            
            st.image("powerbi1.png",use_column_width=True)

            # URL del informe de Power BI
            power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=3399bd68-83bc-4743-9ada-3fe3a484f63e&autoAuth=true&ctid=5260dc4c-ecd4-4a81-bfa2-7e56e6346691"

            # Usar un iframe para incrustar el informe
            st.markdown(f'<iframe title="ProyectoBootcamp" width="1140" height="541.25" src="{power_bi_url}" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)




if __name__ == "__main__":
    main()