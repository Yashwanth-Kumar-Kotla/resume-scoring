# 🚀 Quick Start Guide - Resume Scoring Agent

## What This Agent Does

This AI agent provides:

✅ **ATS Scoring** - Tests your resume against 6 real ATS systems:
- Workday
- Taleo (Oracle)
- SuccessFactors (SAP)
- iCIMS
- Greenhouse
- Lever

✅ **Holistic Evaluation** - Scores your resume across:
- Open Source Contributions
- Self/Personal Projects
- Production Experience
- Technical Skills
- Bonus Points & Deductions

✅ **Skill Extraction** - From job descriptions:
- Extracts all skills mentioned in JD
- Identifies skills you already have
- Identifies missing skills
- You verify which ones you actually have

✅ **Optimization Suggestions** - AI-powered recommendations:
- Quick wins to improve ATS score
- Bullets to strengthen
- Keywords to add intelligently
- How to keep resume to 1 page

## Setup (5 minutes)

### 1. Install Dependencies

```bash
cd ~/resume-scoring
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up API Keys

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
nano .env
```

### 3. Prepare Files

Create a `data/` folder with:
- `resume.docx` - Your resume in Word format
- `job_description.txt` - (Optional) Job description to tailor to

```bash
mkdir -p data
# Copy your files to data/ folder
```

## Usage

### Basic Usage - Score Your Resume

```bash
python main.py --resume data/resume.docx
```

This will:
1. Parse your resume
2. Score against 6 ATS systems
3. Provide holistic evaluation
4. Generate reports in `output/` folder

### With Job Description - Optimize for Specific Job

```bash
python main.py --resume data/resume.docx --jd data/job_description.txt
```

This will additionally:
1. Extract skills from job description
2. Identify missing skills
3. Ask you to verify which ones you have (interactive)
4. Generate optimization suggestions
5. Show estimated score improvement

### Non-Interactive Mode - Skip Verification

```bash
python main.py --resume data/resume.docx --jd data/job_description.txt --non-interactive
```

Skips the interactive skill verification step.

## Output Files

The agent generates several reports in the `output/` folder:

1. **01_ats_scores.txt** - Detailed ATS scoring for all 6 systems
   - What each system found
   - Specific suggestions to improve

2. **02_holistic_evaluation.txt** - Holistic evaluation report
   - Scores across all dimensions
   - Key strengths
   - Areas for improvement

3. **03_comprehensive_analysis.txt** - Combined analysis
   - ATS + Holistic scores together
   - Skills analysis
   - Recommendations

4. **04_skills_analysis.json** - Structured skills data
   - Present skills
   - Missing skills
   - Verified skills

## Example Workflow

### Scenario: You have 0 callbacks on 300 applications

```bash
# Step 1: Diagnose your current resume
python main.py --resume data/old_resume.docx

# Look at output/01_ats_scores.txt
# Are you getting 60+/100 on all ATS systems? If not, format is the problem
# If you're getting 80+, format is fine - problem is content/matching

# Step 2: Get a data science job posting you like
# Save it as data/job_description.txt

# Step 3: Analyze your resume against that job
python main.py --resume data/old_resume.docx --jd data/job_description.txt

# Step 4: Review output files
# - How many skills are missing?
# - Which ones do you actually have?
# - Make list of verified skills

# Step 5: Create new resume with improvements
# (Manual editing or use with Resume-Matcher tool)

# Step 6: Test improved resume
python main.py --resume data/new_resume.docx --jd data/job_description.txt

# Step 7: Verify score improved
# Check output/01_ats_scores.txt and output/02_holistic_evaluation.txt
```

## Understanding the Scores

### ATS Scores (out of 100)

- **90-100: Excellent** - Will definitely pass ATS
- **80-89: Good** - Likely to pass, minor issues
- **70-79: Fair** - Might pass, needs improvements
- **60-69: Poor** - Likely to be rejected by ATS
- **<60: Critical** - Will almost certainly fail ATS

