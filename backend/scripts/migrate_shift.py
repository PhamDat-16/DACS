import os
import sys
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.config import settings

def migrate():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS shift VARCHAR(100) DEFAULT 'Ca Sáng (06h - 14h)';")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active';")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS assigned_lot VARCHAR(255) DEFAULT 'Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)';")
    conn.commit()
    print("Database migration successful: shift, status, assigned_lot verified.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    migrate()
