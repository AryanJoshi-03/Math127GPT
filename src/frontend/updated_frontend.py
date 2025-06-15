import streamlit as st
import os
import sys
import time
import json
from frontend.utils.question_loader import QuestionLoader

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

        .practice-button {
            background-color: var(--secondary) !important;
            color: white !important;
            font-weight: 600 !important;
            margin: 15px 0 25px 0 !important;
            padding: 12px 20px !important;
        }
    
        .practice-button:hover {
            background-color: #e05f05 !important;
            transform: translateY(-2px) !important;
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
        
    if 'problem_steps' not in st.session_state:
        st.session_state.problem_steps = []
        
    if 'step_progress' not in st.session_state:
        st.session_state.step_progress = []

    if 'use_regular_interface' not in st.session_state:
        st.session_state.use_regular_interface = False

    if 'original_question' not in st.session_state:
        st.session_state.original_question = None
        
    if 'similar_question' not in st.session_state:
        st.session_state.similar_question = None
        
    if 'current_question_text' not in st.session_state:
        st.session_state.current_question_text = None

    # Initialize MathAssistant in session state
    if 'assistant' not in st.session_state:
        # Now import and initialize the math assistant
        from backend.math_assistant import MathAssistant
        with st.spinner("🧠 Initializing AI Assistant..."):
            st.session_state.assistant = MathAssistant()

    if 'question_loader' not in st.session_state:
        st.session_state.question_loader = QuestionLoader()

def generate_similar_question(question):
    """
    Generates a similar question using the MathAssistant's LLM capabilities.
    """
    # Get assistant from session state
    assistant = st.session_state.assistant
    
    # Use the dedicated method for generating similar questions
    similar_question = assistant.generate_similar_question(question)
    
    # In case of failure, fall back to simple number replacement
    if "Could not generate" in similar_question:
        st.warning("Using fallback method to generate similar question")
        import re
        import random
        
        # Simple replacement of numbers with slightly different ones
        def replace_number(match):
            num = int(match.group(0))
            # Change by up to 50% but at least by 1
            change = max(1, int(num * random.uniform(0.1, 0.5)))
            if random.choice([True, False]):
                return str(num + change)
            else:
                return str(max(1, num - change))
        
        # Replace numbers in the question
        modified_question = re.sub(r'\d+', replace_number, question)
        return modified_question
    
    return similar_question

# === Navigation Function ===
def navigate_to(destination, chapter=None, section=None, question=None, help_mode=None):
    print(f"DEBUG: navigate_to called with destination={destination}, chapter={chapter}, section={section} (type={type(section)}), question={question}, help_mode={help_mode}")
    
    # Force section to string if it's not None
    if section is not None:
        section = str(section)
        print(f"DEBUG: Converting section to string: {section}")
    
    st.session_state.navigation_path = [destination]
    if chapter:
        st.session_state.current_chapter = chapter
    if section:
        st.session_state.current_section = section
    if question:
        st.session_state.current_question = question
    if help_mode:
        st.session_state.help_mode = help_mode
        # Reset chat history when starting a new help mode
        st.session_state.chat_history = []
        # Reset step-related variables
        st.session_state.step_index = 0
        st.session_state.problem_steps = []
        st.session_state.step_progress = []
        
        # If we're in step-by-step mode and have a question, load its steps
        if help_mode == "Step-by-Step" and question:
            question_data = st.session_state.question_loader.get_question_by_id(question)
            if question_data and 'steps' in question_data:
                st.session_state.problem_steps = question_data['steps']
                st.session_state.step_progress = [{"completed": False, "attempts": 0, "user_answer": ""} for _ in question_data['steps']]
    
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
    print(f"DEBUG: render_questions - current_section = {st.session_state.current_section} (type={type(st.session_state.current_section)})")
    
    # Ensure current_section is a string
    section = str(st.session_state.current_section)
    print(f"DEBUG: render_questions - using section = {section}")
    
    questions = st.session_state.question_loader.load_section_questions(
        st.session_state.current_chapter,
        section
    )
    
    for i, question in enumerate(questions):
        card_id = f"q_{question['id']}"
        col1, col2 = st.columns([10, 1])
        with col1:
            if st.button(f"Question {i+1}: {question['text']}", key=card_id):
                # Store the question in session state before navigation
                st.session_state.current_question = question['id']
                st.session_state.original_question = question
                st.session_state.current_question_text = question['text']
                navigate_to("question_detail", 
                    chapter=st.session_state.current_chapter, 
                    section=section,
                    question=question['id'])
    
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Sections", key="back_to_sections"):
        navigate_to("chapters", chapter=st.session_state.current_chapter)
    st.markdown("</div>", unsafe_allow_html=True)

# === Render Question Detail Page ===
def render_question_detail():
    render_breadcrumb()
    question_id = st.session_state.current_question
    
    # Get the original question data. This will be used for things like 'id', 'type', etc.
    if 'original_question' not in st.session_state or not st.session_state.original_question:
        original_question_data = st.session_state.question_loader.get_question_by_id(question_id)
        if original_question_data:
            st.session_state.original_question = original_question_data
            # If current_question_text is not set (i.e., not coming from a similar question), set it to original
            if not st.session_state.current_question_text:
                st.session_state.current_question_text = original_question_data['text']
    else:
        original_question_data = st.session_state.original_question
        # Ensure current_question_text is set if we just landed here directly on an original question
        if not st.session_state.current_question_text:
            st.session_state.current_question_text = original_question_data['text']

    # Ensure we always have a current_question_text to display
    if not st.session_state.current_question_text and original_question_data:
        st.session_state.current_question_text = original_question_data['text']
    
    if not original_question_data:
        st.error("Question not found")
        return
    
    st.markdown(f"<h1>Question {original_question_data['id']}</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='card'>
        <p style='font-size: 18px;'>{st.session_state.current_question_text}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Four Buttons Section ---
    st.markdown('<div class="practice-button-container">', unsafe_allow_html=True)
    if st.button("✨ Practice with Similar Question", key="practice_button", use_container_width=True):
        with st.spinner("Generating similar question..."):
            similar_question = generate_similar_question(st.session_state.current_question_text)
            st.session_state.similar_question = similar_question
            st.session_state.current_question_text = similar_question
        navigate_to("similar_question", 
                    chapter=st.session_state.current_chapter,
                    section=st.session_state.current_section,
                    question=question_id)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h2>How would you like help with this question?</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("I'm completely lost and I don't know where to start with this problem", use_container_width=True):
            st.session_state.help_mode = "Conceptual Help"
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.step_index = 0     # Reset step index
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter, 
                      section=st.session_state.current_section, 
                      question=question_id, 
                      help_mode="Conceptual Help")
    with col2:
        if st.button("I know the concept but I'm not sure how to apply it to this problem", use_container_width=True):
            st.session_state.help_mode = "Application Help"
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.step_index = 0     # Reset step index
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter, 
                      section=st.session_state.current_section, 
                      question=question_id, 
                      help_mode="Application Help")
    with col3:
        if st.button("I need step-by-step guidance to solve this problem", use_container_width=True):
            st.session_state.help_mode = "Step-by-Step"
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.step_index = 0     # Reset step index
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter, 
                      section=st.session_state.current_section, 
                      question=question_id, 
                      help_mode="Step-by-Step")

    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Questions", key="back_to_questions"):
        navigate_to("sections", chapter=st.session_state.current_chapter, section=st.session_state.current_section)
    st.markdown("</div>", unsafe_allow_html=True)

