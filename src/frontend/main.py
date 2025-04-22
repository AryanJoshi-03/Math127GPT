# src/frontend/main.py
import streamlit as st
import os
import sys
import time

def run_frontend():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
    # IMPORTANT: This must be the first Streamlit command
    st.set_page_config(
        page_title="Math 127 Assistant",
        page_icon="➗",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Now it's safe to import backend modules
    from backend.math_assistant import MathAssistant
    
    # Initialize all the components
    initialize_styling()
    initialize_session_state()
    main()

def initialize_styling():
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
            cursor: pointer; /* Shows hand cursor on hover */
            color: #4a5568; /* Change this to your preferred text color */
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

    st.markdown("""
    <style>
        /* Style the button to look like a card */
        div[data-testid="stButton"] > button {
            background-color: white;
            color: #4a5568;
            border-radius: var(--radius);
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
            text-align: left;
            display: block;
            width: 100%;
        }

        div[data-testid="stButton"] > button:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
            background-color: white; /* Keep white on hover */
        }

        /* Fix the markdown styling inside buttons */
        div[data-testid="stButton"] button h2, 
        div[data-testid="stButton"] button h3 {
            margin-top: 0;
            color: #4a5568;
        }

        div[data-testid="stButton"] button p {
            color: #4a5568;
        }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
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

    # Initialize MathAssistant in session state
    if 'assistant' not in st.session_state:
        # Now import and initialize the math assistant
        from backend.math_assistant import MathAssistant
        with st.spinner("🧠 Initializing AI Assistant..."):
            st.session_state.assistant = MathAssistant()

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

# === Render Sections Page ===
def render_sections():
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

# === Render Questions Page ===
def render_questions():
    render_breadcrumb()
    
    st.markdown(f"<h1>Section {st.session_state.current_section} Questions</h1>", unsafe_allow_html=True)
    
    # Example questions for each section
    # In a real app, these would come from your database
    questions = [
        "f(x) = x^4 - 32x^2. Enter the critical points in increasing order. Then, (a) Use the derivative to find all critical points. x1 , x2 , and x3. Then, (b) Use a graph to classify each critical point as a local minimum, a local maximum, or neither. Express it as x1 = _ is (a local maximum / a local minimum / neither, where _ refers to value of x) Answer it in that format. Do the same for x2 and x3 ",
        "Solve the equation 2x² - 8x + 7 = 0",
        "Calculate the limit as x approaches 2 of (x² - 4)/(x - 2)",
        "Find the indefinite integral of g(x) = 5x⁴ - 3x² + 2x",
        "Determine if the series Σ(1/n²) from n=1 to infinity converges or diverges"
    ]
    
    for i, question in enumerate(questions[:3]):  # Just show 3 questions for the demo
        card_id = f"q_{i+1}"
        
        col1, col2 = st.columns([10, 1])
        
        # Use a container for styling
        with col1:
            if st.button(f"Question {i+1}: {question}", key=card_id):
                navigate_to("questions", 
                    chapter=st.session_state.current_chapter, 
                    section=st.session_state.current_section,
                    question=i+1)

    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Sections", key="back_to_sections"):
        navigate_to("chapters", chapter=st.session_state.current_chapter)
    st.markdown("</div>", unsafe_allow_html=True)

# === Render Question Detail Page ===
def render_question_detail():
    render_breadcrumb()
    
    question_num = st.session_state.current_question
    
    # Sample questions (in a real app, get this from your database)
    questions = [
        "f(x) = x^4 - 32x^2. Enter the critical points in increasing order. Then, (a) Use the derivative to find all critical points. x1 , x2 , and x3. Then, (b) Use a graph to classify each critical point as a local minimum, a local maximum, or neither. Express it as x1 = _ is (a local maximum / a local minimum / neither, where _ refers to value of x) Answer it in that format. Do the same for x2 and x3 ",
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
        if st.button(
            """I'm completely lost and I don't know where to start with this problem""", 
            use_container_width=True
            ): 
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_num,
                      help_mode="Conceptual Help")
            
    with col2:
        if st.button(
            """I know the concept but I'm not sure how to apply it to this problem""", 
            use_container_width=True
            ): 
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_num,
                      help_mode="Application Help")
            
    with col3:
        if st.button(
            """I need step-by-step guidance to solve this problem""", 
            use_container_width=True
            ): 
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

