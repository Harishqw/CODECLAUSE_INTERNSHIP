import tkinter as tk
import smtplib
from email.message import EmailMessage
import sqlite3

# Initialize Tkinter application
app = tk.Tk()
app.title("Mail Application")

# Database setup
conn = sqlite3.connect('mail_app.db')
c = conn.cursor()

# Create table for storing user configurations
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, smtp_server TEXT, smtp_port INTEGER)''')
conn.commit()

# Function to send email
def send_email():
    sender_email = username_entry.get()
    recipient_email = recipient_entry.get()
    subject = subject_entry.get()
    message_body = message_text.get("1.0", tk.END)

    smtp_server = smtp_server_entry.get()
    smtp_port = int(smtp_port_entry.get())
    smtp_username = username_entry.get()
    smtp_password = password_entry.get()

    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            record_email(sender_email, recipient_email, subject)
            status_label.config(text="Email sent successfully!", fg="green")
    except Exception as e:
        status_label.config(text="Error: " + str(e), fg="red")

# Function to record sent email in the database
def record_email(sender, recipient, subject):
    c.execute("INSERT INTO sent_emails (sender, recipient, subject) VALUES (?, ?, ?)", (sender, recipient, subject))
    conn.commit()

# Function to create a new user
def create_user():
    username = new_username_entry.get()
    password = new_password_entry.get()
    smtp_server = smtp_server_entry.get()
    smtp_port = int(smtp_port_entry.get())

    c.execute("INSERT INTO users (username, password, smtp_server, smtp_port) VALUES (?, ?, ?, ?)",
              (username, password, smtp_server, smtp_port))
    conn.commit()

# Function to login
def login():
    username = username_entry.get()
    password = password_entry.get()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        status_label.config(text="Login successful!", fg="green")
        # Additional actions after login (e.g., enable email sending)
    else:
        status_label.config(text="Invalid username or password", fg="red")

# GUI elements
# Login
username_label = tk.Label(app, text="Username:")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(app)
username_entry.grid(row=0, column=1)

password_label = tk.Label(app, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(app, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(app, text="Login", command=login)
login_button.grid(row=2, column=0)

# New User Creation
new_username_label = tk.Label(app, text="New Username:")
new_username_label.grid(row=3, column=0)
new_username_entry = tk.Entry(app)
new_username_entry.grid(row=3, column=1)

new_password_label = tk.Label(app, text="New Password:")
new_password_label.grid(row=4, column=0)
new_password_entry = tk.Entry(app, show="*")
new_password_entry.grid(row=4, column=1)

create_user_button = tk.Button(app, text="Create User", command=create_user)
create_user_button.grid(row=5, column=0)

# Email Sending
recipient_label = tk.Label(app, text="Recipient Email:")
recipient_label.grid(row=6, column=0)
recipient_entry = tk.Entry(app)
recipient_entry.grid(row=6, column=1)

subject_label = tk.Label(app, text="Subject:")
subject_label.grid(row=7, column=0)
subject_entry = tk.Entry(app)
subject_entry.grid(row=7, column=1)

message_label = tk.Label(app, text="Message:")
message_label.grid(row=8, column=0)
message_text = tk.Text(app, height=5, width=30)
message_text.grid(row=8, column=1)

smtp_server_label = tk.Label(app, text="SMTP Server:")
smtp_server_label.grid(row=9, column=0)
smtp_server_entry = tk.Entry(app)
smtp_server_entry.grid(row=9, column=1)

smtp_port_label = tk.Label(app, text="SMTP Port:")
smtp_port_label.grid(row=10, column=0)
smtp_port_entry = tk.Entry(app)
smtp_port_entry.grid(row=10, column=1)

send_button = tk.Button(app, text="Send Email", command=send_email)
send_button.grid(row=11, column=0)

status_label = tk.Label(app, text="")
status_label.grid(row=12, columnspan=2)

# Start Tkinter event loop
app.mainloop()

# Close database connection
conn.close()
