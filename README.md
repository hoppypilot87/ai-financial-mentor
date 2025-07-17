# 💬 AI Financial Mentor

An interactive AI-powered **financial mentor** that simulates the advice styles of different financial personas (like Warren Buffett, a budgeting coach, or a financial planner).  

Built with **OpenAI GPT**, **Streamlit**, and usage tracking logic.  

---

## 🚀 Features
✅ **Multiple Mentor Personas**  
- Warren Buffett (value investing approach)  
- Financial Coach (everyday budgeting & saving tips)  
- Budgeting Expert (step-by-step money management)

✅ **Free vs Pro Plan Simulation**  
- **Free Plan:** 1 question/day, 30 questions/month  
- **Pro Plan:** 10 questions/day, hidden monthly cap  

✅ **Usage Tracking**  
- Daily & monthly counters persist in a `usage_tracker.json`  
- Prevents overuse and encourages upgrading  

✅ **Brief vs Detailed Answer Mode**  
- Choose short 3–4 sentence replies or more detailed explanations  

✅ **Disclaimer Gating**  
- Users **must accept a disclaimer** before asking questions  

✅ **Clean Frontend**  
- Built with Streamlit  
- Intuitive dropdowns for persona, plan, and answer style  

---

## 🖼️ Demo Screenshot  

![AI Mentor Screenshot](screenshot.png)  

---

## 📂 Project Structure  

```
ai-financial-mentor/
│
├── app.py                # Streamlit frontend
├── backend.py            # Backend logic (usage tracking + API call)
├── mentor.py             # Core mentor functions
├── usage_tracker.json    # Tracks daily/monthly usage
├── .env.example          # Example for environment variables
└── README.md             # Project documentation
```

---

## ⚡ Quick Start  

1️⃣ **Clone the Repo**  
```bash
git clone https://github.com/hoppypilot87/ai-financial-mentor.git
cd ai-financial-mentor
```

2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```

3️⃣ **Set Your OpenAI API Key**  
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_key_here
```

4️⃣ **Run the App**  
```bash
streamlit run app.py
```

---

## 🏗️ Tech Stack  

- **Python 3.10+**  
- **OpenAI GPT (gpt-4o-mini)**  
- **Streamlit** for frontend  
- **dotenv + json** for config & usage tracking  

---

## 📜 License  

This project is **proprietary**. You may view, clone, and run this project for personal, non-commercial purposes. You may NOT redistribute, sublicense, or use this code in commercial products.   

---

🌟 What This Project Demonstrates

✅ Seamless AI integration into a user-friendly financial web app
✅ Practical OpenAI API usage with real-world constraints like free vs. pro plan limits
✅ Thoughtful UX design, including gated access, usage tracking, and clear upgrade paths
✅ Responsible AI deployment with legal disclaimers and explicit user consent  

---

👨‍💻 **Created by:** Philip Haapala  
🔗 **GitHub:** [hoppypilot87](https://github.com/hoppypilot87)  
