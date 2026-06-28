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
            text = cls._extract_pdf_text(file_path)
        elif file_ext == "docx":
            text = cls._extract_docx_text(file_path)
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
        
        return text

    @classmethod
    def _extract_pdf_text(cls, file_path: str) -> str:
        text = ""
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Clean up spaces within lines but keep newlines for section detection
        lines = text.split('\n')
        cleaned_lines = [' '.join(line.split()) for line in lines]
        text = '\n'.join(cleaned_lines)
        
        return text

    @classmethod
    def _extract_docx_text(cls, file_path: str) -> str:
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            lines = text.split('\n')
            cleaned_lines = [' '.join(line.split()) for line in lines]
            text = '\n'.join(cleaned_lines)
            return text
        except ImportError:
            raise Exception("python-docx not installed. Run: pip install python-docx")

    @classmethod
    def extract_phone(cls, text: str) -> Optional[str]:
        match = re.search(r'\+91\s*\d{5}\s*\d{5}', text)
        if match:
            digits = re.sub(r'\D', '', match.group())
            return f"+91 {digits[-10:-5]} {digits[-5:]}"
        
        match = re.search(r'\+91\s*([6-9]\d{9})', text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
        match = re.search(r'\b([6-9]\d{9})\b', text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
        match = re.search(r'\b0([6-9]\d{9})\b', text)
        if match:
            digits = match.group(1)
            return f"+91 {digits[:5]} {digits[5:]}"
        
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
        lines = text.split('\n')
        
        # Find section headers (lines that match section patterns)
        section_starts = {}
        
        for i, line in enumerate(lines):
            line_clean = line.strip().lower()
            line_clean = re.sub(r'[_\-=\*]+', '', line_clean).strip()
            
            for section_name, pattern in cls.section_patterns.items():
                if re.match(r'^' + pattern + r'$', line_clean, re.IGNORECASE):
                    if section_name not in section_starts:
                        section_starts[section_name] = i
        
        # Extract content between sections
        sorted_sections = sorted(section_starts.items(), key=lambda x: x[1])
        
        for idx, (section_name, start_line) in enumerate(sorted_sections):
            if idx + 1 < len(sorted_sections):
                end_line = sorted_sections[idx + 1][1]
            else:
                end_line = len(lines)
            
            content_lines = lines[start_line + 1:end_line]
            content = '\n'.join(content_lines).strip()
            sections[section_name] = content
        
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