import whisper

model = whisper.load_model("base")
result = model.transcribe("sample-0.mp3",fp16=False)


