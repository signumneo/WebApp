import boto3
import random
import string
import hashlib
from faker import Faker

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

table_name = "message_information"

# Create the table
table = dynamodb.create_table(
    TableName=table_name,
    AttributeDefinitions=[
        {"AttributeName": "Id", "AttributeType": "N"},
    ],
    KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

# Wait for the table to be created
table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

# Create an instance for the Faker class
fake = Faker()

# DeWax Tray ID options defined for the demo database
P3_val = ["S001", "S010", "S011", "S100", "S101", "S110", "S111"]
P9_val = ["S001", "S010", "S100", "S101", "S110", "S111"]


# Generate and insert fake message information
with table.batch_writer() as batch:
    for _ in range(200):
        EType = 0
        Id = fake.random_int(min=100000000, max=999999999)
        Fb = fake.random_int(min=100000000, max=999999999)
        P1 = fake.random_int(min=1000001, max=9999999)
        P2 = "".join(
            [
                str(random.randint(100, 999)),
                "".join(random.choices(string.ascii_letters, k=3)),
                str(random.randint(100, 999)),
                "".join(random.choices(string.ascii_letters, k=3)),
                str(random.randint(100, 999)),
            ]
        )
        P3 = random.choice(P3_val)
        P4 = ""
        P5 = ""
        P6 = ""
        P7 = ""
        P8 = ""
        P9 = random.choice(P9_val)
        P10 = ""
        P11 = 0
        P12 = fake.random_int(min=0, max=1)
        P13 = 0
        P14 = 0
        P15 = fake.random_int(min=0, max=1)
        P16 = 0
        P17 = fake.random_int(min=0, max=1)
        P18 = 0
        P19 = 0
        P20 = 0

        item = {
            "Id": Id,
            "EType": EType,
            "Fb": Fb,
            "P1": P1,
            "P2": P2,
            "P3": P3,
            "P4": P4,
            "P5": P5,
            "P6": P6,
            "P7": P7,
            "P8": P8,
            "P9": P9,
            "P10": P10,
            "P11": P11,
            "P12": P12,
            "P13": P13,
            "P14": P14,
            "P15": P15,
            "P16": P16,
            "P17": P17,
            "P18": P18,
            "P19": P19,
            "P20": P20,
        }

        batch.put_item(Item=item)

print(f"Table '{table_name}' created with 500 fake rows.")
