########################################################################### Application V.1 ############################################################################################
# Import the necessary libraries and modules.
from flask import Flask, render_template, request, redirect, session

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
collection = db["user_information"]


# App route creation
@app.route("/")
def login():
    return render_template("login.html")


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


# Dashboard route defined
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        return redirect("/")


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


# Running the app
if __name__ == "__main__":
    app.run()


########################################################################################################################################################################################
