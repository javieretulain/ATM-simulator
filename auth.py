import bcrypt
from database import get_connection

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def register_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed = hash_password(password).decode("utf-8")

    try:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, hashed)
        )
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password, balance FROM users WHERE email=%s",
        (email,)
    )
    user = cur.fetchone()
    conn.close()
    
    stored_hash = user[1].encode("utf-8")
    
    if user and check_password(password, stored_hash):
        return user
    
    return None
