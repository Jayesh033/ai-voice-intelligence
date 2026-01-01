from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import assemblyai as aai
from nlp import analyze_text
import traceback

app = FastAPI(title="Audio Analysis API - AssemblyAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Configure AssemblyAI
ASSEMBLYAI_API_KEY = "################"  # Replace with your actual API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

print("✓ AssemblyAI configured")

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Audio Analysis API with AssemblyAI",
        "transcriber": "AssemblyAI"
    }

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analyze uploaded audio using AssemblyAI for better accuracy.
    """
    file_path = None
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print(f"Saving file to: {file_path}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"File saved, transcribing with AssemblyAI...")
        
        # Configure transcription settings
        config = aai.TranscriptionConfig(
            speaker_labels=True,  # Identify different speakers
            auto_highlights=True,  # Auto extract important moments
            entity_detection=True,  # Detect names, locations, etc.
            sentiment_analysis=True,  # Built-in sentiment
            punctuate=True,
            format_text=True
        )
        
        # Transcribe
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path, config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")
        
        transcription = transcript.text
        print(f"Transcription complete ({len(transcription)} chars)")
        
        # Get AssemblyAI's entity detection - safely check for entities
        entities_detected = []
        if hasattr(transcript, 'entities') and transcript.entities:
            for entity in transcript.entities:
                entity_dict = {
                    "text": entity.text,
                    "type": entity.entity_type
                }
                entities_detected.append(entity_dict)
        
        # Get sentiment from AssemblyAI - check different possible attribute names
        sentiments = []
        sentiment_results = None
        
        # Try different attribute names
        if hasattr(transcript, 'sentiment_analysis_results'):
            sentiment_results = transcript.sentiment_analysis_results
        elif hasattr(transcript, 'sentiment_analysis'):
            sentiment_results = transcript.sentiment_analysis
        
        if sentiment_results:
            for sentiment in sentiment_results:
                sent_dict = {
                    "text": getattr(sentiment, 'text', ''),
                    "sentiment": getattr(sentiment, 'sentiment', 'NEUTRAL')
                }
                if hasattr(sentiment, 'confidence'):
                    sent_dict["confidence"] = sentiment.confidence
                sentiments.append(sent_dict)
        
        # Do our NLP analysis
        print("Running additional NLP analysis...")
        analysis = analyze_text(transcription)
        
        # Merge AssemblyAI insights with our analysis
        if entities_detected:
            analysis["assemblyai_entities"] = entities_detected
        
        if sentiments:
            analysis["assemblyai_sentiments"] = sentiments
        
        # Get auto highlights
        highlights = []
        if hasattr(transcript, 'auto_highlights') and transcript.auto_highlights:
            if hasattr(transcript.auto_highlights, 'results') and transcript.auto_highlights.results:
                for highlight in transcript.auto_highlights.results[:10]:
                    highlight_dict = {
                        "text": highlight.text,
                        "count": getattr(highlight, 'count', 1)
                    }
                    if hasattr(highlight, 'timestamps'):
                        highlight_dict["timestamps"] = [
                            {"start": t.start, "end": t.end} for t in highlight.timestamps
                        ]
                    highlights.append(highlight_dict)
        
        if highlights:
            analysis["highlights"] = highlights
        
        # Get speaker information if available
        speakers_info = []
        if hasattr(transcript, 'utterances') and transcript.utterances:
            for utterance in transcript.utterances[:20]:  # Limit to first 20
                speakers_info.append({
                    "speaker": getattr(utterance, 'speaker', 'Unknown'),
                    "text": utterance.text,
                    "start": getattr(utterance, 'start', 0),
                    "end": getattr(utterance, 'end', 0)
                })
        
        if speakers_info:
            analysis["speakers"] = speakers_info
        
        # Get audio duration
        duration = None
        if hasattr(transcript, 'audio_duration'):
            duration = transcript.audio_duration
        
        return {
            "success": True,
            "transcription": transcription,
            "analysis": analysis,
            "file_info": {
                "filename": file.filename,
                "size_bytes": len(content),
                "duration_seconds": duration
            }
        }
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
        
    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
            except Exception as e:
                print(f"Could not delete file: {e}")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("Starting Audio Analysis API with AssemblyAI")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")