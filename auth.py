import hashlib
from database import get_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, balance FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )

    user = cur.fetchone()
    conn.close()
    return user
