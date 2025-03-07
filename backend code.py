from fastapi import FastAPI, Depends, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
from celery import Celery

# FastAPI App
app = FastAPI()

# Database Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["smart_agenda"]
users_collection = db["users"]
tasks_collection = db["tasks"]

# Security (Password Hashing & JWT)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Celery (For Notifications)
celery = Celery("tasks", broker="redis://localhost:6379/0")

# Models
class UserCreate(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: str
    priority: int  # 1 = High, 2 = Medium, 3 = Low
    estimated_time: int  # Minutes

class TaskResponse(TaskCreate):
    id: str

class TokenData(BaseModel):
    username: str

# Utility Functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Speech-to-Text Task Input
@app.post("/add_task_voice/")
def add_task_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a task...")
        audio = recognizer.listen(source)
    try:
        task_text = recognizer.recognize_google(audio)
        return {"task": task_text}
    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}
    except sr.RequestError:
        return {"error": "Speech recognition service unavailable"}

# AI Task Prioritization
@app.get("/prioritize_tasks/")
def prioritize_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0, "priority": 1, "estimated_time": 1}))
    df = pd.DataFrame(tasks)
    df = df.sort_values(by=["priority", "estimated_time"], ascending=[True, True])
    return df.to_dict(orient="records")

# Schedule Notifications
@celery.task
def send_notification(task_id: str):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        print(f"Reminder: Your task '{task['title']}' is due soon!")

@app.post("/schedule_notification/{task_id}")
def schedule_notification(task_id: str):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    celery.send_task("send_notification", args=[task_id], countdown=60)  # Sends reminder in 1 min
    return {"message": "Notification scheduled"}

# Productivity Analytics
@app.get("/analytics/")
def analytics():
    tasks = list(tasks_collection.find({}, {"_id": 0, "estimated_time": 1}))
    df = pd.DataFrame(tasks)
    plt.hist(df["estimated_time"], bins=5)
    plt.title("Time Spent on Tasks")
    plt.savefig("analytics.png")
    return {"message": "Analytics saved as 'analytics.png'"}

# User Authentication
@app.post("/register/")
def register(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    users_collection.insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user: UserCreate):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/add_task/", response_model=TaskResponse)
def add_task(task: TaskCreate):
    task_data = task.dict()
    task_data["created_at"] = datetime.utcnow()
    result = tasks_collection.insert_one(task_data)
    task_data["id"] = str(result.inserted_id)
    return task_data

@app.get("/tasks/")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 1, "title": 1, "description": 1, "deadline": 1, "priority": 1}))
    for task in tasks:
        task["id"] = str(task["_id"])
        del task["_id"]


## this is code that turns speech into text that the LLM model can use to create schedules

#this was cut to speech.py

