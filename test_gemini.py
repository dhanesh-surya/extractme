import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Test image path
test_image = "media/marksheets/test_marksheet.jpg"

model_names = [
    'gemini-2.5-flash',
    'gemini-flash-latest',
    'gemini-pro',
]

print("Testing Gemini models with marksheet image...")
print("=" * 60)

for model_name in model_names:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Try to generate content with image
        image = Image.open(test_image)
        response = model.generate_content(["Extract the first student's name from this marksheet", image])
        
        print(f"✓ SUCCESS! Model {model_name} works!")
        print(f"  Response: {response.text[:200]}...")
        break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:150]}")
        continue
else:
    print("\n❌ None of the models worked with images!")
