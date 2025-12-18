# Quick Start Guide - Industry Level Setup

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables

```bash
# Create .env file from template
cp .env.example .env

# Edit .env file (use any text editor)
# Set your admin credentials:
# ADMIN_USERNAME=your_username
# ADMIN_PASSWORD=your_secure_password
```

**Important:** Change the default admin password before running in production!

### Step 3: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### Step 4: Run Application

```bash
streamlit run main.py
```

That's it! The application will be available at `http://localhost:8501`

## 🔧 Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Code Formatting

```bash
# Format code with black
black .

# Check code style
flake8 .

# Type checking
mypy .
```

## 📝 Environment Variables

Required variables in `.env` file:

```env
# Admin Configuration (REQUIRED)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here

# Optional - defaults provided
DATABASE_PATH=data/user_pdfs.db
MAX_UPLOAD_SIZE=5242880
SPACY_MODEL=en_core_web_sm
LOG_LEVEL=INFO
DEBUG=False
```

## 🐛 Troubleshooting

### Issue: Module not found
**Solution:** Make sure you're in the project root directory and dependencies are installed.

### Issue: spaCy model not found
**Solution:** Run `python -m spacy download en_core_web_sm`

### Issue: Database errors
**Solution:** Ensure `data/` directory exists and has write permissions.

### Issue: Admin login not working
**Solution:** Check your `.env` file has correct `ADMIN_USERNAME` and `ADMIN_PASSWORD`

## 📚 Next Steps

1. **Read** `INDUSTRY_UPGRADE_SUMMARY.md` for detailed improvements
2. **Review** `INDUSTRY_ASSESSMENT.md` for original assessment
3. **Check** logs in `logs/app.log` for any issues

## 🔒 Security Reminders

- ✅ Never commit `.env` file (it's in .gitignore)
- ✅ Use strong passwords in production
- ✅ Change default admin credentials
- ✅ Review logs regularly for security issues

---

**Happy Coding! 🎉**

