---
name: keyword_strategy_jd_specific
description: "CRITICAL: Only add JD-specific keywords, never carry over irrelevant keywords from previous tailorings"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2a79b5a5-35a8-4ed6-978d-20b57b176ce1
  modified: 2026-07-27T22:58:38.355Z
---

## CRITICAL RULE: JD-Specific Keywords Only

**Problem I was making:**
- ❌ Adding FloatMe keywords (Kubernetes, Airflow) to Meds.com resume
- ❌ Result: Overkill keywords that don't match the role
- ❌ Bloated resume with irrelevant technical terms

**Correct Approach:**

### Step 1: ALWAYS Start Fresh
```
Use: data/resume.docx (base resume)
NOT: previous tailored resumes (FloatMe, etc.)
```

### Step 2: Extract Keywords ONLY from Current JD
For each new JD:
1. Read the JD carefully
2. Extract ONLY the keywords mentioned in THAT JD
3. Don't add keywords "just in case"
4. Don't carry over from previous JDs

### Step 3: Match Keywords to Resume
```
FloatMe JD mentions: Kubernetes, Airflow, SageMaker
→ Add if you have them

Meds.com JD mentions: SQL, Statistical Modeling, Churn Prediction, Dashboards
→ Add if you have them (ignore Kubernetes, Airflow, etc.)
```

### Example: Right vs Wrong

**WRONG (Overkill):**
```
Meds.com JD: "SQL, Python, Dashboards, Churn Prediction"
Added keywords: SQL ✓, Python ✓, Dashboards ✓, Churn ✓
+ Kubernetes ✗ (not in JD)
+ Airflow ✗ (not in JD)
+ SageMaker ✗ (not in JD)
```

**RIGHT (Specific):**
```
Meds.com JD: "SQL, Python, Dashboards, Churn Prediction"
Added keywords: SQL ✓, Python ✓, Dashboards ✓, Churn ✓
(ignore Kubernetes, Airflow, SageMaker - not relevant)
```

## Rule Summary

✅ **Always start from base resume**
✅ **Extract keywords ONLY from current JD**
✅ **Don't carry over keywords from previous JDs**
✅ **Quality > Quantity (specific > overkill)**
✅ **Check: Is this keyword in the JD I'm applying to?**

## Why This Matters

- ATS systems penalize keyword overkill (irrelevant terms)
- Hiring managers spot bloated resumes
- Focused resumes = better match score
- "Overkill" signals you didn't read the JD carefully

