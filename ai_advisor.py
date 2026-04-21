from data.skills_db import CAREER_PATHS

GREETINGS = ["hello", "hi", "hey", "greetings", "howdy", "sup", "good morning", "good afternoon"]

CAREER_KEYWORDS = {k.lower(): k for k in CAREER_PATHS.keys()}

QUESTION_PATTERNS = {
    "salary": ["salary", "pay", "earn", "income", "money", "compensation", "wage"],
    "skills_needed": ["what skills", "which skills", "skills needed", "skills required", "need to learn", "learn for"],
    "demand": ["demand", "job market", "hiring", "jobs available", "in demand", "future"],
    "roadmap": ["roadmap", "path", "how to become", "get into", "start", "begin", "steps"],
    "comparison": ["vs", "versus", "compare", "difference", "better", "best"],
    "beginner": ["beginner", "new to", "just starting", "no experience", "start from scratch"],
    "switch": ["switch", "transition", "change career", "move to", "pivot"],
    "remote": ["remote", "work from home", "wfh", "freelance"],
    "certification": ["certification", "certificate", "certified", "exam", "course"],
}


def detect_intent(message: str) -> dict:
    """Detect the intent of a user message."""
    msg_lower = message.lower()

    # Check for greeting
    for greet in GREETINGS:
        if greet in msg_lower:
            return {"type": "greeting"}

    # Detect mentioned career
    mentioned_career = None
    for kw, career in CAREER_KEYWORDS.items():
        if kw in msg_lower:
            mentioned_career = career
            break

    # Detect question type
    question_type = "general"
    for q_type, patterns in QUESTION_PATTERNS.items():
        for pattern in patterns:
            if pattern in msg_lower:
                question_type = q_type
                break

    return {
        "type": "question",
        "career": mentioned_career,
        "question_type": question_type,
        "raw": message,
    }


def generate_response(message: str, user_skills: list[str] = None) -> str:
    """Generate a response to a user message using rule-based logic."""
    intent = detect_intent(message)
    user_skills = user_skills or []

    if intent["type"] == "greeting":
        return (
            "👋 Hello! I'm your **AI Career Advisor**. I can help you with:\n\n"
            "- 🎯 Career path recommendations\n"
            "- 💰 Salary insights for different roles\n"
            "- 📚 Skills you need to learn\n"
            "- 🗺️ Learning roadmaps\n"
            "- 🔄 Career transition advice\n\n"
            "Try asking: *'How do I become a Data Scientist?'* or *'What skills does a DevOps Engineer need?'*"
        )

    career = intent.get("career")
    q_type = intent.get("question_type")

    # Career-specific responses
    if career and career in CAREER_PATHS:
        info = CAREER_PATHS[career]
        required_skills = info["skills"]

        if q_type == "salary":
            return (
                f"💰 **{career} Salary Insights**\n\n"
                f"**Average Salary:** {info['avg_salary']}/year\n"
                f"**Market Demand:** {info['demand']}\n\n"
                f"Salaries vary by location, experience, and company size. "
                f"Senior {career}s can earn significantly more. "
                f"Tech hubs like San Francisco, New York, and Seattle typically offer 20-40% premiums."
            )

        elif q_type == "skills_needed":
            skills_str = ", ".join(f"`{s}`" for s in required_skills[:8])
            return (
                f"🛠️ **Skills for {career}**\n\n"
                f"**Core Skills:** {skills_str}\n\n"
                f"**Key Focus Areas:**\n"
                + _get_focus_areas(career) +
                f"\n\n💡 Start with Python and SQL as they're foundational for most tech careers."
            )

        elif q_type == "roadmap" or q_type == "skills_needed":
            return (
                f"🗺️ **How to Become a {career}**\n\n"
                f"**Phase 1 – Foundation (Months 1-3):**\n"
                f"Learn core programming and tools relevant to the role.\n\n"
                f"**Phase 2 – Core Skills (Months 3-6):**\n"
                f"Deep dive into: {', '.join(required_skills[:4])}\n\n"
                f"**Phase 3 – Projects (Months 6-9):**\n"
                f"Build 3-5 portfolio projects to demonstrate skills.\n\n"
                f"**Phase 4 – Job Search (Month 9+):**\n"
                f"Apply, network, and prepare for technical interviews.\n\n"
                f"📌 **Average time:** 6-12 months for career transition"
            )

        elif q_type == "demand":
            return (
                f"📈 **{career} Job Market**\n\n"
                f"**Current Demand:** {info['demand']}\n\n"
                + _get_market_insights(career) +
                f"\n\n🔗 Check LinkedIn, Indeed, and Glassdoor for current openings."
            )

        else:
            # General career info
            user_matched = [s for s in user_skills if s in required_skills]
            missing = [s for s in required_skills if s not in user_skills]

            response = (
                f"{info['icon']} **{career} Overview**\n\n"
                f"**Description:** {info['description']}\n\n"
                f"**Salary:** {info['avg_salary']}/year\n"
                f"**Demand:** {info['demand']}\n\n"
                f"**Required Skills:** {', '.join(f'`{s}`' for s in required_skills[:6])}\n\n"
            )

            if user_skills:
                if user_matched:
                    response += f"✅ **You already have:** {', '.join(user_matched[:5])}\n\n"
                if missing:
                    response += f"📚 **Skills to learn:** {', '.join(missing[:5])}\n\n"

            response += "💡 **Tip:** " + _get_career_tip(career)
            return response

    # No career detected – handle general questions
    if q_type == "beginner":
        return (
            "🌱 **Getting Started in Tech**\n\n"
            "Great news – it's never too late to start! Here's a beginner roadmap:\n\n"
            "1. **Pick a language:** Python is the most beginner-friendly\n"
            "2. **Learn basics:** Variables, loops, functions (2-4 weeks)\n"
            "3. **Build projects:** Start small, grow gradually\n"
            "4. **Choose a path:** Web Dev, Data Science, or DevOps\n"
            "5. **Practice daily:** Even 1 hour a day adds up!\n\n"
            "📚 **Free resources:** freeCodeCamp, The Odin Project, Codecademy\n\n"
            "Which area interests you most? Ask me about any specific career!"
        )

    elif q_type == "switch":
        return (
            "🔄 **Career Transition Tips**\n\n"
            "Switching to tech is very doable! Here's how:\n\n"
            "**Step 1 – Assess transferable skills**\n"
            "Your existing skills (communication, problem-solving, domain expertise) are valuable.\n\n"
            "**Step 2 – Pick a target role**\n"
            "Consider: Data Analyst, Product Manager, QA Engineer, or Junior Developer.\n\n"
            "**Step 3 – Learn systematically**\n"
            "Dedicate 2-3 hours/day. Most people transition in 6-12 months.\n\n"
            "**Step 4 – Build a portfolio**\n"
            "Projects > certifications. Show real work.\n\n"
            "**Step 5 – Network actively**\n"
            "LinkedIn, meetups, Twitter/X tech community.\n\n"
            "Which field are you considering switching to?"
        )

    elif q_type == "remote":
        return (
            "🏠 **Remote Work in Tech**\n\n"
            "Tech is one of the most remote-friendly industries!\n\n"
            "**Most remote-friendly roles:**\n"
            "- 💻 Full Stack / Frontend Developer\n"
            "- 🧪 Data Scientist\n"
            "- 🔧 DevOps Engineer\n"
            "- 🔒 Cybersecurity Analyst\n\n"
            "**Top remote platforms:**\n"
            "- Remote.co, We Work Remotely, Toptal, Upwork\n\n"
            "**Tip:** Build a strong GitHub portfolio – remote employers rely on it!"
        )

    elif q_type == "comparison":
        return (
            "⚖️ **Career Comparison**\n\n"
            "I can compare specific careers for you! Try asking:\n"
            "- *'Data Scientist vs ML Engineer'*\n"
            "- *'Frontend vs Backend Developer'*\n"
            "- *'DevOps vs Cloud Architect'*\n\n"
            "Or tell me which two careers you're deciding between!"
        )

    elif q_type == "certification":
        return (
            "🏆 **Top Tech Certifications**\n\n"
            "**Cloud:** AWS Certified Solutions Architect, Google Cloud Professional\n"
            "**DevOps:** Certified Kubernetes Administrator (CKA), HashiCorp Terraform\n"
            "**Data:** Google Data Analytics, IBM Data Science Professional\n"
            "**Security:** CompTIA Security+, CEH, CISSP\n"
            "**Development:** Meta Front-End Developer, AWS Developer Associate\n\n"
            "💡 Certifications are great supplements but **portfolio projects** matter more to most employers."
        )

    else:
        return (
            "🤔 I'd love to help! Here are some things you can ask me:\n\n"
            "- *'How do I become a Data Scientist?'*\n"
            "- *'What salary does a DevOps Engineer make?'*\n"
            "- *'What skills do I need for ML Engineering?'*\n"
            "- *'I'm a beginner, where do I start?'*\n"
            "- *'How do I switch careers to tech?'*\n"
            "- *'Which tech jobs are remote-friendly?'*\n\n"
            "Just type your question and I'll do my best to help! 🚀"
        )


