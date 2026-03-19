class VocabularyAnalyzer:
    """Tool to assess vocabulary diversity and richness in the passage."""
    
    def analyze(self, text: str) -> dict:
        # Mock logic based on unique words vs total words (Type-Token Ratio)
        words = text.lower().split()
        unique_words = set(words)
        richness_score = len(unique_words) / len(words) if words else 0
        
        return {
            "total_words": len(words),
            "unique_words": len(unique_words),
            "richness_score": round(richness_score * 100, 2),
            "feedback": "Good variety of words used throughout the passage."
        }
