import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory and its parent to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_dir)
sys.path.extend([project_dir, parent_dir])

# Import the Streamlit frontend
from frontend.updated_frontend import run_frontend

if __name__ == "__main__":
    print("🚀 Starting Math Assistant...")
    print("📚 Loading backend services...")
    # The backend initialization happens within the frontend
    print("🖥️ Launching frontend interface...")
    run_frontend()
