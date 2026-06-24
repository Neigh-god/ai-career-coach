from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class SkillGapResult:
    target_role: str
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    matching_skills: List[str]
    skill_coverage_percent: float  # 0 to 100
    learning_recommendations: List[Dict[str, str]]  # e.g., [{"skill": "Docker", "resource": "Docker Docs"}]


class SkillGapAnalyzer:
    """
    Analyzes the gap between user's current skills and target role requirements.
    Uses a simple built-in mapping. In production, this would call an AI API.
    """
    
    # Built-in skill requirements for common roles
    ROLE_REQUIREMENTS: Dict[str, List[str]] = {
        "Software Engineer": ["Python", "Git", "Data Structures", "Algorithms", "SQL", "System Design"],
        "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Visualization"],
        "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
        "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript", "Web Performance"],
        "Backend Developer": ["Python", "Node.js", "Databases", "API Design", "Caching", "Microservices"],
    }
    
    def analyze(self, current_skills: List[str], target_role: str) -> SkillGapResult:
        """
        Compare current skills against target role requirements.
        """
        # Normalize inputs
        target_role = target_role.strip()
        current_skills_lower = [s.lower().strip() for s in current_skills]
        
        # Get required skills for the role
        required_skills = self.ROLE_REQUIREMENTS.get(target_role, [])
        if not required_skills:
            required_skills = []  # Unknown role
        
        required_lower = [s.lower().strip() for s in required_skills]
        
        # Find matches and gaps
        matching_skills = []
        missing_skills = []
        
        for req, req_lower in zip(required_skills, required_lower):
            if req_lower in current_skills_lower:
                matching_skills.append(req)
            else:
                missing_skills.append(req)
        
        # Calculate coverage percentage
        total_required = len(required_skills)
        if total_required > 0:
            coverage = (len(matching_skills) / total_required) * 100
        else:
            coverage = 0.0
        
        # Generate learning recommendations for missing skills
        recommendations = []
        for skill in missing_skills:
            recommendations.append({
                "skill": skill,
                "resource": f"Learn {skill} via official documentation or online courses",
                "priority": "high" if coverage < 50 else "medium"
            })
        
        return SkillGapResult(
            target_role=target_role,
            current_skills=current_skills,
            required_skills=required_skills,
            missing_skills=missing_skills,
            matching_skills=matching_skills,
            skill_coverage_percent=round(coverage, 2),
            learning_recommendations=recommendations
        )
    
    def get_supported_roles(self) -> List[str]:
        """Return list of roles we have skill data for."""
        return list(self.ROLE_REQUIREMENTS.keys())