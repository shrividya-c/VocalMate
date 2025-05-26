# 🎙️ VocalMate – AI Voice Assistant

**VocalMate** is a Python-based AI voice assistant that uses the power of **Groq’s LLaMA 3 (70B)** model for real-time natural language interactions. Designed for smart automation and enhanced user engagement, VocalMate lets you interact with your computer using your voice – just like talking to a friend.

---

## 🚀 Features

- 🎤 **Real-Time Voice Interaction**  
  Powered by Groq's LLaMA 3 (70B) API for intelligent, conversational responses.

- 🌐 **Voice-Controlled Automation**  
  Perform tasks like:
  - Opening websites (e.g., YouTube, Google)
  - Searching Wikipedia
  - Fetching the latest news
  - Playing local music
  - Telling time-based greetings

- ⏰ **Smart Reminders**
  - Hydration reminders and customizable alerts to boost productivity and wellness.

- 🧠 **Contextual Understanding**  
  Understands context and responds intelligently to follow-up queries.

---

## 🛠️ Built With

- **Python** – Core language
- **[Groq API](https://groq.com/)** – For LLaMA 3 (70B) language model integration
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** – For capturing user voice commands
- **[gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)** – For converting responses to speech
- **[Pygame](https://www.pygame.org/)** – For playing audio
- **[News API](https://newsapi.org/)** – To fetch real-time news updates
- **[Wikipedia API](https://pypi.org/project/wikipedia/)** – For answering knowledge-based queries


---

## 🚀 Getting Started

1. **Clone the repository**

```bash
   git clone https://github.com/shrividya-c/vocalmate.git
   cd vocalmate
```

2. **Install dependencies**

```bash
    pip install -r requirements.txt
 ```

3. **Set up your API keys**  
Store the API keys as environment variables:

```env
   GROQ_API_KEY=your_groq_api_key
   NEWS_API_KEY=your_newsapi_key
```

## Run the App
```bash
python vocalmate.py
```
Start speaking when prompted. VocalMate will respond with intelligent actions and speech.