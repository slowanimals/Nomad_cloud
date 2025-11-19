from flask import Flask, render_template, url_for, redirect, request
import main
import read
import render
from pathlib import Path
import shutil
import math
from functools import lru_cache
import os
import sys
from paths import BASE_DIR, STATIC_DIR, TRIPS_DIR, CACHE_DIR, THUMBS_DIR

app = Flask(__name__)

for d in [TRIPS_DIR, CACHE_DIR, THUMBS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

@lru_cache(maxsize=1)
def dist_cache(folder_tuple):
    miles = round(main.dist() * 0.621371, 2) #convert to miles
    covered = round(((miles*100)/57500000), 7) #57.5m is sq miles of earth's land
    norm = (((math.log(1 + covered))/math.log(101)) * 100) * 5 #normalize value for prog bar
    coveredF = format(covered,'.5f') #prevents scientific notation from being displayed
    return miles, coveredF, norm

@app.route('/')
def index():
    folder_path = TRIPS_DIR
    folders = [f.name.split('/')[-1] for f in folder_path.iterdir()]
    folders = sorted(folders,reverse=False)

    folder_tuple = tuple(folders)
    miles, covered, norm = dist_cache(folder_tuple)

    return render_template('index.html',items=folders, miles=miles, covered=covered, norm=norm)


@app.route('/generate', methods=['POST'])
def generate():
    main.run()
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    folder_name = request.form['folder_name']
    upload_path = TRIPS_DIR / folder_name
    os.makedirs(upload_path, exist_ok=True)

    for file in files:
        if file.filename:
            file.save(upload_path/file.filename)
    return redirect('/')

@app.route('/delete',methods=['POST'])
def delete():
    folder_name = request.form['folder_name']
    fpath = TRIPS_DIR / folder_name
    if fpath.exists():
        try:
            shutil.rmtree(fpath)
        except OSError as e:
            print('Error deleting file')

    return redirect('/')

@app.route('/delcache', methods=['POST'])
def delcache():
    fpath = CACHE_DIR
    if fpath.exists():
        try:
            shutil.rmtree(fpath)
        except OSError as e:
            print('Error deleting cache')
    return redirect('/')

if __name__ == '__main__':
   app.run(port=8000, debug=True)


