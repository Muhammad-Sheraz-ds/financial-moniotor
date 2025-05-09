import httpx
import os
from fastapi import HTTPException

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def analyze_transactions_with_gpt(transactions):
    transaction_data = "\n".join(
        f"{t.date}: {t.description} - ${t.amount} ({t.category})"
        for t in transactions
    )

    prompt = (
        "You are a financial performance analyst for a mid-sized finance company.\n"
        "Based on the following transactions, generate a concise report including:\n"
        "- Financial health overview\n"
        "- Major spending patterns\n"
        "- Any unusual activities\n"
        "- Key recommendations to improve financial performance\n\n"
        f"Transactions:\n{transaction_data}"
    )

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful financial analyst AI."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = httpx.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq AI failed: {str(e)}")
