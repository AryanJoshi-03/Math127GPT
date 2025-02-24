import streamlit as st

st.set_page_config(
    page_title="Math 127 Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #7C4DFF;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        width: 180px;
        margin: 10px;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #6930FF;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h1.title {
        color: #7C4DFF;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>Math 127 Chatbot</h1>", unsafe_allow_html=True)

st.text("Your AI-powered learning assistant for Math 127. Struggling with a concept? Need guidance on a problem? This chatbot is here to provide hints, explanations, and step-by-step guidance to help you understand—without just giving you the answers. Learn smarter, not harder!")

st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("Go to the Chapters"):
        st.switch_page("pages/chapters.py")
    
with col2:
    st.button("FAQs")