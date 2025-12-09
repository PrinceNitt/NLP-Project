<center>

# Resume Parser Using NLP

</center>

## 📋 Table of Contents
- [Overview](#overview)
- [प्रोजेक्ट के बारे में (About the Project in Hindi)](#प्रोजेक्ट-के-बारे-में-about-the-project-in-hindi)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How to Run the Application](#how-to-run-the-application)
- [Functionalities](#functionalities)
  - [User](#user)
  - [Recruiters](#recruiters)
  - [Feedback](#feedback)
  - [Admin](#admin)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Team](#team)
- [License](#license)

## Overview

The **Resume NLP Parser** revolutionizes the recruitment process by employing sophisticated Natural Language Processing (NLP) techniques. This tool efficiently extracts, analyzes, and visualizes data from resumes, enabling data-driven decision-making in hiring. Tailored for both candidates and recruiters, it enhances the application experience by parsing resumes comprehensively and offering powerful insights.

## प्रोजेक्ट के बारे में (About the Project in Hindi)

**Resume NLP Parser** ek advanced tool hai jo Natural Language Processing (NLP) techniques ka use karke resumes ko analyze karta hai. Ye project recruitment process ko simple aur efficient banata hai.

### मुख्य विशेषताएं (Key Highlights):
- 📄 **Resume Parsing**: PDF resumes se automatically information extract karta hai
- 🔍 **Skill Extraction**: Candidate ki skills ko identify karta hai
- 👤 **Contact Details**: Name, email, phone number extract karta hai
- 🎓 **Education Info**: Degree aur educational background nikalta hai
- 💼 **Experience Level**: Work experience aur seniority level determine karta hai
- 📊 **Resume Score**: 100 me se resume ko score deta hai
- 🎯 **Job Recommendations**: Candidate ke liye suitable jobs suggest karta hai

### किसके लिए है ये प्रोजेक्ट (Who is this for):
1. **Job Seekers**: Apne resume ko analyze kar sakte hain aur improve kar sakte hain
2. **Recruiters**: Multiple resumes ko quickly screen kar sakte hain
3. **HR Teams**: Candidate selection process ko fast kar sakte hain
4. **Students**: NLP aur machine learning seekhne ke liye example project

### कैसे काम करता है (How it works):
1. User apna resume PDF format me upload karta hai
2. System NLP algorithms use karke resume ko parse karta hai
3. Important information automatically extract ho jati hai
4. User ko parsed data visual format me dikhta hai
5. System resume ko score deta hai aur improvements suggest karta hai

## Key Features

- **Comprehensive Resume Parsing**: Extracts detailed information including contact details, skills, work experience, and educational background from resumes in PDF formats.

- **Advanced NLP Analysis**: Utilizes leading-edge NLP libraries such as NLTK and spaCy to delve into resume text, identifying keywords, phrases, and patterns to evaluate candidates' qualifications comprehensively.

- **Intuitive Data Visualization**: Presents parsed data through interactive visualizations, empowering recruiters with efficient insights into applicants' profiles.

- **Robust Search and Filtering**: Offers powerful search and filtering functionalities, enabling swift access to specific candidate information.

## Technologies Used

The project leverages the following technologies and tools:

- **Python 3.12**: Primary programming language for NLP, data analysis, and backend functionalities.
- **NLP Libraries**: 
  - **NLTK**: Natural Language Toolkit for text processing
  - **spaCy**: Advanced NLP library for named entity recognition (NER) and text parsing
  - **en_core_web_sm**: spaCy's English language model
- **Web Interface**: **Streamlit** - Creates a user-friendly web-based interface for seamless user interaction
- **PDF Processing**: 
  - **PyMuPDF (fitz)**: For extracting text and data from PDF documents
- **Data Visualization**: 
  - **Matplotlib**: For static visualizations
  - **Plotly**: For interactive visualizations
- **Database Management**: **SQLite** - Efficiently manages and queries resume data
- **Model Training**: Incorporates spaCy's NER pipeline for training custom models for skill extraction
- **Data Handling**: **Pandas** - For data manipulation and CSV file operations

## Project Structure

```
NLP-Project/
├── main.py                  # Main application entry point
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── SETUP.md                 # Detailed setup guide
├── .gitignore              # Git ignore rules
│
├── modules/                 # Application modules
│   ├── __init__.py         # Package initializer
│   ├── users.py            # User mode functionality
│   ├── recruiters.py       # Recruiter mode functionality
│   ├── admin.py            # Admin panel functionality
│   └── feedback.py         # Feedback system
│
├── utils/                   # Utility modules
│   ├── __init__.py         # Package initializer
│   ├── resume_parser.py    # Core resume parsing logic
│   └── resume_store.py     # Resume storage utilities
│
├── scripts/                 # Training and utility scripts
│   ├── __init__.py         # Package initializer
│   ├── train_model.py      # Model training script
│   └── train_2.py          # Additional training utilities
│
├── data/                    # Data files and database
│   ├── newSkills.csv       # Skills database
│   ├── UpdatedSkills.csv   # Updated skills list
│   ├── sugestedSkills.csv  # Job-wise suggested skills
│   ├── majors.csv          # Academic majors list
│   ├── position.csv        # Job positions and keywords
│   ├── feedback_data.csv   # User feedback storage
│   └── user_pdfs.db        # SQLite database for uploaded PDFs
│
└── TrainedModel/           # Trained NLP models
    └── skills/             # Custom trained skill extraction model
```

## How to Run the Application

> **📖 For detailed setup instructions, see [SETUP.md](SETUP.md)**

### Prerequisites
- Python 3.8 or higher (Python 3.12 recommended)
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection (for initial model downloads)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrinceNitt/NLP-Project.git
   cd NLP-Project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy English model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Download NLTK data** (if not automatically downloaded)
   ```python
   python -c "import nltk; nltk.download('punkt')"
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

7. **Access the application**
   - The application will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`

### Optional: Training the Custom NER Model

The application includes a custom skill extraction model that can be trained for better accuracy. If you want to use the trained model:

1. **Train the model**
   ```bash
   python scripts/train_model.py
   ```
   This will create a trained model in the `TrainedModel/skills/` directory.

2. **Verify the model**
   ```bash
   python -c "import spacy; nlp = spacy.load('TrainedModel/skills'); print('Model loaded successfully')"
   ```

**Note:** The application will work without the trained model by using CSV-based skill extraction. The trained model enhances accuracy but is not required.

### Quick Start (Hindi/Hinglish)
```bash
# Repository clone karo
git clone https://github.com/PrinceNitt/NLP-Project.git
cd NLP-Project

# Dependencies install karo
pip install -r requirements.txt

# spaCy model download karo
python -m spacy download en_core_web_sm

# Application run karo
streamlit run main.py
```

## Functionalities

### User

The User section allows individuals to upload their resumes. The system then extracts and displays parsed information, showcasing extracted details such as:

- **Personal Information**: First name, last name, email, phone number
- **Skills**: Technical and non-technical skills extracted from the resume
- **Education**: Degree, major, and educational institutions
- **Experience**: Level of experience (Entry Level, Mid-Junior, Mid-Senior, Senior)
- **Resume Score**: A score out of 100 based on completeness
- **Job Suggestions**: Recommended positions based on skills and experience
- **Skill Suggestions**: Skills needed for desired job roles

**How to use:**
1. Select "Users" from the sidebar
2. Upload your resume in PDF format
3. View the extracted information and your resume score
4. Enter a desired job role to get skill recommendations

### Recruiters

Recruiters can upload multiple resumes and specify desired skills. The system performs skill-based searching across the resumes, presenting the findings in a structured format for better evaluation.

**Features:**
- Upload multiple resumes simultaneously
- Define required skills for a position
- Automatically extract candidate names
- Match candidate skills with job requirements
- View all parsed skills from each resume
- Get a clear "Found/Not Found" status for each required skill
- Save required skills to the database for future reference

**How to use:**
1. Select "Recruiters" from the sidebar
2. Upload one or more PDF resumes
3. Enter required skills (comma-separated)
4. Click "Save Required Skills" to store them
5. Review candidate information and skill matches

### Feedback

This section enables users to provide feedback, suggestions, or improvements for the system's enhancement. Users can share their thoughts on improving parsing accuracy, user interface, or additional functionalities.

**Features:**
- Submit feedback with your name
- Share suggestions for improvement
- Report parsing issues
- Request new features
- All feedback is timestamped and stored

**How to use:**
1. Select "Feedback" from the sidebar
2. Enter your name
3. Write your feedback or suggestions
4. Click "Submit Feedback"

### Admin

Admins have privileged access, requiring authentication to access this section. They can review uploaded resumes, manage feedback received from users, and download uploaded resumes for further analysis or archiving.

**Features:**
- Secure login with username and password
- View all uploaded resumes
- Download resumes for offline review
- Access all user feedback
- View latest 10 feedbacks by default
- Option to view all feedback data

**Admin Credentials:**
- Username: `prince81`
- Password: `12345`

**How to use:**
1. Select "Admin" from the sidebar
2. Enter admin credentials
3. View uploaded resumes and download them
4. Review user feedback
5. Click "View More Feedbacks" to see all feedback

**Note:** Admin credentials should be changed in production environment for security reasons.

## Troubleshooting

### Common Issues and Solutions

#### 1. spaCy Model Not Found
**Error:** `Can't find model 'en_core_web_sm'`

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

#### 2. NLTK Data Not Found
**Error:** `Resource punkt not found`

**Solution:**
```python
import nltk
nltk.download('punkt')
```

#### 3. Import Error for Modules
**Error:** `ModuleNotFoundError: No module named 'modules'`

**Solution:**
- Ensure you're running the application from the project root directory
- Check that the `modules/` directory exists with `__init__.py`

#### 4. Database Connection Error
**Error:** `no such table: user_uploaded_pdfs`

**Solution:**
- The table will be created automatically on first use
- Ensure the `data/` directory has write permissions

#### 5. PDF Upload Issues
**Problem:** PDF not parsing correctly

**Solutions:**
- Ensure the PDF is not password-protected
- Check that the PDF contains searchable text (not just images)
- Try re-saving the PDF if it's corrupted

#### 6. Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Run on a different port
streamlit run main.py --server.port 8502
```

#### 7. Missing CSV Files
**Error:** `FileNotFoundError: data/newSkills.csv`

**Solution:**
- Ensure all CSV files are in the `data/` directory
- Check that you haven't moved files after cloning

### Performance Tips
- For large PDF files, processing may take 10-30 seconds
- Close unnecessary applications to free up RAM
- Use PDF files under 5MB for best performance
- Clear browser cache if the UI behaves unexpectedly

## Future Enhancements

In the pipeline for this project are several enhancements:

- **Machine Learning Integration**: 
  - Integrate machine learning algorithms for better resume categorization
  - Add resume ranking based on job descriptions
  - Implement candidate scoring using ML models

- **Enhanced Skill Extraction**:
  - Improve skill extraction accuracy with advanced NER models
  - Add support for industry-specific terminology
  - Implement fuzzy matching for skill variations

- **Multi-format Support**:
  - Add support for DOCX and TXT resume formats
  - Enable bulk processing of resumes
  - Support for multi-language resumes

- **Advanced Analytics**:
  - Add data visualization dashboards
  - Implement candidate comparison features
  - Generate hiring insights and statistics

- **Customization Features**: 
  - Offer customization options for parsing algorithms
  - Tailor extraction to specific job roles or industries
  - Allow custom skill databases

- **Database Integration and Management**: 
  - Implement PostgreSQL/MySQL for production use
  - Add data export functionality (Excel, CSV)
  - Implement search and filter capabilities

- **API Development**:
  - RESTful API for integration with other systems
  - Webhook support for automated workflows
  - Third-party ATS integration

- **Security Enhancements**:
  - Add OAuth/SAML authentication
  - Implement role-based access control (RBAC)
  - Add data encryption for sensitive information
  - Implement audit logging

- **UI/UX Improvements**:
  - Add dark mode support
  - Implement drag-and-drop file upload
  - Add progress indicators for long-running operations
  - Mobile-responsive design

## Team

- **Prince Kumar** (106121096)
- **Roushan Kumar** (106121108)

## License

This project is open-source and available for educational and research purposes. Please provide appropriate attribution when using or modifying this code.

---

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the team members
- Use the Feedback section in the application

---

**Made with ❤️ using Python, spaCy, and Streamlit**