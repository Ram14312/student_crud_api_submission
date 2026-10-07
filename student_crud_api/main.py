from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field,EmailStr
import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()

app=FastAPI()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
client = create_client(SUPABASE_URL,SUPABASE_KEY)

class Student(BaseModel):
    name:str
    email:EmailStr
    age:int = Field(ge=18, le=100)
    course:list[str]

@app.post("/students")
def add_Student(student:Student):
    new_student = client.table("students").select("student_id").eq("email",student.email).execute()
    if new_student.data:
        raise HTTPException(
            status_code=409,
            detail= "student is already present"
        )
    response = client.table("students").insert(student.dict()).execute()
    return response.data

@app.get("/students")
def get_students():
    response = client.table("students").select("*").execute()

    if response.data:
        return response.data
    else :
        raise HTTPException(
            status_code=404,
            detail="no student records found"
        ) 


@app.get("/students/{student_id}")
def get_student(student_id):
    response = client.table("students").select("*").eq("student_id",student_id).execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="studnet record not found"
        )
    else:
        return response.data

@app.put("/students/{student_id}")
def update_student_detail(student:Student,student_id:int):
    find_student = client.table("students").select("student_id").eq("student_id",student_id).execute()
    
    if not find_student.data:
        raise HTTPException(
            status_code=404,
            detail="studnet record not found"
        )

    response = client.table("students").update(student.dict()).eq("student_id",student_id).execute() 
    return response.data

@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    response = client.table("students").delete().eq("student_id",student_id).execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="student record not found"
        )
    else :
        return {
            "message": "Student deleted successfully",
            "student": response.data
        }

 