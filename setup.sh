#!/bin/bash
# Setup Resume Scoring Agent

echo "📁 Creating project structure..."
mkdir -p {data,output,logs,tests}
mkdir -p src/{ats,scoring,ai,utils}

echo "📄 Creating README..."
cat > README.md << 'READMEEOF'
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
python main.py --resume resume.docx --jd "job_description.txt"
```

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
READMEEOF

echo "✅ Project structure created!"
ls -la

