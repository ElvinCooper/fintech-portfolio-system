from app.database.config import conectar_db


def test_connection():
    conn = conectar_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                sql = "SELECT 1 FROM DUAL"
                cursor.execute(sql)

                print("\n--- Prueba de conexion ---")
                print(cursor.fetchall())
                # for row in cursor:
                #     print(f"ID: {row[0]} | Nombre: {row[1]} | Email: {row[2]}")
        finally:
            conn.close()


if __name__ == "__main__":
    test_connection()