from flask import Flask, render_template, request, jsonify
from utils.llm_flashcard_generator import generate_flashcards
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form.get("text", "").strip()
        logger.debug(f"Received POST request with text: {input_text[:50]}...")
        
        if not input_text:
            return jsonify({"error": "Please enter some text to generate flashcards"}), 400
            
        try:
            flashcards = generate_flashcards(input_text)
            logger.debug(f"Generated {len(flashcards)} flashcards")
            
            # Debugging: Log actual flashcard content
            for i, card in enumerate(flashcards):
                logger.debug(f"Card {i+1}: Q: {card['question']} | A: {card['answer']}")
            
            return jsonify({"flashcards": flashcards})
        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            return jsonify({"error": "Flashcard generation failed. Please try again with different text."}), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)