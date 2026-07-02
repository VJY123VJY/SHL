import json
import os
import re
from typing import List, Dict, Any

def load_catalog(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def search_catalog(catalog: List[Dict[str, Any]], constraints: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
    scores = []
    query = constraints.get("full_text", "").lower()
    for item in catalog:
        text = " ".join([item.get("name", ""), item.get("description", ""), " ".join(item.get("tags", []))]).lower()
        score = 0
        for t in item.get("tags", []):
            if t.lower() in query:
                score += 3
        if constraints.get("role") and constraints["role"].lower() in text:
            score += 2
        for s in constraints.get("skills", []):
            if s in text:
                score += 2
        if constraints.get("seniority"):
            if constraints["seniority"] in ("senior", "lead", "principal") and "lead" in text:
                score += 1
        for w in re.findall(r"\w+", query):
            if w in text:
                score += 0.2
        if score > 0:
            scores.append((score, item))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [{"name": it["name"], "url": it["url"], "test_type": it.get("test_type", "")} for _, it in scores[:top_k]]
