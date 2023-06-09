import random
from faker import Faker
from .contacts_model import Contact


fake = Faker()


# Generate fake contacts
def generate_fake_contacts(num_contacts):
    fake_contacts = []
    
    for _ in range(num_contacts):
        full_name = fake.name()
        user_age = random.randint(16, 99)
        user_profession = fake.job()
        phone_number = fake.phone_number()
        email = fake.email()
        contact = Contact(
            full_name=full_name,
            user_age=user_age,
            user_profession=user_profession,
            phone_number = phone_number,
            email=email
        )
        contact.save()
        
        fake_contacts.append(contact)
    
    return fake_contacts


# Generate fake contacts
num_contacts = 10
contacts = generate_fake_contacts(num_contacts)