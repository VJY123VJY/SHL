from fastapi import HTTPException
from typing import List, Dict, Any
import os

from app.schemas import Message, ChatRequest
from app.intent import is_compare_request, is_refusal_topic, extract_constraints
from app.catalog import load_catalog, search_catalog


# Load catalog
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "catalog.json")
CATALOG = load_catalog(CATALOG_PATH)


from app import app


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    messages = [m.dict() for m in req.messages]
    if not any(m["role"] == "user" for m in messages):
        raise HTTPException(status_code=400, detail="No user message provided")

    last_user_msgs = [m for m in messages if m["role"] == "user"]
    last_text = last_user_msgs[-1]["content"] if last_user_msgs else ""

    if is_refusal_topic(last_text):
        return {"reply": "Sorry—I can only help with SHL assessments and catalog queries. I cannot provide legal, salary, or medical advice.", "recommendations": [], "end_of_conversation": False}

    if is_compare_request(last_text):
        # try to find quoted names first
        quoted = []
        try:
            import re

            quoted = re.findall(r'"([^"]+)"', last_text)
        except Exception:
            quoted = []
        names = quoted
        matches = []
        for n in names:
            for it in CATALOG:
                if n.lower() in it["name"].lower():
                    matches.append(it)
                    break
        if len(matches) >= 2:
            a, b = matches[0], matches[1]
            reply = f"Comparison between {a['name']} and {b['name']}:\n{a['name']}: {a['description']}\n{b['name']}: {b['description']}\nSources: {a['url']}, {b['url']}"
            return {"reply": reply, "recommendations": [], "end_of_conversation": False}
        else:
            return {"reply": "I couldn't identify two assessments to compare. Please name them exactly as in the SHL catalog.", "recommendations": [], "end_of_conversation": False}

    constraints = extract_constraints(messages)
    if not constraints.get("role") or (not constraints.get("seniority") and not constraints.get("skills")):
        missing = []
        if not constraints.get("role"):
            missing.append("what role or job title you're hiring for")
        if not constraints.get("seniority") and not constraints.get("skills"):
            missing.append("seniority level (junior/mid/senior) or key skills")
        q = "Could you clarify " + " and ".join(missing) + "?"
        return {"reply": q, "recommendations": [], "end_of_conversation": False}

    recs = search_catalog(CATALOG, constraints)
    if not recs:
        return {"reply": "I couldn't find matching SHL assessments in the catalog for that description.", "recommendations": [], "end_of_conversation": False}

    reply = f"Got it. Here are {min(len(recs),10)} assessments that match your requirements."
    return {"reply": reply, "recommendations": recs[:10], "end_of_conversation": True}
