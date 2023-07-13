########################################################################### Application V.1 ############################################################################################
# Import the necessary libraries and modules.
from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

### Notes: Importing pymongo used for communication with MongoDB.
from pymongo import MongoClient

### Notes: Importing bcrypt can sometimes lead to "Module not found" errors because of installation issues.
### Fixes: Locate the scripts folder in the Python directory and then reinstall bcrypt in order for it to be detected while executing the python file.
import bcrypt

# App instance creation
app = Flask(__name__)

### Notes: Secret key created for user session management. Will update this at a later stage.
app.secret_key = "1b5c2e4e0a8d736f"

# MongoDB connection
client = MongoClient(host="mongodb://localhost:27017/")

### Notes: Database and connection monitored using MongoDB Compass. Reference snippets in images folder.
db = client["GlidewellMemphis"]
collection = db["message_information"]


## SQLite3 Database connection
conn = sqlite3.connect(
    "./Dashboard - Testing/Test_Version1/SQLite_Message.db", check_same_thread=False
)
cursor = conn.cursor()

"""
# App route creation
@app.route("/")
def login():
    return render_template("index.html")



# Authentication route defined
@app.route("/authenticate", methods=["POST"])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]

    user = collection.find_one({"Username": username})

    # Using hashed passwords stored in the database for user authentication
    if user:
        hashed_password = user["Hashed Password"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            session["username"] = username
            return redirect("/dashboard")

    error_message = "User credentials invalid. Please check and try again."
    return render_template("login.html", error=error_message)
"""


# Dashboard route defined
@app.route("/")
def dashboard():
    ## MongoDB data retrieval and display on the template
    data_mongodb = collection.find()  # Retrieve all the data from the database

    ## SQLite3 data retrieval and display on the template
    cursor.execute("SELECT * FROM message_information")
    data_sqlite = cursor.fetchall()  # Fetch all rows

    return render_template(
        "index1.html", data_mongodb=data_mongodb, data_sqlite=data_sqlite
    )


@app.route("/create", methods=["POST"])
def create():
    etype = request.form.get("etype")
    job_id = request.form.get("job_id")
    fb = request.form.get("fb")
    p1 = request.form.get("p1")
    p2 = request.form.get("p2")
    p3 = request.form.get("p3")
    p4 = request.form.get("p4")
    p5 = request.form.get("p5")
    p6 = request.form.get("p6")
    p7 = request.form.get("p7")
    p8 = request.form.get("p8")
    p9 = request.form.get("p9")
    p10 = request.form.get("p10")
    p11 = request.form.get("p11")
    p12 = request.form.get("p12")
    p13 = request.form.get("p13")
    p14 = request.form.get("p14")
    p15 = request.form.get("p15")
    p16 = request.form.get("p16")
    p17 = request.form.get("p17")
    p18 = request.form.get("p18")
    p19 = request.form.get("p19")
    p20 = request.form.get("p20")

    collection.insert_one(
        {
            "EType": etype,
            "Id": job_id,
            "Fb": fb,
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

    cursor.execute(
        "INSERT INTO message_information (EType, Id, Fb, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            etype,
            job_id,
            fb,
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
    flash("Data added successfully to the database")
    try:
        conn.commit()
        print("Data committed successfully to SQLite database")
    except sqlite3.Error as e:
        print("Error occurred during data commit:", e)

    return redirect("/")


@app.route("/read", methods=["POST"])
def read():
    fb = request.form.get("fb")
    p1 = request.form.get("p1")
    p2 = request.form.get("p2")
    p3 = request.form.get("p3")

    job_mongodb = collection.find_one({"Fb": fb, "P1": p1, "P2": p2, "P3": p3})
    cursor.execute(
        "SELECT * FROM message_information WHERE Fb = ? AND P1 = ? AND P2 = ? AND P3 = ?",
        (fb, p1, p2, p3),
    )
    job_sqlite = cursor.fetchone()

    return render_template(
        "popup.html", data_mongodb=job_mongodb, data_sqlite=job_sqlite
    )


@app.route("/update/<id>", methods=["POST"])
def update(id):
    new_data = request.form.get("new_data")
    collection.update_one({"_id": id}, {"$set": {"data": new_data}})
    cursor.execute(
        "UPDATE message_information SET data = ? WHERE id = ?", (new_data, id)
    )
    conn.commit()
    return redirect("/")


@app.route("/delete/<Fb>", methods=["POST"])
def delete(Fb):
    collection.delete_one({"Fb": Fb})
    cursor.execute("DELETE FROM message_information WHERE Fb = ?", (Fb,))
    conn.commit()
    return redirect("/")


"""
@app.route("/newuser")
def new_user():
    return render_template("newuser.html")


### Notes: Information collected from the user can be updated during the final stages of development
# Create user route defined
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

    user_exists = collection.find_one({"Username": username})

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

    collection.insert_one(user_data)
    success_message = "User profile successfully created"
    return render_template("newuser.html", success=success_message)


# Logout route defined
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

"""

# Running the app
if __name__ == "__main__":
    app.run()

########################################################################################################################################################################################
