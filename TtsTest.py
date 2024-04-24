import threading
import speech_recognition as sr
from openai import OpenAI
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)  # Define the client instance

def chat_with_gpt(input_text, client):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": input_text}],
            max_tokens=2500
        )
        if completion.choices and completion.choices[0].message:
            return completion.choices[0].message
        else:
            return "No response from GPT"
    except Exception as e:
        return f"Error from GPT: {str(e)}"

def recognize_speech(recognizer, microphone):
    print("Listening...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

def speak_text(gpt_response):
    response = gpt_response.content
    subprocess.call(['say', response])

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    while True:
        user_input = recognize_speech(recognizer, microphone)
        if user_input is None:
            continue  # Continue listening if no input is detected

        user_input_lower = user_input.lower()
        if user_input_lower == "exit":
            break  # Exit the loop if the user says "exit"
        elif user_input_lower == "clear":
            os.system('clear')
            continue
        elif user_input_lower == "take a screenshot":
            screenshot_path = "/Screenshots/"
            os.system(f'screencapture {screenshot_path}')
            continue
        
        threading.Thread(target=process_input, args=(user_input,)).start()

def process_input(user_input):
    gpt_response = chat_with_gpt(user_input, client)
    print(f'Response: "{gpt_response.content}"')
    speak_text(gpt_response)

if __name__ == "__main__":
    main()