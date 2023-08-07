# Import the necessary libraries
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    get_flashed_messages,
    session,
    url_for,
)
from pymongo import MongoClient
import sqlite3
import time
import boto3
import bcrypt
import time
import os

# Create the application instance
app = Flask(__name__)
app.secret_key = "1b5c2e4e0a8d736f"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db_mongodb = client["GlidewellMemphis"]
collection_mongodb = db_mongodb["message_information"]
collection_user = db_mongodb["user_information"]

# SQLite3 Database connection
conn_sqlite = sqlite3.connect(
    "./local databases/SQLite_Message.db", check_same_thread=False
)
print("SQLite Connection:", conn_sqlite)

cursor_sqlite = conn_sqlite.cursor()
print("SQLite Cursor:", cursor_sqlite)

# DynamoDB connection
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
table_name = "process_information"


# Login route
@app.route("/")
def login():
    return render_template("login.html")


# Authentication route
@app.route("/authenticate", methods=["POST"])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]

    user = collection_user.find_one({"Username": username})

    # Using hashed passwords stored in the database for user authentication
    if user:
        hashed_password = user["Hashed Password"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            session["username"] = username
            # Store the 'database' value in the session before redirection
            session["database"] = request.form.get(
                "database", "mongodb"
            )  # Default to "mongodb" if not set
            return redirect("/verification")
        else:
            # Redirect to the login page with an error message
            flash("User credentials invalid. Please check and try again.", "error")
            return render_template("login.html")
    else:
        flash("User credentials invalid. Please check and try again.", "error")
        return render_template("login.html")


# New user login template
@app.route("/newuser")
def new_user():
    return render_template("newuser.html")


# Route to create a new user
@app.route("/createuser", methods=["POST"])
def create_user():
    tech_id = request.form["tech_id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    department = request.form["department"]
    username = request.form["username"]
    password = request.form["password"]
    re_enter_password = request.form["re_enter_password"]

    if password != re_enter_password:
        error_message = "Passwords do not match. Please try again."
        return render_template("newuser.html", error=error_message)

    user_exists = collection_mongodb.find_one({"Username": username})

    if user_exists:
        error_message = "User already registered. Please return to the login page."
        return render_template("newuser.html", error=error_message)

    # Hashing the password for added security
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_data = {
        "Tech ID": tech_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Department": department,
        "Username": username,
        "Password": password,
        "Hashed Password": hashed_password.decode("utf-8"),
    }

    collection_user.insert_one(user_data)
    success_message = "User profile successfully created"
    return render_template("newuser.html", success=success_message)


# Verification route
@app.route("/verification", methods=["GET"])
def user_verification():
    if "username" in session:
        database = session.get("database", "mongodb")
        # Retrieve the 'database' value from the session  # Default to "mongodb" if not set
        return redirect(url_for("dashboard", database=database))
    else:
        return redirect("/")


@app.route("/dashboard/<database>", methods=["GET", "POST"])
def dashboard(database="mongodb"):
    if request.method == "POST":
        new_database = request.form.get("database")
        if new_database in ["mongodb", "sqlite", "dynamodb"]:
            database = new_database

    dashboard_name = ""
    is_mongodb = None
    is_sqlite = None
    is_dynamodb = None
    data = []
    column_names = []

    # Fetch data and column names based on the selected database
    if database == "mongodb":
        # Fetch data from MongoDB
        data = collection_mongodb.find().limit(15)
        is_mongodb = True
        is_sqlite = False
        is_dynamodb = False
        dashboard_name = "MongoDB Database"

        # Get column names from the first document (assumes all documents have the same keys)
        if data:
            column_names = list(data[0].keys())

    elif database == "sqlite":
        try:
            cursor_sqlite.execute("SELECT * FROM message_information LIMIT 15")
            data = cursor_sqlite.fetchall()
            is_sqlite = True
            is_mongodb = False
            is_dynamodb = False
            dashboard_name = "SQLite Database"
            print("Query Result:", data)

            # Get column names from the SQLite table
            if data:
                column_names = [
                    description[0] for description in cursor_sqlite.description
                ]

        except sqlite3.Error as e:
            print("Error executing query:", e)

    elif database == "dynamodb":
        # Fetch data from DynamoDB
        table = dynamodb.Table(table_name)
        response = table.scan()
        print(response["Items"])

        # Get the list of items from the response
        data = response.get("Items", [])

        # Convert the DynamoDB item format to regular dictionaries
        data = [dict(item) for item in data]

        is_mongodb = False
        is_sqlite = False
        is_dynamodb = True
        dashboard_name = "DynamoDB Database"

        # Get column names from the DynamoDB data
        if data:
            column_names = list(data[0].keys())

    else:
        flash("Invalid database selected")
        return redirect("/")

    return render_template(
        "index.html",
        data=data,
        is_mongodb=is_mongodb,
        is_sqlite=is_sqlite,
        is_dynamodb=is_dynamodb,
        dashboard_name=dashboard_name,
        column_names=column_names,  # Pass the column names to the template
    )


# Defining a separate route in order to monitor an endpoint in case the functionality is required
@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    # Extract the relevant data from the JSON
    etype = data["Data"]["EType"]
    Id = data["Data"]["Id"]
    Fb = data["Data"]["Fb"]
    p1 = data["Data"]["P1"]
    p2 = data["Data"]["P2"]
    p3 = data["Data"]["P3"]
    p4 = data["Data"]["P4"]
    p5 = data["Data"]["P5"]
    p6 = data["Data"]["P6"]
    p7 = data["Data"]["P7"]
    p8 = data["Data"]["P8"]
    p9 = data["Data"]["P9"]
    p10 = data["Data"]["P10"]
    p11 = data["Data"]["P11"]
    p12 = data["Data"]["P12"]
    p13 = data["Data"]["P13"]
    p14 = data["Data"]["P14"]
    p15 = data["Data"]["P15"]
    p16 = data["Data"]["P16"]
    p17 = data["Data"]["P17"]
    p18 = data["Data"]["P18"]
    p19 = data["Data"]["P19"]
    p20 = data["Data"]["P20"]

    # Store the data in MongoDB
    collection_mongodb.insert_one(
        {
            "EType": etype,
            "Id": Id,
            "Fb": Fb,
            "P1": p1,
            "P2": p2,
            "P3": p3,
            "P4": p4,
            "P5": p5,
            "P6": p6,
            "P7": p7,
            "P8": p8,
            "P9": p9,
            "P10": p10,
            "P11": p11,
            "P12": p12,
            "P13": p13,
            "P14": p14,
            "P15": p15,
            "P16": p16,
            "P17": p17,
            "P18": p18,
            "P19": p19,
            "P20": p20,
        }
    )

    # Store the data in SQLite3
    cursor_sqlite.execute(
        "INSERT INTO message_information (EType, Id, Fb, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            etype,
            Id,
            Fb,
            p1,
            p2,
            p3,
            p4,
            p5,
            p6,
            p7,
            p8,
            p9,
            p10,
            p11,
            p12,
            p13,
            p14,
            p15,
            p16,
            p17,
            p18,
            p19,
            p20,
        ),
    )
    conn_sqlite.commit()

    # Store the data in DynamoDB
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            "EType": etype,
            "Id": Id,
            "Fb": Fb,
            "P1": p1,
            "P2": p2,
            "P3": p3,
            "P4": p4,
            "P5": p5,
            "P6": p6,
            "P7": p7,
            "P8": p8,
            "P9": p9,
            "P10": p10,
            "P11": p11,
            "P12": p12,
            "P13": p13,
            "P14": p14,
            "P15": p15,
            "P16": p16,
            "P17": p17,
            "P18": p18,
            "P19": p19,
            "P20": p20,
        }
    )

    flash("Entry created successfully")
    return jsonify({"success": True})


