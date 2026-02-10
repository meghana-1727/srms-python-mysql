# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:06:02 2026

@author: Meghana
"""

import mysql.connector

ADMIN_PASS = "admin123"

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Meghana@1703",
        database="student_system"
    )

# ---------------- STUDENT FUNCTIONS ----------------

def student_login():
    roll = int(input("Enter Roll Number: "))
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    student = cur.fetchone()

    if not student:
        print("Student not found")
        return

    print(f"\nWelcome, {student['name']}")
    print(f"Roll: {student['roll']}, Branch: {student['branch']}, CGPA: {student['cgpa']}")
    student_menu(roll)

    cur.close()
    conn.close()

def student_menu(roll):
    while True:
        print("\n1. Raise Correction Ticket")
        print("2. View Ticket Status")
        print("3. Logout")
        ch = input("Enter choice: ")

        if ch == "1":
            raise_ticket(roll)
        elif ch == "2":
            view_ticket_status(roll)
        elif ch == "3":
            break
        else:
            print("Invalid choice")

def raise_ticket(roll):
    field = input("Enter field to correct (name/branch/year/cgpa/phone): ")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    student = cur.fetchone()

    if field not in student:
        print("Invalid field")
        return

    old_val = str(student[field])
    print("Current Value:", old_val)
    new_val = input("Enter new value: ")

    cur.execute("""
        INSERT INTO tickets (roll, field_name, old_value, new_value, status)
        VALUES (%s, %s, %s, %s, 'Pending')
    """, (roll, field, old_val, new_val))

    conn.commit()
    print("Ticket submitted successfully")

    cur.close()
    conn.close()

def view_ticket_status(roll):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM tickets WHERE roll=%s", (roll,))
    tickets = cur.fetchall()

    if not tickets:
        print("No tickets found")
    else:
        for t in tickets:
            print(f"ID:{t['ticket_id']} | Field:{t['field_name']} | {t['old_value']} -> {t['new_value']} | Status:{t['status']}")

    cur.close()
    conn.close()

# ---------------- ADMIN FUNCTIONS ----------------

def admin_login():
    pwd = input("Enter Admin Password: ")
    if pwd == ADMIN_PASS:
        print("Login successful")
        admin_menu()
    else:
        print("Incorrect password")

def admin_menu():
    while True:
        print("\n1. Add Student")
        print("2. View All Students")
        print("3. Process Tickets")
        print("4. Logout")
        ch = input("Enter choice: ")

        if ch == "1":
            add_student()
        elif ch == "2":
            view_students()
        elif ch == "3":
            process_tickets()
        elif ch == "4":
            break
        else:
            print("Invalid choice")

def add_student():
    roll = int(input("Roll: "))
    name = input("Name: ")
    branch = input("Branch: ")
    year = int(input("Year: "))
    cgpa = float(input("CGPA: "))
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s)
    """, (roll, name, branch, year, cgpa, phone))

    conn.commit()
    print("Student added successfully")

    cur.close()
    conn.close()

def view_students():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    for s in rows:
        print(s)

    cur.close()
    conn.close()

def process_tickets():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM tickets WHERE status='Pending'")
    tickets = cur.fetchall()

    if not tickets:
        print("No pending tickets")
        return

    for t in tickets:
        print("\n--------------------")
        print("Ticket ID:", t['ticket_id'])
        print("Roll:", t['roll'])
        print("Field:", t['field_name'])
        print("Old:", t['old_value'])
        print("New:", t['new_value'])

        action = input("Approve (A) / Reject (R) / Skip (S): ").lower()

        if action == "a":
            cur.execute(f"""
                UPDATE students SET {t['field_name']}=%s WHERE roll=%s
            """, (t['new_value'], t['roll']))

            cur.execute("UPDATE tickets SET status='Approved' WHERE ticket_id=%s", (t['ticket_id'],))
            conn.commit()
            print("Ticket approved and record updated")

        elif action == "r":
            cur.execute("UPDATE tickets SET status='Rejected' WHERE ticket_id=%s", (t['ticket_id'],))
            conn.commit()
            print("Ticket rejected")

    cur.close()
    conn.close()

# ---------------- MAIN ----------------

def main():
    while True:
        print("\nSTUDENT RECORD MANAGEMENT SYSTEM")
        print("1. Student Login")
        print("2. Admin Login")
        print("3. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            student_login()
        elif ch == "2":
            admin_login()
        elif ch == "3":
            print("Goodbye")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
