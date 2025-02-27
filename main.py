import tkinter as tk
from datetime import datetime 
from tkinter import messagebox
from tkinter import font
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_records.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    dob DATE,
    graduation_date DATE,
    job_status TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS graduation_summaries (
    entry_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    summary_date DATE,
    summary_text TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# Function to add a new student
def add_student():
    name = entry_name.get()
    dob = entry_dob.get()
    graduation_date = entry_graduation_date.get()
    job_status = entry_job_status.get()

    if not (name.replace(" ", "") and dob.replace(" ", "") and graduation_date.replace(" ", "") and job_status.replace(" ", "")):
        messagebox.showinfo("Error", "Please enter missing information")
    else:
        cursor.execute('''
            INSERT INTO students (name, dob, graduation_date, job_status)
            VALUES (?, ?, ?, ?)
        ''', (name.strip(), dob, graduation_date.strip(), job_status.strip()))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()

# Function to add a graduation summary
def add_summary():
    student_id = entry_student_id.get()
    summary_date = entry_summary_date.get()
    summary_text = entry_summary_text.get()

    if not (summary_text.replace(" ", "") and summary_date.replace(" ", "") and student_id.replace(" ", "")):
        messagebox.showinfo("Error", "Please enter missing information")
    else:
        cursor.execute('''
            INSERT INTO graduation_summaries (student_id, summary_date, summary_text)
            VALUES (?, ?, ?)
        ''', (student_id, summary_date, summary_text.strip()))
        conn.commit()
        messagebox.showinfo("Success", "Summary added successfully!")
        clear_fields()

# Clear input fields after submission
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_graduation_date.delete(0, tk.END)
    entry_job_status.delete(0, tk.END)
    entry_student_id.delete(0, tk.END)
    entry_summary_date.delete(0, tk.END)
    entry_summary_text.delete(0, tk.END)

# Function to display student records
def display_students(order_by=None):
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()

    if order_by == "graduation_date":
        rows = sorted(rows, key=lambda x: x[3])  # Sort by graduation_date
    elif order_by == "name":
        rows = sorted(rows, key=lambda x: x[1])  # Sort by name
    
    listbox_students.delete(0, tk.END)  # Clear current listbox
    for row in rows:
        listbox_students.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Graduation: {row[3]} | Job Status: {row[4]}")

# Function to display summaries for the selected student
def display_summaries(event):
    selected_student_index = listbox_students.curselection()
    if selected_student_index:
        selected_student_id = listbox_students.get(selected_student_index).split(" | ")[0].split(": ")[1]  # Extract student ID
        cursor.execute('''
            SELECT * FROM graduation_summaries WHERE student_id = ?
        ''', (selected_student_id,))
        summaries = cursor.fetchall()
        
        listbox_summaries.delete(0, tk.END)  # Clear current summaries listbox
        if summaries:
            for summary in summaries:
                listbox_summaries.insert(tk.END, f"Date: {summary[2]} | {summary[3]}")
        else:
            listbox_summaries.insert(tk.END, "No summaries available for this student.")

# Create main window
current_date = datetime.now()
formatted_time = current_date.strftime("%Y-%m-%d")
root = tk.Tk()
root.title(f"Student Record System | {formatted_time}")

# Labels and input fields for adding students
label_name = tk.Label(root, text="Name:", font="Monserrat")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_dob = tk.Label(root, text="DOB (YYYY-MM-DD):")
label_dob.grid(row=1, column=0, padx=10, pady=5)
entry_dob = tk.Entry(root)
entry_dob.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

label_graduation_date = tk.Label(root, text="Graduation Date (YYYY-MM-DD):")
label_graduation_date.grid(row=2, column=0, padx=10, pady=5)
entry_graduation_date = tk.Entry(root)
entry_graduation_date.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

label_job_status = tk.Label(root, text="Job Status:")
label_job_status.grid(row=3, column=0, padx=10, pady=5)
entry_job_status = tk.Entry(root)
entry_job_status.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

btn_add_student = tk.Button(root, text="Add Student", command=add_student)
btn_add_student.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Labels and input fields for adding graduation summaries
label_student_id = tk.Label(root, text="Student ID:")
label_student_id.grid(row=5, column=0, padx=10, pady=5)
entry_student_id = tk.Entry(root)
entry_student_id.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

label_summary_date = tk.Label(root, text="Summary Date (YYYY-MM-DD):")
label_summary_date.grid(row=6, column=0, padx=10, pady=5)
entry_summary_date = tk.Entry(root)
entry_summary_date.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

label_summary_text = tk.Label(root, text="Summary Text:")
label_summary_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
entry_summary_text = tk.Entry(root)
entry_summary_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

btn_add_summary = tk.Button(root, text="Add Summary", command=add_summary)
btn_add_summary.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Listbox to display students
label_display = tk.Label(root, text="Student Records:")
label_display.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

listbox_students = tk.Listbox(root, height=10, width=80)  # Widened listbox
listbox_students.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

# Buttons to sort students
btn_sort_by_name = tk.Button(root, text="Sort by Name", command=lambda: display_students("name"))
btn_sort_by_name.grid(row=12, column=0, padx=10, pady=5, sticky="ew")

btn_sort_by_graduation = tk.Button(root, text="Sort by Graduation Date", command=lambda: display_students("graduation_date"))
btn_sort_by_graduation.grid(row=12, column=1, padx=10, pady=5, sticky="ew")

# Button to display student records
btn_display = tk.Button(root, text="Show All Students", command=lambda: display_students())
btn_display.grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Listbox to display summaries for the selected student
label_summaries_display = tk.Label(root, text="Graduation Summaries:")
label_summaries_display.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

listbox_summaries = tk.Listbox(root, height=10, width=80)  # Widened listbox
listbox_summaries.grid(row=15, column=0, columnspan=2, padx=10, pady=5)

# Bind listbox click event to display summaries
listbox_students.bind('<<ListboxSelect>>', display_summaries)

# Configure row and column weights to allow for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_rowconfigure(11, weight=1)
root.grid_rowconfigure(12, weight=1)
root.grid_rowconfigure(13, weight=1)
root.grid_rowconfigure(14, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the main loop
root.mainloop()

# Close the connection when done
conn.close()
