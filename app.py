from flask import Flask, render_template, request
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    while True:
        try:
            print("Trying to connect to MySQL...")
            connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DB")
            )
            print("MySQL connection successful!")
            return connection
        except Exception as e:
            print("MySQL not ready, waiting 3 seconds...")
            time.sleep(3)

# Create DB connection with retry
db = get_db_connection()
cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form["message"]
        cursor.execute(
            "INSERT INTO messages (content) VALUES (%s)",
            (message,)
        )
        db.commit()

    cursor.execute("SELECT content FROM messages")
    messages = cursor.fetchall()

    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
