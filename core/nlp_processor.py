import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_info(prompt: str) -> dict:
    doc = nlp(prompt)

    # -------------- INIT --------------
    extracted_info = {
        "name": None,
        "introduction": None,
        "skills": [],
        "experience": [],
        "projects": [],
        "education": [],
        "contacts": [],
    }

    # -------------- NAME --------------
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_info["name"] = ent.text
            break

    # -------------- CONTACTS --------------
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
    phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", prompt)
    linkedin = re.findall(r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9-_/]+", prompt)

    if emails:
        extracted_info["contacts"].append({"heading": "Email", "details": emails[0]})
    if phones:
        extracted_info["contacts"].append({"heading": "Phone", "details": phones[0]})
    if linkedin:
        extracted_info["contacts"].append({"heading": "LinkedIn", "details": linkedin[0]})

    if not extracted_info["name"] and emails:
        email_prefix = emails[0].split('@')[0]
        extracted_info["name"] = email_prefix.replace('.', ' ').replace('_', ' ').title()

    # -------------- SKILLS --------------
    SKILLS_KEYWORDS = [
        "python", "javascript", "java", "c++", "c#", "typescript", "php", "go", "swift", "kotlin",
        "django", "flask", "react", "vue", "node.js", "angular", "express.js", "spring", "svelte",
        "postgresql", "mysql", "mongodb", "sqlite", "redis", "aws", "docker", "git", "graphql", "rest", "api",
        "linux", "html", "css", "tailwind", "bootstrap", "ci/cd", "jenkins", "terraform", "ansible"
    ]
    lowered_prompt = prompt.lower()
    for skill in SKILLS_KEYWORDS:
        if re.search(rf"\b{re.escape(skill)}\b", lowered_prompt):
            formatted = skill.replace("js", "JS").replace("css", "CSS").replace("html", "HTML").upper() \
                if skill.isupper() else skill.title()
            if formatted not in extracted_info["skills"]:
                extracted_info["skills"].append(formatted)

    # -------------- PARAGRAPH BLOCKS --------------
    blocks = re.split(r"\n\s*\n|(?<=\.)\s{2,}", prompt.strip())

    intro_lines = []
    for block in blocks:
        lower_block = block.lower()

        # ----------- Education -----------
        if any(kw in lower_block for kw in ["bachelor", "master", "university", "graduated", "degree in"]):
            extracted_info["education"].append({"heading": "Education", "details": block.strip()})
            continue

        # ----------- Projects -----------
        if any(kw in lower_block for kw in ["project", "built", "developed", "dashboard", "app", "platform"]):
            title_match = re.findall(r"(named|called)?\s*['\"]?([A-Z][\w\s\-]{2,})['\"]?", block)
            title = title_match[-1][-1] if title_match else "Project"
            extracted_info["projects"].append({"heading": title.strip(), "details": block.strip()})
            continue

        # ----------- Experience -----------
        if any(kw in lower_block for kw in ["intern", "engineer", "developer", "worked at", "joined", "team"]):
            extracted_info["experience"].append({"heading": "Work Experience", "details": block.strip()})
            continue

        # ----------- Intro (Fallback) -----------
        if not extracted_info["introduction"]:
            if not any(keyword in lower_block for keyword in [
                "intern", "project", "university", "degree", "skills", "education", "linkedin", "email"
            ]):
                intro_lines.append(block.strip())

    if intro_lines:
        extracted_info["introduction"] = " ".join(intro_lines)
    else:
        extracted_info["introduction"] = "A summary of professional experience and skills."

    return extracted_info
