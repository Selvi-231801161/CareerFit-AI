import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill_extractor import extract_skills, categorize_skills, get_skill_strength
from career_matcher import match_careers, get_top_careers, get_career_readiness_score, get_skill_gap
from roadmap_generator import generate_roadmap, get_priority_skills
from courses import get_all_course_recommendations
from ai_advisor import generate_response

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerFit AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0f1a 0%, #1a1a2e 50%, #0f3460 100%);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    transition: all 0.2s;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(99, 102, 241, 0.2);
}

/* Main header */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f64f59 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.main-header h1 { font-size: 2.4rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.main-header p { font-size: 1.1rem; opacity: 0.9; margin: 0.5rem 0 0 0; }

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99,102,241,0.6);
}

/* Career cards */
.career-card {
    background: linear-gradient(135deg, #1e293b, #1a1a2e);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s;
}
.career-card:hover {
    border-color: rgba(99,102,241,0.6);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.15);
}

/* Skill badges */
.skill-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.2rem;
}
.skill-badge.missing {
    background: rgba(239,68,68,0.1);
    border-color: rgba(239,68,68,0.3);
    color: #fca5a5;
}
.skill-badge.present {
    background: rgba(34,197,94,0.1);
    border-color: rgba(34,197,94,0.3);
    color: #86efac;
}

/* Section headers */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(99,102,241,0.3);
}

/* Course card */
.course-card {
    background: #1e293b;
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
}
.course-card a {
    color: #818cf8;
    text-decoration: none;
    font-weight: 500;
}
.course-card a:hover { color: #a5b4fc; }

/* Roadmap step */
.roadmap-step {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-left: 4px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
}

/* Chat */
.chat-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border-radius: 12px 12px 4px 12px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0 0.5rem 20%;
    color: white;
}
.chat-ai {
    background: #1e293b;
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 12px 12px 12px 4px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 20% 0.5rem 0;
    color: #e2e8f0;
}

