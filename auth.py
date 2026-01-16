import bcrypt
from database import get_connection

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def register_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed = hash_password(password)

    try:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password, balance FROM users WHERE email=?",
        (email,)
    )
    user = cur.fetchone()
    conn.close()

    if user and check_password(password, user[1]):
        return user

    return None
