import openai
import os

from flask import Flask, request
from moviepy.editor import *

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    
    if 'file' not in request.files:
        return "No file given"

    file = request.files['file']

    # If the user does not select a file, the browser also submits an empty part without a filename
    if file.filename == '':
        return "No selected file"

    # If the file exists
    if file:

        # Save the uploaded video file
        video_path = os.path.join("path", "to", "uploaded_video.mp4")
        file.save(video_path)
        
        # Convert the video to MP3 using moviepy
        video = VideoFileClip(video_path)
        audio_path = os.path.join("path", "to", "audio.mp3")
        video.audio.write_audiofile(audio_path)

        return f"Conversion successful. Audio file saved at {audio_path}"

if __name__ == '__main__':
    app.run(debug=True)
    

openai.api_key = "mykey"


