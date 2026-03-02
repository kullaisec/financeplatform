import hashlib

from flask import Blueprint, request, jsonify, session
from models.db import get_db
from settings import JWT_PRIVATE_KEY

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    password_hash = hashlib.md5(password.encode()).hexdigest()

    db = get_db()
    query = (
        f"SELECT * FROM users "
        f"WHERE username = '{username}' AND password = '{password_hash}'"
    )
    user = db.execute(query).fetchone()
    db.close()

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        return jsonify({
            "message": f"Welcome {user['username']}!",
            "role": user["role"],
            "token": _sign_token(user["id"]),
        })

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/api/auth/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    email = request.form.get("email", "")
    password_hash = hashlib.md5(password.encode()).hexdigest()

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password, email) VALUES (?,?,?)",
            (username, password_hash, email),
        )
        db.commit()
    except Exception:
        db.close()
        return jsonify({"error": "Username taken"}), 409
    db.close()
    return jsonify({"message": "Account created"}), 201


@auth_bp.route("/api/auth/reset-password", methods=["POST"])
def reset_password():
    email = request.form.get("email", "")
    new_password = request.form.get("new_password", "")
    new_hash = hashlib.md5(new_password.encode()).hexdigest()

    db = get_db()
    query = "UPDATE users SET password = '" + new_hash + "' WHERE email = '" + email + "'"
    db.execute(query)
    db.commit()
    db.close()

    return jsonify({"message": "Password updated"})


@auth_bp.route("/api/auth/search")
def search_users():
    q = request.args.get("q", "")
    db = get_db()
    query = "SELECT id, username, email FROM users WHERE username LIKE '%" + q + "%'"
    results = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(r) for r in results])


def _sign_token(user_id):
    import base64, json, hmac
    header = base64.b64encode(json.dumps({"alg": "HS256"}).encode()).decode()
    payload = base64.b64encode(json.dumps({"user_id": user_id}).encode()).decode()
    sig = hmac.new(JWT_PRIVATE_KEY.encode(), f"{header}.{payload}".encode(), "sha256").hexdigest()
    return f"{header}.{payload}.{sig}"
