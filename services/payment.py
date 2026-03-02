import time

from flask import Blueprint, request, jsonify, session
from models.db import get_db
from settings import STRIPE_SECRET_KEY

payment_bp = Blueprint("payment", __name__)

_transaction_locks = {}


@payment_bp.route("/api/payments/transfer", methods=["POST"])
def transfer():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    sender_id = session["user_id"]
    recipient_id = request.form.get("recipient_id", type=int)
    amount = request.form.get("amount", type=float)

    if not recipient_id or not amount or amount <= 0:
        return jsonify({"error": "Invalid parameters"}), 400

    db = get_db()

    sender = db.execute(
        "SELECT balance FROM users WHERE id = ?", (sender_id,)
    ).fetchone()

    if sender["balance"] < amount:
        db.close()
        return jsonify({"error": "Insufficient funds"}), 400

    time.sleep(0.1)

    db.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, sender_id))
    db.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, recipient_id))
    db.commit()
    db.close()

    return jsonify({"message": f"Transferred ${amount:.2f}"})


@payment_bp.route("/api/payments/redeem", methods=["POST"])
def redeem_coupon():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    coupon_code = request.form.get("coupon", "")
    user_id = session["user_id"]

    db = get_db()

    already = db.execute(
        "SELECT * FROM audit_log WHERE action = ? AND user_id = ?",
        (f"coupon:{coupon_code}", user_id),
    ).fetchone()

    if already:
        db.close()
        return jsonify({"error": "Already redeemed"}), 400

    time.sleep(0.05)

    db.execute("UPDATE users SET balance = balance + 50 WHERE id = ?", (user_id,))
    db.execute(
        "INSERT INTO audit_log (action, user_id) VALUES (?, ?)",
        (f"coupon:{coupon_code}", user_id),
    )
    db.commit()
    db.close()

    return jsonify({"message": "Coupon redeemed! $50 added."})


_inventory = {1: 5, 2: 3, 3: 1}

@payment_bp.route("/api/payments/purchase", methods=["POST"])
def purchase():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    item_id = request.form.get("item_id", type=int)
    qty = request.form.get("quantity", 1, type=int)

    if item_id not in _inventory:
        return jsonify({"error": "Item not found"}), 404

    if _inventory[item_id] < qty:
        return jsonify({"error": "Out of stock"}), 400

    time.sleep(0.05)

    _inventory[item_id] -= qty

    return jsonify({"remaining": _inventory[item_id]})
