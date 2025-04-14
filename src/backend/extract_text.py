# backend/extract_text.py
import os
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# AWS S3 Configuration
def get_aws_credentials():
    """Get AWS credentials from environment variables"""
    return {
        "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.getenv("AWS_REGION"),
        "s3_bucket_name": os.getenv("AWS_BUCKET_NAME")
    }

def initialize_s3_client():
    """Initialize and verify S3 client connection"""
    creds = get_aws_credentials()
    
    if not all([creds["aws_access_key"], creds["aws_secret_key"], creds["aws_region"], creds["s3_bucket_name"]]):
        print("❌ Missing AWS credentials. Check your .env file")
        return None
        
    try:
        s3_client = boto3.client(
            "s3",
            region_name=creds["aws_region"],
            aws_access_key_id=creds["aws_access_key"],
            aws_secret_access_key=creds["aws_secret_key"]
        )
        # Test connection
        s3_client.list_buckets()
        return s3_client
    except Exception as e:
        print(f"❌ AWS S3 connection error: {e}")
        return None

def list_pdfs_from_s3(s3_client, bucket_name):
    """List all PDFs in S3 bucket"""
    if not s3_client:
        return []
        
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in response:
            print(f"⚠️ No objects found in bucket: {bucket_name}")
            return []
            
        return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pdf")]
    except Exception as e:
        print(f"❌ Error listing PDFs: {e}")
        return []

def download_pdfs(s3_client, bucket_name):
    """Download PDFs from S3 bucket"""
    try:
        with st.spinner("📥 Downloading PDFs from S3..."):
            pdf_files = list_pdfs_from_s3(s3_client, bucket_name)
            
            if not pdf_files:
                st.warning("⚠️ No PDFs found in S3 bucket!")
                return False
            
            # Create downloads directory if it doesn't exist
            os.makedirs("downloads", exist_ok=True)
            
            for file_name in pdf_files:
                local_path = os.path.join("downloads", os.path.basename(file_name))
                s3_client.download_file(bucket_name, file_name, local_path)
        
        return True
    except Exception as e:
        st.error(f"❌ Failed to download PDFs from S3: {str(e)}")
        return False

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using LangChain"""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Add source metadata
        for page in pages:
            page.metadata["source"] = os.path.basename(pdf_path)
        
        return pages
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return []

def process_pdfs():
    """Process all downloaded PDFs and split into chunks"""
    docs = []
    
    try:
        with st.spinner("📄 Processing PDFs..."):
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                st.warning("⚠️ Downloads directory not found!")
                return []

            for file in os.listdir(downloads_dir):
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(downloads_dir, file)
                    documents = extract_text_from_pdf(pdf_path)
                    docs.extend(documents)

            if not docs:
                st.warning("⚠️ No PDFs processed!")
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
        st.error(f"❌ Failed to process PDFs: {str(e)}")
        return []

if __name__ == "__main__":
    # Test functionality
    s3_client = initialize_s3_client()
    bucket_name = get_aws_credentials()["s3_bucket_name"]
    
    if s3_client and bucket_name:
        download_pdfs(s3_client, bucket_name)
        chunks = process_pdfs()
        print(f"Processed {len(chunks)} chunks from PDFs")