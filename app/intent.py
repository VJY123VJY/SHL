import re
from typing import List, Dict, Any


def is_compare_request(text: str) -> bool:
    return bool(re.search(r"\b(difference|compare|vs|v s|what is the difference)\b", text, re.I))


def is_refusal_topic(text: str) -> bool:
    return bool(re.search(r"\b(legal|law|lawsuit|salary|pay|fire|firing|termination|medical)\b", text, re.I))


def extract_constraints(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    full = " ".join(m["content"] for m in messages if m["role"] in ("user", "assistant"))
    role = None
    seniority = None
    skills = []

    m = re.search(r"hiring\s+(an|a)?\s*([A-Za-z0-9 \-+]+?)(?:\swho|\swith|\sfor|\s$|\.)", full, re.I)
    if m:
        role = m.group(2).strip()

    m2 = re.search(r"\b(junior|mid[- ]level|midlevel|senior|entry|lead|principal)\b", full, re.I)
    if m2:
        seniority = m2.group(1).lower()

    tech = re.findall(r"\b(Java|Python|SQL|stakeholders|communication|leadership|teamwork|coding|programming)\b", full, re.I)
    skills = list({s.lower() for s in tech})

    return {"role": role, "seniority": seniority, "skills": skills, "full_text": full}
