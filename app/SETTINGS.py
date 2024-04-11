from os import environ as env

JWT_KEY = "test"
USER_APP_IP = "http://127.0.0.1:8001"
CELLS_APP_IP = "http://192.168.0.113:8000/cells"
KEYS = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOSTNAME", "POSTGRES_DB"]
USER, PASSWORD, HOSTNAME, DATABASE = (env.get(i, "test") for i in KEYS)
# SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}'
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
