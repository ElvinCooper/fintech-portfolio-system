import re

import oracledb

user = "system"
password = "Myoraclesecret"
dsn = "localhost:1522/XEPDB1"

conn = oracledb.connect(user=user, password=password, dsn=dsn)
cursor = conn.cursor()

with open("missing_parts.sql", encoding="utf-8") as f:
    sql_script = f.read()

statements = re.split(r"^\s*/\s*$", sql_script, flags=re.MULTILINE)

for stmt in statements:
    stmt = stmt.strip()
    if stmt:
        print("Ejecutando bloque...")
        try:
            cursor.execute(stmt)
            print("Éxito.")
        except Exception as e:
            print(f"Error: {e}")

conn.commit()
cursor.close()
conn.close()
print("Terminado.")
