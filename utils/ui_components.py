"""
Modern UI components for Resume Parser NLP Application.
Provides beautiful, modern interface elements.
"""
import streamlit as st
from typing import Optional


def apply_custom_css() -> None:
    """Apply custom CSS for modern, attractive UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main App Styling */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header Styling with Animation */
    h1 {
        color: #1f77b4;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: gradient-shift 3s ease infinite;
        text-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        letter-spacing: -0.02em;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    h2 {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding-bottom: 0.5rem;
        position: relative;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    h3 {
        color: #34495e;
        font-size: 1.6rem;
        font-weight: 600;
        margin-top: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    /* Card Styling */
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        color: white;
    }
    
    .info-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 1rem 0;
        color: white;
    }
    
    /* Button Styling - Premium */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% auto;
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.85rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4), 0 0 0 0 rgba(102, 126, 234, 0.5);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.5px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6), 0 0 0 8px rgba(102, 126, 234, 0.1);
        background-position: right center;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    
    /* Sidebar Styling - Premium */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: sidebar-gradient 8s ease infinite;
    }
    
    @keyframes sidebar-gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Sidebar Elements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* File Uploader Styling */
    .uploadedFile {
        background: #f8f9fa;
        border: 2px dashed #3498db;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Progress Bar - Premium */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% auto;
        animation: progress-gradient 2s ease infinite;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes progress-gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* File Uploader - Premium */
    .uploadedFile {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .uploadedFile::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .uploadedFile:hover {
        border-color: #764ba2;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Text Input Styling - Premium */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        background: white;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 4px 12px rgba(102, 126, 234, 0.2);
        outline: none;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #764ba2;
    }
    
    /* Text Area Styling - Premium */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        background: white;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 4px 12px rgba(102, 126, 234, 0.2);
        outline: none;
        transform: translateY(-2px);
    }
    
    /* Selectbox Styling - Premium */
    .stSelectbox > div > div > select {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        outline: none;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #27ae60;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #e74c3c;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #3498db;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #f39c12;
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent #667eea transparent;
    }
    </style>
    """, unsafe_allow_html=True)


def create_hero_section(title: str, subtitle: str = "") -> None:
    """Create an attractive hero section with premium design."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255,255,255,0.1) inset;
        position: relative;
        overflow: hidden;
        animation: hero-gradient 8s ease infinite;
    ">
        <style>
        @keyframes hero-gradient {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        </style>
        <div style="position: relative; z-index: 1;">
            <h1 style="
                color: white; 
                margin: 0; 
                font-size: 3.5rem; 
                font-weight: 800;
                text-shadow: 0 4px 20px rgba(0,0,0,0.2);
                letter-spacing: -0.02em;
                line-height: 1.2;
            ">
                {title}
            </h1>
            {f'<p style="color: rgba(255,255,255,0.95); font-size: 1.3rem; margin-top: 1.5rem; font-weight: 400; text-shadow: 0 2px 10px rgba(0,0,0,0.1);">{subtitle}</p>' if subtitle else ''}
        </div>
        <div style="
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        "></div>
        <style>
        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            50% {{ transform: translate(-20px, -20px) rotate(180deg); }}
        }}
        </style>
    </div>
    """, unsafe_allow_html=True)


