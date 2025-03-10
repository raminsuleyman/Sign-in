import sqlite3

from hashing import hash_password


def register():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists.")

    conn.close()

def login():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()

    if user:
        print("Login successful! Welcome,", username)
    else:
        print("Invalid username or password.")

    conn.close()

def forgot_password():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    username = input("Enter your username: ")

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        new_password = input("Enter your new password: ")
        hashed_new_password = hash_password(new_password)

        # Update password in database
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()

        print("Password reset successful!")
    else:
        print("Username not found.")

    conn.close()
