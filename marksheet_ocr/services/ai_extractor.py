"""
AI-powered text extraction service using Google Gemini Vision API
"""
import os
import json
import google.generativeai as genai
from PIL import Image
from django.conf import settings


class AIExtractor:
    """Extract structured data from marksheet images using Gemini AI"""
    
    def __init__(self):
        # Get API key from Django settings
        api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your-gemini-api-key-here':
            raise ValueError(
                "GEMINI_API_KEY not set in .env file. "
                "Please get your API key from https://makersuite.google.com/app/apikey"
            )
        genai.configure(api_key=api_key)
        
        # Try different model names in order of preference (based on actual available models)
        model_names = [
            'gemini-2.5-flash',
            'gemini-flash-latest',
            'gemini-pro',
            'models/gemini-2.5-flash',
            'models/gemini-flash-latest',
            'models/gemini-pro'
        ]
        
        last_error = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"Successfully initialized model: {model_name}")
                break
            except Exception as e:
                last_error = e
                continue
        else:
            raise ValueError(f"Could not initialize any Gemini model. Last error: {last_error}")
    
    def extract_marksheet_data(self, image_path):
        """
        Extract student data from marksheet image
        
        Args:
            image_path: Path to the marksheet image
            
        Returns:
            List of dictionaries containing student data
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create detailed prompt for structured extraction
            prompt = """
            Analyze this marksheet image and extract ALL student information in JSON format.
            
            For EACH student in the image, extract:
            1. Roll Number (ROLL NO.)
            2. Student Name (STUDENT'S NAME)
            3. Father's/Husband's Name (FATHER'S/HUSBAND NAME)
            4. Mother's Name (if available)
            5. Enrollment Number (if available)
            6. All subjects with their codes and names
            7. For each subject, extract marks:
               - Theory ESE (External Semester Examination)
               - Theory Internal
               - Practical marks
               - Practical Internal
            8. Aggregate percentage
            9. Result status (e.g., "PASS FIRST", "PASS SECOND", "FAIL")
            
            Return the data as a JSON array with this exact structure:
            [
                {
                    "roll_number": "294343",
                    "name": "KHEL KUMAR",
                    "father_name": "SHRI TIJ RAM",
                    "mother_name": "SMT. INDER BAI",
                    "enrollment_number": "SHRI21S0370 VID-(SHRI21S0371A)",
                    "subjects": [
                        {
                            "code": "01",
                            "name": "PC HINDI LANGUAGE",
                            "theory_ese": 24,
                            "theory_internal": null,
                            "practical": null,
                            "practical_internal": null
                        },
                        {
                            "code": "02",
                            "name": "PC ENGLISH LANGUAGE",
                            "theory_ese": 50,
                            "theory_internal": null,
                            "practical": null,
                            "practical_internal": null
                        }
                    ],
                    "percentage": 62.66,
                    "result": "PASS FIRST"
                }
            ]
            
            IMPORTANT:
            - Extract ALL students visible in the image
            - Use null for marks that are not available or shown as "..."
            - Be precise with numbers
            - Include all subjects for each student
            - Return ONLY valid JSON, no additional text
            """
            
            # Generate response
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            students_data = json.loads(response_text)
            
            return students_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}\nResponse: {response_text}")
        except Exception as e:
            raise Exception(f"Error extracting data with AI: {str(e)}")
    
    def validate_student_data(self, student_data):
        """
        Validate extracted student data
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Boolean indicating if data is valid
        """
        required_fields = ['roll_number', 'name', 'subjects']
        
        # Check required fields
        for field in required_fields:
            if field not in student_data or not student_data[field]:
                return False
        
        # Validate subjects
        if not isinstance(student_data['subjects'], list) or len(student_data['subjects']) == 0:
            return False
        
        # Validate each subject
        for subject in student_data['subjects']:
            if 'code' not in subject or 'name' not in subject:
                return False
        
        return True
