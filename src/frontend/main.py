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
        
    if 'problem_steps' not in st.session_state:
        st.session_state.problem_steps = []
        
    if 'step_progress' not in st.session_state:
        st.session_state.step_progress = []

    if 'use_regular_interface' not in st.session_state:
        st.session_state.use_regular_interface = False

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
        
        # Reset step-related variables
        st.session_state.step_index = 0
        st.session_state.problem_steps = []
    
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
    
    # Define predefined steps for specific questions
    if question_num == 1 and help_mode == "Step-by-Step":  # For question 1 (critical points question)
        predefined_steps = [
            "Find the derivative of f(x) = x^4 - 32x^2.",
            "Set the derivative equal to zero and solve for x.",
            "List all critical points in increasing order.",
            "For x = -4, classify whether it's a local maximum, local minimum, or neither.",
            "For x = 0, classify whether it's a local maximum, local minimum, or neither.",
            "For x = 4, classify whether it's a local maximum, local minimum, or neither."
        ]
        
        # Answers for validation (for question 1)
        step_answers = {
            0: ["4x^3 - 64x", "4x^3-64x", "4x³ - 64x", "4x³-64x"],  # Multiple valid formats for derivative
            1: ["4x^3 - 64x = 0", "4x(x^2 - 16) = 0", "4x(x - 4)(x + 4) = 0"],  # Setting derivative to zero
            2: ["-4, 0, 4"],  # Critical points in increasing order
            3: ["local minimum", "minimum", "local min"],  # Classification for x = -4
            4: ["local maximum", "maximum", "local max"],  # Classification for x = 0
            5: ["local minimum", "minimum", "local min"]   # Classification for x = 4
        }
        
        # Explanations for incorrect answers (for question 1)
        step_hints = {
            0: "When finding the derivative, remember to apply the power rule to each term. For x^4, the derivative is 4x^3, and for -32x^2, the derivative is -64x.",
            1: "To find critical points, set the derivative equal to zero and solve for x. Factor out common terms to make solving easier.",
            2: "Make sure you've found all values where the derivative equals zero, and list them in increasing order (from smallest to largest).",
            3: "To classify a critical point, look at the behavior of the function around that point. At x = -4, what happens to the function values as you approach from the left and from the right?",
            4: "At x = 0, examine what happens to the function values as x moves from negative to positive.",
            5: "Similar to the other points, at x = 4, determine what happens to the function values as you approach from the left and from the right."
        }
    else:
        # For other questions or modes, no predefined steps
        predefined_steps = []
        step_answers = {}
        step_hints = {}
    
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
                
        elif help_mode == "Step-by-Step":
            # For question 1 with predefined steps
            if question_num == 1 and len(predefined_steps) > 0:
                # Initialize with the first step
                st.session_state.step_index = 0
                
                # Store the predefined steps in session state for later use
                st.session_state.problem_steps = predefined_steps
                
                # Use the first predefined step as the initial message
                message = f"I'll guide you through solving this problem step by step. For each step, I'll ask you to provide your solution, and I'll check if you're on the right track.\n\n**Step 1:** {predefined_steps[0]}\n\nPlease provide your solution for this step."
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": message
                })
            else:
                # For other questions, use the dynamic approach
                auto_prompt = "Break down this problem into clear, sequential steps that I need to complete. For each step, explain what I need to do, but don't solve it for me. I'll provide my solution for each step, and you'll verify if I'm correct. Let's start with step 1."
                
                # Make sure step_index is set to 0 for starting
                st.session_state.step_index = 0
                
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
            
            # Different handling based on help mode and question
            if help_mode == "Step-by-Step" and question_num == 1 and len(predefined_steps) > 0:
                # For question 1 with predefined steps
                current_step = st.session_state.step_index
                
                # Check if the user's answer is a question
                is_question = user_input.strip().endswith("?")
                
                if is_question:
                    # Handle user questions by passing to the assistant
                    query = f"""
                    Question: {question}
                    User question: {user_input}
                    We are on step {current_step + 1}: {predefined_steps[current_step]}
                    
                    Please answer their question to help guide them through this step, but don't give them the exact answer.
                    """
                    
                    # Show typing indicator
                    message_placeholder = st.empty()
                    message_placeholder.markdown("<div class='bot-message'>Thinking...</div>", unsafe_allow_html=True)
                    
                    # Get answer from the assistant
                    result = assistant.get_answer(query, help_mode)
                    
                    if result:
                        answer = result["answer"]
                        sources = result["sources"]
                        
                        if sources:
                            source_text = "\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in sources])
                            answer = answer + source_text
                    else:
                        answer = "I'm sorry, I couldn't generate guidance for that question."
                    
                else:
                    # Check if the answer is correct for this step
                    valid_answers = step_answers.get(current_step, [])
                    is_correct = False
                    
                    # Normalize the input for comparison
                    normalized_input = user_input.strip().lower().replace(" ", "")
                    
                    # Check against all valid answer formats
                    for valid_answer in valid_answers:
                        normalized_valid = valid_answer.strip().lower().replace(" ", "")
                        if normalized_input == normalized_valid or normalized_valid in normalized_input:
                            is_correct = True
                            break
                    
                    if is_correct:
                        # Move to the next step if the answer is correct
                        st.session_state.step_index += 1
                        next_step = st.session_state.step_index
                        
                        if next_step < len(predefined_steps):
                            answer = f"Correct! Great job.\n\n**Step {next_step + 1}:** {predefined_steps[next_step]}\n\nPlease provide your solution for this step."
                        else:
                            answer = "Congratulations! You've successfully completed all steps of this problem. You've shown a good understanding of finding and classifying critical points."
                    else:
                        # Provide a hint if the answer is wrong
                        hint = step_hints.get(current_step, "Try checking your work and try again.")
                        answer = f"That's not quite right. {hint}\n\nLet's try again. **Step {current_step + 1}:** {predefined_steps[current_step]}"
            
            elif help_mode == "Step-by-Step":
                # For other questions using step-by-step mode, use the dynamic approach
                query = f"""
                Question: {question}
                Current step: {st.session_state.step_index}
                Student solution for current step: {user_input}
                Help mode: {help_mode}
                
                Instructions for Step-by-Step mode:
                1. Check if the student's solution for the current step is correct.
                2. If correct, praise them, then increment the step counter and present the next step to solve.
                3. If incorrect, kindly point out there's a mistake without giving away the answer, and ask them to try again.
                4. If they ask a question instead of providing a solution, answer their question to guide them, but don't solve the step for them.
                5. If they've completed all steps, congratulate them on solving the problem.
                """
                
                # Show typing indicator
                message_placeholder = st.empty()
                message_placeholder.markdown("<div class='bot-message'>Thinking...</div>", unsafe_allow_html=True)
                
                # Get answer from the assistant
                result = assistant.get_answer(query, help_mode)
                
                if result:
                    # Format the answer with sources
                    answer = result["answer"]
                    sources = result["sources"]
                    
                    # If this is a correct step in step-by-step mode, increment the step counter
                    if "correct" in answer.lower() and "next step" in answer.lower():
                        st.session_state.step_index += 1
                    
                    if sources:
                        source_text = "\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in sources])
                        answer = answer + source_text
                else:
                    answer = "I'm sorry, I couldn't generate an answer for that question."
            
            else:
                # Regular query format for Conceptual Help and Application Help modes
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
            
            # Add assistant message to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
            
            # Remove typing indicator and refresh
            if 'message_placeholder' in locals():
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

