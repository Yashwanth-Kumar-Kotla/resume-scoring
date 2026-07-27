"""
ATS Scoring Module - Tests resume against 6 real ATS systems
Based on: Workday, Taleo, SuccessFactors, iCIMS, Greenhouse, Lever
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ATSScore:
    system_name: str
    overall_score: int
    formatting: int
    keywords: int
    sections: int
    experience: int
    education: int
    verdict: str
    suggestions: List[str]


class ATSScorer:
    def __init__(self):
        self.ats_systems = {
            "Workday": WorkdayScorer(),
            "Taleo": TaleoScorer(),
            "SuccessFactors": SuccessFactorsScorer(),
            "iCIMS": iCIMSScorer(),
            "Greenhouse": GreenhouseScorer(),
            "Lever": LeverScorer(),
        }

    def score_all(self, resume_text: str, resume_dict: Dict = None) -> Dict[str, ATSScore]:
        """Score resume against all 6 ATS systems"""
        results = {}
        for system_name, scorer in self.ats_systems.items():
            results[system_name] = scorer.score(resume_text, resume_dict)
        return results

    def get_average_score(self, results: Dict[str, ATSScore]) -> float:
        """Get average score across all ATS systems"""
        scores = [r.overall_score for r in results.values()]
        return sum(scores) / len(scores) if scores else 0


class BaseATSScorer:
    """Base scorer with common logic"""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.formatting_score = 0
        self.keywords_score = 0
        self.sections_score = 0
        self.experience_score = 0
        self.education_score = 0

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        raise NotImplementedError

    def check_formatting(self, resume_text: str) -> int:
        """Check if resume has good ATS-friendly formatting"""
        score = 100
        issues = []

        # Check for graphics/images (bad for ATS)
        if any(word in resume_text.lower() for word in ["image", "figure", "chart", "graph"]):
            score -= 10
            issues.append("Images/graphics detected - may cause parsing issues")

        # Check for special characters
        special_chars = resume_text.count("●") + resume_text.count("■") + resume_text.count("◆")
        if special_chars > 5:
            score -= 5
            issues.append("Multiple special characters - use standard bullets")

        # Check for tables (problematic for ATS)
        if any(char in resume_text for char in ["│", "┌", "└", "─"]):
            score -= 15
            issues.append("Tables detected - convert to simple format")

        # Check for line breaks/spacing issues
        if resume_text.count("\n") < 5:
            score -= 5
            issues.append("Poor spacing - use line breaks for readability")

        return max(score, 0)

    def check_sections(self, resume_text: str) -> int:
        """Check if resume has essential sections"""
        score = 0
        required_sections = {
            "contact": ["email", "@", "phone", "+"],
            "experience": ["experience", "work", "employment"],
            "education": ["education", "degree", "university", "college"],
            "skills": ["skills", "technical", "proficiency"],
        }

        text_lower = resume_text.lower()
        found_sections = 0

        for section, keywords in required_sections.items():
            if any(kw in text_lower for kw in keywords):
                score += 25
                found_sections += 1

        return score

    def check_keywords(self, resume_text: str) -> int:
        """Check keyword density and variety"""
        text_lower = resume_text.lower()

        # Common technical keywords
        tech_keywords = {
            "python", "java", "sql", "aws", "machine learning", "data analysis",
            "javascript", "react", "angular", "docker", "kubernetes", "git",
            "agile", "scrum", "rest api", "microservices", "cloud", "devops"
        }

        found_keywords = sum(1 for kw in tech_keywords if kw in text_lower)
        keyword_score = min(100, (found_keywords / len(tech_keywords)) * 100)

        return int(keyword_score)

    def check_experience(self, resume_text: str) -> int:
        """Check quality of experience descriptions"""
        score = 50

        # Look for quantifiable achievements
        metrics_patterns = [
            r"\d+%",  # percentages
            r"\d+\s*(?:million|thousand|k)",  # large numbers
            r"improved|increased|reduced|achieved",  # action words
        ]

        matches = sum(len(re.findall(pattern, resume_text.lower())) for pattern in metrics_patterns)
        score += min(50, matches * 5)

        return min(100, score)

    def check_education(self, resume_text: str) -> int:
        """Check education section quality"""
        score = 50
        text_lower = resume_text.lower()

        # Look for degree types
        degrees = ["bachelor", "master", "phd", "associate", "diploma", "b.s.", "m.s.", "b.a.", "m.a."]
        if any(degree in text_lower for degree in degrees):
            score += 30

        # Look for university/college names
        if any(word in text_lower for word in ["university", "college", "institute"]):
            score += 20

        return min(100, score)


class WorkdayScorer(BaseATSScorer):
    """Workday ATS - Strict keyword matching, focus on parsing"""

    def __init__(self):
        super().__init__("Workday")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        overall = int(
            (self.formatting_score * 0.2 +
             self.keywords_score * 0.25 +
             self.sections_score * 0.2 +
             self.experience_score * 0.2 +
             self.education_score * 0.15)
        )

        suggestions = []
        if self.keywords_score < 70:
            suggestions.append("Add more technical keywords relevant to target role")
        if self.formatting_score < 90:
            suggestions.append("Improve formatting - remove special characters and tables")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="Workday",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )


class TaleoScorer(BaseATSScorer):
    """Taleo (Oracle) - ML-based semantic matching"""

    def __init__(self):
        super().__init__("Taleo")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        # Taleo weights experience and keywords heavily
        overall = int(
            (self.formatting_score * 0.15 +
             self.keywords_score * 0.3 +
             self.sections_score * 0.15 +
             self.experience_score * 0.25 +
             self.education_score * 0.15)
        )

        suggestions = []
        if self.experience_score < 70:
            suggestions.append("Strengthen experience descriptions with quantifiable results")
        if self.keywords_score < 75:
            suggestions.append("Include industry-specific terminology")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="Taleo",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )


class SuccessFactorsScorer(BaseATSScorer):
    """SuccessFactors (SAP) - Skills and competencies focus"""

    def __init__(self):
        super().__init__("SuccessFactors")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        overall = int(
            (self.formatting_score * 0.15 +
             self.keywords_score * 0.35 +
             self.sections_score * 0.2 +
             self.experience_score * 0.2 +
             self.education_score * 0.1)
        )

        suggestions = []
        if self.keywords_score < 80:
            suggestions.append("Add comprehensive skills section with specific competencies")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="SuccessFactors",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )


class iCIMSScorer(BaseATSScorer):
    """iCIMS - Context-aware NLP matching"""

    def __init__(self):
        super().__init__("iCIMS")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        # iCIMS is most sophisticated - weights everything balanced
        overall = int(
            (self.formatting_score * 0.2 +
             self.keywords_score * 0.25 +
             self.sections_score * 0.2 +
             self.experience_score * 0.2 +
             self.education_score * 0.15)
        )

        suggestions = []
        if overall < 80:
            suggestions.append("Ensure keywords align with job description context")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="iCIMS",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )


class GreenhouseScorer(BaseATSScorer):
    """Greenhouse - Scorecards, hiring manager review, focus on relevance"""

    def __init__(self):
        super().__init__("Greenhouse")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        # Greenhouse prioritizes experience quality and measurable impact
        overall = int(
            (self.formatting_score * 0.15 +
             self.keywords_score * 0.2 +
             self.sections_score * 0.15 +
             self.experience_score * 0.35 +
             self.education_score * 0.15)
        )

        suggestions = []
        if self.experience_score < 80:
            suggestions.append("Include metrics and quantifiable achievements in experience")
        if self.keywords_score < 70:
            suggestions.append("Align keywords with job posting requirements")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="Greenhouse",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )


class LeverScorer(BaseATSScorer):
    """Lever - Contextual matching with emphasis on candidate source tracking"""

    def __init__(self):
        super().__init__("Lever")

    def score(self, resume_text: str, resume_dict: Dict = None) -> ATSScore:
        self.formatting_score = self.check_formatting(resume_text)
        self.keywords_score = self.check_keywords(resume_text)
        self.sections_score = self.check_sections(resume_text)
        self.experience_score = self.check_experience(resume_text)
        self.education_score = self.check_education(resume_text)

        # Lever weights keywords and experience
        overall = int(
            (self.formatting_score * 0.15 +
             self.keywords_score * 0.28 +
             self.sections_score * 0.15 +
             self.experience_score * 0.27 +
             self.education_score * 0.15)
        )

        suggestions = []
        if self.keywords_score < 75:
            suggestions.append("Add relevant keywords for better contextual matching")

        verdict = "Likely to Pass" if overall >= 80 else "May Fail" if overall < 60 else "Likely to Pass"

        return ATSScore(
            system_name="Lever",
            overall_score=overall,
            formatting=self.formatting_score,
            keywords=self.keywords_score,
            sections=self.sections_score,
            experience=self.experience_score,
            education=self.education_score,
            verdict=verdict,
            suggestions=suggestions
        )
