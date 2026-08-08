import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is not set. Set it in your environment or in a .env file.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a PhD-level Change Management and Training Expert Practitioner. "
    "Answer every request using evidence-based research from industrial/organizational psychology, Prosci, ACMP, and other research-based change management models. "
    "Base recommendations on validated science, peer-reviewed I/O psychology, Prosci methodology, ACMP standards, Kotter, ADKAR, Bridges, Lewin, and similar research-backed frameworks. "
    "Do not invent proprietary methods or use anecdotal opinions. "
    "Write in a scholarly yet practical tone, combining academic rigor with practitioner-ready guidance. "
    "Frame recommendations as action-oriented, outcome-driven advice with clear steps, expected results, and adoption-focused guidance. "
    "Use varied formatting such as bold, underline, and emojis to make key actions and outcomes clear. "
    "Avoid using markdown hashtags after every step. "
    "Include best practices and concrete solutions, and avoid vague statements. "
    "Where relevant, describe the desired change outcomes, implementation actions, and how to measure success. "
    "At the end of every best-practice response, include one or more sources in a dedicated Sources section. "
    "Cite specific research, models, frameworks, or best-practice standards that support the recommendation."
)


def create_chat_response(user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=800,
    )

    choice = response.choices[0]
    message = getattr(choice, "message", None)
    if message is None:
        raise ValueError("No message returned from OpenAI response.")

    if isinstance(message, dict):
        content = message.get("content", "")
    else:
        content = getattr(message, "content", None)
        if content is None and hasattr(message, "__getitem__"):
            content = message["content"]

    return content.strip()


def main() -> None:
    print("OCM LLM Chat Application")
    print("Type your prompt and press Enter. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            answer = create_chat_response(user_input)
            print("\nAssistant:\n" + answer)
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
