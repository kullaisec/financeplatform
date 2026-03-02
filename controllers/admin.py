import os

from flask import Blueprint, request, jsonify, session, current_app
from models.db import get_db
from settings import (
    SECRET_KEY, DB_HOST, DB_USER, DB_PASSWORD,
    AWS_ACCESS_KEY_ID, STRIPE_SECRET_KEY,
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    db = get_db()
    users = db.execute("SELECT id, username, email, role, balance FROM users").fetchall()
    logs = db.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 50").fetchall()
    db.close()

    return jsonify({
        "users": [dict(u) for u in users],
        "audit_log": [dict(l) for l in logs],
    })


@admin_bp.route("/admin/config", methods=["POST"])
def update_config():
    if session.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    key = request.form.get("key")
    value = request.form.get("value")
    current_app.config[key] = value
    return jsonify({"message": f"Config '{key}' updated"})


@admin_bp.route("/admin/query", methods=["POST"])
def run_query():
    if session.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    query = request.form.get("query", "")
    db = get_db()
    try:
        rows = db.execute(query).fetchall()
        db.commit()
        db.close()
        return jsonify({"rows": [dict(r) for r in rows]})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/admin/debug")
def debug_info():
    return jsonify({
        "secret_key": SECRET_KEY,
        "db_host": DB_HOST,
        "db_user": DB_USER,
        "db_password": DB_PASSWORD,
        "aws_key": AWS_ACCESS_KEY_ID,
        "stripe_key": STRIPE_SECRET_KEY,
        "app_config": {k: str(v) for k, v in current_app.config.items()},
        "env_vars": dict(os.environ),
    })
