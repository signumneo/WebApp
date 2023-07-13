import json
import csv
import os

target_column = "ObjectJSON"
csv_file = "DynamoDB_Message.csv"

# Open the database file
with open("DynamoDB_Message.db", "r", encoding="utf-8", errors="replace") as file:
    # Read the rows from the file
    rows = file.readlines()

# Extract JSON information from the target column and write to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(
        [
            "P1",
            "P2",
            "P3",
            "P4",
            "P5",
            "P6",
            "P7",
            "P8",
            "P9",
            "EType",
            "P10",
            "P20",
            "P12",
            "P11",
            "P14",
            "P13",
            "P16",
            "P15",
            "P18",
            "P17",
            "P19",
            "Id",
            "Fb",
        ]
    )

    # Extract JSON information from the target column in each row
    for row in rows:
        # Remove newline characters from the row
        row = row.strip()

        # Extract the JSON data from the target column
        try:
            json_data = json.loads(row)[target_column]

            # Extract the required information from the JSON data
            extracted_info = [
                json_data.get("P1", {}).get("N", ""),
                json_data.get("P2", {}).get("S", ""),
                json_data.get("P3", {}).get("S", ""),
                json_data.get("P4", {}).get("S", ""),
                json_data.get("P5", {}).get("S", ""),
                json_data.get("P6", {}).get("S", ""),
                json_data.get("P7", {}).get("S", ""),
                json_data.get("P8", {}).get("S", ""),
                json_data.get("P9", {}).get("S", ""),
                json_data.get("EType", {}).get("N", ""),
                json_data.get("P10", {}).get("S", ""),
                json_data.get("P20", {}).get("N", ""),
                json_data.get("P12", {}).get("N", ""),
                json_data.get("P11", {}).get("N", ""),
                json_data.get("P14", {}).get("N", ""),
                json_data.get("P13", {}).get("N", ""),
                json_data.get("P16", {}).get("N", ""),
                json_data.get("P15", {}).get("N", ""),
                json_data.get("P18", {}).get("N", ""),
                json_data.get("P17", {}).get("N", ""),
                json_data.get("P19", {}).get("N", ""),
                json_data.get("Id", {}).get("N", ""),
                json_data.get("Fb", {}).get("N", ""),
            ]

            # Write the extracted information to the CSV file
            writer.writerow(extracted_info)
        except (json.JSONDecodeError, KeyError) as e:
            print("Error extracting JSON information:", e)
            print("Skipping problematic row:", row)
