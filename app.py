import streamlit as st
from backend import ask_ai_mentor  # ✅ Connects to backend logic

# ✅ Track disclaimer agreement
if "agreed_to_disclaimer" not in st.session_state:
    st.session_state.agreed_to_disclaimer = False

# ✅ Track if usage is exceeded
if "limit_reached" not in st.session_state:
    st.session_state.limit_reached = False

# ✅ App Title
st.title("💬 AI Financial Mentor")
st.write("Welcome! You can now chat with your AI financial mentor persona.")

# ✅ Show disclaimer BEFORE unlocking anything
if not st.session_state.agreed_to_disclaimer:
    st.warning("""
    ### ⚠️ Disclaimer
    
    This AI Financial Mentor is for **educational purposes only**.  
    - It is **NOT licensed financial advice**.  
    - It should NOT be relied upon for investment, legal, tax, or financial decisions.  
    - Always consult a qualified financial advisor before making any decisions.
    
    By clicking **I Agree**, you acknowledge:
    - You are using this tool at your **own risk**.
    - The developers are **not responsible** for any outcomes from your use of this tool.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I Agree"):
            st.session_state.agreed_to_disclaimer = True
            st.rerun()

    with col2:
        if st.button("❌ I Do Not Agree"):
            st.stop()  # stops app if reject

    st.stop()  # stops rest of UI

# ✅ If agreed, unlock AI Mentor UI
st.info("✅ You have accepted the disclaimer. You can now use the AI Mentor.")

# 🔓 Mentor Style Dropdown
mentor_style = st.selectbox(
    "Select your AI Mentor style:",
    ["Warren Buffett", "Financial Coach", "Budgeting Expert"]
)

# 🔓 Answer Mode Toggle
answer_mode = st.radio(
    "How do you want your answers?",
    ["Brief (3–4 sentences)", "Detailed (more explanation)"]
)

# 🔓 Plan Type
plan_type = st.radio("Your plan type:", ["Free", "Pro"])

# 🔓 Question Input
question = st.text_area("Ask your financial question here:")

# ✅ Dynamic usage indicator (always above button)
if st.session_state.limit_reached:
    st.error("🚫 Daily limit reached for FREE plan (1/day). Try again tomorrow or upgrade!")
    
    # ✅ Show Upgrade button ONLY after hitting limit
    if st.button("🚀 Upgrade to Pro for more responses"):
        st.info("💳 Upgrade page coming soon! You’ll unlock 10/day & 250/month.")

else:
    st.caption("📊 Usage: 0/1 today | 0/30 this month")

# ✅ Button to Get Advice
if st.button("💡 Get Advice", key="ask_advice_button"):
    if question.strip():
        with st.spinner("Thinking..."):
            # Map selections
            persona_key = mentor_style.lower().replace(" ", "_")
            mode_key = "brief" if "Brief" in answer_mode else "detailed"
            plan_key = plan_type.lower()

            # Call backend AI mentor
            reply = ask_ai_mentor(
                persona=persona_key,
                question=question,
                plan=plan_key,
                mode=mode_key
            )

            # ✅ If backend returns a limit message, show only ONCE
            if reply.startswith("🚫 Daily limit reached"):
                st.error(reply)
                st.button("🚀 Upgrade to Pro for more responses", key="upgrade_button")
            else:
                # ✅ Normal AI reply
                st.write(reply)

    else:
        st.warning("Please enter a question first.")

# ✅ Footer Note
st.markdown("---")
st.caption(
    "This AI mentor is NOT a licensed financial advisor. It is for educational purposes only and should not replace professional advice."
)
