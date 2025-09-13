import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import pytesseract
import cv2
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def preprocess_image(image):
    """Preprocess image for better OCR results"""
    # Convert PIL image to OpenCV format
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    # Morphological operations to clean up the image
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return cleaned

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Convert back to PIL Image for pytesseract
        pil_image = Image.fromarray(processed_image)
        
        # Extract text using pytesseract
        # Try different OCR configurations for better results
        config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"\'\\/-+=*&%$#@^~`|<> '
        
        text = pytesseract.image_to_string(pil_image, config=config)
        
        # Clean up the extracted text
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 2:  # Filter out very short lines
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def summarize_text(text):
    """Summarize the extracted text using OpenAI"""
    if not text or len(text.strip()) < 10:
        return "No meaningful text found to summarize."
    
    try:
        prompt = f"""
        Please analyze and summarize the following text extracted from a classroom whiteboard. 
        The text may contain mathematical equations, diagrams, notes, or other educational content.
        
        Please provide:
        1. A clear, concise summary of the main topics
        2. Key concepts and important points
        3. Any mathematical formulas or equations (if present)
        4. The overall theme or subject matter
        
        Text to analyze:
        {text}
        
        Please format your response in a clear, structured way that would be helpful for students.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an educational assistant that helps summarize classroom whiteboard content in a clear and helpful way."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Read the image
            image = Image.open(io.BytesIO(file.read()))
            
            # Extract text
            extracted_text = extract_text_from_image(image)
            
            # Generate summary
            summary = summarize_text(extracted_text)
            
            # Create response
            result = {
                'extracted_text': extracted_text,
                'summary': summary,
                'timestamp': datetime.now().isoformat(),
                'filename': file.filename
            }
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