def render_similar_question():
    render_breadcrumb()
    
    question_id = st.session_state.current_question
    original_question = st.session_state.original_question
    similar_question = st.session_state.similar_question

    st.session_state.current_question_text = similar_question

    st.markdown(f"<h1>Similar Practice Question</h1>", unsafe_allow_html=True)

    st.success("✅ Similar practice question generated successfully!")
    
    # Add comparison of original and similar questions
    st.markdown(f"""
    <div class='card'>
        <h3>Practice Question:</h3>
        <p>{similar_question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2>How would you like help with this question?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(
            """I'm completely lost and I don't know where to start with this problem""", 
            use_container_width=True
            ): 
            # Store the practice question as the current question
            st.session_state.current_question_text = similar_question
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_id,
                      help_mode="Conceptual Help")
            
    with col2:
        if st.button(
            """I know the concept but I'm not sure how to apply it to this problem""", 
            use_container_width=True
            ): 
            # Store the practice question as the current question
            st.session_state.current_question_text = similar_question
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_id,
                      help_mode="Application Help")
            
    with col3:
        if st.button(
            """I need step-by-step guidance to solve this problem""", 
            use_container_width=True
            ): 
            # Store the practice question as the current question
            st.session_state.current_question_text = similar_question
            navigate_to("question_detail", 
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_id,
                      help_mode="Step-by-Step")
    
    # Add a button to generate another similar question
    st.markdown('<div class="practice-button-container">', unsafe_allow_html=True)
    if st.button("🔄 Generate Another Similar Question", key="another_similar_button", use_container_width=True):
        # Generate a different similar question
        new_similar_question = generate_similar_question(original_question['text'])
        st.session_state.similar_question = new_similar_question
        st.session_state.current_question_text = new_similar_question # Ensure this is also updated
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Back to Original Question", key="back_to_original"):
        # Explicitly set current_question_text back to the original question's text
        st.session_state.current_question_text = st.session_state.original_question['text']
        navigate_to("questions", 
                  chapter=st.session_state.current_chapter,
                  section=st.session_state.current_section,
                  question=question_id)
    st.markdown("</div>", unsafe_allow_html=True)

