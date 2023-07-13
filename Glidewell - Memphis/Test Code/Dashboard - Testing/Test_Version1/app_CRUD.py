# ... import statements and other code ...


# Update route defined
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        # Retrieve updated data from the form
        etype = request.form["etype"]
        fb = request.form["fb"]
        p1 = request.form["p1"]
        p2 = request.form["p2"]
        p3 = request.form["p3"]
        # ... retrieve other fields ...

        # Update the data in MongoDB
        collection.update_one(
            {"ID": id},
            {
                "$set": {
                    "EType": etype,
                    "Fb": fb,
                    "P1": p1,
                    "P2": p2,
                    "P3": p3,
                    # ... update other fields ...
                }
            },
        )

        # Update the data in SQLite
        cursor.execute(
            "UPDATE message_information SET EType = ?, Fb = ?, P1 = ?, P2 = ?, P3 = ? WHERE ID = ?",
            (
                etype,
                fb,
                p1,
                p2,
                p3,
                # ... update other fields ...
                id,
            ),
        )
        conn.commit()

        return redirect("/")  # Redirect to the dashboard or any other appropriate page
    else:
        # Retrieve the existing data for the specified ID from MongoDB
        data_mongodb = collection.find_one({"ID": id})

        # Retrieve the existing data for the specified ID from SQLite
        cursor.execute("SELECT * FROM message_information WHERE ID = ?", (id,))
        data_sqlite = cursor.fetchone()

        return render_template(
            "update.html", data_mongodb=data_mongodb, data_sqlite=data_sqlite
        )


# Delete route defined
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        # Delete the data from MongoDB
        collection.delete_one({"ID": id})

        # Delete the data from SQLite
        cursor.execute("DELETE FROM message_information WHERE ID = ?", (id,))
        conn.commit()

        return redirect("/")  # Redirect to the dashboard or any other appropriate page
    else:
        # Retrieve the existing data for the specified ID from MongoDB
        data_mongodb = collection.find_one({"ID": id})

        # Retrieve the existing data for the specified ID from SQLite
        cursor.execute("SELECT * FROM message_information WHERE ID = ?", (id,))
        data_sqlite = cursor.fetchone()

        return render_template(
            "delete.html", data_mongodb=data_mongodb, data_sqlite=data_sqlite
        )


# ... other routes and app.run() statement ...
