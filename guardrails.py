import re

REFUSAL_MESSAGE = (
    "I'm here to answer questions about Wentao Jiang's background, projects, "
    "skills, education, work experience, and portfolio. Please ask something related to Wentao's profile."
)

MAX_INPUT_LENGTH = 500


def is_prompt_injection(question: str) -> bool:
    q = question.lower().strip()

    injection_patterns = [
        "ignore your prompt",
        "ignore previous instructions",
        "ignore all previous instructions",
        "forget your instructions",
        "forget all previous instructions",
        "disregard previous instructions",
        "override your instructions",
        "bypass your instructions",
        "you are now",
        "act as",
        "pretend to be",
        "reveal your prompt",
        "show me your prompt",
        "show your system prompt",
        "what is your system prompt",
        "print your instructions",
        "developer message",
        "system message",
        "jailbreak",
        "dan mode",
    ]

    return any(pattern in q for pattern in injection_patterns)


def is_obviously_off_topic(question: str) -> bool:
    q = question.lower().strip()

    off_topic_patterns = [
        r"\bweather\b",
        r"\bstock\b",
        r"\bcrypto\b",
        r"\bbitcoin\b",
        r"\brecipe\b",
        r"\bcook\b",
        r"\bmovie recommendation\b",
        r"\btravel plan\b",
        r"\btranslate\b",
        r"\bwrite an essay\b",
        r"\bsolve this math\b",
        r"\bcapital of\b",
        r"\bwho is the president\b",
        r"\bnews\b",
        r"\bnba\b",
        r"\bfootball\b",
        r"\bsoccer\b",
        r"\bgame recommendation\b",
    ]

    return any(re.search(pattern, q) for pattern in off_topic_patterns)


def is_profile_related(question: str) -> bool:
    q = question.lower().strip()

    allowed_keywords = [
        # identity
        "wentao", "jiang", "kyrie", "you", "your", "he", "his",

        # profile / resume
        "profile", "resume", "cv", "background", "education",
        "university", "mcmaster", "major", "degree",

        # career
        "experience", "internship", "work", "job", "career",
        "data analyst", "llm engineer", "developer", "hire",
        "available", "contact", "email", "linkedin", "github",

        # skills
        "skill", "skills", "python", "sql", "tableau", "excel",
        "machine learning", "data analysis", "llm", "rag", "openai",
        "streamlit", "api", "frontend", "backend",

        # projects
        "project", "projects", "chatbot", "portfolio", "forhome",
        "a/b testing", "dashboard",
    ]

    return any(keyword in q for keyword in allowed_keywords)


def is_allowed_question(question: str) -> bool:
    if not question or len(question.strip()) == 0:
        return False

    if len(question) > MAX_INPUT_LENGTH:
        return False

    if is_prompt_injection(question):
        return False

    if is_obviously_off_topic(question):
        return False

    if not is_profile_related(question):
        return False

    return True