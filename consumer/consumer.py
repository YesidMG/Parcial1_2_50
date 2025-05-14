import pika, json, time

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
channel.exchange_declare(exchange="booking_notifications", exchange_type="fanout")
result = channel.queue_declare(queue='notifications_queue', durable=True)
queue_name = result.method.queue
channel.queue_bind(exchange="booking_notifications", queue=queue_name)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Notificación → Reserva {data['id']} {data['status']}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
