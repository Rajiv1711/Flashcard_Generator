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

## Future Improvements

### Enhanced AI Models
Upgrade to more powerful models for higher quality flashcards:

```bash
# Install LLaMA (7B parameters)
ollama pull llama

# Install Mistral (7B parameters - recommended)
ollama pull mistral
```

Then modify `utils/llm_flashcard_generator.py`:

```python
# Change from TinyLLaMA:
json={"model": "tinyllama", "prompt": prompt, "stream": False}

# To Mistral:
json={"model": "mistral", "prompt": prompt, "stream": False}

# Or to LLaMA:
json={"model": "llama", "prompt": prompt, "stream": False}
```

### Model Comparison

| Model      | Quality | Speed | RAM  | Best For         |
|------------|---------|-------|------|------------------|
| tinyllama  | ⭐⭐      | ⚡⚡⚡  | 1GB  | Quick testing     |
| llama      | ⭐⭐⭐⭐    | ⚡⚡   | 4GB  | Balanced quality  |
| mistral    | ⭐⭐⭐⭐⭐   | ⚡    | 5GB  | Premium results   |

### Advanced Configuration

For better control with larger models:

```python
json={
    "model": "mistral",
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.7,    # Creativity (0=strict, 1=creative)
        "num_ctx": 4096,       # Context window size
        "top_k": 40,           # Output diversity
        "num_predict": 500     # Max tokens to generate
    }
}
```

### Hardware Recommendations

- **TinyLLaMA**: Works on 4GB RAM systems  
- **LLaMA / Mistral**: Require at least 8GB RAM (16GB recommended)  
- **For GPU Acceleration**: Install NVIDIA drivers and CUDA toolkit

### Prompt Optimization

For best results with larger models, enhance your prompt:

```python
prompt = (
    f"Create exactly {num_flashcards} conceptual flashcards from the text.\n\n"
    f"Focus on relationships between ideas, not just facts.\n\n"
    f"Format EXACTLY as:\n"
    f"Q: <clear question ending with '?'>\n"
    f"A: <1-sentence answer>\n\n"
    f"Critical Rules:\n"
    f"- Questions must test understanding, not memorization\n"
    f"- Answers should explain concepts, not just state facts\n"
    f"- Never include equations or complex symbols\n\n"
    f"Text:\n{content.strip()}"
)
```

### Performance Tips

- **For long texts (>1000 words) with Mistral**:
  - Increase timeout to 300 seconds
  - Use `num_ctx: 8192` in options

- **For technical subjects**:
  - Add: `"Explain concepts in simple terms"` to prompt

- **For better retention**:
  - Add: `"Create questions that connect to real-world examples"` to prompt
