import render
import folium
from pathlib import Path
import os
import random
import shutil
from paths import TRIPS_DIR, THUMBS_DIR, STATIC_DIR

def run():
    base_map = folium.Map(location = (34.0556, -117.1825), 
                 zoom_start = 4, 
                 tiles='Esri.WorldTopoMap',
                 no_wrap = True,
                 max_zoom = 16, #inward
                 min_zoom = 2, #outward
                 max_bounds=True
                 )

    if THUMBS_DIR.exists():
        shutil.rmtree(THUMBS_DIR)
    THUMBS_DIR.mkdir(parents=True,exist_ok=True)

    folder_path = TRIPS_DIR
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir() if f.is_dir()]
    folders.remove('.gitkeep')
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'black']

    print('starting...')
    for name in folders:
        print(name)
        trip_path = TRIPS_DIR / name
        render.plot(base_map, str(trip_path), colors[random.randint(0, len(colors)-1)])
    
    print('done!')
    base_map.save(str(STATIC_DIR / 'themap.html'))

def dist():
    dist = 0.0
    folder_path = TRIPS_DIR
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir() if f.is_dir()]
    for f in folders:
        dist += render.getDist(str(TRIPS_DIR/f), dist)
    
    return dist

#trips = Path(__file__).parent.resolve() / "Trips"

#if __name__ == '__main__':
#    run()
#     #print(dist())
#     #print(constants.DISTANCE)
#     #folders()