---
name: fix_docx_keyword_insertion
description: Root cause and fix for .docx keyword insertion not persisting to file
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2a79b5a5-35a8-4ed6-978d-20b57b176ce1
  modified: 2026-07-27T21:03:20.233Z
---

## Problem Fixed

**Issue:** Keywords were being claimed to be added to resume but NOT actually appearing in the .docx file.

**Example:** "deep learning" was said to be added to XGBoost churn line but the line still read: "Protected an estimated $1M+ in annual revenue with a calibrated XGBoost churn model achieving 69.5% recall..." with NO "deep learning" keyword.

**Root Cause:** 
1. The `save_optimized_resume()` method was clearing ALL paragraphs and re-adding them, destroying formatting
2. Text insertion wasn't checking .docx **run structure** (runs are individual formatted text segments within a paragraph)
3. Using `para.text = new_text` doesn't actually save changes to the .docx file properly
4. No verification was done AFTER saving to confirm changes persisted

## Solution Applied

**Step 1: Proper Run Handling**
```python
# WRONG: para.text = new_text  (doesn't persist)

# RIGHT: Clear runs and add new one
for run in para.runs:
    r = run._element
    r.getparent().remove(r)
new_run = para.add_run(new_text)
new_run.font.name = "Garamond"
```

**Step 2: Immediate Verification**
After saving the .docx file, immediately read it back and check that ALL keywords actually appear:
```python
verify_doc = Document(output_path)
verify_text = "\n".join([p.text for p in verify_doc.paragraphs])

for keyword in added_keywords:
    assert keyword.lower() in verify_text.lower()
    # Show proof of where it appears
```

**Step 3: Return Proof**
Return verification proof with each resume tailoring:
```python
{
    "success": True,
    "keywords_added": ["deep learning", "kubernetes"],
    "verified_in_file": ["deep learning", "kubernetes"],
    "verification_proof": [
        {"keyword": "deep learning", "found_in": "...XGBoost churn model incorporating deep learning..."}
    ]
}
```

## How to Apply

1. **After ANY resume modification:** Read file back immediately and verify changes persisted
2. **NEVER claim success without proof:** Show which lines have the keywords before telling user they're added
3. **Always return verification results:** Include verification_proof in response so user can see WHERE keywords were added
4. **Test all keywords:**  Check that ALL verified skills appear in the FINAL saved file, not just the skills section

## Additional: Honesty Check

**CRITICAL:** Only add keywords if they make sense in context:
- ❌ Don't add "deep learning" to XGBoost churn model (tree-based, not neural nets)
- ❌ Don't add "Kubernetes" if not actually used in CI/CD pipeline
- ❌ Don't add vague keywords like "strategy" without specific technical context

When adding keywords:
1. Check: Does this skill actually describe the work in this bullet?
2. If it's a required skill from JD but not in this bullet, add to Skills section instead
3. Never force keywords into bullets where they don't belong

## Why This Matters

User explicitly stated: "i donot want to keep checking the product again and again if the keywords appeared or not, fix this issue and prevent this from happening again"

Also: "is it making any sense like incorporating deep learning techniques? is that making sense or randomly throwing a keyword without the bullet point increasing the value but turning it into 0, fix this issue"

False claims AND fake keywords destroy trust. ALWAYS verify AND ensure keywords are honest before claiming success.

