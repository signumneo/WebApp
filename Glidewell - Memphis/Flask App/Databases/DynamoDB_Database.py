import boto3
import hashlib
import random
import string

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

table_name = "users_information"

# Create the table
table = dynamodb.create_table(
    TableName=table_name,
    AttributeDefinitions=[
        {"AttributeName": "TechID", "AttributeType": "N"},
    ],
    KeySchema=[{"AttributeName": "TechID", "KeyType": "HASH"}],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

# Wait for the table to be created
table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

# Generate fake data and populate the table
with table.batch_writer() as batch:
    for _ in range(500):
        tech_id = random.randint(100000, 999999)
        first_name = "".join(random.choices(string.ascii_uppercase, k=5))
        last_name = "".join(random.choices(string.ascii_uppercase, k=5))
        department = random.choice(["IT", "HR", "Finance", "Marketing"])
        username = f"{first_name.lower()}.{last_name.lower()}"
        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        item = {
            "TechID": tech_id,
            "FirstName": first_name,
            "LastName": last_name,
            "Department": department,
            "Username": username,
            "Password": password,
            "HashedPassword": hashed_password,
        }

        batch.put_item(Item=item)

print(f"Table '{table_name}' created with 500 fake rows.")