# Route to create an entry in the required database
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        database = request.form.get("database")
        etype = request.form.get("etype")
        Id = request.form.get("Id")
        Fb = request.form.get("Fb")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")

        if not database or not etype or not Id or not Fb or not p1 or not p2:
            flash("All fields are required")
            return redirect("/create")

        if database == "mongodb" or database == "both":
            existing_data_mongodb = collection_mongodb.find_one(
                {
                    "EType": etype,
                    "Id": int(Id),
                    "Fb": int(Fb),
                    "P1": int(p1),
                    "P2": p2,
                }
            )
            if existing_data_mongodb:
                flash("Data already exists in MongoDB")
                time.sleep(3)  # Delay the flash message for 3 seconds
                return redirect("/create")
            collection_mongodb.insert_one(
                {
                    "EType": etype,
                    "Id": int(Id),
                    "Fb": int(Fb),
                    "P1": int(p1),
                    "P2": p2,
                }
            )

        if database == "sqlite" or database == "both":
            existing_data_sqlite = cursor_sqlite.execute(
                "SELECT * FROM message_information WHERE EType = ? AND Id = ? AND Fb = ? AND P1 = ? AND P2 = ?",
                (
                    etype,
                    Id,
                    Fb,
                    int(p1),
                    p2,
                ),
            ).fetchone()
            if existing_data_sqlite:
                flash("Data already exists in SQLite")
                return redirect("/create")
            cursor_sqlite.execute(
                "INSERT INTO message_information (EType, Id, Fb, P1, P2) VALUES (?, ?, ?, ?, ?)",
                (
                    etype,
                    Id,
                    Fb,
                    int(p1),
                    p2,
                ),
            )
            conn_sqlite.commit()

        if database == "dynamodb" or database == "both":
            # Check if the entry already exists in DynamoDB
            table = dynamodb.Table(table_name)
            existing_data_dynamodb = table.get_item(
                Key={"EType": etype, "Id": Id, "Fb": Fb}
            )
            if "Item" in existing_data_dynamodb:
                flash("Data already exists in DynamoDB")
                return redirect("/create")
            table.put_item(
                Item={
                    "EType": etype,
                    "Id": Id,
                    "Fb": Fb,
                    "P1": int(p1),
                    "P2": p2,
                }
            )

        flash("Entry created successfully")
        time.sleep(3)  # Delay the flash message for 3 seconds)
        return redirect("/dashboard/" + database)

    return render_template("create.html")


