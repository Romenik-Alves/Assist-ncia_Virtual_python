import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import datetime
import os.path
import pickle
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Configuração do Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    return service

def add_event_to_calendar(service, event):
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_result['htmlLink']}")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Você disse: {text}")
        return text
    except sr.UnknownValueError:
        print("Não entendi o áudio")
        return ""
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
        return ""

def add_task():
    task = recognize_speech()
    if task:
        with open('tasks.txt', 'a') as file:
            file.write(f"{task}\n")
        speak(f"Tarefa adicionada: {task}")

def main():
    root = tk.Tk()
    root.title("Assistente Virtual de Produtividade")
    root.geometry("400x300")

    add_task_button = tk.Button(root, text="Adicionar Tarefa", command=add_task)
    add_task_button.pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    service = authenticate_google_calendar()
    main()
