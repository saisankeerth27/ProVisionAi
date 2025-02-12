from flask import Flask, request, jsonify, render_template
import os
import base64
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyDb31yr6iBIN-0RGYUF3JDXF3fic3DVacs"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDb31yr6iBIN-0RGYUF3JDXF3fic3DVacs"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def annotate_image(image_path):
    # Read the image file and encode it in base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the payload for the Gemini API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Describe this image in detail."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
                ]
            }
        ]
    }

    # Send the request to the Gemini API
    response = requests.post(GEMINI_API_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API error: {response.status_code}, {response.text}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/annotate', methods=['POST'])
def annotate():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file.'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Get annotation from the Gemini API
            annotation = annotate_image(filepath)
            return jsonify({'success': True, 'annotation': annotation})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Invalid file type.'}), 400

if __name__ == '__main__':
    app.run(debug=True)