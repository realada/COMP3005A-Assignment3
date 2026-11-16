from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import db

# drops the students table if it already exists then creates it each time this program is run
db.restoreTable()

# FUNCTIONS
# deletes the already existing rows of the treeview
# then inserts each student tuple from the list returned from db.getAllstudents() into the treeview
def draw_table():
    for row in tree.get_children():
        tree.delete(row)
    for student in db.getAllStudents():
        tree.insert("", tk.END, values=student)

# gets the date from the calendar object created using tkcalendar which is in the yyyy-mm-dd format and matches the expected datetime.date() object type
# adds default date drop down object to the date label showing the current date
def show_date():
    selected = calendar.get_date()
    date_label.config(text=f"Selected Date: {selected}")

# gets the selected row from the treeview
# if no row selected, it returns none
# converts the list of values from the row into a tuple
# returns the row
def get_selected_row():
    selected = tree.selection()

    if not selected:
        return

    row = tuple(tree.item(selected[0])['values'])
    print(row)
    return row

# handles closing the connection when the program is exited
# then destroying the window
def on_close():
    db.close()
    window.destroy()

# Gets the first name, last name, email, and enrollment dates from the entries in the form
# Checks if any of the entries are empty, informs the user of the error, then returns
# tries adding a new student to the students table using the info gotten from the entries as arguments
# if the email already exists in the table, it returns the error gotten from db.addStudent() and deletes the text from the entry objects then returns
# Returns an exception if the db.addStudent() operation fails
#redraws the table
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

# gets the selected row tuple and if get_selected_row() returns None a message box pops up informing the user to select a student from the treeview first
# gets the student_id from the tuple and converts to an int
# a simple dialogue box pops with an entry for the new email
# Returns if user clicks cancel instead of OK
# checks if the new_email entry was empty and shows a message box informing the user the email can't be empty
# A message box pops up asking the user if they want to go ahead with the update_email() operation and returns if no
# tries the db.updateStudentEmail() function using the student_id and new_email arguments
# gives an error if the email already exists
# informs the user if the db.updateStudentEmail() function fails then returns
# redraws the table
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


# gets the selected row tuple and if get_selected_row() returns None a message box pops up informing the user to select a student from the treeview first
# gets the student_id from the tuple and converts to an int
# message box pops up asking the user if they want to go ahead with the delete operation
# tries to delete the student with db.deleteStudent() using the student_id as an argument
# a message box pops up telling the user if the operation fails
# if deleted returns false, informs the user the student no longer exists
# redraws the table
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
window.title("Students Database")
window.config(padx=50, pady=50)

## Table View
table_title = tk.Label(text="STUDENTS", font=("Arial", 20))
table_title.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Handles drawing the treeview on the window
columns = ("student_id", "first_name", "last_name", "email", "enrollment_date")
tree = ttk.Treeview(window, columns=columns, show="headings")

tree.heading("student_id", text="Student ID")
tree.heading("first_name", text="First name")
tree.heading("last_name", text="Last name")
tree.heading("email", text="Email")
tree.heading("enrollment_date", text="Enrollment date")
tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

draw_table()

## Add new Student form
fname_label = tk.Label(text="First name")
fname_label.grid(row=2, column=0, sticky="e", pady=2)
fname_entry = tk.Entry(width=25)
fname_entry.grid(row=2, column=1, sticky="w")

lname_label = tk.Label(text="Last name")
lname_label.grid(row=3, column=0, sticky="e", pady=2)
lname_entry = tk.Entry(width=25)
lname_entry.grid(row=3, column=1, sticky="w")

email_label = tk.Label(text="Email:")
email_label.grid(row=4, column=0, sticky="e", pady=2)
email_entry = tk.Entry(width=25)
email_entry.grid(row=4, column=1, sticky="w")

date_label = tk.Label(text="Enrollment date:")
date_label.grid(row=5, column=0, sticky="e", pady=2)

calendar = DateEntry(width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
calendar.grid(row=5, column=1, sticky="w")

# Buttons
button_frame = tk.Frame(window)
button_frame.grid(row=6, column=0, columnspan=2, pady=10)

add_student_button = tk.Button(button_frame, text="Add student", command=add_student, width=20)
add_student_button.grid(row=0, column=0, padx=2)

update_email_button = tk.Button(button_frame, text="Update email", command=update_email, width=20)
update_email_button.grid(row=0, column=1, padx=2)

delete_student_button = tk.Button(button_frame, text="Delete student", command=delete_student, width=20)
delete_student_button.grid(row=0, column=2, padx=2)

# Protocol for when the window is exited which calls on_close() command
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()