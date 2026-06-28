import re
import pdfplumber
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ParsedResume:
    raw_text: str = ""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    sections: Dict[str, str] = field(default_factory=dict)


@dataclass
class ResumeScore:
    overall_score: int = 0
    section_scores: Dict = field(default_factory=dict)
    missing_sections: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class ResumeParser:
    phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    section_patterns = {
        'summary': r'(?:professional\s+)?summary|objective|profile|about\s+me',
        'experience': r'experience|employment|work\s+history|professional\s+experience|work\s+experience',
        'education': r'education|academic|qualifications|educational\s+background',
        'skills': r'skills|technical\s+skills|core\s+competencies|expertise',
        'projects': r'projects|personal\s+projects|academic\s+projects',
        'certifications': r'certifications|certificates|licenses',
        'achievements': r'achievements|awards|honors|leadership|accomplishments',
    }
    
    skill_keywords = [
        'python', 'java', 'javascript', 'js', 'typescript', 'html', 'css', 'react',
        'node', 'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'docker', 'git',
        'excel', 'word', 'powerpoint', 'photoshop', 'figma', 'canva', 'seo',
        'marketing', 'sales', 'leadership', 'communication', 'management',
        'business development', 'brand management', 'market research',
        'customer relationship', 'content writing', 'social media',
        'ms excel', 'ms word', 'ms powerpoint', 'adobe photoshop', 'capcut',
        'windows', 'macos', 'public speaking', 'team collaboration', 'problem solving',
        'digital marketing', 'strategic communication', 'customer engagement',
        'brand development', 'entrepreneurship', 'content creation'
    ]

    @classmethod
    def extract_text(cls, file_path: str) -> str:
        text = ""
        file_ext = file_path.lower().split(".")[-1]
        
        if file_ext == "pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif file_ext == "docx":
            try:
                import docx
                doc = docx.Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                raise Exception("python-docx not installed")
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
        
        return text

    @classmethod
    def extract_phone(cls, text: str) -> Optional[str]:
        matches = re.findall(cls.phone_pattern, text)
        
        if matches:
            best_match = max(matches, key=len)
            digits = re.sub(r'\D', '', best_match)
            
            if len(digits) == 10:
                return f"+91 {digits[:5]} {digits[5:]}"
            elif len(digits) == 11 and digits.startswith('0'):
                return f"+91 {digits[1:6]} {digits[6:]}"
            elif len(digits) == 12 and digits.startswith('91'):
                return f"+91 {digits[2:7]} {digits[7:]}"
            
            return best_match
        
        return None

    @classmethod
    def extract_email(cls, text: str) -> Optional[str]:
        match = re.search(cls.email_pattern, text)
        return match.group(0) if match else None

    @classmethod
    def extract_name(cls, text: str) -> Optional[str]:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        skip_words = ['resume', 'cv', 'curriculum', 'vitae']
        
        for line in lines[:5]:
            line_lower = line.lower()
            if not any(sw in line_lower for sw in skip_words):
                words = line.split()
                if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
                    return line
        
        for i, line in enumerate(lines[:10]):
            if '@' in line and i > 0:
                return lines[i-1].strip()
        
        return lines[0] if lines else None

    @classmethod
    def extract_sections(cls, text: str) -> Dict[str, str]:
        sections = {}
        text_lower = text.lower()
        
        positions = []
        for section_name, pattern in cls.section_patterns.items():
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                positions.append((match.start(), section_name))
        
        positions.sort()
        
        for i, (start, name) in enumerate(positions):
            end = positions[i+1][0] if i+1 < len(positions) else len(text)
            section_text = text[start:end].strip()
            lines = section_text.split('\n')
            sections[name] = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
        
        return sections

    @classmethod
    def extract_skills(cls, text: str) -> List[str]:
        found = []
        text_lower = text.lower()
        
        for skill in cls.skill_keywords:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill.title())
        
        sections = cls.extract_sections(text)
        if 'skills' in sections:
            skills_text = sections['skills'].lower()
            for skill in cls.skill_keywords:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, skills_text) and skill.title() not in found:
                    found.append(skill.title())
        
        return list(set(found))

    @classmethod
    def parse_file(cls, file_path: str) -> ParsedResume:
        raw_text = cls.extract_text(file_path)
        
        if not raw_text.strip():
            raise Exception("Could not extract text. Is this a scanned image PDF?")
        
        sections = cls.extract_sections(raw_text)
        
        # Convert section text to list items for analyzer compatibility
        experience_list = [line.strip() for line in sections.get('experience', '').split('\n') if line.strip() and len(line.strip()) > 10]
        education_list = [line.strip() for line in sections.get('education', '').split('\n') if line.strip() and len(line.strip()) > 5]
        projects_list = [line.strip() for line in sections.get('projects', '').split('\n') if line.strip() and len(line.strip()) > 5]
        
        return ParsedResume(
            raw_text=raw_text[:3000],
            name=cls.extract_name(raw_text),
            email=cls.extract_email(raw_text),
            phone=cls.extract_phone(raw_text),
            skills=cls.extract_skills(raw_text),
            experience=experience_list,
            education=education_list,
            projects=projects_list,
            sections=sections
        )