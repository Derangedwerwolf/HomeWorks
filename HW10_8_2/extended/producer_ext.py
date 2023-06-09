import pika
from ..contacts_model import Contact


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create RabbitMQ queue
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

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

print(f" [x] Sent contact IDs to the {contact.preferred_delivery_method}")

# Close the RabbitMQ connection
connection.close()
