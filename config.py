import os
from dotenv import load_dotenv

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
MODEL = os.getenv("MODEL", "gpt-oss-120b")
BASE_URL = os.getenv("BASE_URL", "https://api.cerebras.ai/v1")

DEFAULT_REPOSITORY = "../node-easy-notes-app"