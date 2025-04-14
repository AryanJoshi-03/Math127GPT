import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Import the Streamlit frontend
from frontend.main import run_frontend

if __name__ == "__main__":
    print("🚀 Starting Math Assistant...")
    print("📚 Loading backend services...")
    # The backend initialization happens within the frontend
    print("🖥️ Launching frontend interface...")
    run_frontend()