# BuddyBug_voice_assistant_project

A modern desktop voice assistant with GUI + CLI modes. BuddyBug can execute system commands, process natural language queries, and provide AI-powered responses.

---

🎥 Demo

<img width="1440" height="900" alt="GuiDemo" src="https://github.com/user-attachments/assets/73904954-bb64-445d-9e76-c3bf11daeab5" />

---

✨ Features

🎯 Core Capabilities

🎙 Voice Recognition – Real-time speech-to-text
🗣 Text-to-Speech – Natural voice responses (Edge TTS)
🤖 AI Integration – Hugging Face GPT-based conversational model
💻 Local Commands – Open/close apps, control system
🔀 Dual Interface – GUI and command-line


🎨 GUI Features

🚀 Full-screen modern interface with neon theme
📊 Real-time voice activity visualization
📝 Scrollable chat history
⌨ Multiple input methods: voice, text, keyboard shortcuts
⏳ Session management with timer + date display


🔧 System Integration

Open/close applications
Run system commands (shutdown, restart, explorer)
Open websites in browser
Manage running processes

---

🗂 Project Structure

<img width="299" height="395" alt="image" src="https://github.com/user-attachments/assets/95397e07-dbfb-4f36-a64e-fb8e1361efd5" />

---

🚀 Installation

Prerequisites
Python 3.8+
Windows (recommended)
Microphone + speakers
Internet connection


Setup:

git clone https://github.com/yourusername/BuddyBug-AI.git
cd BuddyBug-AI
pip install -r requirements.txt

Edit config.py and add your Hugging Face token:

HF_TOKEN = "your_hugging_face_token_here"

🔒 Security Tip: Never commit real API keys. Use .env or config files excluded from Git.

---

🎮 Usage

GUI Mode (Recommended):
python gui_main.py

Controls:
Spacebar → Start voice command
ESC → Exit
Mouse Wheel → Scroll chat
Text Box → Type input
Send Button → Submit message

Command-Line Mode:
python main.py

---

💬 Example Interactions

User: "Open Chrome"
BuddyBug: "Opening Chrome now 🚀"

User: "What’s the weather like today?"
BuddyBug: "It looks sunny with a high of 30°C ☀"

User: "Shutdown the PC"
BuddyBug: "Shutting down in 10 seconds…"

---

🛠 Customization

Adding Local Commands

In Brain/processor.py:

elif "open my app" in query:
    os.startfile(r"path\to\your\app.exe")
    return "Opening your application"

Adding Local Responses

In Brain/question_bank.json:

{
  "how are you": "I'm running at full capacity!",
  "your purpose": "To assist you with tasks and information."
}

Change TTS Voice

In Head/Mouth.py:
VOICE = "en-US-AriaNeural"

---

📋 Supported Commands

Applications:
Word, Excel, PowerPoint
Chrome, Edge
VS Code, Copilot
WhatsApp, Skype, LinkedIn
Notepad, File Explorer, Camera


Web:
Open ChatGPT
Open YouTube
Any custom website
System
Shutdown / Restart
File Explorer operations
Process management

---

🔧 Technical Details

ai.py → Hugging Face GPT model integration
processor.py → Fuzzy string matching, command execution
Ear.py → SpeechRecognition API (Google)
Mouth.py → Edge TTS + Pygame playback

Dependencies

speechrecognition>=3.10.0
pygame>=2.5.0
edge-tts>=6.1.0
openai>=1.0.0
rapidfuzz>=3.6.1
asyncio
threading

---

🐛 Troubleshooting

❌ No speech detected
✔ Check mic permissions, unmute, adjust duration.

❌ Network error
✔ Check internet, verify API availability.

❌ App not opening
✔ Confirm paths in processor.py.

❌ TTS not working
✔ Verify Pygame audio + speaker output.

---

🤝 Contributing

1. Fork repo
2. Create a feature branch
3. Commit changes
4. Open PR

---

📄 License

Licensed under the MIT License – see LICENSE.

---

🙏 Acknowledgments

Hugging Face – AI hosting
Google Speech Recognition – Voice input
Microsoft Edge TTS – Natural voices
Pygame Community – Audio playback

---

📞 Support

Check Troubleshooting
Open an Issue
Contact Dev Team

---

Made with ❤ by Aditya Verma
Your personal AI assistant, always at your service!
