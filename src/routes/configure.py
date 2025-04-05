import os
import openai
from dotenv import load_dotenv
import boto3  # type: ignore
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

load_dotenv()

# Retrieve environment variables
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Correctly Initialize Supabase Client
supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Verify if all required environment variables are loaded
if not all([AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, 
            SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY]):
    raise ValueError("❌ Missing one or more environment variables. Please check your .env file.")

print("✅ Environment variables loaded successfully.")

# Initialize AWS S3 Client
try:
    s3_client = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    print("✅ AWS S3 client initialized.")
except Exception as e:
    print(f"❌ Failed to initialize AWS S3: {e}")

# Initialize OpenAI Embeddings
try:
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    print("✅ OpenAI Embeddings initialized.")
except Exception as e:
    print(f"❌ Failed to initialize OpenAI: {e}")

# Step 1: Retrieve PDFs from S3
def download_pdfs():
    try:
        print("📥 Retrieving PDF list from S3...")
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        
        if "Contents" not in response:
            print("⚠️ No PDFs found in S3 bucket!")
            return
        
        for obj in response.get("Contents", []):
            file_name = obj["Key"]
            s3_client.download_file(AWS_BUCKET_NAME, file_name, file_name)
            print(f"✅ Downloaded: {file_name}")

    except Exception as e:
        print("❌ Failed to download PDFs from S3:", e)

# Step 2: Process PDFs
def process_pdfs():
    docs = []
    print("📄 Processing downloaded PDFs...")

    try:
        for file in os.listdir():
            if file.endswith(".pdf"):
                print(f"🔍 Loading {file}...")
                loader = PyPDFLoader(file)
                docs.extend(loader.load())
                print(f"✅ Processed {file}, {len(docs)} pages added.")

        if not docs:
            print("⚠️ No PDFs processed!")
        return docs

    except Exception as e:
        print("❌ Failed to process PDFs:", e)
        return []

# Step 3: Store in Supabase Vector DB
def store_embeddings(docs):
    print("🗄️ Storing embeddings in Supabase Vector Store...")
    
    try:
        if not docs:
            print("⚠️ No documents to store!")
            return None
        
        # ✅ Correctly pass the Supabase client
        vector_store = SupabaseVectorStore.from_documents(
            documents=docs,  # Pass docs directly
            embedding=embeddings,  # Correct argument name
            client=supabase_client  # Pass Supabase client
        )
        print("✅ Embeddings stored successfully.")
        return vector_store

    except Exception as e:
        print("❌ Failed to store embeddings:", e)
        return None

# Step 4: Query Pipeline
def get_answer(query, vector_store):
    try:
        print("🔎 Retrieving answer...")
        if not vector_store:
            print("⚠️ No vector store found!")
            return None
        
        retriever = vector_store.as_retriever()
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
        qa_chain = RetrievalQA(llm=llm, retriever=retriever)
        
        print("📝 Querying LLM...")
        answer = qa_chain.run(query)
        print(f"✅ Answer retrieved: {answer}")
        return answer

    except Exception as e:
        print("❌ Failed to get answer:", e)
        return None

# Step 5: Main Pipeline Execution
def main():
    print("🚀 Starting pipeline execution...")

    download_pdfs()
    docs = process_pdfs()
    
    if not docs:
        print("❌ No documents processed. Exiting...")
        return
    
    vector_store = store_embeddings(docs)
    
    if not vector_store:
        print("❌ Vector store creation failed. Exiting...")
        return

    user_query = input("Enter your question: ")
    answer = get_answer(user_query, vector_store)

    if answer:
        print("💡 Answer:", answer)
    else:
        print("❌ No answer returned.")

# Run Script
if __name__ == "__main__":
    main()
