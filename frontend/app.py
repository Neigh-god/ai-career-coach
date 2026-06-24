import streamlit as st
import requests

# API base URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Coach")
st.markdown("Your personal AI-powered career development assistant.")

# Sidebar navigation
page = st.sidebar.radio(
    "Choose a feature",
    ["🏠 Home", "📄 Resume Analyzer", "🎤 Interview Practice", "📊 Career Report"]
)

# ========== HOME PAGE ==========
if page == "🏠 Home":
    st.header("Welcome!")
    st.write("""
    AI Career Coach helps you:
    - **Analyze your resume** for ATS compatibility
    - **Practice interviews** with AI-generated questions
    - **Identify skill gaps** between your profile and target role
    - **Generate career reports** with actionable next steps
    
    Use the sidebar to navigate between features.
    """)
    
    # Health check
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend API is running")
        else:
            st.warning("⚠️ Backend API returned an error")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ========== RESUME ANALYZER ==========
elif page == "📄 Resume Analyzer":
    st.header("📄 Resume Analyzer")
    st.write("Upload your resume (PDF or DOCX) to get an ATS score and improvement suggestions.")
    
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("File Details")
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        
        with col2:
            if st.button("Analyze Resume", type="primary"):
                with st.spinner("Analyzing your resume..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/resume/upload", files=files, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("✅ Resume analyzed successfully!")
                            
                            # Display score
                            score = data["score"]["overall_score"]
                            st.metric("ATS Score", f"{score}/100")
                            
                            # Progress bar
                            st.progress(score / 100)
                            
                            # Strengths
                            if data["score"]["strengths"]:
                                st.subheader("💪 Strengths")
                                for s in data["score"]["strengths"]:
                                    st.write(f"- {s}")
                            
                            # Weaknesses
                            if data["score"]["weaknesses"]:
                                st.subheader("⚠️ Areas to Improve")
                                for w in data["score"]["weaknesses"]:
                                    st.write(f"- {w}")
                            
                            # Suggestions
                            if data["score"]["suggestions"]:
                                st.subheader("💡 Suggestions")
                                for s in data["score"]["suggestions"]:
                                    st.write(f"- {s}")
                            
                            # Parsed info
                            with st.expander("View Parsed Resume Data"):
                                parsed = data["parsed_data"]
                                st.json({
                                    "Name": parsed.get("name"),
                                    "Email": parsed.get("email"),
                                    "Phone": parsed.get("phone"),
                                    "Skills": parsed.get("skills", [])
                                })
                        else:
                            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend API. Make sure the server is running.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ========== INTERVIEW PRACTICE ==========
elif page == "🎤 Interview Practice":
    st.header("🎤 Interview Practice")
    st.write("Practice interviews with AI-generated questions and get instant feedback.")
    
    # Session setup
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "Interview Type",
            ["behavioral", "technical", "situational"]
        )
    
    with col2:
        question_count = st.slider("Number of Questions", 1, 5, 3)
    
    user_id = st.text_input("Your User ID (any unique string)", value="user-123")
    
    # Start interview
    if st.button("Start Interview", type="primary"):
        with st.spinner("Generating questions..."):
            try:
                response = requests.post(
                    f"{API_URL}/interview/start",
                    json={
                        "user_id": user_id,
                        "category": category,
                        "question_count": question_count
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["interview_session"] = data
                    st.session_state["current_question"] = 0
                    st.success("✅ Interview started!")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend API.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display questions and collect answers
    if "interview_session" in st.session_state:
        session = st.session_state["interview_session"]
        questions = session["questions"]
        current = st.session_state.get("current_question", 0)
        
        st.divider()
        st.subheader(f"Question {current + 1} of {len(questions)}")
        
        if current < len(questions):
            q = questions[current]
            st.info(f"**{q['question']}**")
            st.caption(f"Category: {q['category']} | Difficulty: {q['difficulty']}")
            
            answer = st.text_area("Your Answer", height=150, key=f"answer_{current}")
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("Submit Answer", type="primary"):
                    if answer.strip():
                        with st.spinner("Evaluating your answer..."):
                            try:
                                response = requests.post(
                                    f"{API_URL}/interview/{session['session_id']}/answer",
                                    json={
                                        "question_id": q["id"],
                                        "user_answer": answer
                                    },
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    feedback = response.json()
                                    st.session_state[f"feedback_{current}"] = feedback
                                    st.session_state["current_question"] = current + 1
                                    st.rerun()
                                else:
                                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                                    
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("Please enter an answer before submitting.")
        else:
            st.success("🎉 Interview completed! View your feedback below.")
            
            # Show all feedbacks
            for i in range(len(questions)):
                if f"feedback_{i}" in st.session_state:
                    fb = st.session_state[f"feedback_{i}"]
                    with st.expander(f"Question {i+1} Feedback (Score: {fb['feedback']['score']})"):
                        st.write(f"**Score:** {fb['feedback']['score']}/100")
                        st.write(f"**Strengths:** {fb['feedback']['strengths']}")
                        st.write(f"**Improvements:** {fb['feedback']['improvements']}")
                        st.write(f"**Model Answer:** {fb['feedback']['model_answer']}")
            
            # Get full session feedback
            if st.button("Get Full Session Summary"):
                try:
                    response = requests.get(
                        f"{API_URL}/interview/{session['session_id']}/feedback",
                        timeout=10
                    )
                    if response.status_code == 200:
                        summary = response.json()
                        st.subheader("Session Summary")
                        st.metric("Overall Score", f"{summary.get('overall_score', 'N/A')}")
                        st.metric("Questions Answered", f"{summary['answered_questions']}/{summary['total_questions']}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ========== CAREER REPORT ==========
elif page == "📊 Career Report":
    st.header("📊 Career Report")
    st.write("Generate a comprehensive career report combining resume analysis, skill gaps, and interview performance.")
    
    with st.form("report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("User ID", value="user-123")
            target_role = st.selectbox(
                "Target Role",
                ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer"]
            )
        
        with col2:
            resume_score = st.slider("Your Resume Score", 0, 100, 65)
            current_skills = st.text_area("Your Current Skills (comma-separated)", "Python, Git, SQL")
        
        resume_strengths = st.text_area("Resume Strengths (one per line)", "Strong technical skills\nGood project experience")
        resume_weaknesses = st.text_area("Resume Weaknesses (one per line)", "Lack of metrics\nNo certifications")
        
        interview_session_id = st.text_input("Interview Session ID (optional)", help="Leave empty if you haven't done an interview yet")
        
        submitted = st.form_submit_button("Generate Report", type="primary")
    
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
                
                response = requests.post(
                    f"{API_URL}/report/generate",
                    json=payload,
                    timeout=15
                )
                
                if response.status_code == 200:
                    report = response.json()
                    
                    st.success("✅ Report generated!")
                    
                    # Display report
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Resume Score", report["resume_section"]["overall_score"])
                    
                    with col2:
                        st.metric("Skill Coverage", f"{report['skill_gap_section']['coverage_percent']}%")
                    
                    with col3:
                        if report["interview_section"]:
                            st.metric("Interview Score", report["interview_section"]["average_score"])
                        else:
                            st.metric("Interview Score", "N/A")
                    
                    # Recommendation
                    st.subheader("🎯 Overall Recommendation")
                    st.info(report["overall_recommendation"])
                    
                    # Skill gaps
                    st.subheader("📚 Skill Gaps")
                    if report["skill_gap_section"]["missing_skills"]:
                        for skill in report["skill_gap_section"]["missing_skills"]:
                            st.write(f"- ❌ {skill}")
                    else:
                        st.write("✅ No major skill gaps!")
                    
                    # Learning path
                    if report["skill_gap_section"]["learning_path"]:
                        st.subheader("🎓 Learning Recommendations")
                        for item in report["skill_gap_section"]["learning_path"]:
                            st.write(f"**{item['skill']}** — {item['resource']} (Priority: {item['priority']})")
                    
                    # Next steps
                    st.subheader("🚀 Next Steps")
                    for i, step in enumerate(report["next_steps"], 1):
                        st.write(f"{i}. {step}")
                    
                    # Save report ID
                    st.caption(f"Report ID: `{report['report_id']}` — You can retrieve this report later.")
                    
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend API. Make sure the server is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")