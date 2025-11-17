import os
from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)
