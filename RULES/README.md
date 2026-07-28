# Resume Tailoring Rules & Guidelines

This directory contains all the operational rules, memory, and guidelines for the resume tailoring system. These rules ensure consistent, high-quality resume tailoring across all job applications.

## 📋 How to Use This Directory

### For Claude (on any computer):

When setting up Claude on a new machine:

1. **Copy these files to your Claude memory directory:**
   ```
   ~/.claude/projects/[your-project-id]/memory/
   ```

2. **Or import them as guidelines** by reading them before each job application

3. **All rules are automatically applied** when Claude references the MEMORY.md index

---

## 📁 Files Overview

### **MEMORY.md** (INDEX - Read First!)
- Master index of all rules and guidelines
- Links to specific memory files
- Start here to understand the complete system

### **preference_maximize_ats.md**
- **CRITICAL RULE:** Always add ALL keywords from JD
- Never ask user, just maximize coverage
- But add keywords HONESTLY (don't keyword-stuff)
- Only add keywords that describe actual work

### **keyword_strategy_jd_specific.md**
- **CRITICAL RULE:** Only add JD-specific keywords
- Always start from base resume
- Never carry over irrelevant keywords from previous JDs
- Quality > Quantity

### **keyword_capitalization_style.md**
- **CRITICAL RULE:** All keywords must be Capital Case (Title Case)
- E.g., "Statistical Modeling" not "statistical modeling"
- Ensures authenticity and consistency
- Makes resume look professionally written

### **resume_formatting_standards.md**
- Font sizes (CRITICAL for 1-page format):
  - 14pt: Title (Yashwanth Kumar Kotla)
  - 12pt: Section headers (EDUCATION, EXPERIENCE, etc.)
  - 11pt: Subsection headers (company names, section headers in skills)
  - **9pt: Body text (CRITICAL - don't change!)**
- Line spacing: 1.0 (tight)
- Font: Garamond (always)

### **feedback_keyword_insertion_working.md**
- How to properly insert keywords into .docx files
- Use run-based structure (not direct text replacement)
- Always verify keywords after saving
- Don't claim success without proof

### **fix_docx_keyword_insertion.md**
- How to preserve formatting when adding keywords
- Keep section headers BOLD
- Make content NOT bold
- Separate runs for header vs. content

---

## 🎯 Quick Reference

### The Golden Rules

1. ✅ **Start Fresh**
   - Always use base resume (`data/resume.docx`)
   - Don't carry over keywords from previous JDs

2. ✅ **Add Only Relevant Keywords**
   - Extract keywords from current JD ONLY
   - Don't add "just in case"
   - Quality > Quantity

3. ✅ **Capital Case Everything**
   - "Statistical Modeling" ✓
   - "statistical modeling" ✗
   - Ensures authenticity

4. ✅ **Proper Font Sizes**
   - Body text: 9pt (NON-NEGOTIABLE)
   - Headers: 11-12pt
   - Never change body text to 11pt

5. ✅ **Verify Everything**
   - Read file after saving
   - Confirm keywords actually appear
   - Don't claim success without proof

6. ✅ **Honest Keywords**
   - Only add keywords describing actual work
   - Don't keyword-stuff
   - Avoid contradictions ("deep learning" in tree-based models)

---

## 📊 Workflow

### For Each Job Application:

1. **Read the JD carefully**
   - Extract keywords specific to THAT role
   - Note: What does this role actually need?

2. **Start from base resume**
   - `data/resume.docx` (not previous tailored versions)
   - Ensures clean slate

3. **Add only relevant keywords (Capital Case)**
   - E.g., Capgemini needs "Data Structures, Algorithms, ETL"
   - Meds.com needs "Churn Prediction, Customer Analytics"
   - Don't add FloatMe keywords to Capgemini resume

4. **Verify keywords were added**
   - Read file after saving
   - Confirm in final output
   - Show before/after ATS scores

5. **Generate report**
   - Show ATS scores (before/after)
   - List keywords added
   - Indicate readiness to apply

---

## 🔧 Technical Notes

### For Python/Code Setup

When recreating on another computer:

```bash
# Clone repo
git clone <repo-url>
cd resume-scoring

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy RULES to Claude memory (optional)
cp -r RULES/ ~/.claude/projects/[project-id]/memory/

# Ready to use!
python main.py
```

### For Claude

When setting up Claude on new computer:
1. Copy RULES/ files to your Claude memory directory
2. Claude will automatically reference them
3. All rules will be applied to future resume tailoring

---

## 📝 Sample: How Rules Work Together

**Scenario:** Tailoring for Capgemini Data Engineer role

1. **Keyword Strategy (JD-Specific)**
   - Read: Capgemini JD focuses on SQL, Data Engineering
   - Decision: Add only data engineering keywords
   - NOT: "Kubernetes, Airflow" (these are for other roles)

2. **Capitalization (Capital Case)**
   - Add: "Data Structures", "Algorithms", "Relational Databases"
   - NOT: "data structures", "algorithms", "relational databases"

3. **Formatting (Font Sizes)**
   - Body text stays 9pt
   - Section headers stay 11pt
   - Never change to 11pt for body

4. **Verification (No False Claims)**
   - After saving, read file
   - Confirm keywords actually appear
   - Show proof before claiming success

5. **Honesty (Relevant Keywords)**
   - Add "SQL query optimization" (real work)
   - Don't add "deep learning" (not relevant to data engineer role)

---

## ✅ Checklist Before Applying

- [ ] Used base resume (`data/resume.docx`)
- [ ] Added ONLY keywords from current JD
- [ ] All keywords in Capital Case
- [ ] Body text is 9pt (not 11pt)
- [ ] Section headers are BOLD
- [ ] Read file after saving
- [ ] Keywords actually appear in document
- [ ] Before/after ATS scores generated
- [ ] Resume ready to submit

---

## Questions?

If anything is unclear:
1. Read the relevant memory file (MEMORY.md has the index)
2. Check this README
3. Review past examples in `output/` directory

All guidelines are documented to ensure consistency across applications.
