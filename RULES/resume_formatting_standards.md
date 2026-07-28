---
name: resume_formatting_standards
description: Font size standards for resume tailoring - maintain 1-page format
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2a79b5a5-35a8-4ed6-978d-20b57b176ce1
  modified: 2026-07-27T22:45:36.125Z
---

## CRITICAL: Font Size Standards for 1-Page Resume

**DO NOT CHANGE THESE SIZES** or resume will overflow to 2 pages.

### Required Font Sizes

| Element | Size | Why |
|---------|------|-----|
| Name/Title (Yashwanth Kumar Kotla) | 14pt | Header |
| Section Headers (EDUCATION, EXPERIENCE, PROJECTS, SKILLS, PUBLICATION) | 12pt | Major sections |
| Company/Project names | 11pt | Subsections |
| **Everything else (bullets, coursework, skills content)** | **9pt** | Body text |

### Common Mistake (DON'T DO THIS)
❌ Setting body text to 11pt causes overflow to 2+ pages
❌ Changing all runs to 11pt destroys the 1-page format
❌ Only changing some sections causes inconsistent sizing

### Correct Approach
✅ When modifying projects/experience/bullets: SET TO 9pt
✅ When adding skill headers: SET TO 11pt BOLD (header only)
✅ When adding skill content: SET TO 9pt NOT BOLD
✅ When replacing text: Always specify font size for new runs

### Code Pattern (Safe)

```python
# For body text (bullets, skills content, coursework)
run = para.add_run(text)
run.font.size = Pt(9)
run.font.name = "Garamond"

# For section headers in skills
header_run = para.add_run("ML & Statistics: ")
header_run.font.bold = True
header_run.font.size = Pt(11)
header_run.font.name = "Garamond"

content_run = para.add_run(content)
content_run.font.size = Pt(9)  # CRITICAL: 9pt not 11pt
content_run.font.bold = False
content_run.font.name = "Garamond"
```

### How to Verify
- Count paragraphs: Should be ~38
- Estimated pages: 38 ÷ 40 lines per page = ~1 page
- Font distribution: Most runs should be 9pt (body), few at 11/12/14pt (headers)

