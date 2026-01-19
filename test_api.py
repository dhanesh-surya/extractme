import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key (first 20 chars): {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\nListing all available models:")
print("=" * 80)

try:
    for m in genai.list_models():
        print(f"\nModel: {m.name}")
        print(f"  Display Name: {m.display_name}")
        print(f"  Supported Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