def create_info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """Create an attractive info card with premium design."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12), 0 0 0 1px rgba(255,255,255,0.5) inset;
        margin: 1.5rem 0;
        border-left: 6px solid #3498db;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    ">
        <div style="
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
            animation: card-float 8s ease-in-out infinite;
        "></div>
        <style>
        @keyframes card-float {{
            0%, 100% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(-30px, -30px); }}
        }}
        </style>
        <div style="position: relative; z-index: 1;">
            <h3 style="
                color: #2c3e50; 
                margin-top: 0; 
                font-size: 1.5rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 2rem;">{icon}</span>
                <span>{title}</span>
            </h3>
            <p style="
                color: #34495e; 
                margin-bottom: 0; 
                font-size: 1.05rem;
                line-height: 1.6;
                font-weight: 400;
            ">{content}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_success_card(title: str, content: str, icon: str = "✅") -> None:
    """Create an attractive success card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 1rem 0;
        border-left: 5px solid #27ae60;
    ">
        <h3 style="color: #2c3e50; margin-top: 0;">{icon} {title}</h3>
        <p style="color: #34495e; margin-bottom: 0; font-size: 1rem;">{content}</p>
    </div>
    """, unsafe_allow_html=True)


def display_skill_tags(skills: list, color_scheme: str = "purple", max_display: int = 50) -> None:
    """
    Display skills as attractive tags with premium design.
    Skills are organized in a clean grid layout with better spacing.
    
    Args:
        skills: List of skill names
        color_scheme: Color scheme for the tags (purple, blue, pink, green, red)
        max_display: Maximum number of skills to display
    """
    if not skills:
        st.info("No skills found")
        return
    
    # Handle case where skills might be a JSON string or other format
    if isinstance(skills, str):
        # First try JSON parsing
        try:
            import json
            skills = json.loads(skills)
        except (json.JSONDecodeError, ValueError):
            # If not valid JSON, try to split by common delimiters
            if ',' in skills:
                skills = [s.strip() for s in skills.split(',') if s.strip()]
            elif ';' in skills:
                skills = [s.strip() for s in skills.split(';') if s.strip()]
            elif ' ' in skills:
                # Handle space-separated skills (like "ReactOSGoCollaboration JavaScript MongoDB...")
                # Split by spaces but be smart about it
                import re
                # Split by spaces, but keep multi-word skills together
                parts = skills.split()
                skills = []
                current_skill = ""
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    # Check if this looks like the start of a new skill (capital letter after lowercase)
                    # or if it's a known skill pattern
                    if current_skill and part[0].isupper() and current_skill[-1].islower():
                        # This is likely a new skill
                        if current_skill:
                            skills.append(current_skill)
                        current_skill = part
                    else:
                        # Continue building current skill
                        if current_skill:
                            current_skill += " " + part
                        else:
                            current_skill = part
                if current_skill:
                    skills.append(current_skill)
            else:
                skills = [skills.strip()] if skills.strip() else []
    
    # Ensure skills is a list
    if not isinstance(skills, list):
        if isinstance(skills, (set, tuple)):
            skills = list(skills)
        else:
            skills = []
    
    # Remove duplicates, clean skills, and organize by category
    unique_skills = []
    seen = set()
    for skill in skills:
        # Handle non-string skills
        if not isinstance(skill, str):
            skill = str(skill)
        # Clean skill name
        clean_skill = skill.strip()
        if clean_skill and clean_skill.lower() not in seen:
            unique_skills.append(clean_skill)
            seen.add(clean_skill.lower())
    
    # Categorize skills for better organization
    def categorize_skill(skill: str) -> str:
        """Categorize skill into groups with precise matching."""
        skill_lower = skill.lower().strip()
        skill_normalized = skill_lower.replace('.', '').replace('-', ' ').replace('_', ' ')
        
        # Exact matches first for common skills
        exact_matches = {
            # Databases
            'sql': 'Databases',
            'mongodb': 'Databases',
            'mysql': 'Databases',
            'postgresql': 'Databases',
            'redis': 'Databases',
            'oracle': 'Databases',
            # Web Technologies
            'react': 'Web Technologies',
            'node.js': 'Web Technologies',
            'nodejs': 'Web Technologies',
            'express.js': 'Web Technologies',
            'expressjs': 'Web Technologies',
            'express': 'Web Technologies',
            'angular': 'Web Technologies',
            'vue': 'Web Technologies',
            'html': 'Web Technologies',
            'css': 'Web Technologies',
            # Programming Languages
            'python': 'Programming Languages',
            'java': 'Programming Languages',
            'javascript': 'Programming Languages',
            'typescript': 'Programming Languages',
            'c++': 'Programming Languages',
            'c#': 'Programming Languages',
            'go': 'Programming Languages',
            'rust': 'Programming Languages',
            'ruby': 'Programming Languages',
            'php': 'Programming Languages',
            'swift': 'Programming Languages',
            'kotlin': 'Programming Languages',
            'dart': 'Programming Languages',
            'scala': 'Programming Languages',
            'r': 'Programming Languages',
            'matlab': 'Programming Languages',
            # Soft Skills
            'collaboration': 'Soft Skills',
            'creativity': 'Soft Skills',
            'communication': 'Soft Skills',
            'problem-solving': 'Soft Skills',
            'problem solving': 'Soft Skills',
            'leadership': 'Soft Skills',
            'teamwork': 'Soft Skills',
            'public speaking': 'Soft Skills',
            # Cloud & DevOps
            'git': 'Cloud & DevOps',
            'github': 'Cloud & DevOps',
            'gitlab': 'Cloud & DevOps',
            'docker': 'Cloud & DevOps',
            'kubernetes': 'Cloud & DevOps',
            'aws': 'Cloud & DevOps',
            'azure': 'Cloud & DevOps',
        }
        
        # Check exact matches first
        if skill_lower in exact_matches:
            return exact_matches[skill_lower]
        
        # Check normalized exact matches
        if skill_normalized in exact_matches:
            return exact_matches[skill_normalized]
        
        # Soft Skills - Check with keywords
        soft_skills_keywords = [
            'communication', 'collaboration', 'leadership', 'problem solving', 'problem-solving',
            'creativity', 'teamwork', 'public speaking', 'presentation', 'negotiation',
            'time management', 'adaptability', 'critical thinking', 'analytical', 'interpersonal'
        ]
        if any(soft in skill_normalized for soft in soft_skills_keywords):
            return 'Soft Skills'
        
        # Databases - Check before Programming Languages
        db_keywords = [
            'mongodb', 'mysql', 'postgresql', 'postgres', 'redis', 'oracle', 'cassandra',
            'elasticsearch', 'dynamodb', 'nosql', 'database', 'db', 'sqlite',
            'neo4j', 'couchdb', 'mariadb', 'firebase', 'supabase'
        ]
        if any(db in skill_normalized for db in db_keywords):
            return 'Databases'
        
        # Web Technologies
        web_keywords = [
            'react', 'angular', 'vue', 'node', 'nodejs', 'express', 'expressjs', 'html',
            'css', 'bootstrap', 'tailwind', 'jquery', 'next', 'nextjs', 'nuxt', 'svelte',
            'ember', 'backbone', 'webpack', 'vite', 'npm', 'yarn', 'frontend', 'backend',
            'fullstack', 'full stack'
        ]
        if any(web in skill_normalized for web in web_keywords):
            return 'Web Technologies'
        
        # Cloud & DevOps
        cloud_keywords = [
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s', 'jenkins',
            'terraform', 'ansible', 'ci/cd', 'cicd', 'devops', 'git', 'github', 'gitlab',
            'bitbucket', 'circleci', 'travis', 'github actions', 'cloud', 'serverless'
        ]
        if any(cloud in skill_normalized for cloud in cloud_keywords):
            return 'Cloud & DevOps'
        
        # Data Science & ML
        ml_keywords = [
            'machine learning', 'ml', 'data science', 'tensorflow', 'pytorch', 'keras',
            'pandas', 'numpy', 'scikit', 'sklearn', 'ai', 'artificial intelligence',
            'nlp', 'natural language', 'deep learning', 'neural network', 'opencv',
            'matplotlib', 'seaborn', 'jupyter', 'data analysis', 'data visualization'
        ]
        if any(ml in skill_normalized for ml in ml_keywords):
            return 'Data Science & ML'
        
        # Frameworks & Tools
        framework_keywords = [
            'spring', 'django', 'flask', 'laravel', 'rails', 'ruby on rails', 'graphql',
            'rest', 'restful', 'api', 'fastapi', 'nest', 'nestjs', 'asp.net', 'dotnet',
            '.net', 'symfony', 'codeigniter', 'phalcon'
        ]
        if any(fw in skill_normalized for fw in framework_keywords):
            return 'Frameworks & Tools'
        
        # Programming Languages - Check last
        lang_keywords = [
            'python', 'java', 'javascript', 'typescript', 'cpp', 'csharp',
            'golang', 'rust', 'ruby', 'swift', 'kotlin', 'dart', 'scala',
            'r language', 'r programming', 'julia', 'perl', 'haskell', 'lua',
            'clojure', 'erlang', 'elixir', 'vb.net', 'visual basic', 'cobol',
            'fortran', 'assembly', 'pascal', 'ada', 'abap', 'rpg', 'lisp', 'prolog'
        ]
        if any(lang in skill_normalized for lang in lang_keywords):
            return 'Programming Languages'
        
        return 'Other Skills'
    
    # Group skills by category
    categorized = {}
    for skill in unique_skills[:max_display]:
        category = categorize_skill(skill)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(skill)
    
    # Sort skills within each category alphabetically
    for category in categorized:
        categorized[category] = sorted(categorized[category], key=str.lower)
    
    # Enhanced color schemes with animations
    color_schemes = {
        "purple": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
        "blue": "linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #43e97b 100%)",
        "pink": "linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%)",
        "green": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 50%, #43e97b 100%)",
        "red": "linear-gradient(135deg, #fa709a 0%, #fee140 50%, #ff6b6b 100%)",
    }
    
    gradient = color_schemes.get(color_scheme, color_schemes["purple"])
    
    # Category order for display
    category_order = [
        'Programming Languages',
        'Web Technologies',
        'Databases',
        'Cloud & DevOps',
        'Data Science & ML',
        'Frameworks & Tools',
        'Soft Skills',
        'Other Skills'
    ]
    
    # Create skill tags organized by category
    category_html = ""
    for category in category_order:
        if category in categorized and categorized[category]:
            category_skills = categorized[category]
            skills_html = "".join([
                f'<span style="'
                f'display: inline-block; '
                f'background: {gradient}; '
                f'background-size: 200% auto; '
                f'color: white; '
                f'padding: 0.7rem 1.6rem; '
                f'border-radius: 25px; '
                f'margin: 0.4rem 0.4rem; '
                f'font-size: 0.9rem; '
                f'font-weight: 600; '
                f'box-shadow: 0 4px 15px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.1) inset; '
                f'transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); '
                f'cursor: pointer; '
                f'position: relative; '
                f'overflow: hidden; '
                f'letter-spacing: 0.2px; '
                f'text-shadow: 0 1px 3px rgba(0,0,0,0.2); '
                f'white-space: nowrap; '
                f'onmouseover="this.style.transform=\'translateY(-3px) scale(1.05)\'; this.style.boxShadow=\'0 8px 25px rgba(0,0,0,0.25), 0 0 0 2px rgba(255,255,255,0.2) inset\';" '
                f'onmouseout="this.style.transform=\'translateY(0) scale(1)\'; this.style.boxShadow=\'0 4px 15px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.1) inset\';" '
                f'">{str(skill).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")}</span>'
                for skill in category_skills
            ])
            
            # Escape category name for HTML safety
            category_escaped = str(category).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            category_html += f'''
            <div style="margin-bottom: 2rem;">
                <h4 style="
                    color: #2c3e50;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 2px solid rgba(102, 126, 234, 0.2);
                ">📌 {category_escaped} ({len(category_skills)})</h4>
                <div style="
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: flex-start;
                    align-items: center;
                    gap: 0.5rem;
                    margin: 0;
                    line-height: 1.8;
                ">
                    {skills_html}
                </div>
            </div>
            '''
    
    # Show count if skills are limited
    total_skills = len(skills)
    displayed_count = sum(len(skills) for skills in categorized.values())
    count_info = ""
    if total_skills > displayed_count:
        count_info = f'<div style="color: #7f8c8d; font-size: 0.85rem; margin-top: 1rem; text-align: center; font-weight: 500; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.1);">📊 Showing {displayed_count} of {total_skills} unique skills</div>'
    
    # Ensure category_html is not empty
    if not category_html.strip():
        st.info("No skills to display")
        return
    
    # Render the HTML - use separate markdown calls for better reliability
    try:
        # First render the container
        st.markdown("""
        <div style="
            margin: 1.5rem 0;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
        ">
        """, unsafe_allow_html=True)
        
        # Then render the category HTML
        st.markdown(category_html, unsafe_allow_html=True)
        
        # Render count info if present
        if count_info:
            st.markdown(count_info, unsafe_allow_html=True)
        
        # Close the container and add styles
        st.markdown("""
        </div>
        <style>
        @keyframes skill-gradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        </style>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        # Fallback: display skills in a simpler format if HTML rendering fails
        import traceback
        logger = None
        try:
            from utils.logger import setup_logger
            logger = setup_logger(__name__)
            logger.error(f"Error rendering skills HTML: {e}\n{traceback.format_exc()}")
        except:
            pass
        
        # Show skills as simple tags using Streamlit columns
        st.warning("Displaying skills in simplified format")
        for category in category_order:
            if category in categorized and categorized[category]:
                st.subheader(f"📌 {category} ({len(categorized[category])})")
                # Use st.columns for better layout
                num_cols = min(4, len(categorized[category]))
                if num_cols > 0:
                    cols = st.columns(num_cols)
                    for idx, skill in enumerate(categorized[category][:20]):
                        col_idx = idx % num_cols
                        with cols[col_idx]:
                            st.markdown(f'<span style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; margin: 0.25rem; font-weight: 600;">{skill}</span>', unsafe_allow_html=True)


