from data.skills_db import CAREER_PATHS


def match_careers(user_skills: list[str]) -> list[dict]:
    """Match user skills against career paths and return scored results."""
    user_skills_lower = set(s.lower() for s in user_skills)
    results = []

    for career, info in CAREER_PATHS.items():
        required = set(info["skills"])
        matched = user_skills_lower.intersection(required)
        match_pct = (len(matched) / len(required)) * 100 if required else 0

        results.append({
            "career": career,
            "match_percentage": round(match_pct, 1),
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(required - user_skills_lower)),
            "required_skills": sorted(list(required)),
            "description": info["description"],
            "avg_salary": info["avg_salary"],
            "demand": info["demand"],
            "icon": info["icon"],
        })

    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results


def get_top_careers(user_skills: list[str], n: int = 3) -> list[dict]:
    """Return top N career matches."""
    all_matches = match_careers(user_skills)
    return all_matches[:n]


def get_career_readiness_score(user_skills: list[str]) -> float:
    """Return the highest career match percentage as overall readiness score."""
    matches = match_careers(user_skills)
    if not matches:
        return 0.0
    return matches[0]["match_percentage"]


def get_skill_gap(user_skills: list[str], career: str) -> dict:
    """Get skill gap analysis for a specific career."""
    user_skills_lower = set(s.lower() for s in user_skills)
    career_info = CAREER_PATHS.get(career, {})
    required = set(career_info.get("skills", []))
    matched = user_skills_lower.intersection(required)
    missing = required - user_skills_lower

    return {
        "career": career,
        "required": sorted(list(required)),
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "completion": round((len(matched) / len(required)) * 100, 1) if required else 0,
    }

