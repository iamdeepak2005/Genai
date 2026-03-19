import os
import json
import whisper
from pydub import AudioSegment
from openai import OpenAI
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from app.prompts.tool_prompts import GRAMMAR_EVALUATION_PROMPT, PRONUNCIATION_EVALUATION_PROMPT

@tool(return_direct=True)
def evaluate_grammar(text: str) -> dict:
    """Evaluate grammar of a text and return scores and feedback."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = GRAMMAR_EVALUATION_PROMPT.format(text=text)
    response = llm.invoke(prompt).content
    try:
        if response.startswith("```json"):
            response = response[7:-4]
        return json.loads(response)
    except:
        return {"score": 80, "feedback": "Parse error, assuming good.", "errors_found": []}

@tool(return_direct=True)
def evaluate_reading_classification(word_count: int, reading_time_seconds: int, accuracy_score: int) -> dict:
    """Classify user as Good, Average, or Bad reader based on WPM and accuracy."""
    wpm = int((word_count / max(reading_time_seconds, 1)) * 60)
    classification = "Average Reader"
    if wpm > 120 and accuracy_score > 90:
        classification = "Good Reader"
    elif wpm < 80 or accuracy_score < 70:
        classification = "Bad Reader"
    return {"wpm": wpm, "accuracy_score": accuracy_score, "classification": classification}

@tool(return_direct=True)
def analyze_vocabulary(text: str) -> dict:
    """Analyze vocabulary richness."""
    words = text.lower().split()
    unique_words = set(words)
    richness_score = len(unique_words) / max(len(words), 1)
    return {
        "total_words": len(words),
        "unique_words": len(unique_words),
        "richness_score": round(richness_score * 100, 2),
        "feedback": "Calculated Type-Token Ratio."
    }

class EvaluationAgent:
    _whisper_model = None

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key"))
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
    @property
    def whisper_model(self):
        if EvaluationAgent._whisper_model is None:
            print("Loading Whisper model...")
            EvaluationAgent._whisper_model = whisper.load_model("base")
        return EvaluationAgent._whisper_model

    def _preprocess_audio(self, audio_path: str) -> str:
        """Process audio with FFmpeg (via pydub) to ensure it's in a format Whisper likes."""
        try:
            track = AudioSegment.from_file(audio_path)
            # Normalize: 16kHz, Mono, WAV
            track = track.set_frame_rate(16000).set_channels(1)
            normalized_path = audio_path + ".normalized.wav"
            track.export(normalized_path, format="wav")
            return normalized_path
        except Exception as e:
            print(f"Error preprocessing audio: {e}")
            return audio_path

    def _transcribe_audio(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            return "This is a mock transcription because the audio file was not found."
            
        # 1. Preprocess with FFmpeg
        processed_path = self._preprocess_audio(audio_path)
        
        # 2. Transcribe using local Whisper (which uses FFmpeg internally for loading)
        try:
            result = self.whisper_model.transcribe(processed_path)
            transcript = result.get("text", "").strip()
            
            # Cleanup temporary file if it was created
            if processed_path != audio_path and os.path.exists(processed_path):
                os.remove(processed_path)
                
            return transcript
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return "Transcription failed."

    def _evaluate_pronunciation(self, transcribed: str, expected: str) -> dict:
        prompt = PRONUNCIATION_EVALUATION_PROMPT.format(transcribed=transcribed, expected=expected)
        response = self.llm.invoke(prompt).content
        try:
            if response.startswith("```json"):
                response = response[7:-4]
            return json.loads(response)
        except:
            return {"score": 80, "feedback": "Evaluation failed to parse.", "mispronounced_words": []}

    async def process_request(self, action: str, parameters: dict) -> dict:
        text = parameters.get("text", "")
        audio_ref = parameters.get("user_audio_ref", "none")
        expected_text = parameters.get("expected_text", text)

        transcription = text
        if action in ["evaluate_all", "pronunciation_eval", "reading_eval"]:
            transcription = self._transcribe_audio(audio_ref)
        
        # If transcription is available but text was not provided, use transcription for grammar/vocab
        if transcription and not text:
            text = transcription

        result = {}
        if action in ["evaluate_all", "grammar_eval"]:
            result["grammar"] = evaluate_grammar.invoke({"text": text})
            
        if action in ["evaluate_all", "pronunciation_eval"]:
            result["pronunciation"] = self._evaluate_pronunciation(transcription, expected_text)
            
        if action in ["evaluate_all", "reading_eval"]:
            word_count = len(expected_text.split())
            reading_time = parameters.get("reading_time_seconds", 30)
            accuracy = result.get("pronunciation", {}).get("score", 85)
            result["reading"] = evaluate_reading_classification.invoke({
                "word_count": word_count, 
                "reading_time_seconds": reading_time, 
                "accuracy_score": accuracy
            })
            
        if action in ["evaluate_all", "vocabulary_eval"]:
            result["vocabulary"] = analyze_vocabulary.invoke({"text": text})
            
        if not result:
            raise ValueError(f"Unknown valid action: {action}")
            
        return result
