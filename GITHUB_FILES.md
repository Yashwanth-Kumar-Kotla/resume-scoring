# GitHub Repository Structure

## ✅ FILES TO COMMIT (Tracked in Git)

### Source Code
```
src/
├── ats/
│   └── ats_scorer.py          # 6 ATS system scorers
├── scoring/
│   └── holistic_scorer.py     # Resume evaluation engine
├── utils/
│   ├── parsers.py             # Resume/JD parsing
│   ├── resume_optimizer.py    # Smart keyword insertion
│   └── writers.py             # Report generation
└── agent.py                   # Main AI agent orchestration
```

### Configuration & Setup
```
requirements.txt               # Python dependencies
main.py                       # CLI entry point
README.md                     # Documentation
GITHUB_FILES.md              # This file
```

### Documentation
```
docs/
├── FAST_APPLICATION_GUIDE.md
├── APPLY_WORKFLOW.md
└── EVALUATION_TEMPLATE.md
```

---

## ❌ FILES TO IGNORE (.gitignore)

### User Data (Private)
```
data/resume.docx             # Your personal resume
data/*.docx                  # Any personal documents
applications_tracker.csv     # Your application history
```

### Generated Output
```
output/                      # Generated resumes and reports
*.docx                       # Compiled resume files
```

### Environment & Cache
```
venv/                        # Virtual environment
.env                         # Secret keys/API tokens
__pycache__/                 # Python cache
*.pyc                        # Compiled Python
```

### System Files
```
.DS_Store                    # macOS files
.claude/                     # Claude IDE config
*.log                        # Log files
~$*                          # Office lock files
```

---

## Quick Setup for New Users

```bash
# Clone repo
git clone <repo-url>
cd resume-scoring

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Use the system
python main.py --help
```

---

## What Gets Committed?
- ✅ Source code (Python files)
- ✅ Configuration (requirements.txt, .env.example)
- ✅ Documentation (README, guides)
- ❌ Personal data (resumes, API keys)
- ❌ Generated files (output/)
- ❌ Virtual environment (venv/)

