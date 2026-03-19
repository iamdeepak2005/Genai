import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from app.prompts.tool_prompts import QUESTIONS_PROMPT, PASSAGE_PROMPT

@tool(return_direct=True)
def generate_questions(topic: str = "General Knowledge", difficulty: str = "Medium", count: int = 5) -> str:
    """Generate high-quality assessment questions based on topic, difficulty, and count. Returns a JSON string of questions."""
    print(f"--- Generating questions for topic: {topic}, difficulty: {difficulty}, count: {count} ---")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)
    prompt = QUESTIONS_PROMPT.format(count=count, difficulty=difficulty, topic=topic)
    response = llm.invoke(prompt)
    print("--- RAW LLM RESPONSE START ---")
    print(response.content)
    print("--- RAW LLM RESPONSE END ---")
    return response.content

@tool(return_direct=True)
def generate_passage(topic: str = "General Knowledge", length_words: int = 150, difficulty: str = "Medium", count: int = 5) -> str:
    """Generate a reading passage and multiple-choice questions based on topic, length, difficulty, and count. Returns a JSON string."""
    print(f"--- Generating passage and questions for topic: {topic}, length: {length_words} words, difficulty: {difficulty}, count: {count} ---")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)
    prompt = PASSAGE_PROMPT.format(topic=topic, length_words=length_words, difficulty=difficulty, count=count)
    response = llm.invoke(prompt)
    print("--- RAW LLM RESPONSE START ---")
    print(response.content)
    print("--- RAW LLM RESPONSE END ---")
    return response.content


class AdminAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.tools = [generate_questions, generate_passage]

    def _clean_json_response(self, response: str) -> str:
        """Strip markdown code blocks from the response string."""
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        return response.strip()

    def process_request(self, action: str, parameters: dict) -> dict:
        print(f"--- Processing request action: {action} ---")
        if action == "generate_questions":
            print(f"--- Generating questions for topic: {parameters.get('topic', 'General Knowledge')}, difficulty: {parameters.get('difficulty', 'Medium')}, count: {parameters.get('count', 5)} ---")
            res = generate_questions.invoke({
                "topic": parameters.get("topic", "General Knowledge"),
                "difficulty": parameters.get("difficulty", "Medium"),
                "count": parameters.get("count", 5)
            })
            try:
                # Clean and parse json string
                cleaned_res = self._clean_json_response(res) if isinstance(res, str) else res
                parsed_res = json.loads(cleaned_res) if isinstance(cleaned_res, str) else cleaned_res
                
                # Restructure questions into separate parts for storage/UI
                if isinstance(parsed_res, list):
                    questions = [q.get("question", "") for q in parsed_res]
                    options = [q.get("options", {}) for q in parsed_res]
                    explanations = [q.get("explanation", "") for q in parsed_res]
                    correct_answers = [q.get("correct_answer", "") for q in parsed_res]
                    
                    print(f"--- Successfully generated and restructured {len(questions)} items ---")
                    return {
                        "questions": questions,
                        "options": options,
                        "explanations": explanations,
                        "correct_answers": correct_answers
                    }
                return {"questions": parsed_res}
            except Exception as e:
                print(f"!!! Error parsing questions result: {e} !!!")
                return {"questions": res, "error": f"Could not parse as JSON: {str(e)}"}
            
        elif action == "generate_passage":
            print(f"--- Generating passage and questions for topic: {parameters.get('topic', 'General Knowledge')}, length: {parameters.get('length_words', 150)}, count: {parameters.get('count', 5)} ---")
            res = generate_passage.invoke({
                "topic": parameters.get("topic", "General Knowledge"),
                "length_words": parameters.get("length_words", 150),
                "difficulty": parameters.get("difficulty", "Medium"),
                "count": parameters.get("count", 5)
            })
            try:
                cleaned_res = self._clean_json_response(res) if isinstance(res, str) else res
                parsed_res = json.loads(cleaned_res) if isinstance(cleaned_res, str) else cleaned_res
                
                if isinstance(parsed_res, dict) and "questions" in parsed_res:
                    raw_questions = parsed_res["questions"]
                    if isinstance(raw_questions, list):
                        q_texts = [q.get("question", "") for q in raw_questions]
                        options = [q.get("options", {}) for q in raw_questions]
                        explanations = [q.get("explanation", "") for q in raw_questions]
                        correct_answers = [q.get("correct_answer", "") for q in raw_questions]
                        
                        print("--- Successfully generated and restructured passage and questions ---")
                        return {
                            "passage": parsed_res.get("passage", ""),
                            "questions": q_texts,
                            "options": options,
                            "explanations": explanations,
                            "correct_answers": correct_answers
                        }
                return parsed_res
            except Exception as e:
                print(f"!!! Error parsing passage result: {e} !!!")
                return {"passage": res, "error": f"Could not parse as JSON: {str(e)}"}
        else:
            print(f"!!! Unknown action attempted: {action} !!!")
            raise ValueError(f"Unknown action: {action}")