def create_metric_card(label: str, value: str, delta: Optional[str] = None, icon: str = "📊") -> None:
    """Create an attractive metric card with premium design."""
    delta_html = f'<div style="color: #27ae60; font-size: 0.95rem; margin-top: 0.75rem; font-weight: 600;">{delta}</div>' if delta else ''
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1), 0 0 0 1px rgba(102, 126, 234, 0.1) inset;
        border-left: 6px solid #667eea;
        margin: 0.75rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    ">
        <div style="
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
            animation: metric-float 6s ease-in-out infinite;
        "></div>
        <style>
        @keyframes metric-float {{
            0%, 100% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(-20px, -20px); }}
        }}
        </style>
        <div style="position: relative; z-index: 1;">
            <div style="
                font-size: 2.5rem; 
                margin-bottom: 0.75rem;
                filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
                display: inline-block;
                animation: icon-bounce 2s ease-in-out infinite;
            ">{icon}</div>
            <style>
            @keyframes icon-bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            </style>
            <div style="
                color: #7f8c8d; 
                font-size: 0.95rem; 
                margin-bottom: 0.75rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">{label}</div>
            <div style="
                color: #2c3e50; 
                font-size: 2.5rem; 
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.02em;
            ">{value}</div>
            {delta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_feature_card(title: str, description: str, icon: str = "✨") -> None:
    """Create an attractive feature card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-top: 4px solid #667eea;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <h4 style="color: #2c3e50; margin-top: 0.5rem; margin-bottom: 0.5rem;">{title}</h4>
        <p style="color: #7f8c8d; margin-bottom: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def create_progress_bar(value: int, max_value: int = 100, label: str = "") -> None:
    """Create an attractive progress bar."""
    percentage = (value / max_value) * 100
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        {f'<div style="color: #2c3e50; font-weight: 600; margin-bottom: 0.5rem;">{label}</div>' if label else ''}
        <div style="
            background: #ecf0f1;
            border-radius: 25px;
            height: 30px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                width: {percentage}%;
                border-radius: 25px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 600;
                font-size: 0.9rem;
                transition: width 0.5s ease;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
            ">
                {value}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_badge(text: str, color: str = "blue") -> str:
    """Create an attractive badge."""
    colors = {
        "blue": "#3498db",
        "green": "#27ae60",
        "red": "#e74c3c",
        "orange": "#f39c12",
        "purple": "#9b59b6",
    }
    
    bg_color = colors.get(color, colors["blue"])
    
    return f"""
    <span style="
        background: {bg_color};
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0.25rem;
    ">{text}</span>
    """


def create_animated_header(text: str) -> None:
    """Create an animated header."""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    ">
        <h1 style="
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        ">{text}</h1>
    </div>
    """, unsafe_allow_html=True)

