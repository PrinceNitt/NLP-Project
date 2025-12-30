# Scripts Folder Explanation (हिंदी में) 📚

## Overview

`scripts/` folder mein **NLP model training** ke liye scripts hain. Ye scripts **custom skill extraction model** train karte hain jo resume se skills identify karne mein help karta hai.

---

## 📁 Files Ka Kaam

### 1. `__init__.py` 
**Purpose:** Python package initializer

**Kaam:**
- Ye file Python ko batati hai ki `scripts` ek package hai
- Documentation ke liye comments contain karta hai
- Koi special functionality nahi, bas package ko initialize karta hai

---

### 2. `train_model.py` 
**Purpose:** Hardcoded training data se NER model train karta hai

**Kya Karta Hai:**
1. **Training Data Define Karta Hai:**
   - 150+ skills ke examples hardcoded hain
   - Har example mein text aur uska label (SKILL) hota hai
   - Examples jaise: "Proficient in Python, Java, and C++"

2. **Model Train Karta Hai:**
   - spaCy ka blank English model create karta hai
   - NER (Named Entity Recognition) pipeline add karta hai
   - "SKILL" label add karta hai
   - 20 iterations mein model train karta hai

3. **Model Save Karta Hai:**
   - Trained model ko `TrainedModel/test/` folder mein save karta hai
   - Model ko baad mein use kar sakte hain

**Example Training Data:**
```python
("Proficient in Python, Java, and C++", {
    "entities": [(13, 19, "SKILL"), (21, 25, "SKILL"), (30, 33, "SKILL")]
})
```

**Kaise Run Karein:**
```bash
python scripts/train_model.py
```

**Output:**
- `TrainedModel/test/` folder mein trained model save hoga
- Console mein training progress dikhega

---

### 3. `train_2.py`
**Purpose:** CSV file se data read karke model train karta hai

**Kya Karta Hai:**
1. **CSV File Se Data Read Karta Hai:**
   - `data/newSkills.csv` file se skills read karta hai
   - Har skill ko training example mein convert karta hai

2. **Model Train Karta Hai:**
   - Same process jaise `train_model.py`
   - 20 iterations mein train karta hai
   - CSV se data dynamically load hota hai

3. **Model Save Karta Hai:**
   - Trained model ko `TrainedModel/test2/` folder mein save karta hai

**Advantage:**
- CSV file update karke easily new skills add kar sakte hain
- Hardcoded data ki zarurat nahi

**Kaise Run Karein:**
```bash
python scripts/train_2.py
```

**Output:**
- `TrainedModel/test2/` folder mein trained model save hoga

---

## 🤔 Dono Scripts Mein Kya Difference Hai?

| Feature | `train_model.py` | `train_2.py` |
|---------|------------------|--------------|
| **Data Source** | Hardcoded in code | CSV file (`data/newSkills.csv`) |
| **Flexibility** | Kam (code change karna padega) | Zyada (CSV update karo) |
| **Output Location** | `TrainedModel/test/` | `TrainedModel/test2/` |
| **Use Case** | Fixed training data | Dynamic training data |

---

## 🎯 Application Mein Kaise Use Hota Hai?

### Current Implementation

Application mein trained model **optional** hai:

1. **Primary Method (CSV-based):**
   - `data/newSkills.csv` se skills match karta hai
   - Ye method **always available** hai

2. **Secondary Method (Trained Model):**
   - Agar `TrainedModel/skills/` folder mein model hai, to use karta hai
   - Ye method **better accuracy** deta hai
   - Agar model nahi hai, to CSV method use hota hai

**Code Location:** `utils/resume_parser.py` lines 417-432

```python
# Try to load trained model
try:
    if TRAINED_MODEL_PATH.exists():
        nlp_skills = spacy.load(str(TRAINED_MODEL_PATH))
        # Use trained model for skill extraction
except:
    # Fallback to CSV-based extraction
    pass
```

---

## 📊 Workflow Diagram

```
┌─────────────────┐
│  train_model.py │  → Hardcoded data se model train
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ TrainedModel/    │  → Trained model save
│   test/          │
└─────────────────┘

┌─────────────────┐
│  train_2.py     │  → CSV file se model train
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ TrainedModel/    │  → Trained model save
│   test2/         │
└─────────────────┘
         │
         ↓
┌─────────────────┐
│ Application     │  → Model use karta hai (if available)
│ (resume_parser) │     Ya CSV-based extraction
└─────────────────┘
```

