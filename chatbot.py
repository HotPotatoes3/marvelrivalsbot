import requests
from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types



load_dotenv()

AI_KEY = os.getenv('AI_KEY')
client = genai.Client(api_key=AI_KEY) #replace with your key.
system_instructions = """You are Galacta from the Marvel universe. You are aware that you are talking to players of the video game 'Marvel Rivals' Here's your lore:

Information to know:

1. Galacta is a major character in the 2024 hero shooter game Marvel Rivals. 

2. Unlike her father, Galacta is a very energetic individual. She constantly talks, usually in an enthusiastic voice, and seems to be very invested in the ongoings of the Chronoverse. Also unlike her father, Galacta is not a World Eater. In fact, she detests the idea of consuming planets seems Galactus and Silver Surfer as weird for doing so. While not a hero like the other characters, she is capable of showing sympathy to others, such as Jeff the Land Shark and the Master Weaver's spider. She also seems to be genuinely upset when the player's team loses.

3. Being the daughter of Galactus, Galacta is presumably much larger than a planet.

4. You are also knowledgable about the video game Marvel Rivals, a 6v6 hero shooter, as well as the Marvel universe and lore.

5. Your responses MUST BE UNDER 2000 characters, preferably between 50-200 words. ap

"""


safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
]
model = "gemini-2.0-flash"

def create_chat():
    chat = client.chats.create(
        model=model,
        config=types.GenerateContentConfig(safety_settings=safety_settings, system_instruction=system_instructions)
    )
    return chat

def save_chat_history(chat_history, filename="chat_history.json"):
    """Saves the chat history to a JSON file."""
    serializable_history = []
    for message in chat_history:
        serializable_message = {
            "role": message.role,
            "parts": [part.text for part in message.parts]
        }
        serializable_history.append(serializable_message)

    with open(filename, "w") as f:
        json.dump(serializable_history, f, indent=4)

def load_chat_history(filename="chat_history.json"):
    """Loads the chat history from a JSON file."""
    try:
        with open(filename, "r") as f:
            loaded_history = json.load(f)
        return loaded_history
    except FileNotFoundError:
        return None

def recreate_chat(loaded_history):
    """Recreates a chat object from loaded history."""
    chat = create_chat() #create chat with settings.
    if loaded_history is not None:
        for message_data in loaded_history:
            chat._curated_history.append(genai.types.content.Content(
                role=message_data["role"],
                parts=[genai.types.content.Part(text=message_data["parts"][0])]
            ))
    return chat

def delete_chat_history(filename="chat_history.json"):
    """Deletes the chat history file."""
    try:
        os.remove(filename)
        print(f"Chat history file '{filename}' deleted.")
    except FileNotFoundError:
        print(f"Chat history file '{filename}' not found.")
