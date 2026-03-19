QUESTIONS_PROMPT = """
You are an expert academic examiner and subject matter expert tasked with compiling high-quality assessment questions.
Generate exactly {count} {difficulty}-level multiple-choice questions covering the specific topic: '{topic}'.
Each question should be academically challenging, technically accurate, and unambiguously written.
Do not include conversational filler in your response. Ensure the output strictly conforms to a raw JSON array of objects.
Each object MUST have exactly these fields: "question", "options" (a dictionary with keys "a.", "b.", "c.", "d."), "correct_answer" (the key of the correct option, e.g., "a."), and "explanation".
Output ONLY the raw JSON.
"""

PASSAGE_PROMPT = """
You are a master storyteller and professional educational examiner.
Generate a highly readable and academically sound reading passage strictly revolving around the topic: '{topic}'.
The passage should be approximately {length_words} words in length.

Additionally, generate exactly {count} {difficulty}-level multiple-choice questions based ONLY on the information provided in the passage.
Each question should be academically challenging, technically accurate, and unambiguously written.

Do not include conversational filler in your response. Ensure the output strictly conforms to a raw JSON object with these fields:
"passage": "The generated passage text",
"questions": [
    {{
        "question": "question text",
        "options": {{ "a.": "option 1", "b.": "option 2", "c.": "option 3", "d.": "option 4" }},
        "correct_answer": "a.",
        "explanation": "why this answer is correct"
    }}
]

Output ONLY the raw JSON.
"""
