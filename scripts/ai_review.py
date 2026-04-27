import os
import sys
import httpx
#dsfnajksnfdjak
def review_diff(diff: str) -> str:
    api_key = os.environ["GEMINI_API_KEY"]

    prompt = f"""You are a senior software engineer doing a code review.
Review the following git diff and provide feedback on:
1. Bugs or logical errors
2. Security risks (SQL injection, exposed secrets, etc.)
3. Unclear or confusing logic

Be concise. Use bullet points. If the diff looks fine, say so in one line.
Do NOT rewrite the code unless asked.

--- DIFF ---
{diff}
"""

    response = httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
        json={
            "contents": [{"parts": [{"text": prompt}]}]
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    diff = sys.stdin.read()

    if len(diff.strip()) < 10:
        print("No meaningful diff found.")
        sys.exit(0)

    if len(diff) > 8000:
        diff = diff[:8000] + "\n... (diff truncated)"

    review = review_diff(diff)
    print(review)