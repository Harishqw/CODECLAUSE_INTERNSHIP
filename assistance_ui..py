import tkinter as tk
import speech_recognition as sr

# Initialize the Tkinter application
app = tk.Tk()
app.title("Voice Assistant")

# Function to handle voice input
def handle_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        display_command(command)
        process_command(command)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to display the interpreted command
def display_command(command):
    command_display.config(text="You said: " + command)

# Function to process the command and generate a response
def process_command(command):
    # Here you would implement the logic to interpret the command
    # and generate an appropriate response
    response = "I heard you say: " + command
    display_response(response)

# Function to display the response
def display_response(response):
    response_display.config(text=response)

# Create GUI elements
mic_button = tk.Button(app, text="Click to Speak", command=handle_voice_input)
mic_button.pack()

command_display = tk.Label(app, text="")
command_display.pack()

response_display = tk.Label(app, text="")
response_display.pack()

# Start the Tkinter event loop
app.mainloop()
