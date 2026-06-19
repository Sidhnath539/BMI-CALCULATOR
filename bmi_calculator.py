import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()


# ---------------- BMI FUNCTIONS ---------------- #

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmi():
    try:
        name = name_entry.get()

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        bmi = weight / (height ** 2)
        category = bmi_category(bmi)

        bmi_result.set(f"{bmi:.2f}")
        category_result.set(category)

        cursor.execute("""
        INSERT INTO bmi_data(name, weight, height, bmi, category, date)
        VALUES(?,?,?,?,?,?)
        """,
                       (
                           name,
                           weight,
                           height,
                           bmi,
                           category,
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "BMI Calculated and Saved Successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid values."
        )


# ---------------- HISTORY ---------------- #

def show_history():

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("900x400")

    tree = ttk.Treeview(
        history_window,
        columns=("ID","Name","Weight","Height",
                 "BMI","Category","Date"),
        show="headings"
    )

    columns = [
        "ID",
        "Name",
        "Weight",
        "Height",
        "BMI",
        "Category",
        "Date"
    ]

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM bmi_data")

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)


# ---------------- GRAPH ---------------- #

def show_graph():

    cursor.execute("""
    SELECT date,bmi FROM bmi_data
    ORDER BY id
    """)

    records = cursor.fetchall()

    if len(records) == 0:
        messagebox.showwarning(
            "No Data",
            "No records found."
        )
        return

    dates = [row[0] for row in records]
    bmi_values = [row[1] for row in records]

    plt.figure(figsize=(10,5))
    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.title("BMI Trend Analysis")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ---------------- STATISTICS ---------------- #

def show_statistics():

    cursor.execute("""
    SELECT AVG(bmi),
           MAX(bmi),
           MIN(bmi)
    FROM bmi_data
    """)

    result = cursor.fetchone()

    if result[0] is None:
        messagebox.showwarning(
            "No Data",
            "No records available."
        )
        return

    avg_bmi = result[0]
    max_bmi = result[1]
    min_bmi = result[2]

    messagebox.showinfo(
        "BMI Statistics",
        f"""
Average BMI : {avg_bmi:.2f}

Highest BMI : {max_bmi:.2f}

Lowest BMI : {min_bmi:.2f}
"""
    )


# ---------------- SEARCH USER ---------------- #

def search_user():

    user = search_entry.get()

    cursor.execute("""
    SELECT * FROM bmi_data
    WHERE name=?
    """, (user,))

    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo(
            "Not Found",
            "No records found."
        )
        return

    result_window = tk.Toplevel(root)
    result_window.title("User History")

    tree = ttk.Treeview(
        result_window,
        columns=("ID","Name","Weight","Height",
                 "BMI","Category","Date"),
        show="headings"
    )

    columns = [
        "ID",
        "Name",
        "Weight",
        "Height",
        "BMI",
        "Category",
        "Date"
    ]

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    for row in rows:
        tree.insert("", tk.END, values=row)


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("600x600")
root.configure(bg="sky blue")

title = tk.Label(
    root,
    text="Advanced BMI Calculator",
    font=("Arial",20,"bold"),
    bg="#f4f4f4"
)

title.pack(pady=10)

# Name

tk.Label(
    root,
    text="Name",
    font=("Arial",12),
    bg="#f4f4f4"
).pack()

name_entry = tk.Entry(
    root,
    font=("Arial",12)
)

name_entry.pack(pady=5)

# Weight

tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial",12),
    bg="#f4f4f4"
).pack()

weight_entry = tk.Entry(
    root,
    font=("Arial",12)
)

weight_entry.pack(pady=5)

# Height

tk.Label(
    root,
    text="Height (m)",
    font=("Arial",12),
    bg="#f4f4f4"
).pack()

height_entry = tk.Entry(
    root,
    font=("Arial",12)
)

height_entry.pack(pady=5)

# Result Variables

bmi_result = tk.StringVar()
category_result = tk.StringVar()

# Calculate Button

tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="green",
    fg="white",
    font=("Arial",12)
).pack(pady=10)

# BMI Result

tk.Label(
    root,
    text="BMI",
    font=("Arial",12),
    bg="#f4f4f4"
).pack()

tk.Label(
    root,
    textvariable=bmi_result,
    font=("Arial",14,"bold"),
    bg="#f4f4f4"
).pack()

# Category

tk.Label(
    root,
    text="Category",
    font=("Arial",12),
    bg="#f4f4f4"
).pack()

tk.Label(
    root,
    textvariable=category_result,
    font=("Arial",14,"bold"),
    bg="#f4f4f4"
).pack()

# Search User

tk.Label(
    root,
    text="Search User",
    font=("Arial",12),
    bg="#f4f4f4"
).pack(pady=10)

search_entry = tk.Entry(
    root,
    font=("Arial",12)
)

search_entry.pack()

tk.Button(
    root,
    text="Search History",
    command=search_user,
    bg="blue",
    fg="white"
).pack(pady=5)

# History Button

tk.Button(
    root,
    text="View All History",
    command=show_history,
    bg="orange",
    fg="white",
    font=("Arial",12)
).pack(pady=10)

# Graph Button

tk.Button(
    root,
    text="BMI Trend Graph",
    command=show_graph,
    bg="purple",
    fg="white",
    font=("Arial",12)
).pack(pady=10)

# Statistics Button

tk.Button(
    root,
    text="Statistics",
    command=show_statistics,
    bg="brown",
    fg="white",
    font=("Arial",12)
).pack(pady=10)

root.mainloop()

conn.close()