from pathlib import Path 

# --- Cloud-safe folder setup ----
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

TRIPS_DIR = STATIC_DIR / 'Trips'
CACHE_DIR = STATIC_DIR / 'cache'
THUMBS_DIR = STATIC_DIR / 'thumbs'