---
name: maximize_ats_always
description: "Always add ALL keywords to maximize ATS score, never ask the user"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2a79b5a5-35a8-4ed6-978d-20b57b176ce1
  modified: 2026-07-27T21:06:46.061Z
---

## Rule: Always Maximize ATS Coverage (HONESTLY)

**Preference:** When tailoring resume for any job, ALWAYS add ALL relevant keywords from the JD.

**CRITICAL CONSTRAINT:** Only add keywords that HONESTLY describe work actually done. Never keyword-stuff.

**Why:** User's priority is getting through ATS systems to human reviewers. More keywords = higher ATS score = more callbacks. BUT fake keywords destroy credibility with human reviewers and can tank your chances if hiring manager spots nonsense.

**How to apply:**
1. Extract ALL skills from JD
2. Identify which ones are missing from resume
3. Add ONLY skills that honestly describe work actually done
4. **SMART PLACEMENT:**
   - ✅ If keyword naturally fits in experience bullet → add there
   - ✅ If keyword doesn't fit experience bullets → add to Skills section (ATS still matches it)
   - ❌ Never force keyword into bullet where it contradicts actual work
5. Check: Does this skill make sense in this context?
6. Verify keywords actually appear in final resume
7. Don't ask user - just maximize coverage HONESTLY

**DO NOT DO:** Keyword stuffing
- ❌ "XGBoost churn model incorporating deep learning" (tree models != deep learning)
- ❌ "CI/CD pipeline with Kubernetes" (if not actually used)
- ❌ "strategy optimization" (too vague, doesn't describe specific work)

**INSTEAD DO:** Contextual keywords
- ✅ "XGBoost churn model achieving 69.5% recall via SMOTE-balanced training and threshold optimization"
- ✅ "3-stage CI/CD pipeline with Docker containerization"
- ✅ "automated ETL pipelines consolidating 5+ business data sources"

**Current target:** 90%+ JD skill coverage on every application, all honest

**Do not:** Ask user "Option A or B" - always do both (add all keywords that apply)
