# Arquitectura del Proyecto
El sistema está compuesto por los siguientes servicios:

## API (FastAPI):

Permite a los usuarios crear reservas y consultar el estado de las mismas.
Publica mensajes en RabbitMQ para que sean procesados por el servicio worker.

## Worker:

* Consume los mensajes de RabbitMQ, procesa las reservas y actualiza su estado (por ejemplo, confirmed o rejected).
* Publica notificaciones en un exchange de RabbitMQ para que sean consumidas por otros servicios.

## Notify (Consumer):

Escucha las notificaciones publicadas por el worker y las registra en los logs.

## RabbitMQ:

Sistema de mensajería que permite la comunicación entre los servicios.
Almacenamiento (JSON):

Las reservas se almacenan en un archivo booking_store.json que es compartido entre los servicios api y worker.

# Cómo Ejecutar el Proyecto


1. Clonar el Repositorio

git clone https://github.com/YesidMG/Parcial1_2_50.git

2. Construir y Levantar los Servicios

docker-compose up --build

Esto levantará los siguientes servicios:

API en http://localhost:8000
RabbitMQ Management en http://localhost:15672 (usuario: guest, contraseña: guest)

# Endpoints de la API

1. Crear una Reserva

mediante curl o postman al end point http://localhost:8000/book cree un post que contenga

{
    "patient_name": "Alejo Martinez",
    "appointment_time": "2025-07-14T10:00:00",
    "timeslot": "morning"
}

esto regresara algo como lo siguiente 
{
    "booking_id": "50508644-5cd4-4fcb-8bfe-2ba095e63c67",
    "status": "pending"
}

2. Consultar el Estado de la Reserva:

al endpoint http://localhost:8000/booking/{booking_id} realice una consulta y dira el estado de la cita