# === AI Chat Interface (Integrated with MathAssistant) ===
def render_chat_interface():
    render_breadcrumb()
    
    question_num = st.session_state.current_question
    help_mode = st.session_state.help_mode
    
    # Sample questions
    questions = [
        "f(x) = x^4 - 32x^2. Enter the critical points in increasing order. Then, (a) Use the derivative to find all critical points. x1 , x2 , and x3. Then, (b) Use a graph to classify each critical point as a local minimum, a local maximum, or neither. Express it as x1 = _ is (a local maximum / a local minimum / neither, where _ refers to value of x) Answer it in that format. Do the same for x2 and x3 ",
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
    
    # Initialize first message if empty
    if len(st.session_state.chat_history) == 0:
        # Get assistant from session state
        assistant = st.session_state.assistant
        
        # Create automatic prompt based on help mode
        if help_mode == "Conceptual Help":
            auto_prompt = "explain what the question is asking me to do. Retrieve from PDF 4.1.1. DO NOT explain how to solve the question"
        elif help_mode == "Application Help":
            auto_prompt = "Explain how to solve the question. Retrieve information from the 4.1.1 PDF, but DO NOT give the actual answer. Only explain."
        elif help_mode == "Step-by-Step":
            auto_prompt = "Let's solve this step by step. First, explain what we're being asked to do in this problem."
        else:
            auto_prompt = "How can I help you with this problem?"
        
        # Show loading message while getting the answer
        with st.spinner("Getting initial information for you..."):
            # For the query, combine the question with the auto prompt
            query = f"Question: {question}\nStudent input: {auto_prompt}\nHelp mode: {help_mode}"
            
            # Get answer from the assistant
            result = assistant.get_answer(query, help_mode)
            
            if result:
                # Format the answer with sources
                answer = result["answer"]
                sources = result["sources"]
                
                if sources:
                    source_text = "\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in sources])
                    answer = answer + source_text
            else:
                answer = "I'm sorry, I couldn't generate an answer for that question."
            
            # Add assistant message to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
    
    # Display chat messages
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
    
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
            
            # Get assistant from session state
            assistant = st.session_state.assistant
            
            # For the query, combine the question with the user's input
            query = f"Question: {question}\nStudent input: {user_input}\nHelp mode: {help_mode}"
            
            # Show typing indicator
            message_placeholder = st.empty()
            message_placeholder.markdown("<div class='bot-message'>Thinking...</div>", unsafe_allow_html=True)
            
            # Get answer from the assistant
            result = assistant.get_answer(query, help_mode)
            
            if result:
                # Format the answer with sources
                answer = result["answer"]
                sources = result["sources"]
                
                if sources:
                    source_text = "\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in sources])
                    answer = answer + source_text
            else:
                answer = "I'm sorry, I couldn't generate an answer for that question."
            
            # Add assistant message to chat
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
            
            # Remove typing indicator and refresh
            message_placeholder.empty()
            st.rerun()
    
    # Navigation button
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

# === Main Routing Logic ===
def main():
    # Sidebar with admin access
    with st.sidebar:
        st.markdown("## Admin Panel")
        if st.button("Refresh PDF Database"):
            with st.spinner("🔄 Refreshing PDF database..."):
                # Re-initialize the assistant
                from backend.math_assistant import MathAssistant
                st.session_state.assistant = MathAssistant()
                st.success("✅ PDF database refreshed successfully!")
    
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
    run_frontend()