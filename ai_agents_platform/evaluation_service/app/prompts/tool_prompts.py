GRAMMAR_EVALUATION_PROMPT = """
Act as an expert English essay grader.
Evaluate the following text for grammatical correctness on a scale of 0 to 100.
Provide detailed constructive feedback highlighting subject-verb agreements, tense consistencies, and punctuation.
Strictly return a JSON formatted object containing exactly these fields:
- "score" (integer)
- "feedback" (string)
- "errors_found" (list of strings describing specific errors)

Text to evaluate:
{text}
"""

PRONUNCIATION_EVALUATION_PROMPT = """
You are an expert English Phonetics analyzer.
I will provide a 'transcribed' text (what the user actually said) and an 'expected' text (what they should have said).
Compare them carefully. Deduct points for missing words, significantly mispronounced words, and hesitations.
Strictly return a JSON formatted object containing exactly these fields:
- "score" (integer out of 100)
- "feedback" (string containing overall impression)
- "mispronounced_words" (list of strings capturing significantly incorrect words)

Transcribed text: '{transcribed}'
Expected text: '{expected}'
"""
