import psycopg2
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

app = FastAPI()
origins= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Connexion
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    cursor_factory=RealDictCursor
)

@app.get('/') # Le frontend appelle /api/
async def get_students_data():
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, specialite, annee FROM students;")
    students = cursor.fetchall()
    cursor.close()
    
    return {"students": students, "message": "Étape 2 complétée : données des étudiants chargées."}



