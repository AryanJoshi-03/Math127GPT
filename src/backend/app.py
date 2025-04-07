# src/backend/app.py
import os
import streamlit as st
from dotenv import load_dotenv
import boto3
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

class MathAssistant:
    def __init__(self):
        self.embeddings = self.initialize_openai()
        self.vector_store = self.load_or_create_vector_store()
    
    def initialize_openai(self):
        """Initialize OpenAI embeddings"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        if not OPENAI_API_KEY:
            print("❌ Missing OpenAI API key. Please check your .env file.")
            return None
        
        try:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            return embeddings
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI: {e}")
            return None

    def initialize_aws_s3(self):
        """Initialize AWS S3 client"""
        AWS_REGION = os.getenv("AWS_REGION")
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
        
        if not all([AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME]):
            print("❌ Missing one or more AWS environment variables.")
            return None, None
        
        try:
            s3_client = boto3.client(
                "s3",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            return s3_client, S3_BUCKET_NAME
        except Exception as e:
            print(f"❌ Failed to initialize AWS S3: {e}")
            return None, None

    def list_pdfs_from_s3(self, s3_client, bucket_name):
        """List all PDFs in S3 bucket"""
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pdf")]
        except Exception as e:
            print(f"❌ Error listing PDFs: {e}")
            return []

    def download_pdfs(self, s3_client, bucket_name):
        """Download PDFs from S3 bucket"""
        try:
            print("📥 Downloading PDFs from S3...")
            pdf_files = self.list_pdfs_from_s3(s3_client, bucket_name)
            
            if not pdf_files:
                print("⚠️ No PDFs found in S3 bucket!")
                return False
            
            # Create downloads directory if it doesn't exist
            os.makedirs("downloads", exist_ok=True)
            
            for pdf_key in pdf_files:
                local_path = os.path.join("downloads", pdf_key)
                # Create subdirectories if needed
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                s3_client.download_file(bucket_name, pdf_key, local_path)
                print(f"✅ Downloaded: {pdf_key}")
            
            return True
        except Exception as e:
            print(f"❌ Failed to download PDFs from S3: {str(e)}")
            return False

    def process_pdfs(self):
        """Process PDFs and create chunks"""
        docs = []
        
        try:
            print("📄 Processing PDFs...")
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                print("⚠️ Downloads directory not found!")
                return []

            for root, _, files in os.walk(downloads_dir):
                for file in files:
                    if file.endswith(".pdf"):
                        pdf_path = os.path.join(root, file)
                        loader = PyPDFLoader(pdf_path)
                        documents = loader.load()
                        
                        # Add source filename to metadata
                        for doc in documents:
                            doc.metadata["source"] = file
                        
                        docs.extend(documents)

            if not docs:
                print("⚠️ No PDFs processed!")
                return []
                
            # Split documents into smaller chunks for better retrieval
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            chunks = text_splitter.split_documents(docs)
            return chunks
        except Exception as e:
            print(f"❌ Failed to process PDFs: {str(e)}")
            return []

    def create_vector_store(self, chunks):
        """Create in-memory vector store"""
        try:
            print("🧠 Creating vector store...")
            if not chunks:
                print("⚠️ No document chunks to index!")
                return None
            
            # Create FAISS vector store from documents
            vector_store = FAISS.from_documents(chunks, self.embeddings)
            return vector_store
        except Exception as e:
            print(f"❌ Failed to create vector store: {str(e)}")
            return None

    def save_vector_store(self, vector_store, filename="pdf_vectorstore.faiss"):
        """Save vector store for future use"""
        if vector_store:
            try:
                vector_store.save_local(filename)
                print("✅ Vector store saved successfully!")
                return True
            except Exception as e:
                print(f"❌ Failed to save vector store: {str(e)}")
                return False
        return False

    def load_vector_store(self, filename="pdf_vectorstore.faiss"):
        """Load existing vector store if available"""
        try:
            if os.path.exists(filename):
                print("⏳ Loading existing vector store...")
                vector_store = FAISS.load_local(filename, self.embeddings)
                print("✅ Loaded existing vector store!")
                return vector_store
            return None
        except Exception as e:
            print(f"❌ Failed to load vector store: {str(e)}")
            return None

    def load_or_create_vector_store(self):
        """Try to load existing vector store or create a new one"""
        # First, attempt to load existing vector store
        vector_store = self.load_vector_store()
        
        if not vector_store:
            print("Creating a new vector store...")
            s3_client, bucket_name = self.initialize_aws_s3()
            if s3_client and bucket_name:
                if self.download_pdfs(s3_client, bucket_name):
                    chunks = self.process_pdfs()
                    vector_store = self.create_vector_store(chunks)
                    if vector_store:
                        self.save_vector_store(vector_store)
        
        return vector_store

    def get_answer(self, query, help_mode="General"):
        """Enhanced query method with context-aware prompting"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        try:
            if not self.vector_store:
                print("⚠️ No vector store found!")
                return None
            
            # Create a retriever from the vector store
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}  # Return top 3 most relevant chunks
            )
            
            # Enhanced prompts based on help mode
            if help_mode == "Conceptual Help":
                custom_prompt = """The student needs help understanding a concept.
                Explain the question's goal and core concept clearly.
                Break down the fundamental ideas in simple terms.
                Use analogies where helpful.
                Question: {query}
                """
            elif help_mode == "Application Help":
                custom_prompt = """The student understands the basic concept but needs help applying it.
                Explain how to connect the dots between theory and application.
                Provide a step-by-step approach to solve this type of problem.
                Identify key insights needed to make progress.
                Question: {query}
                """
            elif help_mode == "Step-by-Step":
                custom_prompt = """The student wants a detailed, step-by-step explanation.
                Break down the solution into precise, sequential steps.
                Explain the reasoning behind each step.
                Highlight important techniques and strategies.
                Question: {query}
                """
            else:
                custom_prompt = "Please provide a detailed and helpful answer to the following question: {query}"
            
            # Use more capable model for better answers
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY, 
                model_name="gpt-3.5-turbo",
                temperature=0.2  # Slightly more creative for explanations
            )
            
            # Create a QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",  # Simple method that passes all retrieved docs
                retriever=retriever,
                return_source_documents=True  # Return source documents for citations
            )
            
            print("🤔 Generating answer...")
            enhanced_query = custom_prompt.format(query=query)
            result = qa_chain({"query": enhanced_query})
            
            answer = result["result"]
            sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            unique_sources = list(set(sources))
            
            return {
                "answer": answer,
                "sources": unique_sources
            }
        except Exception as e:
            print(f"❌ Failed to get answer: {str(e)}")
            return None

# For testing the class when run directly
if __name__ == "__main__":
    assistant = MathAssistant()
    
    # Test query
    test_query = "What is the derivative of a polynomial function?"
    result = assistant.get_answer(test_query)
    
    if result:
        print("\n\n💡 Answer:", result["answer"])
        print("\n📚 Sources:", ", ".join(result["sources"]))
    else:
        print("❌ No answer generated.")