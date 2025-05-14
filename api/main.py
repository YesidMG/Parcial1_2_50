from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import pika
import json
from storage.db import load_booking_store, save_booking_store

app = FastAPI()

class Booking(BaseModel):
    patient_name: str
    timeslot: str

@app.post("/book")
def book_appointment(data: Booking):
    booking_id = str(uuid.uuid4())
    booking_store = load_booking_store()  # Cargar el archivo JSON dinámicamente
    booking_store[booking_id] = {"status": "pending", **data.dict()}
    save_booking_store(booking_store)  # Guarda los datos en el archivo JSON
    print(f"Reserva creada: {booking_id} → {booking_store[booking_id]}")

    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="confirm_queue", durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='confirm_queue',
        body=json.dumps({"id": booking_id}),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

    return {"booking_id": booking_id, "status": "pending"}

@app.get("/booking/{booking_id}")
def get_status(booking_id: str):
    booking_store = load_booking_store()  # Cargar el archivo JSON dinámicamente
    return booking_store.get(booking_id, {"error": "Not found"})
