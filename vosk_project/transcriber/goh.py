import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("C:/Users/Arad/Desktop/vosk_project/transcriber/vosk-model-small-fa-0.4")  # پوشه مدل فارسی

def transcribe_audio(file_path):
    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
        raise ValueError("فایل باید WAV با فرمت mono PCM باشد.")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))
    results.append(json.loads(rec.FinalResult()))

    text = " ".join([res.get("text", "") for res in results])
    return text
