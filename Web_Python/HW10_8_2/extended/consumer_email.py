import pika, sys, os
from ..contacts_model import Contact


def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Create RabbitMQ queue
    channel.queue_declare(queue='email_queue')

    # Define callback function for message processing
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        contact_id = int(body.decode())
        contact = Contact.objects(id=contact_id).first()
        
        if contact:
            
            # Perform email sending logic here
            print(f"Sending email to contact - ID: {contact.id}, Full Name: {contact.full_name}, Email: {contact.email}")

            # Mark the contact as sent
            contact.is_sent = True
            contact.save()
        else:
            print(f"Contact not found with ID: {contact_id}")

    # Set up message consumer
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    # Start consuming messages
    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            