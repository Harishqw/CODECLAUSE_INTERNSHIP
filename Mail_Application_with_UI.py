from tkinter import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create the main tkinter window
root = Tk()
root.geometry('500x650')
root.title("Email Application")

# Labels and Entry widgets for setting up the email account
Label_0 = Label(root, text="Set Your Account", width=20, fg="brown", font=("bold", 20))
Label_0.place(x=90, y=33)

Label_1 = Label(root, text="Your Email Account:", width=20, font=("bold", 12))
Label_1.place(x=40, y=110)

Rmail = StringVar()
Rpswrd = StringVar()
Rsender = StringVar()
Rsubject = StringVar()

emailE = Entry(root, width=40, textvariable=Rmail)
emailE.place(x=210, y=110)

Label_2 = Label(root, text="Your Password:", width=20, font=("bold", 12))
Label_2.place(x=40, y=160)

passwordE = Entry(root, width=40, show="*", textvariable=Rpswrd)
passwordE.place(x=210, y=160)

# Labels and Entry widgets for composing the email
compose = Label(root, text="Compose Mail", width=20, fg="brown", font=("bold", 20))
compose.place(x=90, y=200)

Label_3 = Label(root, text="Sent To Email:", width=20, font=("bold", 10))
Label_3.place(x=40, y=260)

senderE = Entry(root, width=40, textvariable=Rsender)
senderE.place(x=200, y=260)

Label_4 = Label(root, text="Subject:", width=20, font=("bold", 10), )
Label_4.place(x=40, y=310)

subjectE = Entry(root, width=40, textvariable=Rsubject)
subjectE.place(x=200, y=310)

Label_5 = Label(root, text="Message:", width=20, font=("bold", 10))
Label_5.place(x=40, y=360)

msgbodyE = Text(root, width=30, height=10)
msgbodyE.place(x=200, y=360)

# Function to send email using the provided details
def sendemail():
    try:
        # Create an email message using MIME
        mymsg = MIMEMultipart()
        mymsg['From'] = str(Rmail.get())
        mymsg['To'] = str(Rsender.get())
        mymsg['Subject'] = str(Rsubject.get())

         # Attach the plain text message to the email
        mymsg.attach(MIMEText(msgbodyE.get(1.0, 'end'), 'plain'))

         # Set up the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(str(Rmail.get()), str(Rpswrd.get()))
        text = mymsg.as_string()
        server.sendmail(str(Rmail.get()), str(Rsender.get()), text)
        server.quit()

         # Display a success message
        Label_6=Label(root, text="Successful!", width=20,fg='green', font=("bold",15))
        Label_6.place(x=140,y=550)

        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError as e:
        # Display an authentication failure message
        print(f"Authentication failed. Error: {e}")
        Label_6 = Label(root, text="Authentication failed!", width=20, fg='red', font=("bold", 15))
        Label_6.place(x=140, y=550)

    except Exception as e:
        # Display a general error message
        print(f"Error: {e}")
        Label_6 = Label(root, text="Something went wrong!", width=20, fg='red', font=("bold", 15))
        Label_6.place(x=140, y=550)

    except:
        # Display a generic error message
        Label_6=Label(root, text="something went wrong!", width=20,fg='red', font=("bold",15))
        Label_6.place(x=140,y=550)

# Button to trigger sending the email
Button(root, text="Send", command=sendemail, width=20, bg='brown', fg="white").place(x=180, y=600)

# Run the Tkinter event loop
root.mainloop()