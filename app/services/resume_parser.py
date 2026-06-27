import re
import pdfplumber
from typing import Dict, List, Optional
import io


class ResumeParser:
    def __init__(self):
        # INDIAN PHONE ONLY: +91 98765 43210, 9876543210, +91-98765-43210
        self.phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
        
        # Email pattern
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Section headers - case insensitive
        self.section_patterns = {
            'summary': r'(?:professional\s+)?summary|objective|profile|about\s+me',
            'experience': r'experience|employment|work\s+history|professional\s+experience|work\s+experience',
            'education': r'education|academic|qualifications|educational\s+background',
            'skills': r'skills|technical\s+skills|core\s+competencies|expertise',
            'projects': r'projects|personal\s+projects|academic\s+projects',
            'certifications': r'certifications|certificates|licenses',
            'achievements': r'achievements|awards|honors|leadership|accomplishments',
        }
        
        # Skills keywords including business/soft skills
        self.skill_keywords = [
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

    def extract_text(self, file_bytes: bytes, file_type: str) -> str:
        """Extract text from PDF."""
        text = ""
        
        if file_type == 'application/pdf':
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            raise Exception("Only PDF files supported")
        
        return text

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract Indian phone numbers."""
        # Find all matches
        matches = re.findall(self.phone_pattern, text)
        
        if matches:
            # Return the longest match (most complete)
            best_match = max(matches, key=len)
            
            # Format nicely: +91 92598 46665
            digits = re.sub(r'\D', '', best_match)  # Remove non-digits
            
            if len(digits) == 10:
                return f"+91 {digits[:5]} {digits[5:]}"
            elif len(digits) == 11 and digits.startswith('0'):
                return f"+91 {digits[1:6]} {digits[6:]}"
            elif len(digits) == 12 and digits.startswith('91'):
                return f"+91 {digits[2:7]} {digits[7:]}"
            
            return best_match
        
        return None

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email."""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else None

    def extract_name(self, text: str) -> Optional[str]:
        """Extract name from first lines."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Skip common header words
        skip_words = ['resume', 'cv', 'curriculum', 'vitae']
        
        for line in lines[:5]:  # Check first 5 lines
            line_lower = line.lower()
            if not any(sw in line_lower for sw in skip_words):
                words = line.split()
                if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
                    return line
        
        # Fallback: first line before email
        for i, line in enumerate(lines[:10]):
            if '@' in line and i > 0:
                return lines[i-1].strip()
        
        return lines[0] if lines else None

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract resume sections."""
        sections = {}
        text_lower = text.lower()
        
        # Find all section positions
        positions = []
        for section_name, pattern in self.section_patterns.items():
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                positions.append((match.start(), section_name))
        
        positions.sort()
        
        # Extract content between sections
        for i, (start, name) in enumerate(positions):
            end = positions[i+1][0] if i+1 < len(positions) else len(text)
            section_text = text[start:end].strip()
            lines = section_text.split('\n')
            sections[name] = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
        
        return sections

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        found = []
        text_lower = text.lower()
        
        for skill in self.skill_keywords:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill.title())
        
        # Also check skills section
        sections = self.extract_sections(text)
        if 'skills' in sections:
            skills_text = sections['skills'].lower()
            for skill in self.skill_keywords:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, skills_text) and skill.title() not in found:
                    found.append(skill.title())
        
        return list(set(found))

    def parse_resume(self, file_bytes: bytes, file_type: str) -> Dict:
        """Main parse function."""
        raw_text = self.extract_text(file_bytes, file_type)
        
        if not raw_text.strip():
            raise Exception("Could not extract text. Is this a scanned image PDF?")
        
        sections = self.extract_sections(raw_text)
        
        result = {
            'name': self.extract_name(raw_text),
            'email': self.extract_email(raw_text),
            'phone': self.extract_phone(raw_text),
            'skills': self.extract_skills(raw_text),
            'raw_text': raw_text[:1000],
            'sections': sections
        }
        
        result['score'] = self.calculate_score(result)
        return result

    def calculate_score(self, data: Dict) -> Dict:
        """Calculate ATS score."""
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Contact info (30 points)
        if data['name']:
            score += 10
            strengths.append("Name clearly identified")
        else:
            weaknesses.append("Name not found")
            suggestions.append("Add your name at the top of the resume")
        
        if data['email']:
            score += 10
            strengths.append("Email present")
        else:
            weaknesses.append("Email not found")
            suggestions.append("Add a professional email address")
        
        if data['phone']:
            score += 10
            strengths.append("Phone number present")
        else:
            weaknesses.append("Phone number not found")
            suggestions.append("Add Indian mobile number (+91 format)")
        
        # Sections (40 points)
        s = data['sections']
        if s.get('summary'):
            score += 10
            strengths.append("Professional summary present")
        else:
            suggestions.append("Add a professional summary at the top")
        
        if s.get('experience'):
            score += 15
            strengths.append("Work experience section found")
        else:
            weaknesses.append("No work experience section found")
            suggestions.append("Add a work experience section with job details")
        
        if s.get('education'):
            score += 10
            strengths.append("Education section present")
        else:
            weaknesses.append("Education section not detected")
            suggestions.append("Add an education section with degree details")
        
        if s.get('skills') or data['skills']:
            score += 5
            strengths.append("Skills listed")
        else:
            weaknesses.append("Limited skills listed")
            suggestions.append("Add more relevant skills and technologies")
        
        # Projects (10 points)
        if s.get('projects'):
            score += 10
            strengths.append("Projects section present")
        else:
            suggestions.append("Consider adding a projects section to showcase practical work")
        
        # Achievements (10 points)
        if s.get('achievements') or s.get('certifications'):
            score += 10
            strengths.append("Achievements/certifications listed")
        else:
            suggestions.append("Add certifications or achievements to stand out")
        
        score = min(score, 100)
        
        if score < 50:
            suggestions.insert(0, "Consider using a standard resume format with clear section headers")
        
        return {
            'overall_score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions
        }