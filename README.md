# Interactive Flashcard Generator

![Flashcard Generator Demo]

Transform any educational text into interactive flashcards using AI. This web application leverages TinyLLaMA to generate question-answer pairs from your input text, creating an efficient learning experience.

## Features
- 🧠 AI-powered flashcard generation
- 📱 Responsive mobile-friendly design
- 🔄 Interactive flashcard navigation
- 📊 Learning progress tracking
- ✅ Knowledge mastery feedback
- ⚡ Real-time processing

## Installation & Setup

### Prerequisites
- Python 3.9+
- Ollama installed ([installation guide](https://ollama.com/download))
- TinyLLaMA model installed: `ollama pull tinyllama`

### Steps
1. Clone repository:
```bash
git clone https://github.com/yourusername/flashcard-generator.git
cd flashcard-generator
```
## Project Structure
```
project-root/
├── app.py
├── utils/
│   └── llm_flashcard_generator.py
├── templates/
│   └── index.html
└── requirements.txt
```
## Usage Instructions

1. Paste text into input box
2. Click "Generate Flashcards"
3. Navigate cards with Previous/Next buttons
4. Track progress via statistics panel

## Troubleshooting Tips

- No flashcards? Ensure Ollama is running (`ollama serve`)
- Empty responses? Try simpler/shorter text
- Installation issues? Verify Python ≥3.9
