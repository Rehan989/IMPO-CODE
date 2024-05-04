from flask import Flask, request, send_file, jsonify
from src.parallel_process_azure import convert_text_to_speech_with_threading
from src.config import CHUNK_SIZE
from src.utils import text_parse
import os

import uuid
# import logging
# import warnings
# from datetime import datetime
# import os 
# from src.logger import setup_logger
# from src.text_to_speech import text_to_audio

# LOG_PATH = os.path.join(os.getcwd(), "logs")

# warnings.filterwarnings("ignore")

# os.makedirs(LOG_PATH, exist_ok=True)

# date = datetime.now().strftime("%Y_%m_%d")

# log = setup_logger(
#     out_file=f"{LOG_PATH}/{date}.log", stderr_level=logging.INFO
# )

app = Flask(__name__)
AUDIO_FOLDER = './audio'
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
CHUNK_SIZE = 1024

@app.route("/")
def just_check():
    return "<p>Welcome to Text-to-Speech project</p>"


@app.route("/text", methods=["POST"])
def text_process():
    if request.method != "POST":
        return "Invalid method", 405
    
    try:
        # Retrieve the input data
        text = request.json.get('text', "")
        voice_name = request.json.get('voice_name', "default")
        
        if not text:
            return "Text field is empty", 400
        
        # Generate a unique filename for the audio file
        unique_filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(AUDIO_FOLDER, unique_filename)
        
        # Call your function to convert text to speech
        audio_stream = convert_text_to_speech_with_threading(voice_name, text, CHUNK_SIZE)
        
        if audio_stream:
            # Make sure the audio stream is at the beginning
            audio_stream.seek(0)  # Set to start of the stream

            # Read the bytes from the BytesIO object
            audio_bytes = audio_stream.read()  # Read the bytes to ensure valid data
            
            # Save the audio bytes to a file
            with open(file_path, 'wb') as f:
                f.write(audio_bytes)
            
            # Return the filename to the client
            return jsonify({"filename": unique_filename}), 200
        
        return "Error occurred--Audio stream not found", 500
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
        
@app.route("/file", methods=["POST"])
def file_process():
    
    try:
        
        if request.method == "POST":
            print("started")
                       
            text_file = request.files['file']
            voice_name = request.form.get('voice_name')
            
            text = text_file.read().decode('utf-8')
            chunk_size = CHUNK_SIZE
            
            audio_stream = convert_text_to_speech_with_treadding(voice_name, text, chunk_size)
        
            if audio_stream:              
                return send_file(audio_stream, as_attachment=True, download_name="audio.wav")
            
            else:
                return "Error occurred--Audio stream not found"
                
        else:
            return "enter valid Method"       
                
                   
    except Exception as e:
        print(str(e))
        
        
# @app.route("/image", methods=["POST"])
# def image_process():
    
#     try:
              
           
        
#     except Exception as e:
#         print(str(e))
        
        
        
if __name__ == '__main__':
    app.run()