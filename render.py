import osmnx as ox
import read
import folium
from PIL import Image
from pathlib import Path
import math
import pickle
import os

#for haversine
def convert2radians(latlon):
    return [math.radians(latlon[0]), math.radians(latlon[1])]

#haversine formula
def getDist(folder, num):
    total = 0
    data = read.get_exif_data(folder)
    for i in range(len(data)-1):
        r = 6371 #earth radius
        orig = convert2radians(data[i][1]['location']) #(lat, long)
        dest = convert2radians(data[i+1][1]['location']) #(lat,long)

        a = ( (math.sin((dest[0]-orig[0])/2))**2 ) + ( ((math.cos(orig[0]))*(math.cos(dest[0]))) * ((math.sin((dest[1]-orig[1])/2))**2 ) )
        c = 2 * math.asin(math.sqrt(a))
        total += r * c
    return total

#creates a cache of graph routes so that they don't have to be constantly reloaded
def get_or_cache(lat_mid, lon_mid): 
    cache_key = f'{round(lat_mid,4)}_{round(lon_mid,4)}'
    cache_file = f'static/cache/{cache_key}.pkl'
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    G = ox.graph_from_point((lat_mid,lon_mid), dist=15000,network_type='all')
    os.makedirs('static/cache', exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(G,f)
    
    return G


def plot(base, folder, color):
    group = folium.FeatureGroup(name=folder)

    places = read.get_exif_data(folder) #5087, 5100 are in sitka
    #map = folium.Map(location = places[0][1]['location'], zoom_start = 14)

    if not places:
        return

    for i in range(len(places) - 1):
        orig = places[i][1]['location'] #(lat, long)
        dest = places[i+1][1]['location'] #(lat,long)
        img_name = places[i][0]
        date = places[i][1]['time']
        path = places[i][1]['path'].replace('static/', '')
        thumb = places[i][1]['thumb']
        folder_name = folder.split('/')[-1]

        popup = f"""
                <b> {img_name} </b><br>
                <img src = {path} width = "200">
                """ 
        
        icon = folium.CustomIcon(
            thumb,
            icon_size = (40,40),
            shadow_size = (40,40),
            shadow_anchor=(10,40)
        )

        folium.Marker(
                    orig, 
                    icon = icon,
                    tooltip = img_name,
                    popup = popup,
                    #opacity = 0.5
                    ).add_to(group)
        
        lat_mid = (orig[0] + dest[0]) / 2
        lon_mid = (orig[1] + dest[1]) / 2
        
        print(folder_name) ##
        try:
            G = get_or_cache(lat_mid,lon_mid)
            
            #find nearest node, switch lat & long
            orig_node = ox.nearest_nodes(G, orig[1], orig[0])
            dest_node = ox.nearest_nodes(G, dest[1], dest[0])

            

            sp = ox.shortest_path(G, orig_node, dest_node, weight = 'length')
            path_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in sp]
            
            print(folder_name, path_coords) ##
            #print(folder_name) ##

            #if path doesn't begin at origin, fill in gap
            if path_coords[0] != orig:
                folium.PolyLine((orig, path_coords[0]), 
                            color = color,
                            tooltip = f'{folder_name}',
                            weight = 4).add_to(group)
                
            folium.PolyLine(path_coords, 
                            color = color,
                            tooltip = f'{folder_name}',
                            weight = 4).add_to(group)
            
            #if path doesn't go until destination, fill in gap
            if path_coords[-1] != dest:
                folium.PolyLine((path_coords[-1], dest), 
                            color = color,
                            tooltip = f'{folder_name}',
                            weight = 4).add_to(group)
           
        except:
            #if unable to generate graph, create standard polyline
            folium.PolyLine(locations = [orig, dest], 
                            color = color,
                            tooltip = f'{folder_name}',
                            weight=4).add_to(group)
            print(f'{folder_name}, skipped osmnx') ##
    

    last_meta = places[-1][1]
    last_name = places[-1][0]

    last_popup = f"""
                <b> {last_name}</b><br>
                <img src = "{last_meta['path'].replace('static/','')}" width = "200">
                """ 
        
    last_icon = folium.CustomIcon(
        last_meta['thumb'],
        icon_size = (40,40),
        shadow_size = (40,40),
        shadow_anchor=(20,30)
    )
    
    #last marker
    folium.Marker(
        location = places[-1][1]['location'],
        tooltip= f'{last_name}',
        popup = last_popup,
        icon = last_icon,
        #opacity = 0.5
        ).add_to(group)
    
    group.add_to(base)

    #map.save('testmap3.html')
