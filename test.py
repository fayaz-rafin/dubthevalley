import whisper
from googletrans import Translator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

from whisper import Segment
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip




# Load the Whisper model and transcribe audio
model = whisper.load_model("base")
result = model.transcribe("ml.mov")
transcribed_text = result["text"]
print(transcribed_text)
# Translate the text using the Google Translate API
translator = Translator()

# Example: Translate the text from "en" (English) to "fr" (French)
target_language = "fr"  # You can specify the target language code
translated_text = translator.translate(
    transcribed_text, src="en", dest=target_language).text

# Print the translated text
print("Original Text:")
print(transcribed_text)

print("\nTranslated Text:")
print(translated_text)

# Save the translated text to a file
with open("translated.txt", "w", encoding="utf-8") as f:
    f.write(translated_text)

myobj = gTTS(text=translated_text, lang=target_language, slow=False)

myobj.save("welcome.mp3")
title = input("Enter a title: ")
video_clip = VideoFileClip("ml.mov")
audio_clip = AudioFileClip("welcome.mp3")
final_clip = video_clip.set_audio(audio_clip)



def add_subtitles_to_frame(t):
    # Find the subtitle segment that matches the current time 't'
    for subtitle in subtitles:
        if subtitle.start <= t <= subtitle.end:
            return subtitle.content
    return ''


video_with_subtitles = video_clip.fl(add_subtitles_to_frame)
video_with_subtitles.write_videofile(
    final_clip.write_videofile(title + ".mp4"))
