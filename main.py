# main.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# ---- temporary "database" + login state ----
USERS = {
    "admin": "admin123",
    "gabby": "password123"
}
app.config["LOGGED_IN"] = False
# --------------------------------------------


@app.route("/")
def root():
    """
    Root endpoint to check API health.
    """
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    """
    Simple logic function to test mathematics.
    """
    return jsonify({"result": a + b})


@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint using a temporary in-memory database.
    Expects JSON: {"username": "...", "password": "..."}
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        app.config["LOGGED_IN"] = True
        return jsonify({"message": "login successful"}), 200

    app.config["LOGGED_IN"] = False
    return jsonify({"message": "invalid credentials"}), 401


@app.route("/subtract/<int:a>/<int:b>")
def subtract(a, b):
    """
    Subtract endpoint that can ONLY be accessed after login.
    """
    if not app.config.get("LOGGED_IN", False):
        return jsonify({"error": "unauthorized, please login first"}), 401

    return jsonify({"result": a - b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
