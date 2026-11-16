import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import errors
from pathlib import Path
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

def restoreTable() -> None:
    sql = (Path(__file__).parent.parent / "students.sql").read_text()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    except Exception:
        conn.rollback()
        raise

# getAllStudents(): Retrieves and displays all records from the students table.
def getAllStudents() -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY student_id")
        rows = cur.fetchall()
    conn.rollback()
    return rows

# addStudent(first_name, last_name, email, enrollment_date): Inserts a new student record into the students table.
def addStudent(first_name: str, last_name: str, email: str, enrollment_date: date | None = None) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s);",
                (first_name, last_name, email, enrollment_date)
                )
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
        raise ValueError("The student already exists")
    except Exception:
        conn.rollback()
        raise

# updateStudentEmail(student_id, new_email): Updates the email address for a student with the specified student_id.
def updateStudentEmail(student_id: int, new_email: str) -> bool:
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students "
                "SET email = %s "
                "WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount > 0
        conn.commit()
        return updated
    except errors.UniqueViolation:
        conn.rollback()
        raise ValueError("That email is already in use.")
    except Exception:
        conn.rollback()
        raise

# deleteStudent(student_id): Deletes the record of the student with the specified student_id.
def deleteStudent(student_id: int) -> bool:
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students "
                "WHERE student_id = %s;",
                (student_id,),
            )
            deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    except Exception:
        conn.rollback()
        raise

def close():
    conn.close()