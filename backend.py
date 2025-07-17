# backend.py
import os
import json
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load .env and API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ No OPENAI_API_KEY found. Set it in .env or as an environment variable.")

client = OpenAI(api_key=api_key)

# ✅ Usage tracking
USAGE_FILE = "usage_tracker.json"
LIMITS = {
    "free": {"daily": 1, "monthly": 30},
    "pro": {"daily": 10, "monthly": 250}
}

# ✅ Disclaimer
DISCLAIMER = (
    "⚠️ *Disclaimer: This is AI-generated financial information for educational purposes only.*\n"
    "It is **NOT** licensed or personalized financial advice.\n"
    "Always consult a certified financial professional before making any investment decisions.\n\n"
)

# ✅ Persona prompts
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

# ✅ Load or initialize usage tracking
def load_usage():
    if not os.path.exists(USAGE_FILE):
        return {"date": str(datetime.date.today()), "daily_count": 0, "monthly_count": 0}
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

def reset_usage_if_needed(usage):
    today = datetime.date.today()
    last_date = datetime.datetime.strptime(usage["date"], "%Y-%m-%d").date()

    # Reset daily count if a new day
    if today > last_date:
        usage["daily_count"] = 0
        # Reset monthly count if new month
        if today.month != last_date.month:
            usage["monthly_count"] = 0
        usage["date"] = str(today)

    return usage

def can_still_ask(plan="free"):
    """
    Checks if the user is under their daily/monthly limit.
    Returns (True, usage_dict) if allowed,
            (False, message) if not.
    """
    usage = load_usage()
    usage = reset_usage_if_needed(usage)
    save_usage(usage)  # Save any resets

    daily_limit = LIMITS[plan]["daily"]
    monthly_limit = LIMITS[plan]["monthly"]

    if usage["daily_count"] >= daily_limit:
        return False, f"🚫 Daily limit reached for **{plan.upper()}** plan ({daily_limit}/day). Try again tomorrow or upgrade!"
    if usage["monthly_count"] >= monthly_limit:
        return False, f"🚫 Monthly limit reached for **{plan.upper()}** plan ({monthly_limit}/month). Upgrade for more access!"

    return True, usage  # ✅ Still allowed

def increment_usage(usage):
    usage["daily_count"] += 1
    usage["monthly_count"] += 1
    save_usage(usage)

# ✅ Main function to ask the AI Mentor
def ask_ai_mentor(persona: str, question: str, plan: str = "free", mode: str = "brief") -> str:
    """
    Ask the AI Mentor a financial question with usage tracking.

    ✅ FIXED: Now the first allowed request actually returns an answer,
    and usage is only incremented AFTER a successful response.
    """

    # ✅ Step 1: Check if user still has quota BEFORE making API call
    allowed, usage_or_msg = can_still_ask(plan)
    if not allowed:
        return usage_or_msg  # 🚫 Directly return limit message
    else:
        usage = usage_or_msg  # ✅ Safe usage object

    # ✅ Step 2: Persona style
    style_prompt = PERSONA_PROMPTS.get(persona.lower(), PERSONA_PROMPTS["generic"])

    # ✅ Step 3: Adjust question for mode
    if mode == "brief":
        question = f"Answer very briefly in 3-4 sentences max. {question}"
    else:
        question = f"Provide a concise but more detailed explanation. {question}"

    # ✅ Step 4: Make the API call
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": style_prompt},
                {"role": "user", "content": question}
            ]
        )
        ai_reply = response.choices[0].message.content.strip()

        # ✅ Step 5: Only increment usage AFTER a successful reply
        increment_usage(usage)

        return DISCLAIMER + ai_reply

    except Exception as e:
        return f"❌ Error contacting AI Mentor: {e}"
