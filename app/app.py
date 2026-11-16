from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import db

db.restoreTable()

#Every time user added, table is redrawn (ie db.getAllUsers() called)
def draw_table():
    for row in tree.get_children():
        tree.delete(row)
    for student in db.getAllStudents():
        tree.insert("", tk.END, values=student)

def show_date():
    selected = calendar.get_date()
    date_label.config(text=f"Selected Date: {selected}")

# def get_selected_row():
#     selected = tree.focus()
#     if selected:
#         row = tree.item(selected)
#message box when email updated or when a student is deleted
def on_close():
    db.close()
    window.destroy()

def add_student():
    first_name = fname_entry.get().strip()
    last_name = lname_entry.get().strip()
    email = email_entry.get().strip()
    enrollment_date = calendar.get_date()
    if not (first_name and last_name and email):
        messagebox.showerror("Missing info", "Ensure all fields are filled out.")
        return
    try: 
        db.addStudent(first_name=first_name, last_name=last_name, email=email, enrollment_date=enrollment_date)
    except Exception as e:
        messagebox.showerror("Could not add student", str(e))
        return

    fname_entry.delete(0, tk.END)
    lname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    draw_table()

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
tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

draw_table()

#Add new Student form
fname_label = tk.Label(text="First name")
fname_label.grid(row=1, column=0, sticky="e", pady=2)
fname_entry = tk.Entry(width=25)
fname_entry.grid(row=1, column=1, sticky="w")

lname_label = tk.Label(text="Last name")
lname_label.grid(row=2, column=0, sticky="e", pady=2)
lname_entry = tk.Entry(width=25)
lname_entry.grid(row=2, column=1, sticky="w")

email_label = tk.Label(text="Email:")
email_label.grid(row=3, column=0, sticky="e", pady=2)
email_entry = tk.Entry(width=21)
email_entry.grid(row=3, column=1, sticky="w")

date_label = tk.Label(text="Enrollment date:")
date_label.grid(row=4, column=0, sticky="e", pady=2)

calendar = DateEntry(width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
calendar.grid(row=4, column=1, sticky="w")

add_button = tk.Button(text="Add student", command=add_student)
add_button.grid(row=5, column=0, pady=10)

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()