from google import genai
from dotenv import load_dotenv  # used to read env files
import os

load_dotenv()   # loads the env file
api_key = os.getenv("GEMINI_API_KEY")   # sets the variable to our gemini_api_key saved in .env


client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a 50 words!"
)

print(response.text)