import psycopg2
conn = psycopg2.connect("postgresql://postgres.iyubjrklyrrjjdbnblmg:cA8JXoabgcJuYDWc@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres")
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(100) UNIQUE;")
    cur.execute("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP;")
    conn.commit()
    print("Database columns added successfully.")
except Exception as e:
    print("Error or already exists:", e)
cur.close()
conn.close()
