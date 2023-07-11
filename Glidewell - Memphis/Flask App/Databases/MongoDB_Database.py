########################################################################################################################################################################################
############################################################### Code to create fake database for testing purposes. #####################################################################
# Import the necessary libraries and modules 
from faker import Faker

### Notes: Comment on bcrypt installation added in the login.html file 
import bcrypt
from pymongo import MongoClient
import random

# Connecting the code to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['GlidewellMemphis']  # Updated database name without space
collection = db['user_information']

# Create Faker instance
fake = Faker()

# Define the list of department options. Initial intuitive guesses. Actual details will be edited in the final stages of development 
departments = ['Engineering and Technology', 'Warehouse', 'Automation', 'IT']

# Generate and insert fake user information
for _ in range(100):
    tech_id = fake.random_int(min=100000, max=999999)
    first_name = fake.first_name()
    last_name = fake.last_name()
    department = random.choice(departments)
    username = fake.user_name()

    # Generate a random password
    password = fake.password()

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a user document
    user_data = {
        'Tech ID': str(tech_id),
        'First Name': first_name,
        'Last Name': last_name,
        'Department': department,
        'Username': username,
        'Password': password,  # Unhashed password
        'Hashed Password': hashed_password.decode('utf-8')  # Hashed password
    }

    # Inserting the user document into the collection
    collection.insert_one(user_data)

# Closing the MongoDB connection
client.close()
