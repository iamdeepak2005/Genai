class ReadingEvaluator:
    """Tool to analyze reading quality and classify the user."""
    
    def evaluate(self, user_audio_ref: str, expected_text: str) -> dict:
        # Mock logic based on word-per-minute or accuracy
        classification = "Good Reader"  # Could be Good, Average, or Bad Reader based on evaluation logic
        
        return {
            "wpm": 150,
            "accuracy_percentage": 92,
            "classification": classification,
            "feedback": f"Maintains a steady pace, categorized as {classification}."
        }
