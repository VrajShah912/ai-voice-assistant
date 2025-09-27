# 🎙️ AI Voice Assistant

An intelligent **voice assistant** that lets you speak, processes your input with a **local AI model (Ollama + Llama 3)**, and responds back in natural voice using **ElevenLabs**.  

This project demonstrates the integration of **speech-to-text (STT)**, **language model reasoning**, and **text-to-speech (TTS)** in a clean Python pipeline.

---

## ✨ Features
- 🎤 **Speech-to-Text**: Captures microphone input and transcribes with Google SpeechRecognition.  
- 🧠 **Local AI Model**: Uses Ollama to run **Llama 3** entirely offline, no API costs or quotas.  
- 🔊 **Text-to-Speech**: ElevenLabs generates human-like spoken responses.  
- 🔄 **Continuous Loop**: Keeps recording, thinking, and responding until stopped.  
- 🔐 **Environment Variables**: API keys stored securely via `.env`.  

---

## 🛠️ Tech Stack
- **Python 3.12+**  
- **Ollama** for local LLM inference  
- **ElevenLabs API** for TTS  
- **Google SpeechRecognition** for STT  
- **sounddevice & soundfile** for recording and playback  
- **dotenv** for key management  

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Install Ollama and Llama 3
```bash
brew install ollama
brew services start ollama
ollama pull llama3
```

Quick test:
```bash
ollama run llama3 "Hello, how are you?"
```

### 5. Setup API Key
Create a `.env` file:
```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

---

## ▶️ Usage
Start the assistant:
```bash
python VoiceAssistant.py
```

Flow:
1. 🎤 Record 5 seconds of audio.  
2. 🗣 Convert speech → text.  
3. 🤖 Llama 3 generates a response.  
4. 🔊 ElevenLabs converts text → voice.  
5. ▶️ Response plays back to you.  

---

## 📂 Project Structure
```
ai-voice-assistant/
│── VoiceAssistant.py   # Main app
│── requirements.txt    # Python dependencies
│── .env                # API keys
│── README.md           # Documentation
```

---

## 🔮 Future Enhancements
- Add **wake word detection** (e.g., "Hey Assistant").  
- Support **streaming audio** instead of fixed chunks.  
- Replace ElevenLabs with **local TTS** (e.g., pyttsx3 or Coqui TTS).  
- Multi-language support.  
- GUI or web interface.  

---

## ⚠️ Notes
- Ollama works best on **macOS (M1/M2)** or Linux.  
- ElevenLabs free tier has daily limits; swap to local TTS for 100% free usage.  
- Intended for **learning/demo purposes**, not production-ready.  

---

## 📜 License
MIT License. Free to use, modify, and share.  
