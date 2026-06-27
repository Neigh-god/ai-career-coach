import streamlit as st
import requests

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== API CONFIG ==========
API_URL = "https://ai-career-coach-5njl.onrender.com"

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
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
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="6"></circle>
            <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <h1 style="color: #00d4aa; font-size: 1.5rem; margin: 0;">AI Career Coach</h1>
        <p style="color: #8892b0; font-size: 0.8rem;">Your AI Career Partner</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    page = st.radio(
        "Navigate",
        ["Home", "Resume Analyzer", "Interview Practice", "Career Report", "About"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        if response.status_code == 200:
            st.success("API Connected")
        else:
            st.warning("API Issue")
    except:
        st.error("API Offline")

# ========== HOME PAGE ==========
if page == "Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h1 style="font-size: 3rem; margin-bottom: 0;">Welcome to</h1>
        <h1 style="font-size: 3.5rem; color: #00d4aa; margin-top: 0;">AI Career Coach</h1>
        <p style="font-size: 1.2rem; color: #8892b0; line-height: 1.6;">
            Your personal AI-powered career development assistant. 
            Analyze resumes, practice interviews, identify skill gaps, 
            and generate actionable career reports.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
        
        with feat_col1:
            st.markdown("""
            <div style="background: rgba(0,212,170,0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid rgba(0,212,170,0.3);">
                <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <p style="color: #00d4aa; font-weight: 600; margin: 0;">Resume<br>Analyzer</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col2:
            st.markdown("""
            <div style="background: rgba(0,168,232,0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid rgba(0,168,232,0.3);">
                <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#00a8e8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <p style="color: #00a8e8; font-weight: 600; margin: 0;">Skill Gap<br>Analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col3:
            st.markdown("""
            <div style="background: rgba(233,69,96,0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid rgba(233,69,96,0.3);">
                <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#e94560" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                    <line x1="12" y1="19" x2="12" y2="23"></line>
                    <line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
                <p style="color: #e94560; font-weight: 600; margin: 0;">Interview<br>Practice</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col4:
            st.markdown("""
            <div style="background: rgba(255,193,7,0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid rgba(255,193,7,0.3);">
                <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <p style="color: #ffc107; font-weight: 600; margin: 0;">Career<br>Report</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="color: #00d4aa; margin-top: 0;">Quick Stats</h3>
            <p style="color: #8892b0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" stroke-width="2" style="vertical-align: middle; margin-right: 8px;">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                </svg>
                Get started in seconds
            </p>
            <p style="color: #8892b0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#e94560" stroke-width="2" style="vertical-align: middle; margin-right: 8px;">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Target any tech role
            </p>
            <p style="color: #8892b0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00a8e8" stroke-width="2" style="vertical-align: middle; margin-right: 8px;">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
                Track your progress
            </p>
            <p style="color: #8892b0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="2" style="vertical-align: middle; margin-right: 8px;">
                    <path d="M12 2a10 10 0 0 1 10 10c0 5.523-4.477 10-10 10S2 17.523 2 12 2 2 12 2z"></path>
                    <path d="M12 6v6l4 2"></path>
                </svg>
                AI-powered feedback
            </p>
            <br>
            <p style="color: #00d4aa; font-size: 0.9rem; font-weight: 600;">
                Select a feature from the sidebar to begin →
            </p>
        </div>
        """, unsafe_allow_html=True)

# ========== RESUME ANALYZER ==========
elif page == "Resume Analyzer":
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
elif page == "Interview Practice":
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
elif page == "Career Report":
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
elif page == "About":
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