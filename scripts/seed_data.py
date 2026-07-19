import os

import pymysql

# Reads MySQL DSN from DATABASE_URL (root:root@tcp(mysql:3306)/nexusguard)
# Falls back to local defaults if not set.
dsn = os.getenv("DATABASE_URL", "root:root@tcp(127.0.0.1:3306)/")

user = "root"
password = "root"
host = "127.0.0.1"
port = 3306

# Parse a DSN like root:root@tcp(host:port)/dbname if provided.
if "@tcp(" in dsn:
    auth, rest = dsn.split("@tcp(", 1)
    user, password = auth.split(":", 1)
    host_port = rest.split(")", 1)[0]
    host, port_str = host_port.split(":")
    port = int(port_str)

conn = pymysql.connect(host=host, port=port, user=user, password=password)
try:
    with conn.cursor() as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS nexusguard")
    conn.commit()
    print("Database 'nexusguard' ensured.")
finally:
    conn.close()

# Connect to the nexusguard database and seed a test device.
conn = pymysql.connect(host=host, port=port, user=user, password=password, database="nexusguard")
try:
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS devices ("
            "id VARCHAR(64) PRIMARY KEY, name VARCHAR(128))"
        )
        cur.execute(
            "INSERT IGNORE INTO devices (id, name) VALUES ('edge-001', 'Test Device')"
        )
    conn.commit()
    print("Data seeded.")
finally:
    conn.close()
