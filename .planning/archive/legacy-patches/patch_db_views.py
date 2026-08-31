import psycopg2

# I will parse the connection string from update_schema.py to ensure it is correct.
with open('/Users/sahiltaware415/expadvisor-backend/update_schema.py', 'r') as f:
    schema_code = f.read()

import re
match = re.search(r'conn\s*=\s*psycopg2\.connect\("([^"]+)"\)', schema_code)
if match:
    conn_str = match.group(1)
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE experiences ADD COLUMN views INTEGER DEFAULT 0;")
        conn.commit()
        print("Views column added to experiences table successfully.")
    except Exception as e:
        print("Error or already exists:", e)
    cur.close()
    conn.close()
else:
    print("Could not find connection string in update_schema.py")
