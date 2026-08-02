# Resume Scoring & Optimization AI Agent

A comprehensive AI agent that:
1. **Scores your resume** against 6 real ATS systems (Workday, Taleo, SuccessFactors, iCIMS, Greenhouse, Lever)
2. **Holistically evaluates** your resume (like hiring-agent)
3. **Extracts missing skills** from job descriptions
4. **Verifies skills** - you confirm which ones you have
5. **Optimizes resume** - adds keywords while strengthening bullets
6. **Preserves formatting** - maintains .docx formatting
7. **Keeps 1 page** - manages space intelligently
8. **Generates reports** - detailed before/after analysis

## Usage
```bash
# Score resume against ATS systems only
python main.py --resume data/resume.docx

# Score resume and optimize for specific job
python main.py --resume data/resume.docx --jd data/job_description.txt

# Non-interactive mode (skip skill verification)
python main.py --resume data/resume.docx --jd data/job_description.txt --non-interactive
```

By default reports and generated files are written to the output directory named "output". Use --output to change the destination.

## Features
- ATS scoring (6 systems)
- Holistic resume evaluation
- Skill extraction & verification
- Intelligent keyword mapping
- Bullet point strengthening
- Space management
- Before/after comparison
- Multiple version generation
- Application tracking

## Project Structure
```
resume-scoring/
├── src/
│   ├── ats/              # ATS scoring logic
│   ├── scoring/          # Holistic evaluation
│   ├── ai/               # LLM-based optimization
│   ├── utils/            # Utilities (parser, writer, etc)
│   └── agent.py          # Main AI agent
├── data/                 # Input files (resume, JD)
├── output/               # Generated resumes & reports
├── logs/                 # Execution logs
└── main.py               # Entry point
```