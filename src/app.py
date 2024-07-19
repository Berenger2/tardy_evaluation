from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from datetime import datetime
from typing import Optional
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

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

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
# Modèle de données pour les soumissions
class FlagEvaluation(BaseModel):
    timestamp: datetime
    id_algo: str
    flag_confirmed: bool
    tqc: Optional[str] = None
    in_process: Optional[bool] = None
    post_fab: Optional[bool] = None

class AlgoEvaluation(BaseModel):
    timestamp: datetime
    id_algo: str
    tqc: str
    q_score: float
    cost_score: Optional[float] = None
    time_frame_score: Optional[float] = None
    reliability_score: Optional[float] = None
    flag_confirmed: Optional[bool] = None

class FormEvaluation(BaseModel):
    timestamp: datetime
    tqc: str
    intervention: str
    intervention_quality: str

class ProdEvaluation(BaseModel):
    timestamp: datetime
    id_algo: str
    tqc: str
    q_score: float
    flag_confirmed: bool
    evaluation: Optional[str] = None
    evaluation_confirmed: Optional[bool] = False
    intervention_level: str
    intervention_score: float
    

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

@app.post("/flag_evaluation")
def submit_flag_evaluation(submission: FlagEvaluation):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO flagevaluation (timestamp, idAlgo, flagConfirmed, tqc, inProcess, postFab)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (submission.timestamp, submission.id_algo, submission.flag_confirmed, submission.tqc, submission.in_process, submission.post_fab))
        conn.commit()
        return {"message": "Evaluation submission saved successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()



@app.post("/formevaluation")
def submit_form_evaluation(form_data: FormEvaluation):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO evaluationformdata (timestamp, tqc, intervention, interventionQuality)
            VALUES (%s, %s, %s, %s)
        """, (form_data.timestamp, form_data.tqc, form_data.intervention, form_data.intervention_quality))
        conn.commit()
        return {"message": "Evaluation form data saved successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
        
        
@app.post("/algoevaluation")
def submit_algo_evaluation(submission_data: AlgoEvaluation):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO algoevaluation (timestamp, idAlgo, tqc, qScore, costScore, timeFrameScore, reliabilityScore, flagConfirmed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (submission_data.timestamp, submission_data.id_algo, submission_data.tqc, submission_data.q_score, submission_data.cost_score, submission_data.time_frame_score, submission_data.reliability_score, submission_data.flag_confirmed))
        conn.commit()
        return {"message": "Evaluation data saved successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()



@app.post("/prodevaluation")
def submit_prod_evaluation(submission_data: ProdEvaluation):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO prodevaluationdata (timestamp, idAlgo, tqc, qScore, flagConfirmed, evaluation, evaluationConfirmed,interventionLevel,interventionScore)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (submission_data.timestamp, submission_data.id_algo, submission_data.tqc, submission_data.q_score, submission_data.flag_confirmed, submission_data.evaluation, submission_data.evaluation_confirmed, submission_data.intervention_level, submission_data.intervention_score))
        conn.commit()
        return {"message": "Prod evaluation data saved successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()