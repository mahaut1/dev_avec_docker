import os
import time
import psycopg2
import redis
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "toto")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ynovdocker")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

db_conn = None
redis_client = None


def connect_with_retry():
    global db_conn, redis_client

    # Postgres
    while True:
        try:
            db_conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                dbname=POSTGRES_DB,
                cursor_factory=RealDictCursor,
            )
            break
        except Exception:
            time.sleep(1)

    # Redis
    while True:
        try:
            redis_client = redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, decode_responses=True
            )
            redis_client.ping()
            break
        except Exception:
            time.sleep(1)


@app.on_event("startup")
def startup():
    connect_with_retry()


@app.get("/")
def get_students():
    """
    Étape 3 :
    - SELECT Postgres
    - compteur Redis atomique
    - réponse attendue par le frontend
    """
    views = redis_client.incr("dashboard:views")

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT nom, promo FROM students ORDER BY id;")
        students = cursor.fetchall()

    return [
        {
            "nom": s["nom"],
            "promo": s["promo"],
            "views": views
        }
        for s in students
    ]
