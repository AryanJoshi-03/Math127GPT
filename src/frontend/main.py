# app.py (main file)
import streamlit as st
import os

# === App Configuration ===
st.set_page_config(
    page_title="Math 127 Assistant",
    page_icon="➗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Custom CSS Styling ===
st.markdown("""
<style>
    /* Base styling */
    :root {
        --primary: #3b82f6;       /* Blue */
        --primary-dark: #2563eb;  /* Darker blue */
        --secondary: #f97316;     /* Orange accent */
        --neutral-50: #f8fafc;    /* Very light gray */
        --neutral-100: #f1f5f9;   /* Light gray */
        --neutral-200: #e2e8f0;   /* Medium-light gray */
        --neutral-800: #1e293b;   /* Dark gray */
        --radius: 10px;           /* Border radius */
    }
    
    /* Main layout */
    .main {
        background-color: var(--neutral-50);
        padding: 20px;
    }
    
    /* Navigation breadcrumb */
    .nav-breadcrumb {
        display: flex;
        gap: 10px;
        align-items: center;
        margin-bottom: 20px;
        padding: 10px 0;
        color: var(--neutral-800);
        font-size: 14px;
    }
    
    /* Headings */
    h1 {
        color: var(--neutral-800);
        font-size: 36px !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
    }
    
    h2 {
        color: var(--neutral-800);
        font-size: 24px !important;
        font-weight: 600 !important;
        margin-bottom: 15px !important;
    }
    
    /* Buttons */
    .primary-button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        margin: 5px 0;
        text-align: left;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .primary-button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .secondary-button {
        background-color: var(--neutral-100);
        color: var(--neutral-800);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius);
        padding: 10px 16px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .secondary-button:hover {
        background-color: var(--neutral-200);
    }
    
    /* Chat interface */
    .chat-container {
        background-color: var(--neutral-50);
        border-radius: var(--radius);
        padding: 20px;
        margin-top: 20px;
        height: 400px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    }

    .user-message {
        background-color: var(--primary);
        color: white;
        padding: 12px 16px;
        border-radius: var(--radius);
        margin: 10px 0;
        max-width: 70%;
        align-self: flex-end;
    }

    .bot-message {
        background-color: var(--neutral-100);
        color: var(--neutral-800);
        padding: 12px 16px;
        border-radius: var(--radius);
        margin: 10px 0;
        max-width: 70%;
        align-self: flex-start;
    }
    
    /* Cards */
    .card {
        background-color: white;
        border-radius: var(--radius);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Icons */
    .icon {
        margin-right: 8px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    div.stButton > button {
        background-color: transparent;
        border: none;
        padding: 0;
        margin: 0;
        box-shadow: none;
        width: 100%;
        height: 100%;
    }
    
    div.stButton > button:hover {
        background-color: transparent;
        transform: none;
    }
    
    /* Path indicator */
    .path-indicator {
        padding: 8px 16px;
        border-radius: var(--radius);
        background-color: var(--neutral-100);
        font-size: 14px;
        margin-bottom: 20px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# === Initialize session state ===
if 'navigation_path' not in st.session_state:
    st.session_state.navigation_path = []

if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = None
    
if 'current_section' not in st.session_state:
    st.session_state.current_section = None
    
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'help_mode' not in st.session_state:
    st.session_state.help_mode = None
    
if 'step_index' not in st.session_state:
    st.session_state.step_index = 0

# === Navigation Function ===
def navigate_to(destination, chapter=None, section=None, question=None, help_mode=None):
    st.session_state.navigation_path = [destination]
    
    if chapter:
        st.session_state.current_chapter = chapter
        st.session_state.navigation_path.append(f"Chapter {chapter}")
        
    if section:
        st.session_state.current_section = section
        st.session_state.navigation_path.append(f"Section {section}")
        
    if question:
        st.session_state.current_question = question
        st.session_state.navigation_path.append(f"Question {question}")
        
    if help_mode:
        st.session_state.help_mode = help_mode
        st.session_state.navigation_path.append(help_mode)
        # Reset chat history when starting a new help mode
        st.session_state.chat_history = []
        st.session_state.step_index = 0
    
    st.rerun()

# === Navigation Breadcrumb ===
def render_breadcrumb():
    breadcrumb_html = "<div class='nav-breadcrumb'>"
    breadcrumb_html += "<a href='#' onclick='javascript:return false;'>Home</a>"
    
    if len(st.session_state.navigation_path) > 0:
        for i, path in enumerate(st.session_state.navigation_path):
            breadcrumb_html += f" > <span>{path}</span>"
    
    breadcrumb_html += "</div>"
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

# === Render Home Screen ===
def render_home():
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1>Math 127 Assistant</h1>", unsafe_allow_html=True)
    
    st.markdown("<p>Your AI-powered learning assistant for Math 127. Struggling with a concept? Need guidance on a problem? This assistant is here to provide hints, explanations, and step-by-step guidance to help you understand—without just giving you the answers.</p>", unsafe_allow_html=True)
    
    st.markdown("<h2>Select a chapter to begin:</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        for i in range(1, 4):
            if st.button(f"📘 Chapter {i}", key=f"ch{i}"):
                navigate_to("chapters", chapter=i)
    
    with col2:
        for i in range(4, 7):
            if st.button(f"📘 Chapter {i}", key=f"ch{i}"):
                navigate_to("chapters", chapter=i)

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2>Quick Links</h2>", unsafe_allow_html=True)
        st.markdown("- [Course Syllabus](#)")
        st.markdown("- [Textbook Resources](#)")
        st.markdown("- [Office Hours Schedule](#)")
    
    with col2:
        st.markdown("<h2>FAQs</h2>", unsafe_allow_html=True)
        st.markdown("This assistant is designed to help you learn the material, not just get answers. It will guide you through problems step-by-step and help you understand the concepts.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === Render Sections Page ===
def render_sections():
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    
    render_breadcrumb()
    
    st.markdown(f"<h1>Chapter {st.session_state.current_chapter} Sections</h1>", unsafe_allow_html=True)
    
    # You can customize sections for each chapter
    sections = {
        1: ["1.1", "1.3", "1.4", "1.5 & 1.6", "1.8", "1.10"],
        2: ["2.1", "Limits and Continuity", "2.2", "2.3", "2.4", "2.5"],
        3: ["3.1", "3.2", "Sine and Cosine", "3.3", "3.4"],
        4: ["4.1", "4.2", "4.3", "4.4", "4.7", "4.8"],
        5: ["5.1", "5.2", "5.3", "5.4", "5.5"]
    }
    
    # Get sections for current chapter
    chapter_sections = sections.get(st.session_state.current_chapter, [])
    
    # Display sections in a grid
    cols = st.columns(3)
    for i, section in enumerate(chapter_sections):
        with cols[i % 3]:
            if st.button(f"📝 Section {section}", key=f"section_{section}"):
                navigate_to("sections", chapter=st.session_state.current_chapter, section=section)
    
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Chapters", key="back_to_chapters"):
        navigate_to("home")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# === Render Questions Page ===
def render_questions():
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    
    render_breadcrumb()
    
    st.markdown(f"<h1>Section {st.session_state.current_section} Questions</h1>", unsafe_allow_html=True)
    
    # Example questions for each section
    # In a real app, these would come from your database
    questions = [
        "Find the derivative of f(x) = 3x² + 2x - 5",
        "Solve the equation 2x² - 8x + 7 = 0",
        "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)",
        "Find the indefinite integral of g(x) = 5x⁴ - 3x² + 2x",
        "Determine if the series Σ(1/n²) from n=1 to infinity converges or diverges"
    ]
    
    for i, question in enumerate(questions[:3]):  # Just show 3 questions for the demo
        st.markdown(f"""
        <div class='card'>
            <h2>Question {i+1}</h2>
            <p>{question}</p>
            <div style='text-align: right;'>
                <button class='secondary-button' onclick='javascript:void(0);'>View Details</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Select Question {i+1}", key=f"q_{i+1}"):
            navigate_to("questions", 
                        chapter=st.session_state.current_chapter, 
                        section=st.session_state.current_section,
                        question=i+1)

    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Sections", key="back_to_sections"):
        navigate_to("chapters", chapter=st.session_state.current_chapter)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# === Render Question Detail Page ===
def render_question_detail():
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    
    render_breadcrumb()
    
    question_num = st.session_state.current_question
    
    # Sample questions (in a real app, get this from your database)
    questions = [
        "Find the derivative of f(x) = 3x² + 2x - 5",
        "Solve the equation 2x² - 8x + 7 = 0",
        "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)",
        "Find the indefinite integral of g(x) = 5x⁴ - 3x² + 2x",
        "Determine if the series Σ(1/n²) from n=1 to infinity converges or diverges"
    ]
    
    question = questions[question_num - 1] if question_num <= len(questions) else "Sample question"
    
    st.markdown(f"<h1>Question {question_num}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card'>
        <p style='font-size: 18px;'>{question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2>How would you like help with this question?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>I'm completely lost</h3>
            <p>I don't know where to start with this problem.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Conceptual Help", key="help_lost"):
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_num,
                      help_mode="Conceptual Help")
            
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>I know the concept</h3>
            <p>But I'm not sure how to apply it to this problem.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Application Help", key="help_apply"):
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_num,
                      help_mode="Application Help")
            
    with col3:
        st.markdown("""
        <div class='card'>
            <h3>I need step-by-step</h3>
            <p>Guide me through solving this problem step by step.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Step-by-Step Help", key="help_steps"):
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_num,
                      help_mode="Step-by-Step")
    
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Questions", key="back_to_questions"):
        navigate_to("sections", 
                  chapter=st.session_state.current_chapter,
                  section=st.session_state.current_section)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# === AI Chat Interface ===
def render_chat_interface():
    # st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    
    render_breadcrumb()
    
    question_num = st.session_state.current_question
    help_mode = st.session_state.help_mode
    
    # Sample questions (in a real app, get this from your database)
    questions = [
        "Find the derivative of f(x) = 3x² + 2x - 5",
        "Solve the equation 2x² - 8x + 7 = 0",
        "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)",
        "Find the indefinite integral of g(x) = 5x⁴ - 3x² + 2x",
        "Determine if the series Σ(1/n²) from n=1 to infinity converges or diverges"
    ]
    
    question = questions[question_num - 1] if question_num <= len(questions) else "Sample question"
    
    st.markdown(f"<h1>{help_mode}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card'>
        <h3>Question {question_num}:</h3>
        <p>{question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat display
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Initialize first message if empty
    if len(st.session_state.chat_history) == 0:
        if help_mode == "Conceptual Help":
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "I understand you're feeling lost with this problem. Let's start by understanding the core concepts involved. What specific part is confusing you about derivatives?"
            })
        elif help_mode == "Application Help":
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Great, so you understand the basic concept but need help applying it to this specific problem. Let's break down how to approach finding the derivative of a polynomial function."
            })
        elif help_mode == "Step-by-Step":
            # For step-by-step, we'll create a guided sequence
            steps = [
                "Let's solve this step by step. First, identify what function we're working with. We have f(x) = 3x² + 2x - 5. What rule do we need to apply to find the derivative?",
                "Great! The power rule states that if f(x) = x^n, then f'(x) = n·x^(n-1). Let's apply this to each term. What's the derivative of the first term, 3x²?",
                "Correct! Now let's find the derivative of the second term, 2x.",
                "Perfect! And what about the last term, -5?",
                "Excellent! Now let's combine all terms to get the complete derivative."
            ]
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": steps[0]
            })
    
    # Display chat messages
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close the chat-container div
    
    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your response:", placeholder="Type your answer or question here...")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            # Add user message to chat
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Handle step-by-step mode
            if help_mode == "Step-by-Step":
                steps = [
                    "Let's solve this step by step. First, identify what function we're working with. We have f(x) = 3x² + 2x - 5. What rule do we need to apply to find the derivative?",
                    "Great! The power rule states that if f(x) = x^n, then f'(x) = n·x^(n-1). Let's apply this to each term. What's the derivative of the first term, 3x²?",
                    "Correct! Now let's find the derivative of the second term, 2x.",
                    "Perfect! And what about the last term, -5?",
                    "Excellent! Now let's combine all terms to get the complete derivative."
                ]
                
                # Simple progression through steps
                st.session_state.step_index += 1
                if st.session_state.step_index < len(steps):
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": steps[st.session_state.step_index]
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Great job! You've successfully found the derivative of f(x) = 3x² + 2x - 5, which is f'(x) = 6x + 2. Would you like to try another problem?"
                    })
            else:
                # For other modes, just echo a response
                # In a real app, this would call your OpenAI API
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Thanks for your response! This is where the OpenAI API would generate a helpful response based on your input and the question context."
                })
            
            st.rerun()
    
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Change Help Mode", key="change_help"):
        # Reset chat when changing help mode
        st.session_state.chat_history = []
        st.session_state.step_index = 0
        # Explicitly clear help_mode
        st.session_state.help_mode = None
        navigate_to("questions", 
                chapter=st.session_state.current_chapter,
                section=st.session_state.current_section,
                question=question_num)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # st.markdown("</div>", unsafe_allow_html=True)  # Close the app-container div

# === Main Routing Logic ===
def main():
    # Check current navigation state and render appropriate view
    current_view = st.session_state.navigation_path[0] if st.session_state.navigation_path else "home"
    
    if current_view == "home":
        render_home()
    elif current_view == "chapters":
        render_sections()
    elif current_view == "sections":
        render_questions()
    elif current_view == "questions":
        render_question_detail()
    elif current_view == "question_detail" and st.session_state.help_mode:
        render_chat_interface()
    else:
        render_home()

if __name__ == "__main__":
    main()
