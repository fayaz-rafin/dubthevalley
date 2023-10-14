import whisper
from googletrans import Translator
from gtts import gTTS


# Load the Whisper model and transcribe audio
model = whisper.load_model("base")
result = model.transcribe("sample-0.mp3")
transcribed_text = result["text"]
print(transcribed_text)
# Translate the text using the Google Translate API
translator = Translator()

# Example: Translate the text from "en" (English) to "fr" (French)
target_language = "es"  # You can specify the target language code
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
