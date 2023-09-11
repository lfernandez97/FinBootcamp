distancia = tab1.slider("Distancia (km):", 0, 10, 1)

    # Combina la ubicación y la distancia
    ubicacion = None
    if distancia > 0:
        try:
            ubicacion = geocoder.ip('me')
            latitud = ubicacion.latlng[0]
            longitud = ubicacion.latlng[1]
        except Exception as e:
            st.write("No se pudo obtener la ubicación actual.")