### Holistic Score (out of 100)

Similar structure, but evaluates:
- Quality of experience (not just keywords)
- Impact of projects
- Breadth of skills
- Open source engagement

## Quick Tips

### If Your ATS Score is Low (<70)

The issue is **formatting/parsing**:
- Remove images, tables, special characters
- Use standard fonts (Arial, Calibri, Times New Roman)
- Use simple bullet points
- Ensure good spacing/line breaks

### If Your Holistic Score is Low (<60)

The issue is **content**:
- Add more impact metrics to bullets
- Build more substantial projects
- Gain more production experience
- Expand technical skills

### If Both Scores are OK (75+) but You're Getting No Callbacks

The issue is **relevance**:
- You're not tailoring to specific jobs
- Your experience doesn't match what they want
- You need to use Resume-Matcher to tailor each resume

### If One Score is Good, Another is Low

You have a **mismatch**:
- High ATS, Low Holistic = Good formatting, weak content
- Low ATS, High Holistic = Great content, bad formatting

## Troubleshooting

### "No module named 'anthropic'"

```bash
# Make sure venv is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

### "Resume file not found"

```bash
# Make sure path is correct
# File should be in data/ folder
ls -la data/resume.docx
```

### "ANTHROPIC_API_KEY not set"

```bash
# Check .env file exists and has key
cat .env
# Verify key is correct (should start with sk-ant-)
```

### Agent hangs during interactive verification

Press `Ctrl+C` to skip skill verification, use `--non-interactive` flag

## Next Steps

### After Getting Your Scores

1. **Identify your weakest area:**
   - Is it ATS formatting? Fix formatting
   - Is it content quality? Add impact metrics
   - Is it relevance? Use Resume-Matcher to tailor

2. **Create action plan:**
   - Quick fixes: 1-2 hours (formatting, reword bullets)
   - Medium fixes: 1-2 days (add projects, improve skills)
   - Long fixes: weeks (build experience, open source)

3. **Test improvements:**
   - After each major change, re-run agent
   - Track scores over time
   - See what actually helps

4. **Apply strategically:**
   - Before applying, run Resume-Matcher against job
   - Tailor resume for each application
   - Only apply when match is >70%

## Example Output

```
🚀 RESUME SCORING & OPTIMIZATION AI AGENT

📄 Step 1: Parsing resume...
✅ Resume parsed (495 words)

📋 Step 2: Parsing job description...
✅ Job description parsed
   • Total skills found: 15
   • Already in resume: 8
   • Missing skills: 7

🤖 Step 3: Scoring against 6 ATS systems...
✅ ATS Scoring complete
   Average Score: 78/100
   ✅ Workday: 94/100
   ✅ Taleo: 94/100
   ✅ SuccessFactors: 94/100
   ✅ iCIMS: 95/100
   ✅ Greenhouse: 95/100
   ⚠️ Lever: 88/100

📊 Step 4: Holistic evaluation...
✅ Holistic evaluation complete
   Overall Score: 62.0/100
   • Open Source: 5.0/35
   • Self Projects: 25.0/30
   • Production: 20.0/25
   • Technical Skills: 9.0/10

✅ Step 5: Skill Verification
   Found 7 missing skills from job description
   ✅ You confirmed 5 skills you have

📄 ANALYSIS COMPLETE

🎯 Key Metrics:
   • ATS Compatibility: 78/100
   • Holistic Score: 62.0/100
   • ATS Systems Passed: 5/6

📁 Output Files:
   • ATS Report: output/01_ats_scores.txt
   • Holistic Report: output/02_holistic_evaluation.txt
   • Comprehensive Report: output/03_comprehensive_analysis.txt
   • Skills Analysis: output/04_skills_analysis.json
```

## Getting Help

Check the README.md for more detailed documentation.

---

**Ready to improve your resume score? Let's go!** 🚀

```bash
python main.py --resume data/resume.docx
```
