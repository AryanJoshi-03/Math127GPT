# Math127 Assistant

An AI-powered educational assistant developed under the guidance of Professor Maria Nikolaou as part of an independent study at UMass Amherst. This system provides personalized help for students in Mathematics 127, serving approximately 2000 students per semester. Using advanced language models and retrieval-augmented generation, the Math127 Assistant can explain concepts, guide students through problem-solving, and offer step-by-step solutions - all while maintaining a pedagogical approach that emphasizes learning rather than simply providing answers. The project has garnered significant interest, and we are currently in talks with the Computer Science department at UMass Amherst to expand this collaboration between the Mathematics and Computer Science departments.

## ✨ Features

- **Smart Navigation**: Browse through course chapters, sections, and specific problem sets
- **Multiple Learning Modes**:
  - **Conceptual Help**: Explains core concepts and theory
  - **Application Help**: Bridges theory and practical application
  - **Step-by-Step Guidance**: Interactive, progressive problem-solving assistance
- **AI-Powered Assistance**: Context-aware responses based on course materials
- **PDF Knowledge Base**: Automatically processes and indexes course textbooks and materials
- **Progressive Learning**: Hints and guidance instead of direct answers
- **Interactive Learning Interface**: Clean, intuitive UI designed for students

## 🏗️ Architecture & Technologies

### Frontend
- **Streamlit**: Interactive web interface with dynamic components
- **Custom CSS**: Polished, responsive design with card-based navigation

### Backend
- **OpenAI GPT Models**: Powers the AI tutoring capabilities
- **LangChain**: Framework for building context-aware AI applications
- **FAISS Vector Store**: Efficient similarity search for retrieving relevant content
- **AWS S3**: Cloud storage for course materials (PDF documents)
- **PyPDF Loader**: PDF processing and text extraction

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- AWS Account with S3 access
- OpenAI API key

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/math127-assistant.git
cd math127-assistant
```

### Step 2: Set up environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name
```

### Step 4: Add course materials
Upload your course PDFs to the configured S3 bucket. The system will automatically download and process these documents when initialized.

### Step 5: Run the application
```bash
python app.py
```

## 📊 Usage

1. **Browse Content**: Navigate through chapters and sections of Math 127
2. **Select a Question**: Choose from available practice problems
3. **Select Help Mode**:
   - "I'm completely lost and don't know where to start"
   - "I know the concept but am not sure how to apply it"
   - "I need step-by-step guidance"
4. **Interactive Learning**: Engage with the assistant to solve problems, receive hints, and deepen your understanding

## 🖥️ Project Structure

```
math127-assistant/
├── app.py                  # Application entry point
├── frontend/
│   └── main.py             # Streamlit UI implementation
├── backend/
│   ├── math_assistant.py   # Core assistant logic
│   └── extract_text.py     # PDF processing utilities
├── downloads/              # Temporary storage for downloaded PDFs
└── pdf_vectorstore.faiss   # FAISS index of processed documents
```

## 🔧 Key Components

### MathAssistant Class
The core of the system, handling:
- Vector embeddings of course materials
- Context-aware query processing
- Customized response generation based on help mode

### PDF Processing Pipeline
- Downloads course materials from S3
- Extracts and chunks text content
- Creates searchable vector embeddings
- Persists indexed content for quick startup

### Interactive UI
- Navigation breadcrumbs for easy orientation
- Card-based interface for intuitive interaction
- Responsive chat interface for Q&A
- Specialized step-by-step problem-solving interface

## 🧠 Pedagogical Approach

The Math127 Assistant is designed with educational principles in mind:
- Focuses on guiding students to discover solutions, not simply providing answers
- Offers multiple levels of assistance depending on student needs
- Provides contextual explanations that connect to course materials
- Ensures feedback is constructive and encourages deeper understanding
