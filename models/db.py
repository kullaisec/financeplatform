import sqlite3
import hashlib

from settings import SQLITE_PATH


def get_db():
    db = sqlite3.connect(SQLITE_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            balance REAL DEFAULT 100.0
        );
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            title TEXT,
            content TEXT,
            is_private INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS coupons (
            code TEXT PRIMARY KEY,
            value REAL NOT NULL,
            max_uses INTEGER DEFAULT 1,
            times_used INTEGER DEFAULT 0
        );
    """)

    users = [
        ("admin",   hashlib.md5(b"admin123").hexdigest(),  "admin@company.com",   "admin",   10000.0),
        ("alice",   hashlib.md5(b"password1").hexdigest(),  "alice@company.com",   "user",    500.0),
        ("bob",     hashlib.md5(b"password2").hexdigest(),  "bob@company.com",     "user",    300.0),
        ("charlie", hashlib.md5(b"password3").hexdigest(),  "charlie@company.com", "manager", 1500.0),
    ]
    for u in users:
        try:
            db.execute("INSERT INTO users (username, password, email, role, balance) VALUES (?,?,?,?,?)", u)
        except Exception:
            pass

    docs = [
        (1, "Admin Secret Plans",  "Top-secret: merger scheduled for Q3.",  1),
        (2, "Alice's Diary",       "Dear diary, today was a good day.",     1),
        (3, "Bob's Notes",         "Remember to buy milk.",                 0),
        (1, "Server Passwords",    "root:Tru5tN01!, db:S3cure#DB",         1),
    ]
    for d in docs:
        try:
            db.execute("INSERT INTO documents (owner_id, title, content, is_private) VALUES (?,?,?,?)", d)
        except Exception:
            pass

    coupons = [("WELCOME50", 50.0, 1, 0), ("BONUS100", 100.0, 1, 0)]
    for c in coupons:
        try:
            db.execute("INSERT INTO coupons (code, value, max_uses, times_used) VALUES (?,?,?,?)", c)
        except Exception:
            pass

    db.commit()
    db.close()
