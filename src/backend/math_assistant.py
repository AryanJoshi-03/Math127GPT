# backend/math_assistant.py
import os
import streamlit as st
from dotenv import load_dotenv
import boto3
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Import text extraction functions
from backend.extract_text import download_pdfs, process_pdfs

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
            st.error("❌ Missing OpenAI API key. Please check your .env file.")
            return None
        
        try:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            return embeddings
        except Exception as e:
            st.error(f"❌ Failed to initialize OpenAI: {e}")
            return None

    def initialize_aws_s3(self):
        """Initialize AWS S3 client"""
        AWS_REGION = os.getenv("AWS_REGION")
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
        
        if not all([AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME]):
            st.error("❌ Missing one or more AWS environment variables. Please check your .env file.")
            return None, None
        
        try:
            s3_client = boto3.client(
                "s3",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            return s3_client, AWS_BUCKET_NAME
        except Exception as e:
            st.error(f"❌ Failed to initialize AWS S3: {e}")
            return None, None

    def load_or_create_vector_store(self):
        """Try to load existing vector store or create a new one"""
        # First, attempt to load existing vector store
        vector_store = self.load_vector_store()
        
        if not vector_store:
            st.warning("Could not load existing vector store. Creating a new one...")
            s3_client, bucket_name = self.initialize_aws_s3()
            if s3_client and bucket_name:
                if download_pdfs(s3_client, bucket_name):
                    chunks = process_pdfs()
                    vector_store = self.create_vector_store(chunks)
                    if vector_store:
                        self.save_vector_store(vector_store)
        
        return vector_store

    def load_vector_store(self, filename="pdf_vectorstore.faiss"):
        try:
            if os.path.exists(filename):
                with st.spinner("⏳ Loading existing vector store..."):
                    vector_store = FAISS.load_local(
                        filename, 
                        self.embeddings,
                        allow_dangerous_deserialization=True  # Add this parameter
                    )
                    return vector_store
            else:
                return None
        except Exception as e:
            st.error(f"❌ Failed to load vector store: {str(e)}")
            return None

    def create_vector_store(self, chunks):
        """Create in-memory vector store"""
        try:
            with st.spinner("🧠 Creating vector store..."):
                if not chunks:
                    st.warning("⚠️ No document chunks to index!")
                    return None
                
                # Create FAISS vector store from documents
                vector_store = FAISS.from_documents(chunks, self.embeddings)
                return vector_store
        except Exception as e:
            st.error(f"❌ Failed to create vector store: {str(e)}")
            return None

    def save_vector_store(self, vector_store, filename="pdf_vectorstore.faiss"):
        """Save vector store for future use"""
        if vector_store:
            try:
                vector_store.save_local(filename)
                return True
            except Exception as e:
                st.error(f"❌ Failed to save vector store: {str(e)}")
                return False
        return False

    def get_answer(self, query, help_mode):
        """Enhanced query method with context-aware prompting"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        try:
            if not self.vector_store:
                st.warning("⚠️ No vector store found!")
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
            
            with st.spinner("🤔 Generating answer..."):
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
            st.error(f"❌ Failed to get answer: {str(e)}")
            return None