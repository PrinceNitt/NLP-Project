# Setup Guide for Resume Parser NLP Project

This guide will walk you through setting up the Resume Parser application step by step.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Guide](#installation-guide)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Training Custom Models](#training-custom-models)
6. [Common Issues](#common-issues)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher (3.12 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free space
- **Internet**: Required for initial setup and model downloads

### Software Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- pip (usually comes with Python)
- Git ([Download](https://git-scm.com/downloads))

## Installation Guide

### Step 1: Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/PrinceNitt/NLP-Project.git

# OR using SSH
git clone git@github.com:PrinceNitt/NLP-Project.git

# Navigate to project directory
cd NLP-Project
```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- Streamlit (web interface)
- spaCy (NLP library)
- NLTK (natural language toolkit)
- PyMuPDF (PDF processing)
- Pandas (data manipulation)
- And other dependencies

### Step 4: Download NLP Models

**Download spaCy English Model:**
```bash
python -m spacy download en_core_web_sm
```

**Download NLTK Data:**
```bash
python -c "import nltk; nltk.download('punkt')"
```

### Step 5: Verify Installation

Run this command to verify everything is installed correctly:

```bash
python -c 'from modules.users import process_user_mode; print("✓ Installation successful!")'
```

If you see the success message, you're ready to go!

## Configuration

### Directory Structure

Ensure your project has this structure:
```
NLP-Project/
├── main.py
├── requirements.txt
├── README.md
├── SETUP.md
├── .gitignore
├── modules/
│   ├── __init__.py
│   ├── users.py
│   ├── recruiters.py
│   ├── admin.py
│   └── feedback.py
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py
│   └── resume_store.py
├── scripts/
│   ├── __init__.py
│   ├── train_model.py
│   └── train_2.py
├── data/
│   ├── newSkills.csv
│   ├── UpdatedSkills.csv
│   ├── sugestedSkills.csv
│   ├── majors.csv
│   ├── position.csv
│   ├── feedback_data.csv
│   └── user_pdfs.db
└── TrainedModel/
    └── skills/ (optional)
```

### Database Setup

The SQLite database (`user_pdfs.db`) is automatically created in the `data/` directory on first use. No manual configuration needed.

### Admin Credentials

Default admin credentials (should be changed in production):
- Username: `prince81`
- Password: `12345`

To change credentials, edit `modules/admin.py`:
```python
def authenticate_admin(username, password):
    hardcoded_username = "your_username"
    hardcoded_password = "your_password"
    return username == hardcoded_username and password == hardcoded_password
```

## Running the Application

### Start the Application

```bash
streamlit run main.py
```

The application will:
1. Start a local web server
2. Automatically open in your default browser
3. Be available at `http://localhost:8501`

### Using Different Port

If port 8501 is already in use:

```bash
streamlit run main.py --server.port 8502
```

### Running in Headless Mode

For server deployment without auto-opening browser:

```bash
streamlit run main.py --server.headless true
```

## Training Custom Models

The application includes scripts to train custom NER models for better skill extraction.

### Training the Skill Extraction Model

1. **Prepare training data** (already included in `scripts/train_model.py`)

2. **Run the training script:**
   ```bash
   python scripts/train_model.py
   ```

3. **Wait for training to complete** (may take 5-15 minutes depending on your hardware)

4. **Verify the trained model:**
   ```bash
   python -c "import spacy; nlp = spacy.load('TrainedModel/skills'); print('Model loaded successfully!')"
   ```

### Training Data Format

Training data is defined in `scripts/train_model.py` as:
```python
TRAIN_DATA = [
    ("Proficient in Python, Java, and C++", {
        "entities": [(13, 19, "SKILL"), (21, 25, "SKILL"), (30, 33, "SKILL")]
    }),
    # More examples...
]
```

## Common Issues

### Issue 1: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: spaCy Model Not Found

**Error:**
```
OSError: [E050] Can't find model 'en_core_web_sm'
```

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue 3: Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Use a different port
streamlit run main.py --server.port 8502

# OR kill the process using port 8501 (Linux/Mac)
lsof -ti:8501 | xargs kill -9

# OR on Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Issue 4: Permission Denied on Database

**Error:**
```
sqlite3.OperationalError: attempt to write a readonly database
```

**Solution:**
```bash
# Ensure data directory has write permissions
chmod 755 data/
chmod 644 data/*.db
```

### Issue 5: PDF Upload Fails

**Problem:** PDF not parsing correctly

**Solutions:**
- Ensure PDF is not password-protected
- Check that PDF contains searchable text (not scanned images)
- Try re-saving the PDF
- Check file size (keep under 5MB for best performance)

### Issue 6: ImportError for modules

**Error:**
```
ModuleNotFoundError: No module named 'modules'
```

**Solution:**
- Ensure you're in the project root directory
- Check that `modules/__init__.py` exists
- Verify file structure matches the expected layout

## Testing the Application

### Quick Test

1. Start the application
2. Navigate to "Users" section
3. Upload a sample resume PDF
4. Verify that information is extracted correctly

### Full Test Checklist

- [ ] User mode: Upload resume and view extracted info
- [ ] Recruiter mode: Upload multiple resumes and search skills
- [ ] Admin mode: Login and view uploaded resumes
- [ ] Feedback mode: Submit feedback successfully

## Performance Tips

1. **Use smaller PDF files** (< 5MB) for faster processing
2. **Close other applications** to free up RAM
3. **Use SSD** for faster database operations
4. **Clear browser cache** if UI behaves unexpectedly
5. **Restart application** periodically for large batch processing

## Environment Variables (Optional)

You can configure Streamlit using environment variables:

```bash
# Set max upload size (in MB)
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

# Set theme
export STREAMLIT_THEME_BASE=dark
```

## Updating the Application

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the application
streamlit run main.py
```

## Uninstallation

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf NLP-Project
```

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Issues**: Check [GitHub Issues](https://github.com/PrinceNitt/NLP-Project/issues)
- **Feedback**: Use the Feedback section in the app

---

**Happy Parsing! 🚀**
