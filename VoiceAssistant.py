import os
import io
import json
import time
import requests
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from dotenv import load_dotenv

# Load ElevenLabs API key
load_dotenv()
xi_api_key = os.getenv("ELEVENLABS_API_KEY")


# ---------- Ollama: Generate Response ----------
def generate_text(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server not found. Please start it with:")
        print("   brew services start ollama")
        print("   or run: ollama serve")
        return "Sorry, I couldn’t connect to Ollama."
    except Exception as e:
        print(f"⚠️ Error calling Ollama: {e}")
        return "Sorry, I couldn’t process that."


# ---------- Audio Recording ----------
def record_speech(duration, sample_rate=16000):
    print("🎤 Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording


def save_wav(audio_data, filename, sample_rate):
    sf.write(filename, audio_data, sample_rate)


# ---------- Speech-to-Text ----------
def speech_to_text(audiofile):
    rec = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = rec.record(source)

    try:
        text = rec.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    return text


# ---------- ElevenLabs: Text-to-Speech ----------
def generate_audio(text: str):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # default voice ID
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": xi_api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.content
    else:
        print(f"⚠️ ElevenLabs error {response.status_code}: {response.text}")
        return None


def play_audio(audio_bytes):
    audio_stream = io.BytesIO(audio_bytes)
    data, samplerate = sf.read(audio_stream, dtype='float32')
    sd.play(data, samplerate)
    sd.wait()


# ---------- Main Loop ----------
if __name__ == "__main__":
    while True:
        # Record speech for 5 seconds
        record_duration = 5
        sample_rate = 16000
        audio_data = record_speech(record_duration, sample_rate)
        audiofile = "speech_recording.wav"
        save_wav(audio_data, audiofile, sample_rate)

        # Convert recorded speech to text
        input_text = speech_to_text(audiofile)
        print("🗣 Input Text:", input_text)

        if not input_text.strip():
            print("⏭ No speech detected. Retrying...")
            continue

        # Generate new text using Ollama
        generated_text = generate_text(input_text)
        print("🤖 Generated Text:", generated_text)

        # Synthesize the generated text using ElevenLabs API
        audio = generate_audio(generated_text)

        # Play the synthesized audio
        if audio:
            play_audio(audio)

        # Add a delay before recording again
        time.sleep(1)
