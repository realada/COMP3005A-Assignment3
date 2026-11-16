from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import db

db.restoreTable()

#Every time user added, table is redrawn (ie db.getAllUsers() called)
#message box when email updated or to ask if user should be student is deleted

# FUNCTIONS
def draw_table():
    for row in tree.get_children():
        tree.delete(row)
    for student in db.getAllStudents():
        tree.insert("", tk.END, values=student)

def show_date():
    selected = calendar.get_date()
    date_label.config(text=f"Selected Date: {selected}")

def get_selected_row():
    selected = tree.selection()

    if not selected:
        return

    row = tuple(tree.item(selected[0])['values'])
    print(row)
    return row

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
    except ValueError as e:
        messagebox.showerror("Duplicate user", str(e))
        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        return
    except Exception as e:
        messagebox.showerror("Could not add student", str(e))
        return

    fname_entry.delete(0, tk.END)
    lname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    draw_table()

def update_email():
    row = get_selected_row()
    if row is None:
        messagebox.showinfo("No selection", "Please select a student first.")
        return


    student_id = int(row[0])
    new_email = simpledialog.askstring(
        "Update email",
        f"New email for {row[1]} {row[2]}",
        initialvalue=row[3],
        parent=window,
    )

    if new_email is None:
        return
    new_email = new_email.strip()
    if not new_email:
        messagebox.showinfo("Missing email", "Email can't be empty.")
        return

    if not messagebox.askyesno("Confirm", f"Change email {row[3]} with {new_email}?"):
        return

    try:
        updated = db.updateStudentEmail(student_id=student_id, new_email=new_email)
    except ValueError as e:
        messagebox.showerror("Duplicate email", str(e))
        email_entry.delete(0, tk.END)
        return
    except Exception as e:
        messagebox.showerror("Could not update email", str(e))
        return

    if not updated:
        messagebox.showinfo("Not found", "That student does not exist.")

    email_entry.delete(0, tk.END)
    draw_table()

def delete_student():
    row = get_selected_row()
    if row is None:
        messagebox.showinfo("No selection", "Please select a student first.")
        return
    
    student_id = int(row[0])
    if not messagebox.askyesno("Confirm", f"Delete student {row[1]}?"):
        return
    try:
        deleted = db.deleteStudent(student_id=student_id)
    except Exception as e:
        messagebox.showerror("Could not delete", str(e))
        return

    if not deleted:
        messagebox.showinfo("Not found", "That student no longer exists.")
    
    draw_table()




# App GUI
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
email_entry = tk.Entry(width=25)
email_entry.grid(row=3, column=1, sticky="w")

date_label = tk.Label(text="Enrollment date:")
date_label.grid(row=4, column=0, sticky="e", pady=2)

calendar = DateEntry(width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
calendar.grid(row=4, column=1, sticky="w")

add_student_button = tk.Button(text="Add student", command=add_student)
add_student_button.grid(row=5, column=0, pady=5)

update_email_button = tk.Button(text="Update email", command=update_email)
update_email_button.grid(row=5, column=1, pady=5)

delete_student_button = tk.Button(text="Delete student", command=delete_student)
delete_student_button.grid(row=5, column=2, pady=5)


window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()