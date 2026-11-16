import db

students = db.get_all_students()

for student in students:
    print(student)

db.close()