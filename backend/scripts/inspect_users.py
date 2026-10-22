import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
from app.core.config import settings
from app.core.security import verify_password, hash_password

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

try:
    # 1. Ensure assigned_lot column exists in users table
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS assigned_lot VARCHAR(255) DEFAULT 'Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)';")
    conn.commit()
    print("Column assigned_lot added or already exists.")

    # 2. Query all users
    cur.execute("SELECT id, username, email, role, password_hash, full_name FROM users ORDER BY id;")
    rows = cur.fetchall()
    print(f"Total users: {len(rows)}")
    for r in rows:
        uid, uname, email, role, phash, fname = r
        print(f"User #{uid}: {uname} | Email: {email} | Role: {role} | Name: {fname}")
        
        # Test common passwords
        match = []
        for pwd in ['admin123', 'staff123', '123456', 'admin', 'staff', 'password', '12345678']:
            if verify_password(pwd, phash):
                match.append(pwd)
        print(f"   -> Password matches: {match if match else 'NO COMMON PASSWORDS MATCH!'}")

except Exception as e:
    print("Error:", e)
finally:
    cur.close()
    conn.close()
