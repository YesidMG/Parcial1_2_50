import json
import os

# Archivo donde se almacenarán las reservas
DB_FILE = "booking_store.json"

# Función para cargar datos desde el archivo JSON
def load_booking_store():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

# Función para guardar datos en el archivo JSON
def save_booking_store(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
