import speech_recognition as sr
from openai import OpenAI
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) # Define the client instance

def chat_with_gpt(input_text, client):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",  
            messages=[
                {"role": "user", "content": input_text}
            ],
            max_tokens=2500
        )
        if completion.choices and completion.choices[0].message:
            return completion.choices[0].message
        else:
            return "No response from GPT"
    except Exception as e:
        return f"Error from GPT: {str(e)}"

def recognize_speech(timeout=3):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

def speak_text(gpt_response):
    response = gpt_response.content
    subprocess.call(['say', response])
    
def main():
    while True:
        print("Listening...")
        user_input = recognize_speech()
        if user_input is None:
            continue  # Continue listening if no input is detected
        if user_input.lower() == "exit":
            break  # Exit the loop if the user says "exit"
        if user_input.lower() == "clear":
            os.system('clear')
            continue
        if user_input.lower() == "take a screenshot":
            screenshot_path = "/Screenshots/"
            os.system(f'screencapture {screenshot_path}')
            continue
        gpt_response = chat_with_gpt(user_input, client)  # Pass client
        print(f'Response: "{gpt_response.content}"')
        speak_text(gpt_response)
        continue

if __name__ == "__main__":
    main()