# Conversational SHL Assessment Recommender (minimal)

This is a minimal FastAPI implementation for the SHL take-home assessment prototype.

Run locally:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints:
- `GET /health` — returns {"status": "ok"}
- `POST /chat` — accepts JSON `{ "messages": [{"role":"user","content":"..."}, ...] }` and returns `{reply, recommendations, end_of_conversation}`.

Notes:
- This repository ships a small `catalog.json` with example items. For evaluation, replace it with a complete SHL Individual Test Solutions export (must use SHL URLs).
- The chat logic is rule-based for deterministic evaluation without external LLMs.