# Route to read an entry from the required database
@app.route("/read", methods=["GET", "POST"])
def read():
    if request.method == "POST":
        etype = request.form.get("etype")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")

        if not etype or not p1 or not p2:
            flash("All fields are required")
            return redirect("/read")

        data_mongodb = collection_mongodb.find(
            {"EType": int(etype), "P1": p1, "P2": p2}
        )
        d_mongodb = list(data_mongodb)
        print(d_mongodb)

        data_sqlite = cursor_sqlite.execute(
            "SELECT * FROM message_information WHERE EType = ? AND P1 = ? AND P2 = ?",
            (int(etype), int(p1), p2),
        ).fetchall()

        d_sqlite = list(data_sqlite)
        print(d_sqlite)

        if len(d_mongodb) > 0 or len(d_sqlite) > 0:
            return render_template(
                "read.html", data_mongodb=d_mongodb, data_sqlite=d_sqlite
            )
        else:
            flash("No matching entry found")
            return redirect("/read")

    return render_template("read.html")


# Route to update an entry in the required database
@app.route("/update", methods=["GET", "POST"])
def update():
    d_list = []
    dsql_list = []

    if request.method == "POST":
        etype = request.form.get("etype")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")
        p3 = request.form.get("p3")
        database = request.form.get("database")

        if not etype or not p1 or not p2 or not p3 or not database:
            flash("All fields are required")
            return redirect("/update")

        if database == "mongodb" or database == "both":
            data_mongodb = collection_mongodb.find(
                {"EType": int(etype), "P1": int(p1), "P2": p2, "P3": p3}
            )
            d_list = list(data_mongodb)
            print(d_list)

        if database == "sqlite" or database == "both":
            data_sqlite = cursor_sqlite.execute(
                "SELECT * FROM message_information WHERE EType = ?",
                (int(etype), int(p1), p2, p3),
            ).fetchall()
            dsql_list = list(data_sqlite)
            print(dsql_list)

        if database == "dynamodb" or database == "both":
            table = dynamodb.Table(table_name)
            response = table.get_item(Key={"EType": etype, "Id": int(p1), "Fb": p2})
            if "Item" in response:
                d_list.append(response["Item"])

        if len(d_list) > 0 or len(dsql_list) > 0:
            return render_template(
                "update_values.html", data_mongodb=d_list, data_sqlite=dsql_list
            )
        else:
            flash("No matching entry found")
            return redirect("/update")

    return render_template("update.html")


# Route to take in the new values and display the updated entry
@app.route("/update_row", methods=["POST"])
def update_row():
    new_etype = request.form.get("new_etype")
    new_p1 = request.form.get("new_p1")
    new_p2 = request.form.get("new_p2")
    new_p3 = request.form.get("new_p3")
    new_database = request.form.get("new_database")
    etype = request.form.get("etype")
    p1 = request.form.get("p1")
    p2 = request.form.get("p2")
    p3 = request.form.get("p3")
    database = request.form.get("database")

    if not new_etype or not new_p1 or not new_p2 or not new_p3 or not new_database:
        flash("All fields are required")
        return redirect("/update")

    if new_database == "mongodb" or new_database == "both":
        collection_mongodb.update_many(
            {"EType": int(etype), "P1": int(p1), "P2": p2, "P3": p3},
            {
                "$set": {
                    "EType": int(new_etype),
                    "P1": int(new_p1),
                    "P2": new_p2,
                    "P3": new_p3,
                }
            },
        )

    if new_database == "sqlite" or new_database == "both":
        cursor_sqlite.execute(
            "UPDATE message_information SET EType = ?, P1 = ?, P2 = ?, P3 = ? WHERE EType = ?",
            (
                int(new_etype),
                int(new_p1),
                new_p2,
                new_p3,
                int(etype),
            ),
        )
        conn_sqlite.commit()

    if new_database == "dynamodb" or new_database == "both":
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={"EType": int(etype), "Id": int(p1), "Fb": p2})
        if "Item" in response:
            item = response["Item"]
            item["EType"] = int(new_etype)
            item["P1"] = int(new_p1)
            item["P2"] = new_p2
            item["P3"] = new_p3
            table.put_item(Item=item)

    flash("Entry updated successfully")
    return redirect("/dashboard/" + new_database)


# Route to delete an entry from the required database
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        database = request.form.get("database")
        P1 = request.form.get("P1")

        if not database or not P1:
            flash("Database and P1 value are required")
            return redirect("/delete")

        if database == "mongodb":
            collection_mongodb.delete_one({"P1": int(P1)})
        elif database == "sqlite":
            cursor_sqlite.execute(
                "DELETE FROM message_information WHERE P1 = ?", (int(P1),)
            )
            conn_sqlite.commit()
        elif database == "dynamodb":
            table = dynamodb.Table(table_name)
            table.delete_item(Key={"P1": int(P1)})

        flash("Entry deleted successfully")
        return redirect("/dashboard/" + database)

    return render_template("delete.html")


# Logout route defined
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Running the flask application with debug mode enabled for faster troubleshooting
if __name__ == "__main__":
    app.run(debug=True)
