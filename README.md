# Nomad
A new way to visualize your journeys across the world!

<img width="648" height="473" alt="Screenshot 2025-11-13 at 3 30 54 PM" src="https://github.com/user-attachments/assets/1b97f4fc-9e84-4669-8112-1749270f9ee9" />

## Installation (Note: This project will soon be a downloadable app)
1. **Clone Repository**
   - git clone https://github.com/slowanimals/nomad.git
2. **Create Virtual Environment**

   - Mac/Linux:
     - python3 -m venv venv
     - source venv/bin/activate
   - Windows:
     - python -m venv venv
     - venv\Scripts\activate
     
3. **Install Dependencies**
   - pip install -r requirements.txt
4. **Run App**
   - python3 nomad.py
      - Go to the localhost link outputted in terminal (ex: Running on http://127.0.0.1:8000) 

## Tech Stack
- OSMnx
- Folium
- Exifread
- Pathlib
- Pillow
- Python
- Flask
- PyFladesk
- HTML5
- CSS3

## Idea
I wanted to build a desktop app that uses images from your travels to help visualize all of your trips on one map. I also wanted to make a system that can rebuild routes from images
as opposed to needing exact real-time location data.


## Features
- Rendering engine that
  - Plots images on a map
  - Draws polylines using OSMnx network graphs to approximate routes traveled 
- Interactive Folium map
- Dashboard that displays buttons, trips, and metrics
- Thumbnail generation via Pillow to show image previews
   - Thumbnail folder is automatically deleted and repopulated whenever map is regenerating

## How to Use:
- Click on "Upload" to upload any amount of images, then enter the folder name you want the images to go into
  - Entering the name of an existing folder will place the images in that folder
- Click on "Generate" to run the plotting engine after making any changes
  - The engine is heavy, so it may take a minute or so for the new map to generate
- Click on the "Delete" button next to trip names in order to delete the folder

## Features I'm Working On
- Toggle custom colors for polylines
- Enter descriptions for trips
- Edit trip names
- Update images within trips
- Map type customization


