import openai
import tkinter as tk
import speech_recognition as sr
import pyttsx3

# Konfiguracja klucza API OpenAI
API_KEY = "TWOJ_KLUCZ_API"

# Inicjalizacja syntezatora mowy
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def ask_openai(prompt, context=[]):
    """Wysyła zapytanie do OpenAI z kontekstem rozmowy."""
    messages = context + [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        api_key=API_KEY
    )
    answer = response["choices"][0]["message"]["content"]
    context.append({"role": "user", "content": prompt})
    context.append({"role": "assistant", "content": answer})
    return answer

def speak(text):
    """Odtwarza odpowiedź za pomocą syntezatora mowy."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Rozpoznaje mowę użytkownika."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Nasłuchiwanie...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="pl-PL")
            status_label.config(text="Rozpoznano: " + text)
            return text
        except sr.UnknownValueError:
            status_label.config(text="Nie rozpoznano mowy.")
            return ""
        except sr.RequestError:
            status_label.config(text="Błąd połączenia z usługą rozpoznawania.")
            return ""

def send_message():
    """Wysyła wiadomość do OpenAI i wyświetla odpowiedź."""
    user_input = entry.get()
    if not user_input:
        return
    conversation.insert(tk.END, "Ty: " + user_input + "\n", "user")
    entry.delete(0, tk.END)
    response = ask_openai(user_input, context)
    conversation.insert(tk.END, "Asystent: " + response + "\n", "assistant")
    speak(response)

def send_voice():
    """Rozpoznaje mowę i wysyła ją do OpenAI."""
    user_input = recognize_speech()
    if user_input:
        conversation.insert(tk.END, "Ty: " + user_input + "\n", "user")
        response = ask_openai(user_input, context)
        conversation.insert(tk.END, "Asystent: " + response + "\n", "assistant")
        speak(response)

# Inicjalizacja GUI
root = tk.Tk()
root.title("Asystent AI")
root.geometry("500x600")
root.configure(bg="white")

conversation = tk.Text(root, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12))
conversation.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
conversation.tag_config("user", foreground="blue")
conversation.tag_config("assistant", foreground="green")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10, padx=10, fill=tk.X)

send_button = tk.Button(root, text="Wyślij", command=send_message, font=("Arial", 12))
send_button.pack(pady=5)

voice_button = tk.Button(root, text="Mów", command=send_voice, font=("Arial", 12))
voice_button.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10), fg="red")
status_label.pack()

context = []  # Pamięć kontekstowa rozmowy

root.mainloop()
