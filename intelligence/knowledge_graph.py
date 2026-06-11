# intelligence/knowledge_graph.py


SKILL_GRAPH = {

    "machine learning": [
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "xgboost"
    ],

    "deep learning": [
        "cnn",
        "rnn",
        "transformers",
        "bert",
        "llm"
    ],

    "computer vision": [
        "opencv",
        "yolo",
        "image processing"
    ],

    "backend": [
        "fastapi",
        "flask",
        "django",
        "rest api"
    ],

    "cloud": [
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes"
    ]
}


def get_related_skills(skill):
    
    skill = skill.lower()

    return SKILL_GRAPH.get(skill, [])