# === AI Chat Interface (Integrated with MathAssistant) ===
def render_chat_interface():
    render_breadcrumb()
    
    question_id = st.session_state.current_question
    help_mode = st.session_state.help_mode

    # Get the current question text (either original or practice question)
    question = st.session_state.current_question_text if st.session_state.current_question_text else "Sample question"
    
    st.markdown(f"<h1>{help_mode}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card'>
        <h3>Question {question_id}:</h3>
        <p>{question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load questions for the current section
    section = str(st.session_state.current_section)
    
    questions = st.session_state.question_loader.load_section_questions(
        st.session_state.current_chapter,
        section
    )
    
    # Find the question by ID
    question_data = next((q for q in questions if q['id'] == question_id), None)
    if question_data:
        question = question_data['text']
    
    # Initialize first message if empty
    if len(st.session_state.chat_history) == 0:
        # Get assistant from session state
        assistant = st.session_state.assistant
        
        # Create automatic prompt based on help mode
        if help_mode == "Conceptual Help":
            auto_prompt = "explain what the question is asking me to do. Retrieve from PDF 4.1.1. DO NOT explain how to solve the question"
            
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
                
        elif help_mode == "Application Help":
            auto_prompt = "Explain how to solve the question. Retrieve information from the 4.1.1 PDF, but DO NOT give the actual answer. Only explain."
            
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
            
            # Construct conversation history for context
            conversation_history_for_llm = ""
            for msg in st.session_state.chat_history:
                conversation_history_for_llm += f"{msg['role'].capitalize()}: {msg['content']}\n"
            
            # Prepare the query for the assistant, emphasizing no direct answers and context awareness
            query_to_assistant = f"""
            The user is asking a question or making a statement in the context of the original math problem and the ongoing conversation.
            Original Math Question: {question}
            Current Help Mode: {help_mode}
            
            Conversation Context (most recent at bottom):
            {conversation_history_for_llm}
            
            Your instructions as a Math 127 AI Assistant:
            1. Respond directly to the user's latest input, drawing upon the entire conversation history for context.
            2. **CRITICAL: NEVER provide the direct solution or final answer to the math problem or any sub-step.** Your role is to guide, not to solve.
            3. Provide helpful, conceptual, or application-based guidance relevant to the math problem and the current help mode. For instance, if they ask for a next step, guide them to it without giving the exact formula or number.
            4. Maintain a helpful, encouraging, and patient tone.
            5. **STRICTLY adhere to the topic.** If the user asks something completely unrelated to the math problem, the specific step, or the course material, politely inform them that you can only assist with math-related queries for this course. Do not engage in off-topic discussions or try to answer unrelated questions.
            6. If the user makes a statement rather than asking a question, acknowledge their input and offer further guidance or a next logical thought process step.
            """
            
            # Show typing indicator
            message_placeholder = st.empty()
            message_placeholder.markdown("<div class='bot-message'>Thinking...</div>", unsafe_allow_html=True)
            
            # Get answer from the assistant
            result = assistant.get_answer(query_to_assistant, help_mode)
            
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
            
            # Remove typing indicator and refresh
            if 'message_placeholder' in locals():
                message_placeholder.empty()
            st.rerun()

    # Add Try Similar Question button in chat interface
    st.markdown('<div class="practice-button-container">', unsafe_allow_html=True)
    if st.button("✨ Try a Similar Question", key="try_similar_button"):
        # Generate a similar question
        if st.session_state.original_question:
            similar_question = generate_similar_question(st.session_state.original_question['text'])
            st.session_state.similar_question = similar_question
            st.session_state.current_question_text = similar_question  # Update the current question text
            # Reset chat history
            st.session_state.chat_history = []
            st.session_state.step_index = 0
            navigate_to("similar_question",
                      chapter=st.session_state.current_chapter,
                      section=st.session_state.current_section,
                      question=question_id)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation button
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Change Help Mode", key="change_help"):
        # Reset chat when changing help mode
        st.session_state.chat_history = []
        st.session_state.step_index = 0
        # Explicitly clear help_mode
        st.session_state.help_mode = None
        navigate_to("question_detail", 
                chapter=st.session_state.current_chapter,
                section=st.session_state.current_section,
                question=question_id)
    st.markdown("</div>", unsafe_allow_html=True)

# === Improved Step-by-Step Interface ===
def render_improved_step_interface():
    render_breadcrumb()
    
    question_id = st.session_state.current_question
    help_mode = st.session_state.help_mode
    
    # Get the current question text (either original or practice question)
    question = st.session_state.current_question_text
    
    st.markdown(f"<h1>{help_mode}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card'>
        <h3>Question {question_id}:</h3>
        <p>{question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if this is a practice question (not from JSON)
    is_practice_question = question != st.session_state.original_question['text']
    
    if is_practice_question:
        # For practice questions, show a simpler interface with hints
        st.markdown("### Need help? Click to see hints:")
        
        # Get the generic hints from the first question in the section
        section = str(st.session_state.current_section)
        questions = st.session_state.question_loader.load_section_questions(
            st.session_state.current_chapter,
            section
        )
        
        # Get the generic hints from the first question in the section
        generic_hints = None
        for q in questions:
            if 'generic_hints' in q:
                generic_hints = q['generic_hints']
                break
        
        if generic_hints:
            # Display hints in expandable sections
            for i, hint in enumerate(generic_hints, 1):
                with st.expander(f"Hint {i}"):
                    st.markdown(hint)
        else:
            # Fallback to basic hints if none exist in JSON
            basic_hints = [
                "First, identify what type of problem this is and what concepts you need to apply.",
                "Write down the given function or equation exactly as shown.",
                "Apply the necessary mathematical operations to solve the problem.",
                "Verify your answer makes sense in the context of the problem."
            ]
            for i, hint in enumerate(basic_hints, 1):
                with st.expander(f"Hint {i}"):
                    st.markdown(hint)
        
        # Add a text input for the user's answer
        # user_answer = st.text_area("Your answer:", height=150)
        
        # Add a submit button
        # if st.button("Submit Answer"):
        #     if user_answer:
        #         st.success("Answer submitted! Check your work against the hints above.")
        #     else:
        #         st.warning("Please enter your answer before submitting.")
    else:
        # For original questions, use the existing step-by-step interface
        # Get the steps from JSON
        section = str(st.session_state.current_section)
        questions = st.session_state.question_loader.load_section_questions(
            st.session_state.current_chapter,
            section
        )
        question_data = next((q for q in questions if q['id'] == question_id), None)
        predefined_steps = question_data.get('steps', []) if question_data else []
        
        # Initialize step_index if not in session state
        if 'step_index' not in st.session_state:
            st.session_state.step_index = 0
        
        # Initialize a container for showing feedback
        feedback_container = st.container()
        
        # Initialize progress tracking
        if 'step_progress' not in st.session_state or len(st.session_state.step_progress) != len(predefined_steps):
            st.session_state.step_progress = []
            for _ in range(len(predefined_steps)):
                st.session_state.step_progress.append({"completed": False, "attempts": 0, "user_answer": ""})
        
        # Progress bar
        if predefined_steps:
            progress = sum(1 for step in st.session_state.step_progress if step["completed"]) / len(predefined_steps)
            st.progress(progress)
            st.markdown(f"**Progress:** {int(progress * 100)}% complete")
        
        # If this is a question with predefined steps
        if predefined_steps:
            # Get current step
            current_index = st.session_state.step_index
            
            # If we've completed all steps
            if current_index >= len(predefined_steps):
                st.success("🎉 Congratulations! You've successfully completed all steps of this problem!")
                
                # Show a summary of their performance
                st.markdown("### Your Performance Summary")
                total_attempts = sum(step["attempts"] for step in st.session_state.step_progress)
                perfect_steps = sum(1 for step in st.session_state.step_progress if step["attempts"] == 1)
                
                st.markdown(f"- Total steps completed: **{len(predefined_steps)}**")
                st.markdown(f"- Steps completed on first try: **{perfect_steps}**")
                st.markdown(f"- Total attempts across all steps: **{total_attempts}**")
                
                if st.button("Start Over", key="restart_problem"):
                    # Reset progress
                    st.session_state.step_index = 0
                    st.session_state.step_progress = []
                    for _ in range(len(predefined_steps)):
                        st.session_state.step_progress.append({"completed": False, "attempts": 0, "user_answer": ""})
                    st.rerun()
            else:
                # Display completed steps
                if current_index > 0:
                    with st.expander("✅ Completed Steps", expanded=False):
                        for i in range(current_index):
                            step = predefined_steps[i]
                            user_answer = st.session_state.step_progress[i]["user_answer"]
                            st.markdown(f"**Step {i+1}:** {step['instruction']}")
                            st.markdown(f"**Your answer:** {user_answer}")
                            st.markdown("---")
                
                # Display current step
                current_step = predefined_steps[current_index]
                st.markdown(f"### Step {current_index + 1} of {len(predefined_steps)}")
                
                # Create a clean card for the current step
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="margin-top: 0; color: #1e293b;">{current_step['instruction']}</h4>
                    <p style="color: #4a5568;"><strong style="color: #2563eb;">Format:</strong> {current_step.get('format', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show hint in expandable section
                with st.expander("Need a hint?"):
                    st.markdown(current_step.get('hint', ''))
                
                # Focused input for the current step
                with st.form(key=f"step_form_{current_index}", clear_on_submit=False):
                    user_input = st.text_input(
                        "Your answer:", 
                        placeholder=current_step.get('placeholder', ''),
                        key=f"step_input_{current_index}"
                    )
                    
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        submit_button = st.form_submit_button("Submit")
                    
                    with col2:
                        ask_button = st.form_submit_button("Ask a Question Instead")
                
                # Handle submission
                if submit_button and user_input:
                    # For original questions, use predefined valid answers
                    valid_answers = current_step.get('valid_answers', [])
                    is_correct = False
                    
                    # Normalize the input for comparison
                    normalized_input = user_input.strip().lower().replace(" ", "")
                    
                    # Check against all valid answer formats
                    for valid_answer in valid_answers:
                        normalized_valid = valid_answer.strip().lower().replace(" ", "")
                        if normalized_input == normalized_valid or normalized_valid in normalized_input:
                            is_correct = True
                            break
                    
                    feedback = current_step.get('hint', "Try checking your work and try again.")
                    
                    # Increment attempts
                    st.session_state.step_progress[current_index]["attempts"] += 1
                    
                    # Store user's answer
                    st.session_state.step_progress[current_index]["user_answer"] = user_input
                    
                    # Show feedback based on correctness
                    if is_correct:
                        # Mark step as completed
                        st.session_state.step_progress[current_index]["completed"] = True
                        
                        # Display success message
                        feedback_container.success(f"✅ Correct! Great job on step {current_index + 1}.")
                        
                        # Move to next step
                        st.session_state.step_index += 1
                        
                        # Rerun to refresh the page
                        time.sleep(1)  # Small delay for feedback to be visible
                        st.rerun()
                    else:
                        # Display error message with hint
                        feedback_container.error(f"❌ That's not quite right. {feedback}")
                
                # Handle question asking
                if ask_button and user_input and user_input.strip().endswith("?"):
                    feedback_container.info(f"Question received: '{user_input}'\n\nI'll help you with this specific question about step {current_index + 1}.")
                    
                    # Here we would typically call the assistant for help
                    assistant = st.session_state.assistant
                    
                    # Prepare a specific query for this step question
                    query = f"""
                    Question: {question}
                    Current step: "{current_step['instruction']}"
                    Student question: {user_input}
                    Help mode: {help_mode}
                    
                    Instructions:
                    1. Answer their specific question about this step.
                    2. Give helpful guidance without giving away the exact answer.
                    3. Focus only on this current step.
                    """
                    
                    # Show typing indicator
                    with st.spinner("Thinking about your question..."):
                        result = assistant.get_answer(query, help_mode)
                        
                        if result:
                            answer = result["answer"]
                            sources = result["sources"]
                            
                            if sources:
                                source_text = "\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in sources])
                                answer = answer + source_text
                        else:
                            answer = "I'm sorry, I couldn't generate guidance for that question."
                    
                    feedback_container.markdown(f"**Answer to your question:**\n\n{answer}")
    
    # Navigation button
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Change Help Mode", key="change_help"):
        # Reset chat when changing help mode
        st.session_state.chat_history = []
        st.session_state.step_index = 0
        st.session_state.step_progress = []
        # Explicitly clear help_mode
        st.session_state.help_mode = None
        navigate_to("question_detail", 
                  chapter=st.session_state.current_chapter,
                  section=st.session_state.current_section,
                  question=question_id)
    st.markdown("</div>", unsafe_allow_html=True)

# Update the main function to use the improved interface
def main():
    # Sidebar with admin access
    with st.sidebar:
        st.markdown("## Admin Panel")
        if st.button("Refresh PDF Database"):
            with st.spinner("🔄 Refreshing PDF database..."):
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
    elif current_view == "question_detail":
        if st.session_state.help_mode:
            # Show step-by-step or chat interface
            if st.session_state.help_mode == "Step-by-Step" and not st.session_state.get('use_regular_interface', False):
                render_improved_step_interface()
            else:
                render_chat_interface()
        else:
            # Show the four-button detail page
            render_question_detail()
    elif current_view == "similar_question":
        render_similar_question()
    else:
        render_home()

if __name__ == "__main__":
    run_frontend()
