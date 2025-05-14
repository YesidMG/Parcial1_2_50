import pika, time, json, random
from storage.db import load_booking_store, save_booking_store

def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Esperando a RabbitMQ...")
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="confirm_queue", durable=True)
channel.exchange_declare(exchange="booking_notifications", exchange_type="fanout")
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    data = json.loads(body)
    booking_id = data["id"]
    try:
        print(f"Procesando reserva {booking_id}")
        booking_store = load_booking_store()  # Cargar el archivo JSON dinámicamente
        if booking_id not in booking_store:
            raise KeyError(f"Reserva {booking_id} no encontrada en booking_store")

        time.sleep(random.randint(2, 5))  # Simulación
        status = random.choice(["confirmed", "rejected"])
        booking_store[booking_id]["status"] = status
        save_booking_store(booking_store)  # Guarda los datos en el archivo JSON
        print(f"Reserva actualizada: {booking_id} → {booking_store[booking_id]}")

        ch.basic_publish(
            exchange="booking_notifications",
            routing_key="",
            body=json.dumps({"id": booking_id, "status": status})
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except KeyError as e:
        print(f"Error procesando reserva {booking_id}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"Error procesando reserva {booking_id}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

channel.basic_consume(queue="confirm_queue", on_message_callback=callback)
channel.start_consuming()