# === Improved Step-by-Step Interface ===
def render_improved_step_interface():
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
    
    # Define predefined steps with clear instructions and expected formats
    if question_num == 1 and help_mode == "Step-by-Step":  # For question 1 (critical points question)
        predefined_steps = [
            {
                "instruction": "Find the derivative of f(x) = x^4 - 32x^2.",
                "hint": "Apply the power rule to each term. Don't forget to multiply by the power and reduce the exponent by 1.",
                "format": "Enter your answer in the form: ax^n + bx^m + ...",
                "placeholder": "e.g., 3x^2 - 4x"
            },
            {
                "instruction": "Set the derivative equal to zero and factorize the equation.",
                "hint": "Factor out common terms to make solving easier.",
                "format": "You can write out the equation and your factoring steps.",
                "placeholder": "e.g., 3x(x-2) = 0"
            },
            {
                "instruction": "List all critical points in increasing order.",
                "hint": "Make sure to include all values where the derivative equals zero.",
                "format": "Enter the values separated by commas.",
                "placeholder": "e.g., -3, 0, 5"
            },
            {
                "instruction": "For x = -4, classify whether it's a local maximum, local minimum, or neither.",
                "hint": "Look at the behavior of the function around this point.",
                "format": "Enter only: local maximum, local minimum, or neither",
                "placeholder": "e.g., local minimum/ local maximum/ neither"
            },
            {
                "instruction": "For x = 0, classify whether it's a local maximum, local minimum, or neither.",
                "hint": "Examine what happens to the function values as x moves from negative to positive.",
                "format": "Enter only: local maximum, local minimum, or neither",
                "placeholder": "e.g., local minimum/ local maximum/ neither"
            },
            {
                "instruction": "For x = 4, classify whether it's a local maximum, local minimum, or neither.",
                "hint": "Determine what happens to the function values as you approach from the left and from the right.",
                "format": "Enter only: local maximum, local minimum, or neither",
                "placeholder": "e.g., local minimum/ local maximum/ neither"
            }
        ]
        
        # Answers for validation (for question 1)
        step_answers = {
            0: ["4x^3 - 64x", "4x^3-64x", "4x³ - 64x", "4x³-64x"],  # Multiple valid formats for derivative
            1: ["4x^3 - 64x = 0", "4x(x^2 - 16) = 0", "4x(x - 4)(x + 4) = 0", "4x(x^2 - 16)"],  # Setting derivative to zero
            2: ["-4, 0, 4", "-4,0,4", "x = -4, x = 0, x = 4"],  # Critical points in increasing order
            3: ["local minimum", "minimum", "local min"],  # Classification for x = -4
            4: ["local maximum", "maximum", "local max"],  # Classification for x = 0
            5: ["local minimum", "minimum", "local min"]   # Classification for x = 4
        }
        
        # Explanations for incorrect answers (for question 1)
        step_hints = {
            0: "When finding the derivative, remember to apply the power rule to each term. For x^4, the derivative is 4x^3, and for -32x^2, the derivative is -64x.",
            1: "To find critical points, set the derivative equal to zero and solve for x. Factor out common terms to make solving easier.",
            2: "Make sure you've found all values where the derivative equals zero, and list them in increasing order (from smallest to largest).",
            3: "To classify a critical point, look at the behavior of the function around that point. At x = -4, what happens to the function values as you approach from the left and from the right?",
            4: "At x = 0, examine what happens to the function values as x moves from negative to positive.",
            5: "Similar to the other points, at x = 4, determine what happens to the function values as you approach from the left and from the right."
        }
    elif question_num == 2 and help_mode == "Step-by-Step":  # For quadratic equation
        predefined_steps = [
            {
                "instruction": "Write the equation in standard form: ax² + bx + c = 0.",
                "hint": "Rearrange terms if needed.",
                "format": "Enter the equation in the standard form.",
                "placeholder": "e.g., 3x² - 5x + 2 = 0"
            },
            {
                "instruction": "Identify the values of a, b, and c.",
                "hint": "Look at the coefficients of x², x, and the constant term.",
                "format": "Enter as: a = _, b = _, c = _",
                "placeholder": "e.g., a = 3, b = -5, c = 2"
            },
            {
                "instruction": "Calculate the discriminant: b² - 4ac.",
                "hint": "Substitute the values and compute.",
                "format": "Enter the numerical value.",
                "placeholder": "e.g., 25 - 24 = 1"
            },
            {
                "instruction": "Use the quadratic formula: x = (-b ± √(b² - 4ac)) / (2a).",
                "hint": "Substitute the values and compute both solutions.",
                "format": "Enter your calculations and final solutions.",
                "placeholder": "e.g., x = (5 ± √1) / 6 = ..."
            },
            {
                "instruction": "Verify your solutions by substituting them back into the original equation.",
                "hint": "Substitute each solution and check if both sides are equal.",
                "format": "Show your verification steps.",
                "placeholder": "e.g., For x = 1: 3(1)² - 5(1) + 2 = 3 - 5 + 2 = 0 ✓"
            }
        ]
        
        # Add answers for question 2
        step_answers = {
            0: ["2x² - 8x + 7 = 0"],
            1: ["a = 2, b = -8, c = 7"],
            2: ["64 - 56 = 8", "8", "(-8)² - 4(2)(7) = 64 - 56 = 8"],
            3: ["x = (8 ± √8) / 4", "x = 2 ± √2 / 2", "x = 2 + √2 / 2 and x = 2 - √2 / 2", "x ≈ 3.41 and x ≈ 0.59"],
            4: ["verification steps"]  # This would be flexible in checking
        }
        
        step_hints = {
            0: "Make sure the equation is in the form ax² + bx + c = 0. The equation 2x² - 8x + 7 = 0 is already in this form.",
            1: "Look at the coefficients in 2x² - 8x + 7 = 0. The coefficient of x² is a, the coefficient of x is b, and the constant term is c.",
            2: "Substitute a = 2, b = -8, c = 7 into the discriminant formula b² - 4ac.",
            3: "Now use the quadratic formula x = (-b ± √(discriminant)) / (2a) with a = 2, b = -8, and your discriminant.",
            4: "Take each solution and substitute it back into 2x² - 8x + 7 = 0 to verify."
        }
    else:
        # For other questions or modes, no predefined steps
        predefined_steps = []
        step_answers = {}
        step_hints = {}
    
    # Initialize step_index if not in session state
    if 'step_index' not in st.session_state:
        st.session_state.step_index = 0
    
    # Initialize a container for showing feedback
    feedback_container = st.container()
    
    # Initialize progress tracking
    # Always ensure the step_progress list has the correct number of elements
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
                <p style="color: #4a5568;"><strong style="color: #2563eb;">Format:</strong> {current_step['format']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show hint in expandable section
            with st.expander("Need a hint?"):
                st.markdown(current_step['hint'])
            
            # Focused input for the current step
            with st.form(key=f"step_form_{current_index}", clear_on_submit=False):
                user_input = st.text_input(
                    "Your answer:", 
                    placeholder=current_step['placeholder'],
                    key=f"step_input_{current_index}"
                )
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    submit_button = st.form_submit_button("Submit")
                
                with col2:
                    ask_button = st.form_submit_button("Ask a Question Instead")
            
            # Handle submission
            if submit_button and user_input:
                # Check if the answer is correct
                valid_answers = step_answers.get(current_index, [])
                is_correct = False
                
                # Increment attempts
                st.session_state.step_progress[current_index]["attempts"] += 1
                
                # Store user's answer
                st.session_state.step_progress[current_index]["user_answer"] = user_input
                
                # Normalize the input for comparison
                normalized_input = user_input.strip().lower().replace(" ", "")
                
                # Special case for verification step which is more flexible
                if current_index == 4 and "verification" in valid_answers[0]:
                    # For verification steps, we're more lenient
                    if len(normalized_input) > 10:  # Just checking if they wrote something substantial
                        is_correct = True
                else:
                    # Check against all valid answer formats
                    for valid_answer in valid_answers:
                        normalized_valid = valid_answer.strip().lower().replace(" ", "")
                        if normalized_input == normalized_valid or normalized_valid in normalized_input:
                            is_correct = True
                            break
                
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
                    hint = step_hints.get(current_index, "Try checking your work and try again.")
                    feedback_container.error(f"❌ That's not quite right. {hint}")
            
            # Handle question asking
            if ask_button and user_input and user_input.strip().endswith("?"):
                # We'd invoke the AI assistant here for a specific question about this step
                # For now, let's just acknowledge the question
                feedback_container.info(f"Question received: '{user_input}'\n\nI'll help you with this specific question about step {current_index + 1}.")
                
                # Here we would typically call the assistant for help
                # This is a placeholder for where that would happen
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
                    # Get answer from the assistant (this would be the actual implementation)
                    # For now, let's just use a placeholder response
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
    else:
        # For questions without predefined steps, fall back to the existing chat interface
        st.warning("Step-by-step mode with focused inputs is only available for selected practice problems. For this problem, we'll use the regular chat interface instead.")
        
        # Here we would redirect to the regular chat interface
        # Maybe a button to switch to the regular interface
        if st.button("Continue with Regular Interface"):
            st.session_state.use_regular_interface = True
            st.rerun()
    
    # Navigation button
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("← Change Help Mode", key="change_help"):
        # Reset chat when changing help mode
        st.session_state.chat_history = []
        st.session_state.step_index = 0
        st.session_state.step_progress = []
        # Explicitly clear help_mode
        st.session_state.help_mode = None
        navigate_to("questions", 
                  chapter=st.session_state.current_chapter,
                  section=st.session_state.current_section,
                  question=question_num)
    st.markdown("</div>", unsafe_allow_html=True)

# Update the main function to use the improved interface
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
        # Check if we should use the improved interface or fall back to the regular one
        if st.session_state.help_mode == "Step-by-Step" and not st.session_state.get('use_regular_interface', False):
            render_improved_step_interface()
        else:
            render_chat_interface()
    else:
        render_home()

if __name__ == "__main__":
    run_frontend()