import pika
from .contacts_model import Contact


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create RabbitMQ queue
channel.queue_declare(queue='email_queue')

# Send contact IDs to RabbitMQ queue
for contact in Contact.objects:
    channel.basic_publish(
        exchange='',
        routing_key=str(contact.id),
        body=str(contact.id)
    )

print(" [x] Sent contact IDs to the email_queue")

# Close the RabbitMQ connection
connection.close()
