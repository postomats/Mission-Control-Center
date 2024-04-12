from os import environ as env

DEFAULT_KEY = 'test'

JWT_KEY = env.get('JWT_KEY', DEFAULT_KEY)

USER_APP_IP = env.get("CENSUS_HOST", default='localhost:8001')
USER_APP_IP = f'http://{USER_APP_IP}'

POSTOMAT_IP = env.get('POSTOMAT_IP', default="192.168.0.113:8000")
CELLS_APP_IP = f'http://{POSTOMAT_IP}/cells'
print(CELLS_APP_IP)
KEYS = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOSTNAME", "POSTGRES_DB"]
USER, PASSWORD, HOSTNAME, DATABASE = (env.get(i, DEFAULT_KEY) for i in KEYS)
SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}'
#SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
