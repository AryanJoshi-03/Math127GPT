# backend/math_assistant.py
import math
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
            
            # The query from the frontend already contains all necessary instructions and context
            enhanced_query = query
            
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
                result = qa_chain({"query": enhanced_query})
            
            answer = result["result"]
            sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            unique_sources = list(set(sources))
            
            # Post-process the answer to ensure no direct solutions are given
            if "answer" in answer.lower() or "solution" in answer.lower():
                answer = "I can help guide you through this, but I won't provide the direct answer. Let me explain the concepts and steps instead."
            
            return {
                "answer": answer,
                "sources": unique_sources
            }
        except Exception as e:
            st.error(f"❌ Failed to get answer: {str(e)}")
            return None

    def generate_similar_question(self, original_question, question_type=None):
        """Generate a similar math question using LLM"""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        try:
            if not OPENAI_API_KEY:
                return "Could not generate similar question due to missing API key."
    
            # Enhanced prompt specifically for math problems
            prompt = """
            Generate a similar math problem to the following, but with different numbers, 
            variables, or slight variations in the scenario. The new problem should:
            1. Test the same mathematical concepts and skills
            2. Have approximately the same difficulty level
            3. Be clearly stated and unambiguous
            4. Have a different solution than the original
            5. Maintain the same mathematical structure and operations
            6. Keep the same question format and style
            7. If this is a {question_type} type question, maintain the same step structure
    
            Original Question: {question}
    
            New Similar Question:
            """
    
            # Use a direct call to OpenAI API
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY, 
                model_name="gpt-3.5-turbo",  # Consider gpt-4 if available
                temperature=0.7  # Good for creativity while maintaining structure
            )
    
            # Format the prompt with the original question and type
            formatted_prompt = prompt.format(
                question=original_question,
                question_type=question_type if question_type else "general"
            )
    
            # Get the response from the LLM
            response = llm.invoke(formatted_prompt)
    
            # Extract the generated question from the response
            similar_question = response.content.strip()
    
            # If the response is too long, trim it
            if len(similar_question) > 1000:
                similar_question = similar_question[:1000] + "..."
        
            return similar_question
    
        except Exception as e:
            st.error(f"❌ Failed to generate similar question: {str(e)}")
        
            # Enhanced fallback with better mathematical integrity
            try:
                import re
                import random
            
                # More sophisticated number replacement
                def replace_number(match):
                    num = float(match.group(0))
                    # Keep the same order of magnitude but change the value
                    magnitude = max(1, 10 ** int(math.log10(abs(num))) if num != 0 else 1)
                
                    # Generate a new number with the same general magnitude
                    if abs(num) < 1:
                        new_num = round(random.uniform(0.1, 0.9) * (1 if num > 0 else -1), 2)
                    else:
                        new_num = round(random.uniform(0.7, 1.3) * num, 2)
                    
                    # Make sure it's different from original
                    if new_num == num:
                        new_num = num + (0.1 * magnitude if num > 0 else -0.1 * magnitude)
                
                    # Return as integer if original was integer
                    if num.is_integer():
                        return str(int(new_num))
                    return str(new_num)
            
                # Replace numbers in the question
                modified_question = re.sub(r'-?\d+(\.\d+)?', replace_number, original_question)
            
                # Also replace variable names in some cases
                var_mapping = {'x': ['y', 'z', 't'], 'y': ['x', 'z', 'w'], 'f': ['g', 'h', 'F']}
                for old_var, new_vars in var_mapping.items():
                    if old_var in original_question:
                        modified_question = modified_question.replace(old_var, random.choice(new_vars))
            
                return modified_question
            
            except Exception as nested_e:
                # Ultimate fallback if everything else fails
                return f"Unable to generate a similar question. Please try again. Error: {str(nested_e)}"
