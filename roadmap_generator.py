SKILL_ROADMAPS = {
    "python": [
        {"week": 1, "phase": "Basics", "topics": ["Variables & Data Types", "Control Flow", "Functions", "Lists & Dicts"]},
        {"week": 2, "phase": "Intermediate", "topics": ["OOP", "File Handling", "Error Handling", "Modules"]},
        {"week": 3, "phase": "Advanced", "topics": ["Decorators", "Generators", "Async/Await", "Testing"]},
        {"week": 4, "phase": "Projects", "topics": ["Build CLI Tool", "REST API", "Automation Script", "Portfolio"]},
    ],
    "machine learning": [
        {"week": 1, "phase": "Basics", "topics": ["Math Foundations", "NumPy", "Pandas", "Data Preprocessing"]},
        {"week": 2, "phase": "Algorithms", "topics": ["Linear Regression", "Decision Trees", "SVM", "Clustering"]},
        {"week": 3, "phase": "Advanced", "topics": ["Neural Networks", "Feature Engineering", "Model Evaluation", "Ensemble Methods"]},
        {"week": 4, "phase": "Projects", "topics": ["Kaggle Competition", "End-to-End Pipeline", "Model Deployment", "Portfolio"]},
    ],
    "react": [
        {"week": 1, "phase": "Basics", "topics": ["JSX", "Components", "Props", "State"]},
        {"week": 2, "phase": "Intermediate", "topics": ["Hooks", "Context API", "Routing", "Forms"]},
        {"week": 3, "phase": "Advanced", "topics": ["Performance", "Testing", "Redux", "Next.js"]},
        {"week": 4, "phase": "Projects", "topics": ["Portfolio Site", "E-commerce App", "Dashboard", "Open Source"]},
    ],
    "sql": [
        {"week": 1, "phase": "Basics", "topics": ["SELECT Queries", "Filtering", "Sorting", "Joins"]},
        {"week": 2, "phase": "Intermediate", "topics": ["Aggregations", "Subqueries", "Indexing", "Views"]},
        {"week": 3, "phase": "Advanced", "topics": ["Stored Procedures", "Transactions", "Query Optimization", "Window Functions"]},
        {"week": 4, "phase": "Projects", "topics": ["Database Design", "Analytics Report", "Data Pipeline", "Portfolio"]},
    ],
    "docker": [
        {"week": 1, "phase": "Basics", "topics": ["Containers vs VMs", "Docker CLI", "Images", "Containers"]},
        {"week": 2, "phase": "Intermediate", "topics": ["Dockerfiles", "Volumes", "Networks", "Docker Compose"]},
        {"week": 3, "phase": "Advanced", "topics": ["Multi-stage Builds", "Registry", "Security", "Monitoring"]},
        {"week": 4, "phase": "Projects", "topics": ["Containerize App", "CI/CD Pipeline", "Microservices", "Portfolio"]},
    ],
    "aws": [
        {"week": 1, "phase": "Basics", "topics": ["Cloud Concepts", "IAM", "EC2", "S3"]},
        {"week": 2, "phase": "Intermediate", "topics": ["RDS", "Lambda", "VPC", "CloudWatch"]},
        {"week": 3, "phase": "Advanced", "topics": ["EKS", "CDK", "Security", "Cost Optimization"]},
        {"week": 4, "phase": "Projects", "topics": ["Deploy App", "Serverless API", "CI/CD Pipeline", "AWS Certification"]},
    ],
    "tensorflow": [
        {"week": 1, "phase": "Basics", "topics": ["Tensors", "Keras API", "Sequential Model", "Dense Layers"]},
        {"week": 2, "phase": "Intermediate", "topics": ["CNNs", "RNNs", "Transfer Learning", "Data Augmentation"]},
        {"week": 3, "phase": "Advanced", "topics": ["Custom Layers", "GANs", "Transformers", "Model Optimization"]},
        {"week": 4, "phase": "Projects", "topics": ["Image Classifier", "NLP Model", "Deploy with TFServing", "Portfolio"]},
    ],
    "javascript": [
        {"week": 1, "phase": "Basics", "topics": ["Variables", "Functions", "DOM Manipulation", "Events"]},
        {"week": 2, "phase": "Intermediate", "topics": ["Promises", "Async/Await", "ES6+", "Fetch API"]},
        {"week": 3, "phase": "Advanced", "topics": ["TypeScript", "Testing", "Performance", "Design Patterns"]},
        {"week": 4, "phase": "Projects", "topics": ["Interactive Website", "Chrome Extension", "Node App", "Portfolio"]},
    ],
}

DEFAULT_ROADMAP = [
    {"week": 1, "phase": "Basics", "topics": ["Core Concepts", "Fundamentals", "Setup & Tools", "First Examples"]},
    {"week": 2, "phase": "Intermediate", "topics": ["Deeper Topics", "Practice Exercises", "Real Use Cases", "Best Practices"]},
    {"week": 3, "phase": "Advanced", "topics": ["Advanced Patterns", "Optimization", "Integration", "Problem Solving"]},
    {"week": 4, "phase": "Projects", "topics": ["Build a Project", "Code Review", "Deploy", "Add to Portfolio"]},
]


def generate_roadmap(missing_skills: list[str]) -> dict:
    """Generate a learning roadmap for missing skills."""
    if not missing_skills:
        return {}

    roadmap = {}
    for skill in missing_skills[:6]:  # Cap at 6 skills for readability
        skill_lower = skill.lower()
        roadmap[skill] = SKILL_ROADMAPS.get(skill_lower, DEFAULT_ROADMAP)

    return roadmap


def get_priority_skills(missing_skills: list[str], career: str) -> list[str]:
    """Return skills in priority order for a given career."""
    # High-priority skills by career type
    priorities = {
        "Data Scientist": ["python", "machine learning", "sql", "statistics", "tensorflow"],
        "Full Stack Developer": ["javascript", "react", "node.js", "sql", "docker"],
        "ML Engineer": ["python", "machine learning", "docker", "tensorflow", "kubernetes"],
        "DevOps Engineer": ["docker", "kubernetes", "aws", "linux", "terraform"],
        "Frontend Developer": ["javascript", "react", "html", "css", "typescript"],
    }

    priority_list = priorities.get(career, [])
    prioritized = [s for s in priority_list if s in missing_skills]
    remaining = [s for s in missing_skills if s not in prioritized]

    return prioritized + remaining

