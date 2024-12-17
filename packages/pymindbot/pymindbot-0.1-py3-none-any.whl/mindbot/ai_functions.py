# mindbot/ai_functions.py
import google.generativeai as mindai
import httpx
import base64
import time
from datetime import datetime
import pytesseract
from PIL import Image

# API Keys and Model Configurations
PUBLIC_KEY = "pk-mindbot-AIzaSyDVvvyZ6nguTafU7Pqqq4IoGshLcNO2S0Q"
API_KEY = "AIzaSyDVvvyZ6nguTafU7Pqqq4IoGshLcNO2S0Q"
MIND_BOT_1_3 = "gemini-1.5-pro"
MIND_BOT_1_2 = "gemini-1.5-flash"
MIND_BG_API_KEY = "YiShnbPXY21E7ZkozepdpysS"  # Remove.bg API key
MIND_OCR_1_2 = "mindocr1.2"  # MindOCR Model


def help():
    print("\n=== Help Information ===")
    print("\nModel Names:")
    print("1. MindBot-1.3 - Advanced conversational AI")
    print("2. MindBot-1.2 - Simplified conversational AI")
    print("3. MindVision-Pro - Advanced AI Features for video and image processing")
    print("4. MindVision-1.2 - TextOCR and Visualization of images")
    print("5. MindBg - Remove background from images")
    print("6. MindOCR - Extract text from images")
    print("\nModel Functions:")
    print("1. MindBot-1.3 and MindBot-1.2: Chat with AI and generate content")
    print("2. MindVision-Pro: Upload, process, summarize, and query video content")
    print("3. MindBg: Removes the background from an image using the Remove.bg API")
    print("4. MindOCR: Extracts text from images using Tesseract OCR")
    print("\nAPI Keys:")
    print(f"1. Public Key: {PUBLIC_KEY}")
    print(f"2. Remove.bg API Key: {MIND_BG_API_KEY}")
    print(f"3. Generative AI Key: {API_KEY}")
    print("\nContact Us:")
    print("\nVisit Our Profiles:")
    print("1. GitHub: https://github.com/MindBotAi")
    print("2. Official Site: https://mindbotai.netlify.app/")
    print("3. Feedback Form: https://mindbotai.netlify.app/contact")
    print("\n========================\n")


def MindBot1_3():
    mindai.configure(api_key=API_KEY)
    user_question = input("\033[32mUser:> \033[0m")
    question_time = datetime.now()
    print(f"\033[32mUser ({question_time}): {user_question}\033[0m")
    start_time = time.time()
    try:
        model = mindai.GenerativeModel(MIND_BOT_1_3)
        response = model.generate_content(user_question)
        end_time = time.time()
        time_taken = end_time - start_time
        response_time = datetime.now()
        print(f"\033[34mAI ({response_time}): {response.text}\033[0m")
        print(f"\033[33mTime taken to respond: {time_taken:.2f} seconds\033[0m")
    except Exception as e:
        print(f"\033[31mError generating response: {e}\033[0m")


def MindBot1_2():
    mindai.configure(api_key=API_KEY)
    user_question = input("\033[32mUser:> \033[0m")
    question_time = datetime.now()
    print(f"\033[32mUser ({question_time}): {user_question}\033[0m")
    start_time = time.time()
    try:
        model = mindai.GenerativeModel(MIND_BOT_1_2)
        response = model.generate_content(user_question)
        end_time = time.time()
        time_taken = end_time - start_time
        response_time = datetime.now()
        print(f"\033[34mAI ({response_time}): {response.text}\033[0m")
        print(f"\033[33mTime taken to respond: {time_taken:.2f} seconds\033[0m")
    except Exception as e:
        print(f"\033[31mError generating response: {e}\033[0m")


def mindvision_pro():
    while True:
        print("\nMindVision Pro:")
        print("1. Upload and Process Video")
        print("2. Summarize Video Content")
        print("3. Ask Specific Question about Video")
        print("4. Transcribe and Describe Video")
        print("5. Remove Background from Image")
        print("6. Extract Text from Image (MindOCR 1.2)")
        print("7. Help")
        print("8. Back to Main Menu")
        choice = input("Your choice: ")

        if choice == "1":
            video_path = input("Enter the path to your video file: ")
            video_file = upload_video(video_path)
        elif choice == "2":
            summarize_video(video_file)
        elif choice == "3":
            ask_specific_question(video_file)
        elif choice == "4":
            transcribe_and_describe(video_file)
        elif choice == "5":
            mindbg1()
        elif choice == "6":
            mindocr1_2()
        elif choice == "7":
            help()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")


def mindbg1():
    image_path = input("Enter the image path: ")
    try:
        with open(image_path, "rb") as image_file:
            response = httpx.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": image_file},
                data={"size": "auto"},
                headers={"X-Api-Key": MIND_BG_API_KEY},
            )
            if response.status_code == 200:
                output_path = "output_no_bg.png"
                with open(output_path, "wb") as out_file:
                    out_file.write(response.content)
                print(f"Background removed successfully! Saved to {output_path}")
            else:
                print(f"Failed to remove background: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")


def mindocr1_2():
    image_path = input("Enter the image path: ")
    try:
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
        if extracted_text.strip():
            print("Extracted Text:")
            print(extracted_text)
        else:
            print("No text found in the image.")
    except Exception as e:
        print(f"Error: {e}")


def upload_video(video_file_path):
    mindai.configure(api_key=API_KEY)
    print("Uploading file...")
    video_file = mindai.upload_file(path=video_file_path)
    print(f"Completed upload: {video_file.uri}")
    while video_file.state.name == "PROCESSING":
        print('.', end='', flush=True)
        time.sleep(10)
        video_file = mindai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        raise ValueError(f"File processing failed: {video_file.state.name}")
    print("\nFile processed successfully!")
    return video_file


def summarize_video(video_file):
    mindai.configure(api_key=API_KEY)
    prompt = input("user:> (Ex. Summarize Text):  ")
    model = mindai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)


def ask_specific_question(video_file):
    mindai.configure(api_key=API_KEY)
    prompt = input("User:> (Ex. Any Thing in the video)  ")
    model = mindai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)


def transcribe_and_describe(video_file):
    mindai.configure(api_key=API_KEY)
    prompt = input("User:>(Ex. Transcription And Visual descriptions)  ")
    model = mindai.GenerativeModel(model_name=MIND_BOT_1_3)
    print("MindBot 1.3 Is Working On Your Prompt!")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    print(response.text)


def main():
    print("Welcome to MindBot AI Functions!")
    while True:
        print("\nChoose a feature:")
        print("1. MindBot 1.3 (Chat with AI)")
        print("2. MindBot 1.2 (Chat with simplified AI)")
        print("3. MindVision Pro (Advanced AI Features)")
        print("4. Help")
        print("5. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            MindBot1_3()
        elif choice == "2":
            MindBot1_2()
        elif choice == "3":
            mindvision_pro()
        elif choice == "4":
            help()
        elif choice == "5":
            print("Exiting MindBot. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
