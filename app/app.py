from datetime import date
import tkinter as tk
from tkinter import ttk
import db

db.restoreTable()

#Every time user added, table is redrawn (ie db.getAllUsers() called)
def draw_table():
    students = db.getAllStudents()
    for student in students:
        tree.insert("", tk.END, values=student)
    tree.pack(fill="both", expand=True)

# def get_selected_row():
#     selected = tree.focus()
#     if selected:
#         row = tree.item(selected)
#message box when email updated or when a student is deleted
def add_student():
    #tree.insert()
    pass

window = tk.Tk()
window.title("")
window.config(padx=50, pady=50)

columns = ("student_id", "first_name", "last_name", "email", "enrollment_date")
tree = ttk.Treeview(window, columns=columns, show="headings")

tree.heading("student_id", text="Student id")
tree.heading("first_name", text="First name")
tree.heading("last_name", text="Last name")
tree.heading("email", text="Email")
tree.heading("enrollment_date", text="Enrollment date")

draw_table()

#Add new Student
# new_student_label = tk.Label(text="Student Full Name:")
# new_student_entry = tk.Entry(width=21)



window.mainloop()

db.close()