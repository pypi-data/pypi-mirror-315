# mindbot/ai_functions.py

import google.generativeai as genai
import httpx
import base64
import time
from datetime import datetime

API_KEY = "AIzaSyDVvvyZ6nguTafU7Pqqq4IoGshLcNO2S0Q"
MIND_BOT_1_3 = "gemini-1.5-pro"

def interact_with_ai():
    genai.configure(api_key=API_KEY)
    user_question = input("\033[32mUser:> \033[0m")
    question_time = datetime.now()
    print(f"\033[32mUser ({question_time}): {user_question}\033[0m")
    start_time = time.time()
    try:
        model = genai.GenerativeModel(MIND_BOT_1_3)
        response = model.generate_content(user_question)
        end_time = time.time()
        time_taken = end_time - start_time
        response_time = datetime.now()
        print(f"\033[34mAI ({response_time}): {response.text}\033[0m")
        print(f"\033[33mTime taken to respond: {time_taken:.2f} seconds\033[0m")
    except Exception as e:
        print(f"\033[31mError generating response: {e}\033[0m")

def generate_image_prompt_content():
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name=MIND_BOT_1_3)

    image_path = input("Enter the image URL: ")

    try:
        image = httpx.get(image_path)
        image.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"Failed to fetch the image: {e}")
        return

    prompt = input("user:> ")

    try:
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')},
            prompt
        ])
        print("Generated response:")
        print(response.text)
    except Exception as e:
        print(f"Error generating content: {e}")

def upload_video(video_file_path):
    genai.configure(api_key=API_KEY)
    print("Uploading file...")
    video_file = genai.upload_file(path=video_file_path)
    print(f"Completed upload: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        print('.', end='', flush=True)
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(f"File processing failed: {video_file.state.name}")

    print("\nFile processed successfully!")
    return video_file

def summarize_video(video_file):
    genai.configure(api_key=API_KEY)
    prompt = input("user:> (Ex. Summarize Text):  ")
    model = genai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)

def ask_specific_question(video_file):
    genai.configure(api_key=API_KEY)
    prompt = input("User:> (Ex. Any Thing in the video)  ")
    model = genai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)

def transcribe_and_describe(video_file):
    genai.configure(api_key=API_KEY)
    prompt = input("User:>(Ex. Transcription And Visual descriptions)  ")
    model = genai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)