def _get_focus_areas(career: str) -> str:
    areas = {
        "Data Scientist": "- Statistical analysis & modeling\n- Python & R programming\n- ML frameworks (sklearn, TensorFlow)",
        "Full Stack Developer": "- Frontend (React, HTML/CSS)\n- Backend (Node.js, Django)\n- Database design & APIs",
        "ML Engineer": "- Model training & evaluation\n- MLOps & deployment\n- Cloud infrastructure",
        "DevOps Engineer": "- Container orchestration\n- CI/CD pipelines\n- Infrastructure as Code",
        "Frontend Developer": "- Modern JavaScript & TypeScript\n- React/Vue ecosystem\n- UI/UX fundamentals",
        "Cybersecurity Analyst": "- Network security protocols\n- Threat detection & response\n- Security tools & SIEM",
    }
    return areas.get(career, "- Core technical skills\n- Domain knowledge\n- Practical projects")


def _get_market_insights(career: str) -> str:
    insights = {
        "Data Scientist": "Data Science roles have grown 35% YoY. Every industry needs data talent.",
        "ML Engineer": "One of the fastest-growing roles in tech. AI adoption is driving massive demand.",
        "DevOps Engineer": "DevOps adoption is mainstream. Companies across all sectors are hiring.",
        "Cloud Architect": "Cloud migration drives strong demand. Multi-cloud experience is a big plus.",
        "Cybersecurity Analyst": "With rising cyber threats, security professionals are in critical demand.",
        "Full Stack Developer": "Web development remains foundational. Startups especially value full-stack talent.",
    }
    return insights.get(career, "Strong and growing demand across the tech industry.")


def _get_career_tip(career: str) -> str:
    tips = {
        "Data Scientist": "Start with Kaggle competitions to build a competitive portfolio.",
        "Full Stack Developer": "Build and deploy a real project – even a simple CRUD app shows a lot.",
        "ML Engineer": "Contribute to open-source ML projects on GitHub to get noticed.",
        "DevOps Engineer": "Get your AWS or GCP certification – it opens many doors.",
        "Frontend Developer": "Learn design basics – developers who understand UI/UX stand out.",
        "Cybersecurity Analyst": "Set up a home lab and practice ethical hacking on platforms like HackTheBox.",
    }
    return tips.get(career, "Build real projects, document them well, and share them on GitHub.")

