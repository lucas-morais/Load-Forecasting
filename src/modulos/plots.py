import folium
import numpy as np
def mapa(info):

    # Coordenadas de Taperoá
    media_lat = -7.20791
    media_lon = -36.8261

    m =folium.Map(
        location = [media_lat, media_lon],
        zoom_start = 8

    ) 
    for sigla in info:
        folium.Marker(
            location=[info[sigla].get('latitude'), info[sigla].get('longitude')], 
            popup=info[sigla].get('nome'), 
        ).add_to(m)
    
    return m
    
