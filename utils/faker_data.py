from faker import Faker

fake = Faker()

def generate_vendor_data():
    return {
        "vendor_name": fake.company(),
        "address": fake.address(),
        "contact_number": fake.numerify("##########"),
        "pan_number": fake.numerify("##########"),
    }
