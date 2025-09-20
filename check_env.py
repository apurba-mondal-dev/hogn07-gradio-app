import os
from dotenv import load_dotenv

# This is the same function that loads your .env file
load_dotenv()

# We try to get the key from the environment
api_key = os.environ.get("GROQ_API_KEY")

# Now we check if it was found
if api_key:
    # For security, we only show the first and last characters
    print(f"✅ Success! API Key Found: {api_key[:7]}...{api_key[-4:]}")
else:
    print("❌ Error: API Key Not Found.")