# -----------------------------------------------------------------------------------
# AI Mentor Service
# -----------------------------------------------------------------------------------
# ✅ Loads your OpenAI API key securely (supports .env for local dev)
# ✅ Provides an ask_ai_mentor() function to get AI advice styled as different personas
# ✅ Includes a built-in disclaimer for legal safety
# ✅ Ready for future integration into Finory or any app backend
# -----------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load .env file for local development (not needed in prod)
load_dotenv()

# ✅ Fetch API key from env (prod will inject via hosting secrets)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ No OPENAI_API_KEY found. Set it in .env or as an environment variable.")

# ✅ Initialize OpenAI client securely
client = OpenAI(api_key=api_key)

# ✅ Legal Disclaimer (prepended to every response)
DISCLAIMER = (
    "⚠️ *Disclaimer: This is AI-generated financial information for educational purposes only. "
    "It is **NOT** personalized financial advice. Always consult a certified financial professional "
    "before making investment decisions.*\n\n"
)

# ✅ Persona styles (extendable)
PERSONA_PROMPTS = {
    "warren_buffett": (
        "You are Warren Buffett, the legendary value investor. "
        "You give calm, long-term, rational advice about personal finance and investing."
    ),
    "financial_coach": (
        "You are a friendly personal finance coach who focuses on budgeting, saving, and debt reduction "
        "for everyday people."
    ),
    "budgeting_expert": (
        "You are a budgeting guru. Provide step-by-step guidance to optimize savings and manage spending wisely."
    ),
    "generic": (
        "You are a helpful financial assistant who explains things clearly and simply."
    )
}

def ask_ai_mentor(persona: str, question: str) -> str:
    """
    Ask the AI Mentor a financial question.
    
    Args:
        persona (str): The mentor persona ("warren_buffett", "financial_coach", etc.)
        question (str): User's financial question
        
    Returns:
        str: AI-generated response with a disclaimer
    """

    # Pick persona style or fallback to generic
    style_prompt = PERSONA_PROMPTS.get(persona.lower(), PERSONA_PROMPTS["generic"])

    # Call OpenAI chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": style_prompt},
            {"role": "user", "content": question}
        ]
    )

    ai_reply = response.choices[0].message.content.strip()
    return DISCLAIMER + ai_reply


# ✅ Example usage (only runs if called directly)
if __name__ == "__main__":
    print("🤖 AI Mentor Demo\n")
    sample_question = "Should I invest in index funds if I’m in my 30s?"
    reply = ask_ai_mentor("warren_buffett", sample_question)
    print(reply)
