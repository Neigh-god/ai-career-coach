import streamlit as st
import requests

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== API CONFIG ==========
API_URL = "https://ai-career-coach-5njl.onrender.com"

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a1a 0%, #12122a 50%, #0d1b2a 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
        padding: 80px 40px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid rgba(0,212,170,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0,212,170,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4aa, #00a8e8, #e94560, #00d4aa);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 5s ease infinite;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #8892b0;
        max-width: 600px;
        margin: 0 auto 40px;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(90deg, #00d4aa, #00a8e8);
        color: white;
        padding: 16px 32px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 0 10px;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,212,170,0.3);
    }
    
    .btn-secondary {
        background: transparent;
        color: #00d4aa;
        padding: 16px 32px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 600;
        border: 2px solid #00d4aa;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 0 10px;
    }
    
    .btn-secondary:hover {
        background: rgba(0,212,170,0.1);
        transform: translateY(-2px);
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255,255,255,0.03);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255,255,255,0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: var(--accent-color);
        font-weight: 600;
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* Stats Section */
    .stats-section {
        background: rgba(255,255,255,0.03);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        margin: 15px 0;
        color: #8892b0;
    }
    
    .stat-icon {
        width: 20px;
        height: 20px;
        margin-right: 12px;
        color: var(--accent-color);
    }
    
    /* Floating particles */
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #00d4aa;
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
        opacity: 0.3;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) translateX(0); }
        25% { transform: translateY(-20px) translateX(10px); }
        50% { transform: translateY(-10px) translateX(-10px); }
        75% { transform: translateY(-30px) translateX(5px); }
    }
    
    h1 { color: #00d4aa !important; font-weight: 700 !important; }
    h2 { color: #e94560 !important; font-weight: 600 !important; }
    h3 { color: #0f3460 !important; }
    
    .stButton>button {
        background: linear-gradient(90deg, #00d4aa, #00a8e8);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
    }
    
    .stProgress>div>div {
        background: linear-gradient(90deg, #00d4aa, #00a8e8);
    }
    
    [data-testid="stMetricValue"] {
        color: #00d4aa !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Hide default sidebar */
    .css-1d391kg { display: none; }
    .css-1544g2d { display: none; }
</style>
""", unsafe_allow_html=True)

# ========== CUSTOM NAVIGATION ==========
st.markdown("""
<div style="
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    margin-bottom: 20px;
">
    <div style="display: flex; align-items: center; gap: 10px;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="6"></circle>
            <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <span style="color: #00d4aa; font-size: 1.5rem; font-weight: 700;">AI Career Coach</span>
    </div>
    <div style="display: flex; gap: 30px;">
        <a href="?page=home" style="color: #8892b0; text-decoration: none; font-weight: 500; transition: color 0.3s;">Home</a>
        <a href="?page=resume" style="color: #8892b0; text-decoration: none; font-weight: 500; transition: color 0.3s;">Resume</a>
        <a href="?page=interview" style="color: #8892b0; text-decoration: none; font-weight: 500; transition: color 0.3s;">Interview</a>
        <a href="?page=report" style="color: #8892b0; text-decoration: none; font-weight: 500; transition: color 0.3s;">Report</a>
        <a href="?page=about" style="color: #8892b0; text-decoration: none; font-weight: 500; transition: color 0.3s;">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== PAGE SELECTION ==========
query_params = st.query_params
page = query_params.get("page", "home")

# ========== HOME PAGE ==========
if page == "home":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="particle" style="top: 20%; left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="top: 60%; left: 80%; animation-delay: 1s;"></div>
        <div class="particle" style="top: 40%; left: 50%; animation-delay: 2s;"></div>
        <div class="particle" style="top: 80%; left: 20%; animation-delay: 3s;"></div>
        <div class="particle" style="top: 30%; left: 70%; animation-delay: 4s;"></div>
        
        <h1 class="hero-title">AI Career Coach</h1>
        <p class="hero-subtitle">
            Your personal AI-powered career development assistant. 
            Analyze resumes, practice interviews, identify skill gaps, 
            and generate actionable career reports.
        </p>
        <div style="position: relative; z-index: 1;">
            <a href="?page=resume" class="btn-primary">Get Started</a>
            <a href="https://github.com/Neigh-god/ai-career-coach" class="btn-secondary" target="_blank">View on GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Features</h2>", unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card" style="--accent-color: #00d4aa;">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <p class="feature-title">Resume<br>Analyzer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="feature-card" style="--accent-color: #00a8e8;">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#00a8e8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <p class="feature-title">Skill Gap<br>Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="feature-card" style="--accent-color: #e94560;">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#e94560" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
            <p class="feature-title">Interview<br>Practice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col4:
        st.markdown("""
        <div class="feature-card" style="--accent-color: #ffc107;">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <p class="feature-title">Career<br>Report</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="stats-section">
            <h3 style="color: #00d4aa; margin-top: 0;">Quick Stats</h3>
            <div class="stat-item">
                <svg class="stat-icon" style="--accent-color: #00d4aa;" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                </svg>
                Get started in seconds
            </div>
            <div class="stat-item">
                <svg class="stat-icon" style="--accent-color: #e94560;" viewBox="0 0 24 24" fill="none" stroke="#e94560" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Target any tech role
            </div>
            <div class="stat-item">
                <svg class="stat-icon" style="--accent-color: #00a8e8;" viewBox="0 0 24 24" fill="none" stroke="#00a8e8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
                Track your progress
            </div>
            <div class="stat-item">
                <svg class="stat-icon" style="--accent-color: #ffc107;" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a10 10 0 0 1 10 10c0 5.523-4.477 10-10 10S2 17.523 2 12 2 2 12 2z"></path>
                    <path d="M12 6v6l4 2"></path>
                </svg>
                AI-powered feedback
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # API Status
        try:
            response = requests.get(f"{API_URL}/health", timeout=3)
            if response.status_code == 200:
                st.markdown("""
                <div style="background: rgba(0,212,170,0.1); padding: 20px; border-radius: 15px; border: 1px solid rgba(0,212,170,0.3); text-align: center;">
                    <div style="width: 12px; height: 12px; background: #00d4aa; border-radius: 50%; display: inline-block; margin-right: 8px; animation: pulse 2s infinite;"></div>
                    <span style="color: #00d4aa; font-weight: 600;">API Connected</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("API Issue")
        except:
            st.error("API Offline")

# ========== RESUME ANALYZER ==========
elif page == "resume":
    st.markdown("<h1>Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8892b0;'>Upload your resume and get instant ATS feedback</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;">
                <h4 style="color: #00d4aa; margin-top: 0;">File Details</h4>
            """, unsafe_allow_html=True)
            st.write(f"**{uploaded_file.name}**")
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("Analyze Resume", type="primary", use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/resume/upload", files=files, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state["last_resume"] = data
                            st.success("Analysis Complete!")
                        else:
                            st.error(f"{response.json().get('detail', 'Error')}")
                    except Exception as e:
                        st.error(f"{str(e)}")
        
        with col2:
            if "last_resume" in st.session_state:
                data = st.session_state["last_resume"]
                score = data["score"]["overall_score"]
                
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 3rem; font-weight: 700; color: {'#00d4aa' if score >= 70 else '#ffc107' if score >= 50 else '#e94560'};">
                        {score}%
                    </div>
                    <div style="color: #8892b0; font-size: 0.9rem;">ATS Compatibility Score</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.progress(score / 100)
                
                tabs = st.tabs(["Strengths", "Weaknesses", "Suggestions", "Parsed Data"])
                
                with tabs[0]:
                    for s in data["score"]["strengths"]:
                        st.markdown(f"""
                        <div style="background: rgba(0,212,170,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #00d4aa;">
                            {s}
                        </div>
                        """, unsafe_allow_html=True)
                
                with tabs[1]:
                    for w in data["score"]["weaknesses"]:
                        st.markdown(f"""
                        <div style="background: rgba(233,69,96,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #e94560;">
                            {w}
                        </div>
                        """, unsafe_allow_html=True)
                
                with tabs[2]:
                    for s in data["score"]["suggestions"]:
                        st.markdown(f"""
                        <div style="background: rgba(0,168,232,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #00a8e8;">
                            {s}
                        </div>
                        """, unsafe_allow_html=True)
                
                with tabs[3]:
                    parsed = data["parsed_data"]
                    st.json({
                        "Name": parsed.get("name"),
                        "Email": parsed.get("email"),
                        "Phone": parsed.get("phone"),
                        "Skills": parsed.get("skills", [])
                    })

# ========== INTERVIEW PRACTICE ==========
elif page == "interview":
    st.markdown("<h1>Interview Practice</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8892b0;'>Practice with AI-generated questions and get instant feedback</p>", unsafe_allow_html=True)
    
    if "interview_session" not in st.session_state:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox("Interview Type", ["behavioral", "technical", "situational"])
        
        with col2:
            question_count = st.slider("Questions", 1, 5, 3)
        
        with col3:
            user_id = st.text_input("User ID", value="user-123")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Start Interview", type="primary", use_container_width=True):
            with st.spinner("Generating questions..."):
                try:
                    response = requests.post(
                        f"{API_URL}/interview/start",
                        json={"user_id": user_id, "category": category, "question_count": question_count},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.session_state["interview_session"] = response.json()
                        st.session_state["current_q"] = 0
                        st.rerun()
                    else:
                        st.error(f"{response.json().get('detail', 'Error')}")
                except Exception as e:
                    st.error(f"{str(e)}")
    
    else:
        session = st.session_state["interview_session"]
        questions = session["questions"]
        current = st.session_state.get("current_q", 0)
        
        progress = current / len(questions)
        st.progress(progress)
        st.markdown(f"<p style='text-align: center; color: #8892b0;'>Question {current + 1} of {len(questions)}</p>", unsafe_allow_html=True)
        
        if current < len(questions):
            q = questions[current]
            
            st.markdown(f"""
            <div style="background: rgba(0,168,232,0.1); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,168,232,0.3); margin: 20px 0;">
                <p style="color: #00a8e8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;">
                    {q['category']} • {q['difficulty'].upper()}
                </p>
                <h3 style="color: white; margin: 0; font-size: 1.3rem;">{q['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.text_area("Your Answer", height=150, key=f"ans_{current}", placeholder="Type your answer here...")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Submit", type="primary", use_container_width=True):
                    if answer.strip():
                        with st.spinner("Evaluating..."):
                            try:
                                response = requests.post(
                                    f"{API_URL}/interview/{session['session_id']}/answer",
                                    json={"question_id": q["id"], "user_answer": answer},
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    fb = response.json()
                                    st.session_state[f"fb_{current}"] = fb
                                    st.session_state["current_q"] = current + 1
                                    st.rerun()
                            except Exception as e:
                                st.error(f"{str(e)}")
                    else:
                        st.warning("Please enter an answer")
        else:
            st.balloons()
            st.markdown("""
            <div style="text-align: center; padding: 40px;">
                <h1 style="color: #00d4aa; font-size: 3rem;">Interview Complete!</h1>
            </div>
            """, unsafe_allow_html=True)
            
            for i in range(len(questions)):
                if f"fb_{i}" in st.session_state:
                    fb = st.session_state[f"fb_{i}"]
                    score = fb["feedback"]["score"]
                    color = "#00d4aa" if score >= 70 else "#ffc107" if score >= 50 else "#e94560"
                    
                    with st.expander(f"Question {i+1} — Score: {score}/100"):
                        st.markdown(f"""
                        <div style="background: rgba({ '0,212,170' if score >= 70 else '255,193,7' if score >= 50 else '233,69,96'},0.1); 
                                    padding: 15px; border-radius: 10px; 
                                    border-left: 4px solid {color};">
                            <p style="color: {color}; font-weight: 600; margin: 0 0 10px 0;">Score: {score}/100</p>
                            <p><strong>Strengths:</strong> {fb['feedback']['strengths']}</p>
                            <p><strong>Improvements:</strong> {fb['feedback']['improvements']}</p>
                            <p><strong>Model Answer:</strong> {fb['feedback']['model_answer']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            if st.button("Start New Interview", type="primary"):
                del st.session_state["interview_session"]
                st.rerun()

# ========== CAREER REPORT ==========
elif page == "report":
    st.markdown("<h1>Career Report</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8892b0;'>Generate a comprehensive career readiness report</p>", unsafe_allow_html=True)
    
    with st.form("report_form"):
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px;">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("User ID", value="user-123")
            target_role = st.selectbox(
                "Target Role",
                ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer"]
            )
        
        with col2:
            resume_score = st.slider("Resume Score", 0, 100, 65)
            current_skills = st.text_area("Current Skills (comma-separated)", "Python, Git, SQL, Docker")
        
        resume_strengths = st.text_area("Resume Strengths (one per line)", "Strong technical skills\nGood project experience")
        resume_weaknesses = st.text_area("Resume Weaknesses (one per line)", "Lack of metrics\nNo certifications")
        
        interview_session_id = st.text_input("Interview Session ID (optional)", help="Leave empty if no interview done")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Generate Report", use_container_width=True)
    
    if submitted:
        with st.spinner("Generating your career report..."):
            try:
                payload = {
                    "user_id": user_id,
                    "target_role": target_role,
                    "resume_score": resume_score,
                    "resume_strengths": [s.strip() for s in resume_strengths.split("\n") if s.strip()],
                    "resume_weaknesses": [s.strip() for s in resume_weaknesses.split("\n") if s.strip()],
                    "current_skills": [s.strip() for s in current_skills.split(",") if s.strip()]
                }
                
                if interview_session_id.strip():
                    payload["interview_session_id"] = interview_session_id.strip()
                
                response = requests.post(f"{API_URL}/report/generate", json=payload, timeout=15)
                
                if response.status_code == 200:
                    report = response.json()
                    
                    st.balloons()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Resume", f"{report['resume_section']['overall_score']}/100")
                    with col2:
                        st.metric("Skill Coverage", f"{report['skill_gap_section']['coverage_percent']}%")
                    with col3:
                        if report["interview_section"]:
                            st.metric("Interview", f"{report['interview_section']['average_score']}/100")
                        else:
                            st.metric("Interview", "N/A")
                    
                    st.divider()
                    
                    st.markdown(f"""
                    <div style="background: rgba(0,212,170,0.1); padding: 25px; border-radius: 15px; border: 1px solid rgba(0,212,170,0.3); margin: 20px 0;">
                        <h3 style="color: #00d4aa; margin-top: 0;">Overall Recommendation</h3>
                        <p style="color: white; font-size: 1.1rem; line-height: 1.6;">{report['overall_recommendation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    tabs = st.tabs(["Missing Skills", "Learning Path", "Next Steps"])
                    
                    with tabs[0]:
                        if report["skill_gap_section"]["missing_skills"]:
                            for skill in report["skill_gap_section"]["missing_skills"]:
                                st.markdown(f"""
                                <div style="background: rgba(233,69,96,0.1); padding: 12px 20px; border-radius: 8px; margin: 8px 0; 
                                            border-left: 3px solid #e94560; display: flex; align-items: center;">
                                    <span style="font-size: 1.2rem; margin-right: 10px;">X</span>
                                    <span style="color: white; font-weight: 500;">{skill}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.success("No major skill gaps!")
                    
                    with tabs[1]:
                        for item in report["skill_gap_section"]["learning_path"]:
                            priority_color = "#e94560" if item["priority"] == "high" else "#ffc107"
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin: 10px 0;
                                        border-left: 3px solid {priority_color};">
                                <p style="color: white; font-weight: 600; margin: 0;">{item['skill']}</p>
                                <p style="color: #8892b0; margin: 5px 0 0 0; font-size: 0.9rem;">{item['resource']}</p>
                                <span style="background: {priority_color}; color: white; padding: 2px 10px; border-radius: 10px; 
                                            font-size: 0.7rem; text-transform: uppercase;">{item['priority']} priority</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with tabs[2]:
                        for i, step in enumerate(report["next_steps"], 1):
                            st.markdown(f"""
                            <div style="background: rgba(0,168,232,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;
                                        border-left: 3px solid #00a8e8; display: flex; align-items: flex-start;">
                                <span style="background: #00a8e8; color: white; width: 28px; height: 28px; border-radius: 50%; 
                                            display: flex; align-items: center; justify-content: center; margin-right: 15px; 
                                            font-weight: 700; flex-shrink: 0;">{i}</span>
                                <span style="color: white; line-height: 1.5;">{step}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.divider()
                    st.caption(f"Report ID: `{report['report_id']}`")
                    
                else:
                    st.error(f"{response.json().get('detail', 'Error')}")
                    
            except Exception as e:
                st.error(f"{str(e)}")

# ========== ABOUT PAGE ==========
elif page == "about":
    # App Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00d4aa; font-size: 2.5rem;">AI Career Coach</h1>
        <p style="color: #8892b0; font-size: 1.1rem;">Your AI-powered career development partner</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # What We Do + Tech Stack
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What We Do
        
        AI Career Coach helps job seekers and students:
        
        - **Analyze resumes** for ATS compatibility
        - **Identify skill gaps** against target roles
        - **Practice interviews** with AI-generated questions
        - **Generate reports** with actionable next steps
        
        Built with modern AI and data science techniques.
        """)
    
    with col2:
        st.markdown("""
        ### Tech Stack
        
        | Layer | Technology |
        |-------|-----------|
        | Backend | FastAPI |
        | Frontend | Streamlit |
        | Database | SQLAlchemy |
        | AI Engine | Custom NLP |
        | Cloud | Render + Streamlit Cloud |
        
        Open source on GitHub.
        """)
    
    st.divider()
    
    # How It Works
    st.markdown("""
    ### How It Works
    
    1. **Upload your resume** — Get instant ATS score and feedback
    2. **Set your target role** — See skill gaps and learning path
    3. **Practice interviews** — Answer questions and get AI feedback
    4. **Generate report** — Combined readiness score + next steps
    
    All data is processed securely and stored only for your session.
    """)
    
    st.divider()
    
    # Developer Section
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="color: #00d4aa;">About the Developer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    dev_col1, dev_col2 = st.columns([1, 2])
    
    with dev_col1:
        # Your photo
        st.image("frontend/assets/me.png", 
                 caption="Upam - Developer", 
                 use_container_width=True)
        
        # Social links
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://github.com/Neigh-god" style="color: #00d4aa; margin: 0 10px;">GitHub</a>
            <a href="https://linkedin.com/in/your-profile" style="color: #00a8e8; margin: 0 10px;">LinkedIn</a>
        </div>
        """, unsafe_allow_html=True)
    
    with dev_col2:
        st.markdown("""
        ### Hi, I'm Upam!
        
        I'm a passionate developer building AI-powered tools to help people advance their careers. 
        This project combines my interests in:
        
        - **Artificial Intelligence** — Natural language processing for resume analysis
        - **Full-Stack Development** — FastAPI backend with Streamlit frontend
        - **Data Science** — Skill gap analysis and scoring algorithms
        
        ### Why I Built This
        
        I noticed many job seekers struggle with:
        - Not knowing if their resume passes ATS filters
        - Feeling unprepared for technical interviews
        - Not understanding what skills they're missing
        
        AI Career Coach solves all three problems in one platform.
        
        ### Connect With Me
        
        - Open to collaboration and opportunities
        - Always building something new
        - Email: **majiupam@gmail.com**
        """)
    
    st.divider()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #8892b0;">
            Built with care by Upam<br>
            <a href="https://github.com/Neigh-god/ai-career-coach" style="color: #00d4aa;">Star on GitHub</a> • 
            <a href="https://github.com/Neigh-god/ai-career-coach/issues" style="color: #e94560;">Report Issue</a>
        </p>
    </div>
    """, unsafe_allow_html=True)