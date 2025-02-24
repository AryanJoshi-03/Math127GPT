import streamlit as st

st.set_page_config(
    page_title="Math 127 Chapters",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    h1.title {
        color: #7C4DFF;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        
    }
    .stButton>button {
        background-color: #7C4DFF;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        width: 200px;
        margin: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #6930FF;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* Center all buttons */
    .button-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>Choose the Chapter that you have a problem with!</h1>", unsafe_allow_html=True)

# Using containers and custom CSS for better button layout
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Chapter 1"):
        st.session_state.selected_chapter = "1"
        st.switch_page("pages/sections.py")
    if st.button("Chapter 4"):
        st.session_state.selected_chapter = "4"
        st.switch_page("pages/sections.py")
with col2:
    if st.button("Chapter 2"):
        st.session_state.selected_chapter = "2"
        st.switch_page("pages/sections.py")
    if st.button("Chapter 5"):
        st.session_state.selected_chapter = "5"
        st.switch_page("pages/sections.py")
with col3:
    if st.button("Chapter 3"):
        st.session_state.selected_chapter = "3"
        st.switch_page("pages/sections.py")

st.markdown('</div>', unsafe_allow_html=True)