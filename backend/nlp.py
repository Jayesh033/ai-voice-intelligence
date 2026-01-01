import spacy
from transformers import pipeline
import re

# Load models once with error handling
print("Loading NLP models...")

try:
    nlp = spacy.load("en_core_web_sm")  # Using smaller, more reliable model
    print("✓ spaCy model loaded")
except:
    print("! spaCy model not found. Installing...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

try:
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # Force CPU
    )
    print("✓ Sentiment model loaded")
except Exception as e:
    print(f"! Sentiment model error: {e}")
    sentiment_model = None

print("Models ready!")

def extract_dynamic_insights(text: str) -> dict:
    """
    Extract context-aware insights using rule-based NER and pattern matching.
    This is more reliable than LLM-based extraction.
    """
    try:
        doc = nlp(text)
        insights = []
        
        # Extract people (PERSON entities)
        people = list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"]))
        if people:
            insights.append({
                "category": "👤 People",
                "items": people[:10]
            })
        
        # Extract organizations
        orgs = list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
        if orgs:
            insights.append({
                "category": "🏢 Organizations",
                "items": orgs[:10]
            })
        
        # Extract locations
        locations = list(set([ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]))
        if locations:
            insights.append({
                "category": "📍 Locations",
                "items": locations[:10]
            })
        
        # Extract dates and times
        dates = list(set([ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]))
        if dates:
            insights.append({
                "category": "📅 Dates & Times",
                "items": dates[:10]
            })
        
        # Extract monetary amounts
        money = list(set([ent.text for ent in doc.ents if ent.label_ == "MONEY"]))
        if money:
            insights.append({
                "category": "💰 Amounts",
                "items": money[:10]
            })
        
        # Extract percentages and rates
        percentages = list(set([ent.text for ent in doc.ents if ent.label_ == "PERCENT"]))
        if percentages:
            insights.append({
                "category": "📊 Rates/Percentages",
                "items": percentages[:10]
            })
        
        # Extract cardinal numbers (quantities, counts)
        numbers = list(set([ent.text for ent in doc.ents if ent.label_ == "CARDINAL"]))
        if numbers:
            insights.append({
                "category": "🔢 Numbers",
                "items": numbers[:10]
            })
        
        # Extract action items (sentences with modal verbs and future indicators)
        action_patterns = r'\b(will|should|must|need to|have to|going to|needs to|required to|planning to)\b'
        action_items = []
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if re.search(action_patterns, sent_text, re.IGNORECASE) and len(sent_text.split()) > 5:
                action_items.append(sent_text)
        
        if action_items:
            insights.append({
                "category": "✅ Action Items",
                "items": action_items[:5]
            })
        
        # Extract questions (for understanding discussion points)
        questions = [sent.text.strip() for sent in doc.sents if sent.text.strip().endswith('?')]
        if questions:
            insights.append({
                "category": "❓ Questions Discussed",
                "items": questions[:5]
            })
        
        # Generate brief summary
        summary = generate_summary(text, doc)
        
        return {
            "insights": insights,
            "summary": summary
        }
    except Exception as e:
        print(f"Error in extract_dynamic_insights: {e}")
        return {"insights": [], "summary": ""}

def generate_summary(text: str, doc) -> str:
    """
    Generate a brief summary of the conversation.
    """
    try:
        # Get first few sentences as summary
        sentences = [sent.text.strip() for sent in doc.sents]
        if len(sentences) > 0:
            # Take first 2-3 sentences or up to 200 chars
            summary_parts = []
            char_count = 0
            for sent in sentences[:5]:
                if char_count + len(sent) < 300:
                    summary_parts.append(sent)
                    char_count += len(sent)
                else:
                    break
            
            if summary_parts:
                return " ".join(summary_parts)
        
        return text[:300] + "..." if len(text) > 300 else text
    except:
        return ""

def extract_key_phrases(text: str) -> list:
    """
    Extract important noun phrases and key terms.
    """
    try:
        doc = nlp(text)
        key_phrases = []
        
        # Get noun chunks with filtering
        for chunk in doc.noun_chunks:
            # Skip very short phrases and keep meaningful ones
            chunk_text = chunk.text.strip()
            if len(chunk_text.split()) >= 2 and len(chunk_text) > 5:
                # Skip if it's just articles and common words
                if chunk.root.pos_ in ["NOUN", "PROPN"]:
                    key_phrases.append(chunk_text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_phrases = []
        for phrase in key_phrases:
            phrase_lower = phrase.lower()
            if phrase_lower not in seen and len(unique_phrases) < 15:
                seen.add(phrase_lower)
                unique_phrases.append(phrase)
        
        return unique_phrases[:12]
    except Exception as e:
        print(f"Error extracting key phrases: {e}")
        return []

def analyze_text(text: str):
    """
    Main analysis function that coordinates all NLP tasks.
    """
    try:
        doc = nlp(text)

        # -------- ENTITY EXTRACTION --------
        entities = {}
        for ent in doc.ents:
            entities.setdefault(ent.label_, set()).add(ent.text)

        entities = {k: list(v)[:15] for k, v in entities.items()}  # Limit entities per type

        # -------- KEY SENTENCES --------
        key_sentences = []
        
        # Prioritize sentences with named entities
        entity_sentences = []
        for sent in doc.sents:
            if any(ent.text in sent.text for ent in doc.ents):
                entity_sentences.append(sent.text.strip())
        
        # Take up to 5 entity-rich sentences
        key_sentences = entity_sentences[:5]
        
        # If not enough, add first few sentences
        if len(key_sentences) < 3:
            all_sentences = [sent.text.strip() for sent in doc.sents]
            for sent in all_sentences[:5]:
                if sent not in key_sentences:
                    key_sentences.append(sent)
                if len(key_sentences) >= 5:
                    break

        # -------- SENTIMENT --------
        sentiment = {"label": "NEUTRAL", "score": 0.5}
        if sentiment_model:
            try:
                sentiment = sentiment_model(text[:512])[0]
            except Exception as e:
                print(f"Sentiment analysis error: {e}")

        # -------- DYNAMIC INSIGHTS --------
        dynamic_insights = extract_dynamic_insights(text)

        # -------- KEY PHRASES --------
        key_phrases = extract_key_phrases(text)

        return {
            "sentiment": sentiment,
            "entities": entities,
            "key_sentences": key_sentences,
            "dynamic_insights": dynamic_insights,
            "key_phrases": key_phrases
        }
    except Exception as e:
        print(f"Error in analyze_text: {e}")
        # Return minimal valid response
        return {
            "sentiment": {"label": "NEUTRAL", "score": 0.5},
            "entities": {},
            "key_sentences": [text[:500]] if text else [],
            "dynamic_insights": {"insights": [], "summary": text[:300] if text else ""},
            "key_phrases": []
        }