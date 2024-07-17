from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Optional
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Configuration de la connexion à la base de données PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

app = FastAPI()

# Modèle de données pour les soumissions
class EvaluationSubmission:
    def __init__(self, timestamp, id_algo, flag_confirmed, tqc=None, in_process=None, post_fab=None):
        self.timestamp = timestamp
        self.id_algo = id_algo
        self.flag_confirmed = flag_confirmed
        self.tqc = tqc
        self.in_process = in_process
        self.post_fab = post_fab

class EvaluationData:
    def __init__(self, timestamp, id_algo, tqc, q_score, cost_score=None, time_frame_score=None, reliability_score=None, flag_confirmed=None):
        self.timestamp = timestamp
        self.id_algo = id_algo
        self.tqc = tqc
        self.q_score = q_score
        self.cost_score = cost_score
        self.time_frame_score = time_frame_score
        self.reliability_score = reliability_score
        self.flag_confirmed = flag_confirmed

class EvaluationFormData:
    def __init__(self, timestamp, tqc, intervention, intervention_quality):
        self.timestamp = timestamp
        self.tqc = tqc
        self.intervention = intervention
        self.intervention_quality = intervention_quality

class ProdEvaluationData:
    def __init__(self, timestamp, id_algo, tqc, q_score, flag_confirmed, evaluation=None, evaluation_confirmed=False):
        self.timestamp = timestamp
        self.id_algo = id_algo
        self.tqc = tqc
        self.q_score = q_score
        self.flag_confirmed = flag_confirmed
        self.evaluation = evaluation
        self.evaluation_confirmed = evaluation_confirmed

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/test-db-connection")
def test_db_connection():
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return {"message": "Connection to the database was successful"}
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
