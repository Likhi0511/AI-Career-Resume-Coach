import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"
st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(180deg, #0B1120 0%, #0F172A 100%);
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

/* User message */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #1E293B;
}

/* Assistant message */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #111827;
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    background-color: #2563EB;
    color: white;
    border: none;
    padding: 0.5em 1em;
    transition: 0.2s ease;
}

.stButton>button:hover {
    background-color: #1D4ED8;
    transform: scale(1.03);
}

/* Input box */
textarea {
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1F2937;
}

/* Titles */
h1 {
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Subtext */
p {
    color: #9CA3AF;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="AI Career & Resume Coach ",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# SIDEBAR (Career-focused)
# -----------------------------
with st.sidebar:

    st.markdown("""
    <h1 style='text-align:center; 
    background: linear-gradient(90deg, #3B82F6, #22C55E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;'>
    🚀 AI Career & Resume Coach 
    </h1>

    <p style='text-align:center; font-size:16px; color:#9CA3AF;'>
    Analyze resumes, identify skill gaps, and get AI-powered career guidance
    </p>
    """, unsafe_allow_html=True)
    st.divider()
    if st.button("  🧹 Clear Chat"):
        st.session_state.messages = []

    st.divider()
    st.caption("⚡ Powered by RAG + LLM")
    st.caption("🦋 By Likhitha Jalli")
    st.markdown(
        '<a href="https://www.linkedin.com/in/likhithajalli/" target="_blank">🔗 LinkedIn Profile</a>',
        unsafe_allow_html=True
    )

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🚀 AI Career & Resume Coach</h1>
    <p style='text-align:center; color:gray;'>
    Analyze your resume, discover skill gaps, and get personalized career guidance
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SUGGESTED QUESTIONS
# -----------------------------
st.markdown("### 💡 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Skill Gap Analysis"):
        st.session_state.user_input = "What skills are missing in my resume?"

    if st.button("📝 Resume Improvements"):
        st.session_state.user_input = "Suggest improvements to my resume"

with col2:
    if st.button("🎯 Suitable Roles"):
        st.session_state.user_input = "What roles can I apply for?"

    if st.button("🚀 Career Roadmap"):
        st.session_state.user_input = "How can I become an AI engineer?"
# -----------------------------
# CHAT STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.caption("💡 Tip: Ask specific questions to get better insights")
# -----------------------------
# INPUT HANDLING
# -----------------------------
user_input = st.chat_input("Ask about your resume or career...")

# Handle button-triggered input
if "user_input" in st.session_state:
    user_input = st.session_state.user_input
    del st.session_state.user_input

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": user_input,
                        "session_id": "user1"
                    }
                )

                data = response.json()
                answer = data.get("answer", "No response")

            except Exception as e:
                answer = f"Error: {str(e)}"

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
