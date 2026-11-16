import os
from dotenv import load_dotenv
import psycopg2
from datetime import date

load_dotenv()



def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "assignment3"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )

conn = get_connection()

# getAllStudents(): Retrieves and displays all records from the students table.
def get_all_students() -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
    conn.rollback()
    return rows

# addStudent(first_name, last_name, email, enrollment_date): Inserts a new student record into the students table.
def addStudent(first_name: str, last_name: str, email: str, enrollment_date: date | None = None) -> None:
    pass
# updateStudentEmail(student_id, new_email): Updates the email address for a student with the specified student_id.
def updateStudentEmail(student_id: int, new_email: str) -> None:
    pass

# deleteStudent(student_id): Deletes the record of the student with the specified student_id.
def deleteStudent(student_id: int):
    pass

def close():
    conn.close()