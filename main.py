import render
import folium
from pathlib import Path
import os
import random
import shutil

def run():
    base_map = folium.Map(location = (34.0556, -117.1825), 
                 zoom_start = 4, 
                 tiles='Esri.WorldTopoMap',
                 no_wrap = True,
                 max_zoom = 16, #inward
                 min_zoom = 2, #outward
                 max_bounds=True
                 )

    if os.path.exists('static/thumbs'):
        shutil.rmtree('static/thumbs')
    os.mkdir('static/thumbs')

    folder_path = Path('static') / 'Trips'
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir()]
    folders.remove('.gitkeep')
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'black']

    print('starting...')
    for name in folders:
        print(name)
        #try:
        render.plot(base_map, f'static/Trips/{name}', colors[random.randint(0, len(colors)-1)])
        #except UserWarning:
            #render.plot(base_map,f'assets/Trips/{name}','purple')
    print('done!')
    base_map.save('static/themap.html')

def dist():
    dist = 0.0
    folder_path = Path('static') / 'Trips'
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir()]
    folders.remove('.gitkeep')
    for f in folders:
        dist += render.getDist(f'static/Trips/{f}', dist)
    
    return dist

#trips = Path(__file__).parent.resolve() / "Trips"

#if __name__ == '__main__':
#    run()
#     #print(dist())
#     #print(constants.DISTANCE)
#     #folders()