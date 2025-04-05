import os
import boto3
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# ✅ Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# ✅ Function to list all PDFs in S3 bucket
def list_pdfs_from_s3():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pdf")]
    except Exception as e:
        print(f"❌ Error listing PDFs: {e}")
        return []

# ✅ Function to download PDF from S3
def download_pdf_from_s3(pdf_key, download_path):
    try:
        s3_client.download_file(S3_BUCKET_NAME, pdf_key, download_path)
        print(f"✅ Downloaded: {pdf_key}")
        return download_path
    except Exception as e:
        print(f"❌ Error downloading {pdf_key}: {e}")
        return None

# ✅ Function to extract text from PDFs using LangChain
def extract_text_from_pdf(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        documents = text_splitter.split_documents(pages)
        return "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

# ✅ Main pipeline
def main():
    print("🚀 Starting pipeline execution...")
    
    # 1️⃣ Retrieve PDF list from S3
    pdf_files = list_pdfs_from_s3()
    if not pdf_files:
        print("❌ No PDFs found in S3.")
        return

    # 2️⃣ Process each PDF
    for pdf_key in pdf_files:
        local_pdf_path = f"./{pdf_key}"
        downloaded_pdf = download_pdf_from_s3(pdf_key, local_pdf_path)
        
        if downloaded_pdf:
            extracted_text = extract_text_from_pdf(downloaded_pdf)
            print(f"📄 Extracted Text from {pdf_key}:\n{extracted_text[:1000]}...")  # Print first 1000 chars
            
            # Optional: Save extracted text to a local file
            with open(f"{pdf_key}.txt", "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"✅ Saved extracted text to {pdf_key}.txt")

if __name__ == "__main__":
    main()
