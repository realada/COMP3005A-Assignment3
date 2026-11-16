from datetime import date
import db

db.restoreTable()
db.addStudent("Test", "One", "testone@gmail.com", date(2026, 11, 15))

students = db.getAllStudents()
for student in students:
    print(student)

db.close()