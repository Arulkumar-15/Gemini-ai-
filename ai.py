import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError

# Directly set the API key here
api_key = "Api key"

if not api_key:
    raise ValueError("The API key must be set.")

# Configure the Google Generative AI API key
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Function to get the response from the AI model
def get_response():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response.text)
    except InternalServerError as e:
        messagebox.showerror("Server Error", "An internal server error occurred. Please try again later.")
        print(e)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(e)

# Create the GUI
root = tk.Tk()
root.title("Google AI Chatbot")

input_label = tk.Label(root, text="Enter your message:")
input_label.pack(pady=5)

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
input_text.pack(pady=5)

send_button = tk.Button(root, text="Send", command=get_response)
send_button.pack(pady=5)

output_label = tk.Label(root, text="Response:")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
output_text.pack(pady=5)

root.mainloop()
