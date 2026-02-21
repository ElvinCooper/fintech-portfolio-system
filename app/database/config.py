import os

import oracledb
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
ORACLE_PWD = os.getenv("ORACLE_PWD")


def conectar_db():
    try:
        user = os.getenv("DB_USER", "system")
        password = os.getenv("ORACLE_PWD")
        host = "db"
        port = "1521"
        service_name = "XE"

        # conexion
        connection = oracledb.connect(user=user, password=password, dsn=f"{host}:{port}/{service_name}")

        print("Connecion establecidad")
        return connection

    except Exception as e:
        print(f" Error al conectar {e}")
        return None