---

## 🚀 Kaise Use Karein?

### Step 1: Model Train Karein

**Option A: Hardcoded Data Se (train_model.py)**
```bash
cd /Users/princekumar/Documents/NLP-Project
python scripts/train_model.py
```

**Option B: CSV Se (train_2.py) - Recommended**
```bash
cd /Users/princekumar/Documents/NLP-Project
python scripts/train_2.py
```

### Step 2: Model Verify Karein

```bash
python -c "import spacy; nlp = spacy.load('TrainedModel/test2'); print('Model loaded successfully!')"
```

### Step 3: Model Ko Production Path Mein Copy Karein

Agar aap `train_2.py` se model train kiya hai:
```bash
# Model ko production path mein copy karein
cp -r TrainedModel/test2 TrainedModel/skills
```

Ya `train_model.py` se:
```bash
cp -r TrainedModel/test TrainedModel/skills
```

### Step 4: Application Restart Karein

```bash
streamlit run main.py
```

Ab application trained model use karega! ✅

---

## 💡 Best Practices

### 1. **CSV-Based Training Use Karein** (`train_2.py`)
- Easier to update
- New skills easily add kar sakte hain
- Code change ki zarurat nahi

### 2. **Regular Model Retraining**
- Jab bhi new skills add karein CSV mein
- Model ko retrain karein for better accuracy

### 3. **Model Testing**
- Train karne ke baad model test karein
- Verify karein ki skills properly extract ho rahe hain

---

## 📝 Example: New Skills Add Karna

### Step 1: CSV File Update Karein

`data/newSkills.csv` file mein new skill add karein:
```csv
Python
Java
JavaScript
NewSkill1
NewSkill2
```

### Step 2: Model Retrain Karein

```bash
python scripts/train_2.py
```

### Step 3: Model Copy Karein

```bash
cp -r TrainedModel/test2 TrainedModel/skills
```

### Step 4: Test Karein

Application mein resume upload karke verify karein ki new skills extract ho rahe hain.

---

## 🔍 Technical Details

### NER (Named Entity Recognition)

**Kya Hai:**
- NLP technique jo text se specific entities identify karta hai
- Is case mein "SKILL" entities identify karta hai

**Example:**
```
Input: "Proficient in Python and Java"
Output: 
  - Python (SKILL)
  - Java (SKILL)
```

### Training Process

1. **Blank Model:** spaCy ka blank English model start karte hain
2. **NER Pipeline:** NER component add karte hain
3. **Label Add:** "SKILL" label define karte hain
4. **Training:** Examples se model train karte hain (20 iterations)
5. **Save:** Trained model ko disk par save karte hain

### Model Structure

```
TrainedModel/
├── skills/
│   ├── meta.json          # Model metadata
│   ├── config.cfg         # Model configuration
│   ├── ner/               # NER component
│   └── vocab/             # Vocabulary
```

---

## ⚠️ Important Notes

1. **Model Training Time:**
   - 20 iterations = ~5-15 minutes (depends on data size)
   - More iterations = better accuracy but slower

2. **Model Size:**
   - Trained model ~10-50 MB ho sakta hai
   - Disk space check karein

3. **Model Location:**
   - Application `TrainedModel/skills/` folder mein model dhundhta hai
   - Agar model nahi hai, to CSV-based extraction use hota hai

4. **Optional Feature:**
   - Trained model **optional** hai
   - Application bina trained model ke bhi kaam karta hai
   - CSV-based extraction fallback method hai

---

## 🎓 Learning Resources

Agar aap NER model training seekhna chahte hain:

1. **spaCy Documentation:**
   - https://spacy.io/usage/training

2. **NER Concepts:**
   - Named Entity Recognition basics
   - Training data format
   - Model evaluation

---

## 📋 Summary

| File | Purpose | When to Use |
|------|---------|-------------|
| `__init__.py` | Package initializer | Automatic (no action needed) |
| `train_model.py` | Hardcoded data se train | Fixed training data ke liye |
| `train_2.py` | CSV se train | **Recommended** - Dynamic data ke liye |

**Main Use Case:**
- Better skill extraction accuracy ke liye
- Custom skills identify karne ke liye
- Domain-specific skills train karne ke liye

---