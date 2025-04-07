# src/routes/extract_text.py
import os
import boto3
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def list_pdfs_from_s3():
    """List all PDFs in S3 bucket"""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pdf")]
    except Exception as e:
        print(f"❌ Error listing PDFs: {e}")
        return []

def download_pdf_from_s3(pdf_key, download_path):
    """Download a specific PDF from S3"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        
        s3_client.download_file(S3_BUCKET_NAME, pdf_key, download_path)
        print(f"✅ Downloaded: {pdf_key}")
        return download_path
    except Exception as e:
        print(f"❌ Error downloading {pdf_key}: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using LangChain"""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        documents = text_splitter.split_documents(pages)
        return documents, "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return [], ""

def process_all_pdfs():
    """Process all PDFs from S3 bucket"""
    print("🚀 Starting PDF processing...")
    
    # Retrieve PDF list from S3
    pdf_files = list_pdfs_from_s3()
    if not pdf_files:
        print("❌ No PDFs found in S3.")
        return {}
    
    # Create results directory
    os.makedirs("downloads", exist_ok=True)
    
    # Process each PDF
    results = {}
    for pdf_key in pdf_files:
        local_pdf_path = os.path.join("downloads", pdf_key)
        downloaded_pdf = download_pdf_from_s3(pdf_key, local_pdf_path)
        
        if downloaded_pdf:
            documents, extracted_text = extract_text_from_pdf(downloaded_pdf)
            print(f"📄 Extracted text from {pdf_key}")
            
            # Save extracted text to a local file
            text_path = f"{local_pdf_path}.txt"
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            
            # Store results
            results[pdf_key] = {
                "path": local_pdf_path,
                "text_path": text_path,
                "document_count": len(documents)
            }
    
    print(f"✅ Processing completed for {len(results)} PDFs")
    return results

# For direct execution
if __name__ == "__main__":
    results = process_all_pdfs()
    print(f"Processed {len(results)} PDFs:")
    for pdf, info in results.items():
        print(f" - {pdf}: {info['document_count']} chunks")