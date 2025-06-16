import requests
import re
import logging
import html

logger = logging.getLogger(__name__)

def generate_flashcards(content, num_flashcards=5):
    # Enhanced prompt with strict formatting requirements
    prompt = (
        f"Create exactly {num_flashcards} flashcards from the text below. Focus exclusively on key concepts.\n\n"
        f"Format each flashcard EXACTLY as:\n"
        f"Q: <clear question about the text ending with '?'>\n"
        f"A: <concise answer (1 simple sentence only)>\n\n"
        f"Critical Rules:\n"
        f"1. Start each flashcard with 'Q:' followed immediately by a question\n"
        f"2. Follow immediately with 'A:' and the answer\n"
        f"3. Answers must be ONE sentence ONLY - no lists, numbers, or multiple sentences\n"
        f"4. Do NOT include any numbering, titles, or additional text\n"
        f"5. Do NOT include chemical equations in answers\n"
        f"6. Do NOT mention these rules in your response\n"
        f"7. Ensure each flashcard covers a unique concept\n\n"
        f"Text to convert:\n{content.strip()}"
    )

    try:
        logger.debug(f"Sending prompt to model: {prompt[:300]}...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        generated_text = result.get("response", "").strip()
        logger.debug(f"Raw model response:\n{generated_text}")

        if not generated_text:
            logger.error("Error: Empty response from model")
            return []

        flashcards = parse_flashcards(generated_text, num_flashcards)
        
        # If we got fewer than requested, create placeholder cards
        if len(flashcards) < num_flashcards:
            logger.warning(f"Only generated {len(flashcards)} cards, adding placeholders")
            for i in range(len(flashcards), num_flashcards):
                flashcards.append({
                    "question": f"Key concept {i+1} could not be generated",
                    "answer": "Please try different text or rephrase your input"
                })
        
        logger.debug(f"Final flashcards count: {len(flashcards)}")
        return flashcards

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    return []

def parse_flashcards(text, max_count=5):
    """Robust flashcard parsing with multiple strategies"""
    flashcards = []
    
    # Strategy 1: Direct Q/A pairs
    qa_pairs = re.findall(
        r'Q:\s*(.*?\?)\s*A:\s*(.*?)(?=(?:\s*Q:)|$)', 
        text, 
        re.IGNORECASE | re.DOTALL
    )
    for question, answer in qa_pairs:
        flashcards.append({
            "question": clean_text(question),
            "answer": clean_text(answer)
        })
        if len(flashcards) >= max_count:
            return flashcards
    
    logger.debug(f"Direct parsing found {len(flashcards)} cards")
    
    # Strategy 2: Split-based parsing
    if len(flashcards) < max_count:
        segments = re.split(r'\s*Q:\s*', text, flags=re.IGNORECASE)
        # Remove empty segments
        segments = [s.strip() for s in segments if s.strip()]
        
        for seg in segments:
            if len(flashcards) >= max_count:
                break
                
            # Split on first occurrence of "A:"
            parts = re.split(r'\s*A:\s*', seg, maxsplit=1, flags=re.IGNORECASE)
            if len(parts) < 2:
                continue
                
            question = parts[0].strip()
            answer = parts[1].strip()
            
            # Remove any trailing Q markers
            answer = re.split(r'\s*Q:\s*', answer, flags=re.IGNORECASE)[0].strip()
            
            # Ensure proper question formatting
            question = ensure_question(clean_text(question))
            
            if question and answer:
                flashcards.append({
                    "question": question,
                    "answer": clean_text(answer)
                })
        logger.debug(f"Split parsing found {len(flashcards)} cards")
    
    # Strategy 3: Line-by-line parsing
    if len(flashcards) < max_count:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        current_q = None
        
        for line in lines:
            if len(flashcards) >= max_count:
                break
                
            # Detect question lines
            if re.match(r'^(Q:|Question:|\d+[.)]?\s+)\s*', line, re.IGNORECASE):
                if current_q:
                    # Add previous question
                    flashcards.append({
                        "question": ensure_question(clean_text(current_q)),
                        "answer": "Answer not parsed"
                    })
                current_q = re.sub(r'^(Q:|Question:|\d+[.)]?\s+)\s*', '', line, flags=re.IGNORECASE)
            
            # Detect answer lines
            elif re.match(r'^(A:|Answer:|Ans:)\s*', line, re.IGNORECASE) and current_q:
                answer = re.sub(r'^(A:|Answer:|Ans:)\s*', '', line, flags=re.IGNORECASE)
                flashcards.append({
                    "question": ensure_question(clean_text(current_q)),
                    "answer": clean_text(answer)
                })
                current_q = None
            
            # Continuation of answer
            elif current_q and flashcards and flashcards[-1]["question"] == ensure_question(clean_text(current_q)):
                flashcards[-1]["answer"] += " " + clean_text(line)
        
        # Add final question if exists
        if current_q and len(flashcards) < max_count:
            flashcards.append({
                "question": ensure_question(clean_text(current_q)),
                "answer": "Answer not parsed"
            })
        logger.debug(f"Line parsing found {len(flashcards)} cards")
    
    # Post-processing: Clean and deduplicate cards
    clean_cards = []
    seen_questions = set()
    
    for card in flashcards:
        # Clean answer text
        answer = clean_text(card['answer'])
        # Remove trailing numbers and special characters
        answer = re.sub(r'[0-9]+\.\s*', '', answer)
        answer = re.sub(r'^\s*[-*•]\s*', '', answer)
        # Take only the first sentence
        answer = answer.split('.')[0] + '.' if '.' in answer else answer
        
        # Clean question text
        question = clean_text(card['question'])
        # Remove HTML entities
        question = html.unescape(question)
        
        # Deduplicate based on question
        question_key = question[:30].lower()
        if question_key not in seen_questions:
            clean_cards.append({
                "question": ensure_question(question),
                "answer": answer
            })
            seen_questions.add(question_key)
    
    return clean_cards[:max_count]

def clean_text(text):
    """Clean and normalize text"""
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special prefix characters
    text = re.sub(r'^[-*•]\s*', '', text)
    # Remove quotes
    text = re.sub(r'^["\'](.*)["\']$', r'\1', text)
    return text.strip()

def ensure_question(text):
    """Ensure text ends with a question mark"""
    if not text.endswith('?'):
        return text.rstrip('.!') + '?'
    return text