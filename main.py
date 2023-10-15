import os
import openai
import whisper
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from moviepy.editor import VideoFileClip
import whisper
from googletrans import Translator
from gtts import gTTS 
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.editor import *
import json

app = Flask(__name__)
app.config['static'] = 'static'
#openai.api_key = "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"
if app.debug:
    app.add_url_rule('/static/styles.css', 'static', build_only=True)


supported_languages = [
    "English",  "French", "Mandarin (Mainland China)", "Mandarin (Taiwan)", "Portuguese", "Spanish"
]

language_mapping = {
    "English": "en",
    "French": "fr",
    "Mandarin (Mainland China)": "zh-CN",
    "Mandarin (Taiwan)": "zh-TW",
    "Portuguese": "pt",
    "Spanish": "es",
    # Add more languages as needed
}

@app.route('/')
def index():
    return render_template('upload.html', supported_languages = supported_languages)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file given"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        print(file)

        target_language_name = request.form.get('language')

        target_language_code = language_mapping.get(target_language_name, 'en')

        video_path = translate_video(file, target_language_code)
        
        # Return a response indicating success
        #return render_template('upload.html', video_path=video_path)
        return send_file('result.mp4', as_attachment=True)
      

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    print(audio_path)
    result = model.transcribe(audio_path)
    #print(result)
    return result["text"]

def translate_video(submit_file, target_language):

    current_directory = os.getcwd()

    # Create path
    #file_path = os.path.join(current_directory, submit_file.filename)

    file_path = os.path.join(current_directory, "temp.mp4")

    # Save the uploaded file to the local directory
    submit_file.save(file_path)

    # Load the Whisper model and transcribe audio
    transcribed_text = transcribe_audio(file_path)
    
    # Translate the text using the Google Translate Library and target language
    translator = Translator()
    translated_text = translator.translate(transcribed_text, src = "en", dest = target_language).text

    # Print the translated text
    print("Original Text:")
    print(transcribed_text)

    print("\nTranslated Text:")
    print(translated_text)

    # Save the translated text to a file for reference (maybe subtitles in the future)
    with open("translated.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)

    # Translate the audio into the selected language and save as mp3
    translated_audio = gTTS(text=translated_text, lang=target_language, slow=False)
    translated_audio.save("updated_audio.mp3") 
    translated_audio = AudioFileClip("updated_audio.mp3") 

    # Take the original video and put the new audio over it
    video = VideoFileClip(file_path)
    video = video.set_audio(translated_audio)

    #parent_dir = os.path.dirname(current_directory)
    #print("\n HI HIH IHIH" + parent_dir)
    #print(current_directory)
    #video_path = f"{parent_dir}/result.mp4"
    video_path = "result.mp4"
    video.write_videofile(video_path)

    return video_path


if __name__ == '__main__':
    app.run(debug=True)
    




