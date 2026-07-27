"""
Holistic Resume Scorer - Evaluates resume across multiple dimensions
Similar to the hiring-agent model
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import re


@dataclass
class CategoryScore:
    score: float
    max_score: float
    evidence: str


@dataclass
class HolisticScore:
    overall_score: float
    max_score: float
    open_source: CategoryScore
    self_projects: CategoryScore
    production_experience: CategoryScore
    technical_skills: CategoryScore
    bonus_points: float
    deductions: float
    key_strengths: List[str]
    areas_for_improvement: List[str]


class HolisticScorer:
    """Holistic evaluation across multiple dimensions"""

    def __init__(self):
        self.max_scores = {
            "open_source": 35,
            "self_projects": 30,
            "production": 25,
            "technical_skills": 10,
        }

    def score(self, resume_text: str, resume_dict: Dict = None) -> HolisticScore:
        """Score resume holistically"""

        # Score each dimension
        os_score = self._score_open_source(resume_text)
        sp_score = self._score_self_projects(resume_text)
        prod_score = self._score_production(resume_text)
        tech_score = self._score_technical_skills(resume_text)

        # Calculate bonuses and deductions
        bonus = self._calculate_bonus(resume_text)
        deductions = self._calculate_deductions(resume_text)

        # Calculate overall
        total_score = (
            min(os_score["score"], self.max_scores["open_source"]) +
            min(sp_score["score"], self.max_scores["self_projects"]) +
            min(prod_score["score"], self.max_scores["production"]) +
            min(tech_score["score"], self.max_scores["technical_skills"]) +
            bonus -
            deductions
        )

        # Cap at max
        max_possible = sum(self.max_scores.values()) + 20  # 20 bonus max
        total_score = min(total_score, max_possible)

        # Get strengths and improvements
        strengths = self._extract_strengths(resume_text, os_score, sp_score, prod_score, tech_score)
        improvements = self._extract_improvements(os_score, sp_score, prod_score, tech_score)

        return HolisticScore(
            overall_score=total_score,
            max_score=sum(self.max_scores.values()),
            open_source=CategoryScore(
                score=os_score["score"],
                max_score=self.max_scores["open_source"],
                evidence=os_score["evidence"]
            ),
            self_projects=CategoryScore(
                score=sp_score["score"],
                max_score=self.max_scores["self_projects"],
                evidence=sp_score["evidence"]
            ),
            production_experience=CategoryScore(
                score=prod_score["score"],
                max_score=self.max_scores["production"],
                evidence=prod_score["evidence"]
            ),
            technical_skills=CategoryScore(
                score=tech_score["score"],
                max_score=self.max_scores["technical_skills"],
                evidence=tech_score["evidence"]
            ),
            bonus_points=bonus,
            deductions=deductions,
            key_strengths=strengths,
            areas_for_improvement=improvements
        )

    def _score_open_source(self, resume_text: str) -> Dict[str, Any]:
        """Score open source contributions"""
        score = 0
        evidence = "No significant open source contributions mentioned"

        text_lower = resume_text.lower()

        # Check for GitHub profile
        if "github" in text_lower:
            score += 5
            evidence = "GitHub profile referenced"

        # Check for specific OSS keywords
        oss_keywords = ["open source", "contribution", "pull request", "pr", "hacktoberfest", "github"]
        if any(kw in text_lower for kw in oss_keywords):
            score += 15
            evidence = "Some open source engagement mentioned"

        # Check for specific projects
        popular_projects = ["tensorflow", "pytorch", "django", "flask", "react", "vue", "angular",
                          "pandas", "numpy", "scikit-learn", "kubernetes", "docker"]
        if any(proj in text_lower for proj in popular_projects):
            score += 10
            evidence = "Contributions to popular open source projects"

        return {"score": score, "evidence": evidence}

    def _score_self_projects(self, resume_text: str) -> Dict[str, Any]:
        """Score self/personal projects"""
        score = 0
        evidence = "No notable personal projects mentioned"

        text_lower = resume_text.lower()

        # Check for projects section
        if "project" in text_lower:
            score += 10
            evidence = "Projects section present"

        # Check for complexity indicators
        complexity_indicators = ["api", "architecture", "design", "implementation", "deployed",
                               "production", "live", "end-to-end", "full stack", "microservice"]
        complexity_count = sum(1 for ind in complexity_indicators if ind in text_lower)
        score += min(complexity_count * 2, 10)

        # Check for impact/results
        impact_indicators = ["improved", "increased", "reduced", "optimized", "achieved",
                            "users", "%", "impact", "performance"]
        impact_count = sum(1 for ind in impact_indicators if ind in text_lower)
        score += min(impact_count * 1.5, 10)

        if score > 15:
            evidence = f"Projects demonstrate complexity with real-world impact ({score}/30)"

        return {"score": score, "evidence": evidence}

    def _score_production(self, resume_text: str) -> Dict[str, Any]:
        """Score production/work experience"""
        score = 0
        evidence = "Limited production experience"

        text_lower = resume_text.lower()

        # Check for work experience section
        if any(word in text_lower for word in ["experience", "employment", "work"]):
            score += 5

        # Check for professional roles
        roles = ["engineer", "developer", "analyst", "scientist", "architect", "lead", "manager"]
        role_count = sum(1 for role in roles if role in text_lower)
        score += min(role_count * 3, 10)

        # Check for production keywords
        production_keywords = ["production", "deployed", "shipped", "live", "customers", "users",
                              "enterprise", "scale", "distributed", "system"]
        prod_count = sum(1 for kw in production_keywords if kw in text_lower)
        score += min(prod_count * 2, 10)

        if score > 10:
            evidence = f"Relevant production/work experience present ({score}/25)"

        return {"score": score, "evidence": evidence}

    def _score_technical_skills(self, resume_text: str) -> Dict[str, Any]:
        """Score technical skills"""
        score = 0
        evidence = "Limited technical skills mentioned"

        text_lower = resume_text.lower()

        # Major tech categories
        categories = {
            "languages": ["python", "java", "javascript", "c++", "go", "rust", "typescript"],
            "frameworks": ["react", "django", "flask", "spring", "fastapi"],
            "data_tech": ["sql", "pandas", "spark", "kafka", "hadoop"],
            "cloud": ["aws", "gcp", "azure", "docker", "kubernetes"],
            "ml": ["machine learning", "tensorflow", "pytorch", "scikit-learn", "ml"],
        }

        categories_covered = 0
        skills_found = 0

        for category, skills in categories.items():
            if any(skill in text_lower for skill in skills):
                categories_covered += 1
                skill_count = sum(1 for skill in skills if skill in text_lower)
                skills_found += skill_count

        # Score based on breadth and depth
        score = min(categories_covered * 1.5 + skills_found * 0.5, 10)

        if score > 5:
            evidence = f"Solid technical skills across {categories_covered} categories"

        return {"score": score, "evidence": evidence}

    def _calculate_bonus(self, resume_text: str) -> float:
        """Calculate bonus points"""
        bonus = 0
        text_lower = resume_text.lower()

        # LinkedIn profile
        if "linkedin" in text_lower:
            bonus += 1

        # Portfolio/website
        if any(word in text_lower for word in ["portfolio", "website", "blog", "github.io"]):
            bonus += 2

        # Publications/speaking
        if any(word in text_lower for word in ["publication", "conference", "speaker", "blog", "medium"]):
            bonus += 2

        # Certifications
        if any(word in text_lower for word in ["certificate", "certification", "certified"]):
            bonus += 1

        return min(bonus, 20)

    def _calculate_deductions(self, resume_text: str) -> float:
        """Calculate deductions"""
        deductions = 0

        # Typos/grammar (estimate)
        typo_patterns = [r"\b[a-z]{20,}\b"]  # Very long words (likely typo)
        if re.findall("".join(typo_patterns), resume_text.lower()):
            deductions += 2

        # Formatting issues
        if resume_text.count("\n") < 3:
            deductions += 3

        return min(deductions, 10)

    def _extract_strengths(self, resume_text: str, os_score, sp_score, prod_score, tech_score) -> List[str]:
        """Extract key strengths"""
        strengths = []

        if sp_score["score"] >= 15:
            strengths.append("Complex self projects with real-world impact")

        if tech_score["score"] >= 7:
            strengths.append("Strong technical skills across multiple categories")

        if prod_score["score"] >= 12:
            strengths.append("Relevant production/work experience")

        if os_score["score"] >= 15:
            strengths.append("Active in open source community")

        return strengths if strengths else ["Resume demonstrates foundational experience"]

    def _extract_improvements(self, os_score, sp_score, prod_score, tech_score) -> List[str]:
        """Extract areas for improvement"""
        improvements = []

        if os_score["score"] < 10:
            improvements.append("Increase contributions to open source projects")

        if sp_score["score"] < 15:
            improvements.append("Build more complex, impactful personal projects")

        if prod_score["score"] < 12:
            improvements.append("Seek more production/work experience opportunities")

        if tech_score["score"] < 6:
            improvements.append("Expand technical skills across more categories")

        return improvements if improvements else ["Continue building on existing strengths"]
