import random
from typing import List, Optional
from app.models.interview import (
    InterviewQuestion,
    InterviewResponse,
    InterviewFeedback,
    InterviewSession
)


class InterviewEngine:
    """
    Generates interview questions and evaluates answers.
    Uses built-in question banks. In production, this calls OpenAI API.
    """
    
    # Question banks by category
    QUESTIONS = {
        "behavioral": [
            {"question": "Tell me about a time you faced a difficult challenge at work.", "difficulty": "medium"},
            {"question": "Describe a situation where you had to work with a difficult teammate.", "difficulty": "hard"},
            {"question": "Give an example of a goal you set and how you achieved it.", "difficulty": "easy"},
            {"question": "Tell me about a time you failed and what you learned.", "difficulty": "medium"},
            {"question": "Describe a time you had to make a decision without complete information.", "difficulty": "hard"},
        ],
        "technical": [
            {"question": "Explain the difference between a list and a tuple in Python.", "difficulty": "easy"},
            {"question": "What is REST API and how does it work?", "difficulty": "medium"},
            {"question": "Explain database normalization and why it's important.", "difficulty": "medium"},
            {"question": "How would you design a scalable web application?", "difficulty": "hard"},
            {"question": "What are the key differences between SQL and NoSQL databases?", "difficulty": "medium"},
        ],
        "situational": [
            {"question": "Your project deadline is tomorrow but you found a critical bug. What do you do?", "difficulty": "hard"},
            {"question": "A stakeholder keeps changing requirements mid-sprint. How do you handle it?", "difficulty": "medium"},
            {"question": "You disagree with your manager's technical decision. What do you do?", "difficulty": "medium"},
            {"question": "How would you onboard a new junior developer to your team?", "difficulty": "easy"},
        ]
    }
    
    def generate_questions(
        self,
        category: str = "behavioral",
        count: int = 3,
        difficulty: Optional[str] = None
    ) -> List[InterviewQuestion]:
        """
        Generate a list of interview questions.
        """
        bank = self.QUESTIONS.get(category, self.QUESTIONS["behavioral"])
        
        # Filter by difficulty if specified
        if difficulty:
            bank = [q for q in bank if q["difficulty"] == difficulty]
        
        # If not enough questions, use all available
        selected = random.sample(bank, min(count, len(bank)))
        
        questions = []
        for q in selected:
            questions.append(
                InterviewQuestion(
                    category=category,
                    question=q["question"],
                    difficulty=q["difficulty"]
                )
            )
        
        return questions
    
    def evaluate_answer(
        self,
        question: InterviewQuestion,
        response: InterviewResponse
    ) -> InterviewFeedback:
        """
        Evaluate a user's answer and return feedback.
        Uses simple heuristics. In production, uses OpenAI API.
        """
        answer = response.user_answer.lower().strip()
        answer_length = len(answer.split())
        
        # Simple scoring heuristic
        score = 50.0  # Base score
        
        # Length check
        if answer_length < 10:
            score -= 20
            length_feedback = "Your answer is quite short. Try to provide more detail."
        elif answer_length > 50:
            score += 10
            length_feedback = "Good level of detail in your answer."
        else:
            length_feedback = "Adequate length, but you could expand further."
        
        # Keyword checks based on category
        keywords = self._get_keywords_for_question(question)
        matched_keywords = [k for k in keywords if k.lower() in answer]
        
        if matched_keywords:
            score += len(matched_keywords) * 5
            keyword_feedback = f"Good use of relevant concepts: {', '.join(matched_keywords)}."
        else:
            keyword_feedback = "Try to include more specific technical terms or frameworks relevant to the question."
        
        # Cap score
        score = max(0, min(100, score))
        
        # Generate model answer
        model_answer = self._generate_model_answer(question)
        
        # Determine strengths and improvements
        if score >= 80:
            strengths = "Strong answer with good structure and relevant points."
            improvements = "Consider adding a specific example to make it even stronger."
        elif score >= 60:
            strengths = f"Decent answer. {length_feedback}"
            improvements = f"{keyword_feedback} Also, try to structure your answer using the STAR method (Situation, Task, Action, Result)."
        else:
            strengths = "You attempted the question, which is a good start."
            improvements = f"{length_feedback} {keyword_feedback} Practice framing your experiences with clear outcomes."
        
        return InterviewFeedback(
            question_id=response.question_id,
            score=round(score, 2),
            strengths=strengths,
            improvements=improvements,
            model_answer=model_answer
        )
    
    def _get_keywords_for_question(self, question: InterviewQuestion) -> List[str]:
        """Return relevant keywords for a question."""
        keyword_map = {
            "Python": ["python", "list", "tuple", "mutable", "immutable", "data structure"],
            "REST API": ["http", "endpoint", "json", "stateless", "client", "server"],
            "database": ["normalization", "redundancy", "tables", "relations", "schema"],
            "scalable": ["load balancer", "cache", "database", "microservices", "cdn", "horizontal"],
            "SQL": ["relational", "tables", "joins", "acid", "schema"],
            "NoSQL": ["document", "mongodb", "cassandra", "flexible", "scaling"],
            "challenge": ["problem", "solution", "result", "learned", "overcame"],
            "teammate": ["communication", "collaboration", "conflict", "resolution"],
            "goal": ["plan", "steps", "achieved", "measurable", "timeline"],
            "failed": ["lesson", "growth", "reflection", "improvement"],
            "decision": ["analysis", "risk", "outcome", "data", "intuition"],
            "deadline": ["prioritize", "communicate", "quality", "stakeholder"],
            "stakeholder": ["communication", "expectations", "scope", "agile"],
            "disagree": ["respect", "discussion", "evidence", "compromise"],
            "onboard": ["mentorship", "documentation", "support", "feedback"],
        }
        
        # Find matching keywords
        q_lower = question.question.lower()
        found = []
        for key, words in keyword_map.items():
            if key.lower() in q_lower:
                found.extend(words)
        return found
    
    def _generate_model_answer(self, question: InterviewQuestion) -> str:
        """Generate a model/example answer for a question."""
        templates = {
            "behavioral": "Use the STAR method: Describe the Situation, explain your Task, detail the Action you took, and share the Result. Include specific metrics if possible.",
            "technical": "Provide a clear, structured explanation. Start with a definition, explain how it works with an example, and mention when to use it. Include code snippets if relevant.",
            "situational": "Outline your approach step-by-step. Mention who you would communicate with, what factors you consider, and how you balance competing priorities.",
        }
        return templates.get(question.category, "Provide a clear, structured answer with specific examples.")
    
    def create_session(self, user_id: str, category: str, question_count: int = 3) -> InterviewSession:
        """
        Create a new interview session with generated questions.
        """
        questions = self.generate_questions(category=category, count=question_count)
        return InterviewSession(
            user_id=user_id,
            questions=questions,
            status="in_progress"
        )