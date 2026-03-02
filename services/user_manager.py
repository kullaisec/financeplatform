from flask import Blueprint, request, jsonify, session
from models.db import get_db

user_bp = Blueprint("user", __name__)


@user_bp.route("/api/users/<int:user_id>")
def get_profile(user_id):
    db = get_db()
    user = db.execute(
        "SELECT id, username, email, role, balance FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    db.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


@user_bp.route("/api/users/<int:user_id>/update", methods=["POST"])
def update_profile(user_id):
    new_email = request.form.get("email", "")
    new_username = request.form.get("username")

    db = get_db()
    if new_email:
        db.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if new_username:
        db.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    db.commit()
    db.close()

    return jsonify({"message": f"User {user_id} updated"})


@user_bp.route("/api/users/<int:user_id>/role", methods=["POST"])
def update_role(user_id):
    new_role = request.form.get("role", "user")

    db = get_db()
    db.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    db.commit()
    db.close()

    if user_id == session.get("user_id"):
        session["role"] = new_role

    return jsonify({"message": f"Role updated to {new_role}"})


@user_bp.route("/api/users/<int:user_id>/settings", methods=["POST"])
def update_settings(user_id):
    db = get_db()
    for key, value in request.form.items():
        db.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, user_id))
    db.commit()
    db.close()
    return jsonify({"message": "Settings updated"})


@user_bp.route("/api/users/<int:user_id>/documents")
def list_documents(user_id):
    db = get_db()
    docs = db.execute(
        "SELECT id, title, content, is_private FROM documents WHERE owner_id = ?",
        (user_id,),
    ).fetchall()
    db.close()
    return jsonify([dict(d) for d in docs])


@user_bp.route("/api/documents/<int:doc_id>")
def get_document(doc_id):
    db = get_db()
    doc = db.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    db.close()
    if not doc:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(doc))


@user_bp.route("/api/documents/<int:doc_id>/delete", methods=["POST"])
def delete_document(doc_id):
    db = get_db()
    db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    db.commit()
    db.close()
    return jsonify({"message": "Deleted"})
