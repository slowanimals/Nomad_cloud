from flask import Flask, render_template, url_for, redirect, request
import main
import read
import render
from pathlib import Path
import shutil
import math
from functools import lru_cache
from pyfladesk import init_gui
import os
import sys

def resource_path(relative_path): #from pyfladesk github
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)


@lru_cache(maxsize=1)
def dist_cache(folder_tuple):
    miles = round(main.dist() * 0.621371, 2) #convert to miles
    covered = round(((miles*100)/57500000), 7) #57.5m is sq miles of earth's land
    norm = (((math.log(1 + covered))/math.log(101)) * 100) * 5 #normalize value for prog bar
    coveredF = format(covered,'.5f') #prevents scientific notation from being displayed
    return miles, coveredF, norm

@app.route('/')
def index():
    folder_path = Path('static') / 'Trips'
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir()]
    folders.remove('.gitkeep')
    folders = sorted(folders,reverse=False)

    folder_tuple = tuple(folders)
    miles, covered, norm = dist_cache(folder_tuple)
    os.makedirs('static/Trips',exist_ok=True)

    return render_template('index.html',items=folders, miles=miles, covered=covered, norm=norm)


@app.route('/generate', methods=['POST'])
def generate():
    main.run()
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    folder_name = request.form['folder_name']
    upload_path = f'static/Trips/{folder_name}'
    os.makedirs(upload_path, exist_ok=True)

    for file in files:
        if file.filename:
            file.save(f'{upload_path}/{file.filename}')
    return redirect('/')

@app.route('/delete',methods=['POST'])
def delete():
    folder_name = request.form['folder_name']
    fpath = Path('static')/ 'Trips' / folder_name
    if fpath.exists():
        try:
            shutil.rmtree(fpath)
        except OSError as e:
            print('Error deleting file')

    return redirect('/')

@app.route('/delcache', methods=['POST'])
def delcache():
    fpath = Path('static')/'cache'
    if fpath.exists():
        try:
            shutil.rmtree(fpath)
        except OSError as e:
            print('Error deleting cache')
    return redirect('/')

if __name__ == '__main__':
   #app.run(port=8000, debug=True)
   init_gui(app)



