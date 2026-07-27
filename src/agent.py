"""
Main Resume Scoring & Optimization AI Agent
Orchestrates ATS scoring, holistic evaluation, skill extraction, and optimization
"""

import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
import anthropic

from ats.ats_scorer import ATSScorer
from scoring.holistic_scorer import HolisticScorer
from utils.parsers import ResumeParser, JDParser, SkillVerifier
from utils.writers import ReportWriter
from utils.resume_optimizer import ResumeOptimizer, ResumeTailorizer

load_dotenv()


class ResumeScoringAgent:
    """AI Agent for resume scoring and optimization"""

    def __init__(self):
        self.ats_scorer = ATSScorer()
        self.holistic_scorer = HolisticScorer()
        self.jd_parser = JDParser()
        self.skill_verifier = SkillVerifier()
        self.report_writer = ReportWriter()

        # Claude API - optional (for AI suggestions)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        self.model = "claude-opus-4-8"
        if api_key and api_key != "your_api_key_here":
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                print(f"⚠️ Claude API unavailable: {e}")
                print("   Continuing without AI suggestions...\n")

    def run(self, resume_path: str, jd_path: str = None, interactive: bool = True) -> Dict:
        """Run the complete resume scoring and optimization pipeline"""

        print("\n" + "=" * 100)
        print("🚀 RESUME SCORING & OPTIMIZATION AI AGENT")
        print("=" * 100 + "\n")

        # Step 1: Parse resume
        print("📄 Step 1: Parsing resume...")
        resume_data = ResumeParser.parse_docx(resume_path)
        resume_text = resume_data["text"]
        print(f"✅ Resume parsed ({resume_data['word_count']} words)\n")

        # Step 2: Parse JD if provided
        jd_text = None
        extracted_skills = []
        present_skills = []
        missing_skills = []

        if jd_path and os.path.exists(jd_path):
            print("📋 Step 2: Parsing job description...")
            with open(jd_path, 'r') as f:
                jd_text = f.read()

            extracted_skills = self.jd_parser.extract_skills(jd_text)
            skill_assessment = self.jd_parser.assess_relevance(extracted_skills, resume_text)
            present_skills = skill_assessment["present"]
            missing_skills = skill_assessment["missing"]

            print(f"✅ Job description parsed")
            print(f"   • Total skills found: {len(extracted_skills)}")
            print(f"   • Already in resume: {len(present_skills)}")
            print(f"   • Missing skills: {len(missing_skills)}\n")
        else:
            print("⚠️ Step 2: No job description provided (skipping)\n")

        # Step 3: Score with ATS systems
        print("🤖 Step 3: Scoring against 6 ATS systems...")
        ats_results = self.ats_scorer.score_all(resume_text)
        avg_ats_score = self.ats_scorer.get_average_score(ats_results)
        print(f"✅ ATS Scoring complete")
        print(f"   Average Score: {avg_ats_score:.0f}/100")

        for system_name, score in ats_results.items():
            status = "✅" if score.overall_score >= 80 else "⚠️"
            print(f"   {status} {system_name}: {score.overall_score}/100")
        print()

        # Step 4: Holistic evaluation
        print("📊 Step 4: Holistic evaluation...")
        holistic_score = self.holistic_scorer.score(resume_text)
        print(f"✅ Holistic evaluation complete")
        print(f"   Overall Score: {holistic_score.overall_score:.1f}/{holistic_score.max_score}")
        print(f"   • Open Source: {holistic_score.open_source.score:.1f}/{holistic_score.open_source.max_score}")
        print(f"   • Self Projects: {holistic_score.self_projects.score:.1f}/{holistic_score.self_projects.max_score}")
        print(f"   • Production: {holistic_score.production_experience.score:.1f}/{holistic_score.production_experience.max_score}")
        print(f"   • Technical Skills: {holistic_score.technical_skills.score:.1f}/{holistic_score.technical_skills.max_score}")
        print()

        # Step 5: Skill verification (if interactive and JD provided)
        verified_skills = {}
        if interactive and missing_skills:
            print("✅ Step 5: Skill Verification")
            print(f"   Found {len(missing_skills)} missing skills from job description\n")

            verified_skills = self._verify_skills_interactive(missing_skills)
            confirmed_count = len([s for s in verified_skills.values() if s.get('verified')])
            print(f"   ✅ You confirmed {confirmed_count} skills you have\n")
        else:
            print("⏭️ Step 5: Skipping skill verification (non-interactive or no missing skills)\n")
            # In non-interactive mode, assume user has all skills (for testing)
            if missing_skills:
                verified_skills = {skill: {"verified": True, "level": "intermediate", "source": "unknown"}
                                 for skill in missing_skills}

        # Step 6: Tailor resume (if JD provided)
        tailored_resume_path = None
        if jd_path and verified_skills:
            print("🤖 Step 6: Tailoring resume with verified skills...")
            tailorizer = ResumeTailorizer()
            tailor_results = tailorizer.tailor_for_job(
                resume_path,
                jd_text,
                verified_skills,
                output_dir="output"
            )
            tailored_resume_path = tailor_results.get("optimized_path")
            print("✅ Resume tailored and saved")
            print(f"   Optimized resume: {tailored_resume_path}")
            print(f"   Skills added: {', '.join(tailor_results.get('verified_skills_added', []))}\n")
        else:
            print("⏭️ Step 6: Skipping resume tailoring (no JD provided)\n")

        # Step 7: Generate AI optimization suggestions
        print("🤖 Step 7: Generating optimization suggestions...")
        optimization_suggestions = self._get_optimization_suggestions(
            resume_text, jd_text, ats_results, holistic_score, verified_skills
        )
        print("✅ Optimization suggestions generated\n")

        # Step 8: Generate reports
        print("📄 Step 8: Generating reports...")
        output_files = self._generate_reports(
            ats_results, holistic_score, {
                "present": present_skills,
                "missing": missing_skills,
                "verified": verified_skills
            }
        )
        print("✅ Reports generated\n")

        # Step 8: Summary
        print("=" * 100)
        print("📊 ANALYSIS COMPLETE")
        print("=" * 100)
        print(f"\n🎯 Key Metrics:")
        print(f"   • ATS Compatibility: {avg_ats_score:.0f}/100")
        print(f"   • Holistic Score: {holistic_score.overall_score:.1f}/{holistic_score.max_score}")
        print(f"   • ATS Systems Passed: {sum(1 for r in ats_results.values() if r.overall_score >= 80)}/6")

        print(f"\n📁 Output Files:")
        for file_type, file_path in output_files.items():
            print(f"   • {file_type}: {file_path}")

        print(f"\n💡 Key Recommendations:")
        for i, area in enumerate(holistic_score.areas_for_improvement[:3], 1):
            print(f"   {i}. {area}")

        return {
            "resume_path": resume_path,
            "jd_path": jd_path,
            "tailored_resume_path": tailored_resume_path,
            "ats_results": ats_results,
            "holistic_score": holistic_score,
            "skills": {
                "present": present_skills,
                "missing": missing_skills,
                "verified": verified_skills
            },
            "optimization_suggestions": optimization_suggestions,
            "output_files": output_files
        }

    def _verify_skills_interactive(self, missing_skills: List[str]) -> Dict:
        """Interactive skill verification"""
        verified = {}

        # Prioritize skills
        prioritized = self.jd_parser.prioritize_skills("", missing_skills)

        print("   Please verify which skills you actually have:")
        print("   (Respond with: yes/y, no/n, or 'skip' to stop)\n")

        for skill in prioritized[:15]:  # Limit to top 15 skills
            while True:
                response = input(f"   Do you have '{skill}'? (y/n/skip): ").lower().strip()

                if response == "skip":
                    break
                elif response in ["y", "yes"]:
                    level = input(f"     Level (beginner/intermediate/advanced)? ").lower().strip()
                    source = input(f"     Where? (university/project/internship/work): ").lower().strip()

                    verified[skill] = {
                        "verified": True,
                        "level": level,
                        "source": source
                    }
                    print(f"   ✅ Added '{skill}'\n")
                    break
                elif response in ["n", "no"]:
                    verified[skill] = {"verified": False}
                    print(f"   ⏭️ Skipped '{skill}'\n")
                    break
                else:
                    print("   Invalid input. Please enter y/n/skip")

        return verified

    def _get_optimization_suggestions(self, resume_text: str, jd_text: str,
                                     ats_results: Dict, holistic_score: Any,
                                     verified_skills: Dict) -> Dict:
        """Generate optimization suggestions (AI optional)"""

        if not self.client:
            return {
                "suggestions": "⏭️ AI suggestions not available (no API key). Review the reports above for detailed recommendations.",
                "status": "skipped"
            }

        prompt = f"""Analyze this resume and provide specific optimization suggestions.

RESUME:
{resume_text[:2000]}

{'JOB DESCRIPTION:' if jd_text else 'NO JOB DESCRIPTION PROVIDED'}
{jd_text[:1000] if jd_text else '(No JD provided)'}

ATS SCORES:
Average: {sum(r.overall_score for r in ats_results.values()) / len(ats_results):.0f}/100
Workday: {ats_results.get('Workday').overall_score}/100
Greenhouse: {ats_results.get('Greenhouse').overall_score}/100
Lever: {ats_results.get('Lever').overall_score}/100

HOLISTIC EVALUATION:
Overall: {holistic_score.overall_score:.1f}/{holistic_score.max_score}
Open Source: {holistic_score.open_source.score:.1f}/35
Self Projects: {holistic_score.self_projects.score:.1f}/30
Production: {holistic_score.production_experience.score:.1f}/25
Technical Skills: {holistic_score.technical_skills.score:.1f}/10

VERIFIED SKILLS: {len([s for s in verified_skills.values() if s.get('verified')])}

Provide:
1. Top 3 quick wins to improve ATS score
2. Top 3 bullets to strengthen
3. Skills to add (if any)
4. How to keep resume at 1 page while adding keywords
5. Estimated score improvement after changes

Be specific and actionable."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return {
                "suggestions": message.content[0].text,
                "status": "success"
            }
        except Exception as e:
            return {
                "suggestions": f"⚠️ Error generating suggestions: {str(e)}",
                "status": "error"
            }

    def _generate_reports(self, ats_results: Dict, holistic_score: Any, skills: Dict) -> Dict:
        """Generate comprehensive reports"""
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        output_files = {}

        # ATS Report
        ats_report_path = os.path.join(output_dir, "01_ats_scores.txt")
        self.report_writer.generate_ats_report(ats_results, ats_report_path)
        output_files["ATS Report"] = ats_report_path

        # Holistic Report
        holistic_report_path = os.path.join(output_dir, "02_holistic_evaluation.txt")
        self.report_writer.generate_holistic_report(holistic_score, holistic_report_path)
        output_files["Holistic Report"] = holistic_report_path

        # Comprehensive Report
        comprehensive_path = os.path.join(output_dir, "03_comprehensive_analysis.txt")
        self.report_writer.generate_comprehensive_report(ats_results, holistic_score, skills, comprehensive_path)
        output_files["Comprehensive Report"] = comprehensive_path

        # Skills Analysis
        skills_path = os.path.join(output_dir, "04_skills_analysis.json")
        with open(skills_path, 'w') as f:
            json.dump(skills, f, indent=2)
        output_files["Skills Analysis"] = skills_path

        return output_files
