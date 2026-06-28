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
    # Multiple patterns to catch various Indian phone formats
    phone_patterns = [
        r'\+91\s*\d{5}\s*\d{5}',           
        r'\+91\s*\d{10}',                    
        r'\+91[-\s]?\d{5}[-\s]?\d{5}',      
        r'[6-9]\d{9}',                       
        r'0[6-9]\d{9}',                      
        r'91[6-9]\d{9}',                     
    ]
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
       section_patterns = {
        'summary': r'\b(?:professional\s+)?summary\b|\bobjective\b|\bprofile\b|\babout\s+me\b',
        'experience': r'\bexperience\b|\bemployment\b|\bwork\s+history\b|\bprofessional\s+experience\b|\bwork\s+experience\b',
        'education': r'\beducation\b|\bacademic\b|\bqualifications\b|\beducational\s+background\b',
        'skills': r'\bskills\b|\btechnical\s+skills\b|\bcore\s+competencies\b|\bexpertise\b',
        'projects': r'\bprojects\b|\bpersonal\s+projects\b|\bacademic\s+projects\b',
        'certifications': r'\bcertifications\b|\bcertificates\b|\blicenses\b',
        'achievements': r'\bachievements\b|\bawards\b|\bhonors\b|\bleadership\b|\baccomplishments\b',
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
        """Extract text from PDF or DOCX file."""
        text = ""
        file_ext = file_path.lower().split(".")[-1]
        
        if file_ext == "pdf":
            text = cls._extract_pdf_text(file_path)
        elif file_ext == "docx":
            text = cls._extract_docx_text(file_path)
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
        
        return text

    @classmethod
    def _extract_pdf_text(cls, file_path: str) -> str:
        """Extract text from PDF."""
        text = ""
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Normalize whitespace - replace multiple spaces/newlines with single space
        text = ' '.join(text.split())
        
        return text

    @classmethod
    def _extract_docx_text(cls, file_path: str) -> str:
        """Extract text from DOCX."""
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            # Normalize whitespace
            text = ' '.join(text.split())
            return text
        except ImportError:
            raise Exception("python-docx not installed. Run: pip install python-docx")

    @classmethod
    def extract_phone(cls, text: str) -> Optional[str]:
        """Extract Indian phone numbers - tries multiple patterns."""
        # First, try to find +91 followed by digits (with any spacing)
        plus91_pattern = r'\+91\s*\d{5}\s*\d{5}'
        match = re.search(plus91_pattern, text)
        if match:
            digits = re.sub(r'\D', '', match.group())
            return f"+91 {digits[-10:-5]} {digits[-5:]}"
        
        # Try +91 with 10 consecutive digits
        plus91_no_space = r'\+91\s*([6-9]\d{9})'
        match = re.search(plus91_no_space, text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
        # Try 10 digits starting with 6-9
        ten_digit = r'\b([6-9]\d{9})\b'
        match = re.search(ten_digit, text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
        # Try with 0 prefix
        zero_prefix = r'\b0([6-9]\d{9})\b'
        match = re.search(zero_prefix, text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
        return None

    @classmethod
    def extract_email(cls, text: str) -> Optional[str]:
        """Extract email."""
        match = re.search(cls.email_pattern, text)
        return match.group(0) if match else None

    @classmethod
    def extract_name(cls, text: str) -> Optional[str]:
        """Extract name from first lines."""
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
        """Extract resume sections."""
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
        """Extract skills from text."""
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
        """Main parse function."""
        raw_text = cls.extract_text(file_path)
        
        if not raw_text.strip():
            raise Exception("Could not extract text. Is this a scanned image PDF?")
        
        sections = cls.extract_sections(raw_text)
        
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