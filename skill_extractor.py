import re
from data.skills_db import SKILLS_LIST


def extract_skills(text: str) -> list[str]:
    """Extract skills from resume text by matching against skill database."""
    text_lower = text.lower()
    found_skills = set()

    # Sort by length descending to match multi-word skills first
    sorted_skills = sorted(SKILLS_LIST, key=len, reverse=True)

    for skill in sorted_skills:
        # Use word boundary matching for single-word skills
        # For multi-word, use direct substring matching
        if " " in skill or "/" in skill or "." in skill:
            if skill in text_lower:
                found_skills.add(skill)
        else:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

    return sorted(list(found_skills))


def categorize_skills(skills: list[str]) -> dict:
    """Categorize extracted skills into groups."""
    categories = {
        "Programming Languages": ["python", "java", "javascript", "typescript", "c++", "c#",
                                   "ruby", "php", "swift", "kotlin", "go", "rust", "scala",
                                   "r", "matlab", "perl", "bash", "shell", "dart"],
        "Web Development": ["html", "css", "react", "angular", "vue", "node.js", "nodejs",
                            "express", "django", "flask", "fastapi", "spring", "laravel",
                            "jquery", "bootstrap", "tailwind", "graphql", "rest", "next.js"],
        "Data & ML": ["machine learning", "deep learning", "neural networks", "nlp",
                      "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
                      "data analysis", "data science", "statistics", "computer vision"],
        "Databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
                      "sqlite", "oracle", "nosql", "dynamodb", "firebase"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform",
                           "ansible", "jenkins", "ci/cd", "linux", "microservices", "devops"],
        "Tools & Others": ["git", "github", "jira", "agile", "scrum", "excel", "power bi",
                           "tableau", "figma", "communication", "leadership", "teamwork"],
    }

    categorized = {cat: [] for cat in categories}
    uncategorized = []

    for skill in skills:
        placed = False
        for cat, cat_skills in categories.items():
            if skill in cat_skills:
                categorized[cat].append(skill)
                placed = True
                break
        if not placed:
            uncategorized.append(skill)

    if uncategorized:
        categorized["Other"] = uncategorized

    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}


def get_skill_strength(skills: list[str]) -> dict:
    """Assign relative strength scores to skills for radar chart."""
    # Base scores by category weight
    high_value = ["machine learning", "deep learning", "tensorflow", "pytorch",
                  "kubernetes", "spark", "scala", "rust", "go"]
    medium_value = ["python", "java", "javascript", "sql", "docker", "aws", "react",
                    "node.js", "pandas", "numpy"]

    strength = {}
    for skill in skills:
        if skill in high_value:
            strength[skill] = 90
        elif skill in medium_value:
            strength[skill] = 75
        else:
            strength[skill] = 60

    return strength
