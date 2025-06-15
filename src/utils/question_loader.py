import json
import os
import re
from typing import Dict, List, Optional

class QuestionLoader:
    def __init__(self):
        self.questions_cache: Dict[str, List[Dict]] = {}
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions')
    
    def _sanitize_section_name(self, section: str) -> str:
        """Convert section name to a valid filename."""
        # Extract the numeric part if it exists (e.g., "1.1" from "1.1" or "Limits and Continuity")
        match = re.match(r'(\d+\.\d+)', section)
        if match:
            return match.group(1)
        # If no numeric part, use a simplified version of the section name
        return section.lower().replace(' ', '_').replace('&', 'and')
    
    def load_section_questions(self, chapter: int, section: str) -> List[Dict]:
        """Load all questions for a given chapter and section."""
        print("DEBUG: load_section_questions called with chapter =", chapter, "section =", section)
        # Sanitize the section name
        sanitized_section = self._sanitize_section_name(str(section))
        print("DEBUG: Sanitized section =", sanitized_section)
        file_name = f"chapter{chapter}_section{sanitized_section}.json"
        file_path = os.path.join(self.base_path, file_name)
        print("DEBUG: Trying to load file:", file_path)
        cache_key = f"{chapter}_{sanitized_section}"
        if cache_key in self.questions_cache:
            return self.questions_cache[cache_key]
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.questions_cache[cache_key] = data['questions']
                return data['questions']
        except FileNotFoundError:
            print(f"Warning: No questions found for Chapter {chapter}, Section {sanitized_section}")
            return []
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """Get a specific question by its ID (format: chapter.section.question)."""
        try:
            chapter, section, _ = question_id.split('.')
            questions = self.load_section_questions(int(chapter), section)
            return next((q for q in questions if q['id'] == question_id), None)
        except Exception as e:
            print(f"Error getting question by ID: {e}")
            return None
    
    def get_question_steps(self, question_id: str) -> Optional[List[Dict]]:
        """Get the steps for a specific question."""
        question = self.get_question_by_id(question_id)
        return question.get('steps') if question else None
    
    def get_similar_question_template(self, question_id: str) -> Optional[Dict]:
        """Get the template for generating similar questions."""
        question = self.get_question_by_id(question_id)
        if not question:
            return None
            
        # Create a template based on the question type
        template = {
            'type': question['type'],
            'structure': question['text'],
            'steps': question['steps']
        }
        return template 
