import csv
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt # type: ignore


def create_file():
    if not os.path.exists("expense.csv"):
        with open("expense.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "amount", "description"])



def add(date, category, amount, description):
    with open("expense.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

def view():
    expense = []
    with open("expense.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = int(row["amount"])
            expense.append(row)
    return expense


# GUI function
def add_GUI():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "All fields except description are required")
        return

    try:
        amount = int(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for amount")
        return

    add(date, category, amount, description)

    messagebox.showinfo("Success", "Expense has been added")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)


def month():
    data = view()

    if len(data) == 0:
        messagebox.showwarning("No Data", "No expenses found")
        return

    month = month_entry.get()  
    total = 0
    count = 0

    for item in data:
        if item["date"].startswith(month):
            total += item["amount"]
            count += 1

    if count == 0:
        messagebox.showinfo("Result", f"No expenses found for {month}")
    else:
        avg = total / count
        messagebox.showinfo(
            "Monthly Summary",
            f"Month: {month}\nTotal: ₹{total}\nTransactions: {count}\nAverage: ₹{avg:.2f}"
        )


def highest():
    data = view()

    if len(data) == 0:
        messagebox.showwarning("No Data", "No expenses found")
        return

    category_totals = {}

    for item in data:
        category = item["category"]
        amount = item["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    max_category = max(category_totals, key=category_totals.get)
    max_amount = category_totals[max_category]

    messagebox.showinfo(
        "Highest Spending",
        f"Category: {max_category}\nAmount: ₹{max_amount}"
    )


# Pie chart
def pie_chart():
    data = view()

    if len(data) == 0:
        messagebox.showwarning("No Data", "No expenses to show")
        return

    category_totals = {}

    for item in data:
        category = item["category"]
        amount = item["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    
    def format_label(pct):
        total = sum(values)
        amount = int((pct / 100) * total)
        return f"{pct:.1f}% (₹{amount})"

    plt.pie(values, labels=labels, autopct=format_label)
    plt.title("Expense Distribution by Category")
    plt.show()



root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Enter Month (YYYY-MM)").pack()
month_entry = tk.Entry(root)
month_entry.pack()


tk.Button(root, text="Add Expense", command=add_GUI).pack(pady=10)   
tk.Button(root, text="Show Chart", command=pie_chart).pack(pady=10)  
tk.Button(root, text="Monthly Summary", command=month).pack(pady=10)
tk.Button(root, text="Highest Spending Category", command=highest).pack(pady=10)

# Start
create_file()
root.mainloop()