/* Intro text */
.intro-text {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #a855f7); border-radius: 4px; }

/* Demand badge */
.demand-high { color: #34d399; font-weight: 600; }
.demand-medium { color: #fbbf24; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:3rem;'>🎯</div>
        <div style='font-size:1.4rem; font-weight:700; color:#e2e8f0; letter-spacing:-0.5px;'>CareerFit AI</div>
        <div style='font-size:0.8rem; color:#94a3b8; margin-top:0.3rem;'>Intelligent Career Recommender</div>
    </div>
    <hr style='border-color:rgba(99,102,241,0.3); margin: 0.5rem 0 1.2rem 0;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🔍 Career Analyzer", "📊 Skill Insights", "🗺️ Learning Roadmap", "🤖 AI Career Advisor"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:1rem; font-size:0.82rem; color:#94a3b8;'>
        <b style='color:#a5b4fc;'>💡 How to use</b><br><br>
        1. Paste your resume or skills<br>
        2. Click <b>Analyze</b><br>
        3. Explore your career matches<br>
        4. Browse skill gaps & roadmaps<br>
        5. Ask the AI advisor anything!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#475569; text-align:center;'>
        Built with ❤️ using Python & Streamlit<br>No API keys required
    </div>
    """, unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
if "skills" not in st.session_state:
    st.session_state.skills = []
if "career_matches" not in st.session_state:
    st.session_state.career_matches = []
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_career" not in st.session_state:
    st.session_state.selected_career = None


# ─── Helper: Plotly theme ────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#e2e8f0"),
    margin=dict(l=10, r=10, t=40, b=10),
)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 1 — CAREER ANALYZER
# ════════════════════════════════════════════════════════════════════════════════
if page == "🔍 Career Analyzer":

    st.markdown("""
    <div class='main-header'>
        <h1>🎯 Career Analyzer</h1>
        <p>Paste your resume or skills to discover your ideal career path</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    col_input, col_guide = st.columns([3, 1])

    with col_input:
        input_method = st.radio("Input Method", ["✏️ Paste Text", "📄 Upload PDF"], horizontal=True)

        resume_text = ""

        if input_method == "✏️ Paste Text":
            resume_text = st.text_area(
                "Paste your resume, skills, or experience",
                height=220,
                placeholder="Example: I have 3 years of experience in Python, machine learning, pandas, and SQL. I've built deep learning models with TensorFlow and deployed them using Docker and AWS. Familiar with git, Jupyter notebooks, and data visualization with matplotlib...",
                help="You can paste your entire resume or just a list of your skills",
            )
        else:
            uploaded = st.file_uploader("Upload your Resume PDF", type=["pdf"])
            if uploaded:
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded)
                    resume_text = " ".join(page_obj.extract_text() or "" for page_obj in reader.pages)
                    st.success(f"✅ PDF loaded — {len(reader.pages)} page(s), {len(resume_text)} characters extracted")
                    with st.expander("Preview extracted text"):
                        st.text(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
                except ImportError:
                    st.error("PyPDF2 not installed. Run: pip install PyPDF2")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")

        analyze_btn = st.button("🚀 Analyze My Resume", type="primary", use_container_width=True)

    with col_guide:
        st.markdown("""
        <div style='background:#1e293b; border:1px solid rgba(99,102,241,0.25); border-radius:12px; padding:1.2rem; margin-top:1.7rem;'>
            <b style='color:#a5b4fc; font-size:0.9rem;'>📝 Tips for best results</b><br><br>
            <div class='intro-text'>
            ✓ Include all your technical skills<br>
            ✓ Mention tools & frameworks<br>
            ✓ Add cloud platforms used<br>
            ✓ Include databases & DevOps<br>
            ✓ Soft skills count too!
            </div>
        </div>
        """, unsafe_allow_html=True)

    if analyze_btn:
        if not resume_text.strip():
            st.warning("⚠️ Please provide some text or upload a PDF to analyze.")
        else:
            with st.spinner("🔍 Analyzing your skills and matching careers..."):
                skills = extract_skills(resume_text)
                matches = match_careers(skills)
                st.session_state.skills = skills
                st.session_state.career_matches = matches
                st.session_state.analyzed = True
                st.session_state.selected_career = matches[0]["career"] if matches else None

    # ── Results ──────────────────────────────────────────────────────────────
    if st.session_state.analyzed and st.session_state.skills:
        skills = st.session_state.skills
        matches = st.session_state.career_matches

        st.markdown("---")

        # Top metrics
        readiness = get_career_readiness_score(skills)
        top_career = matches[0] if matches else {}

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🔬 Skills Detected", len(skills))
        with c2:
            st.metric("🎯 Readiness Score", f"{readiness:.0f}%")
        with c3:
            st.metric("🏆 Best Match", top_career.get("career", "—")[:18])
        with c4:
            demand = top_career.get("demand", "—")
            st.metric("📈 Market Demand", demand)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Two column layout ─────────────────────────────────────────────────
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown("<div class='section-header'>🏆 Top Career Matches</div>", unsafe_allow_html=True)

            for i, match in enumerate(matches[:5]):
                pct = match["match_percentage"]
                color = "#34d399" if pct >= 60 else "#fbbf24" if pct >= 35 else "#f87171"
                st.markdown(f"""
                <div class='career-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <span style='font-size:1.5rem;'>{match["icon"]}</span>
                            <span style='font-size:1.1rem; font-weight:600; color:#e2e8f0; margin-left:0.5rem;'>
                                #{i+1} {match["career"]}
                            </span>
                        </div>
                        <div style='font-size:1.4rem; font-weight:700; color:{color};'>{pct:.0f}%</div>
                    </div>
                    <div style='margin:0.5rem 0; font-size:0.85rem; color:#94a3b8;'>{match["description"]}</div>
                    <div style='display:flex; justify-content:space-between; font-size:0.82rem; color:#64748b;'>
                        <span>💰 {match["avg_salary"]}</span>
                        <span>📈 {match["demand"]} demand</span>
                        <span>✅ {len(match["matched_skills"])} / {len(match["required_skills"])} skills</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='section-header'>📊 Career Probability</div>", unsafe_allow_html=True)

            top5 = matches[:5]
            fig = go.Figure(go.Bar(
                x=[m["match_percentage"] for m in top5],
                y=[m["career"] for m in top5],
                orientation="h",
                marker=dict(
                    color=[m["match_percentage"] for m in top5],
                    colorscale=[[0, "#4f46e5"], [0.5, "#7c3aed"], [1, "#ec4899"]],
                    line=dict(color="rgba(255,255,255,0.1)", width=1),
                ),
                text=[f"{m['match_percentage']:.0f}%" for m in top5],
                textposition="outside",
                textfont=dict(color="#e2e8f0", size=12),
            ))
            fig.update_layout(
                **PLOT_LAYOUT,
                height=280,
                xaxis=dict(showgrid=False, showticklabels=False, range=[0, 120]),
                yaxis=dict(showgrid=False, autorange="reversed"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gauge
            st.markdown("<div class='section-header'>⚡ Readiness Gauge</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=readiness,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Career Readiness", "font": {"size": 14, "color": "#94a3b8"}},
                number={"suffix": "%", "font": {"size": 32, "color": "#e2e8f0"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#475569"},
                    "bar": {"color": "#6366f1", "thickness": 0.25},
                    "bgcolor": "#1e293b",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 33], "color": "rgba(239,68,68,0.2)"},
                        {"range": [33, 66], "color": "rgba(251,191,36,0.2)"},
                        {"range": [66, 100], "color": "rgba(34,197,94,0.2)"},
                    ],
                    "threshold": {
                        "line": {"color": "#a855f7", "width": 3},
                        "thickness": 0.8,
                        "value": readiness,
                    },
                },
            ))
            fig2.update_layout(**PLOT_LAYOUT, height=220)
            st.plotly_chart(fig2, use_container_width=True)

        # Skill Gap for top career
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-header'>🎯 Skill Gap — {top_career.get('career', '')}</div>", unsafe_allow_html=True)

        gap = get_skill_gap(skills, top_career.get("career", ""))
        col_have, col_missing = st.columns(2)

        with col_have:
            st.markdown(f"**✅ Skills You Have** ({len(gap['matched'])})")
            badges = " ".join(f"<span class='skill-badge present'>{s}</span>" for s in gap["matched"])
            st.markdown(badges or "<span style='color:#64748b'>None detected</span>", unsafe_allow_html=True)

        with col_missing:
            st.markdown(f"**❌ Skills to Learn** ({len(gap['missing'])})")
            badges = " ".join(f"<span class='skill-badge missing'>{s}</span>" for s in gap["missing"])
            st.markdown(badges or "<span style='color:#34d399'>You have all the skills! 🎉</span>", unsafe_allow_html=True)

    elif st.session_state.analyzed:
        st.warning("⚠️ No recognized skills found. Try including more specific technical skills in your input.")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SKILL INSIGHTS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📊 Skill Insights":

    st.markdown("""
    <div class='main-header'>
        <h1>📊 Skill Insights</h1>
        <p>Deep dive into your skill profile and gap analysis</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.analyzed or not st.session_state.skills:
        st.info("👈 Go to **Career Analyzer** first and analyze your resume to see skill insights.")
        st.stop()

    skills = st.session_state.skills
    matches = st.session_state.career_matches

    # Categorized skills
    categorized = categorize_skills(skills)
    st.markdown("<div class='section-header'>🏷️ Skills by Category</div>", unsafe_allow_html=True)

    cat_cols = st.columns(3)
    for i, (cat, cat_skills) in enumerate(categorized.items()):
        with cat_cols[i % 3]:
            st.markdown(f"**{cat}** ({len(cat_skills)})")
            badges = " ".join(f"<span class='skill-badge'>{s}</span>" for s in cat_skills)
            st.markdown(badges, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_radar, col_heat = st.columns(2)

    with col_radar:
        st.markdown("<div class='section-header'>🕸️ Skill Radar</div>", unsafe_allow_html=True)
        display_skills = skills[:12]
        strength = get_skill_strength(display_skills)
        values = [strength.get(s, 60) for s in display_skills]
        if display_skills:
            values_closed = values + [values[0]]
            skills_closed = display_skills + [display_skills[0]]
            fig = go.Figure(go.Scatterpolar(
                r=values_closed,
                theta=skills_closed,
                fill="toself",
                fillcolor="rgba(99,102,241,0.15)",
                line=dict(color="#6366f1", width=2),
                marker=dict(color="#a855f7", size=6),
            ))
            fig.update_layout(
                **PLOT_LAYOUT,
                polar=dict(
                    bgcolor="rgba(30,41,59,0.5)",
                    angularaxis=dict(tickfont=dict(size=10, color="#94a3b8"), linecolor="#334155"),
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=8, color="#64748b"), gridcolor="#1e293b"),
                ),
                height=380,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_heat:
        st.markdown("<div class='section-header'>🔥 Skill Gap Heatmap (Top 5 Careers)</div>", unsafe_allow_html=True)

        top5_careers = [m["career"] for m in matches[:5]]
        all_required = set()
        for m in matches[:5]:
            all_required.update(m["required_skills"])
        heatmap_skills = sorted(list(all_required))[:16]

        matrix = []
        for career_name in top5_careers:
            match = next(m for m in matches if m["career"] == career_name)
            row = [1 if s in match["matched_skills"] else 0 for s in heatmap_skills]
            matrix.append(row)

        fig = go.Figure(go.Heatmap(
            z=matrix,
            x=heatmap_skills,
            y=top5_careers,
            colorscale=[[0, "#ef4444"], [1, "#22c55e"]],
            showscale=True,
            colorbar=dict(
                tickvals=[0, 1], ticktext=["Missing", "Present"],
                tickfont=dict(color="#94a3b8"), len=0.5,
            ),
            hoverongaps=False,
        ))
        fig.update_layout(
            **PLOT_LAYOUT,
            height=380,
            xaxis=dict(tickangle=-40, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed gap per career
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🔍 Detailed Gap Analysis</div>", unsafe_allow_html=True)

    selected = st.selectbox("Select a career to analyze", [m["career"] for m in matches[:8]])
    if selected:
        gap = get_skill_gap(skills, selected)
        match_info = next(m for m in matches if m["career"] == selected)

        prog_col, info_col = st.columns([2, 1])
        with prog_col:
            st.progress(gap["completion"] / 100)
            st.markdown(f"<span style='color:#94a3b8; font-size:0.9rem;'>Completion: **{gap['completion']:.0f}%** &nbsp;|&nbsp; {len(gap['matched'])} of {len(gap['required'])} skills matched</span>", unsafe_allow_html=True)
        with info_col:
            st.markdown(f"💰 **{match_info['avg_salary']}** avg salary")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**✅ You have these:**")
            st.markdown(" ".join(f"<span class='skill-badge present'>{s}</span>" for s in gap["matched"]) or "None", unsafe_allow_html=True)
        with col_b:
            st.markdown("**📚 You need to learn:**")
            st.markdown(" ".join(f"<span class='skill-badge missing'>{s}</span>" for s in gap["missing"]) or "🎉 All skills covered!", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 3 — LEARNING ROADMAP
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Learning Roadmap":

    st.markdown("""
    <div class='main-header'>
        <h1>🗺️ Learning Roadmap</h1>
        <p>Personalized skill-building plan and curated course recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.analyzed or not st.session_state.skills:
        st.info("👈 Go to **Career Analyzer** first and analyze your resume.")
        st.stop()

    skills = st.session_state.skills
    matches = st.session_state.career_matches

    career_options = [m["career"] for m in matches[:6]]
    selected_career = st.selectbox("📌 Generate roadmap for:", career_options)

    if selected_career:
        gap = get_skill_gap(skills, selected_career)
        missing = get_priority_skills(gap["missing"], selected_career)

        col_l, col_r = st.columns([1, 1])

        with col_l:
            st.markdown("<div class='section-header'>📅 Weekly Learning Plan</div>", unsafe_allow_html=True)

            if not missing:
                st.success("🎉 You already have all the required skills for this career!")
            else:
                roadmap = generate_roadmap(missing)

                for skill, weeks in list(roadmap.items())[:4]:
                    st.markdown(f"**🎯 {skill.title()}**")
                    for week_data in weeks:
                        phase_colors = {"Basics": "#6366f1", "Intermediate": "#8b5cf6",
                                        "Advanced": "#a855f7", "Projects": "#ec4899"}
                        color = phase_colors.get(week_data["phase"], "#6366f1")
                        topics_str = " · ".join(week_data["topics"])
                        st.markdown(f"""
                        <div class='roadmap-step' style='border-left-color:{color};'>
                            <div style='font-size:0.8rem; color:#64748b; margin-bottom:0.3rem;'>
                                Week {week_data["week"]} · <span style='color:{color};'>{week_data["phase"]}</span>
                            </div>
                            <div style='color:#cbd5e1; font-size:0.88rem;'>{topics_str}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-header'>📚 Recommended Courses</div>", unsafe_allow_html=True)

            course_recs = get_all_course_recommendations(missing[:6])

            if not course_recs:
                st.info("No missing skills — you're ready for this career!")
            else:
                for skill, courses in course_recs.items():
                    st.markdown(f"**📖 {skill.title()}**")
                    for course in courses:
                        st.markdown(f"""
                        <div class='course-card'>
                            <div style='margin-bottom:0.3rem;'>
                                <a href='{course["url"]}' target='_blank'>🔗 {course["title"]}</a>
                            </div>
                            <div style='font-size:0.78rem; color:#64748b;'>
                                {course["platform"]} &nbsp;·&nbsp; {course["level"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

        # Timeline visualization
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>📈 Learning Timeline</div>", unsafe_allow_html=True)

        n_skills = min(len(missing), 6)
        if n_skills > 0:
            skill_labels = missing[:n_skills]
            starts = [i * 3 for i in range(n_skills)]
            ends = [s + 4 for s in starts]

            fig = go.Figure()
            colors = ["#6366f1", "#8b5cf6", "#a855f7", "#ec4899", "#f43f5e", "#fb923c"]

            for i, (skill, start, end) in enumerate(zip(skill_labels, starts, ends)):
                fig.add_trace(go.Bar(
                    name=skill,
                    x=[end - start],
                    y=[skill],
                    base=start,
                    orientation="h",
                    marker=dict(color=colors[i % len(colors)], opacity=0.85, line=dict(width=0)),
                    text=f"Week {start+1}–{end}",
                    textposition="inside",
                    insidetextfont=dict(color="white", size=11),
                ))

            fig.update_layout(
                **PLOT_LAYOUT,
                height=280,
                barmode="overlay",
                xaxis=dict(title="Weeks", tickfont=dict(color="#94a3b8"), gridcolor="#1e293b"),
                yaxis=dict(tickfont=dict(color="#94a3b8")),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<div class='intro-text'>📌 Estimated total learning time: <b>{ends[-1] if ends else 0} weeks</b> (~{(ends[-1] if ends else 0) // 4} months)</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 4 — AI CAREER ADVISOR
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI Career Advisor":

    st.markdown("""
    <div class='main-header'>
        <h1>🤖 AI Career Advisor</h1>
        <p>Ask anything about careers, skills, salaries, and learning paths</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**💡 Quick Questions:**")
    qcols = st.columns(4)
    quick_prompts = [
        "How do I become a Data Scientist?",
        "What does a DevOps Engineer earn?",
        "I'm a beginner, where do I start?",
        "Which jobs are remote-friendly?",
    ]
    for i, (col, prompt) in enumerate(zip(qcols, quick_prompts)):
        with col:
            if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                user_skills = st.session_state.skills
                response = generate_response(prompt, user_skills)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append({"role": "ai", "content": response})

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style='text-align:center; padding:2rem; color:#475569;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>🤖</div>
                <div style='font-size:1rem;'>Ask me anything about careers, skills, salaries, or learning paths!</div>
                <div style='font-size:0.85rem; margin-top:0.5rem;'>Examples: "How to become ML Engineer?" · "Is Python enough for Data Science?" · "Top paying tech jobs"</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"<div class='chat-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        user_input = st.text_input(
            "Ask the AI Advisor",
            placeholder="e.g. How do I become a Machine Learning Engineer?",
            label_visibility="collapsed",
            key="advisor_input",
        )
    with col_btn:
        send_btn = st.button("Send 🚀", type="primary", use_container_width=True)

    if send_btn and user_input.strip():
        user_skills = st.session_state.skills
        response = generate_response(user_input, user_skills)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "ai", "content": response})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()

    # Context note
    if st.session_state.analyzed and st.session_state.skills:
        st.markdown(f"""
        <div style='background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:0.8rem 1.2rem; margin-top:1rem; font-size:0.85rem; color:#94a3b8;'>
            🔗 <b>Context loaded:</b> {len(st.session_state.skills)} skills from your resume are available to the advisor for personalized responses.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(251,191,36,0.06); border:1px solid rgba(251,191,36,0.2); border-radius:10px; padding:0.8rem 1.2rem; margin-top:1rem; font-size:0.85rem; color:#94a3b8;'>
            💡 <b>Tip:</b> Analyze your resume first on the Career Analyzer page for more personalized advice!
        </div>
        """, unsafe_allow_html=True)
