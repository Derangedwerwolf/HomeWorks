import pika
from ..contacts_model import Contact


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create RabbitMQ queue
channel.queue_declare(queue='email_queue')

# Send contacts to the appropriate queues based on preferred delivery method
for contact in Contact.objects:
    if contact.preferred_delivery_method == "SMS":
        channel.basic_publish(
            exchange='',
            routing_key='sms_queue',
            body=str(contact.id)
        )
    elif contact.preferred_delivery_method == "Email":
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact.id)
        )

print(" [x] Sent contact IDs to the email_queue")

# Close the RabbitMQ connection
connection.close()
