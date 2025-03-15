import dotenv from "dotenv";
import { loadingEnv, insertAllPdfs } from "./helper.js";

// Load environment variables
dotenv.config();

async function initializeSystem() {
    console.log("Initializing system...");

    // Initialize environment
    const { supa, embeddings } = loadingEnv();
    
    // Process PDFs for each assignment bucket
    // Replace these with your actual assignment bucket names
    const assignmentBuckets = ["All Math pdfs"];
    
    for (const bucket of assignmentBuckets) {
        console.log(`Processing PDFs for assignment ${bucket}...`);
        await insertAllPdfs(supa, embeddings, bucket);
    }
    
    console.log("Initialization complete!");
}

// Run the initialization
initializeSystem().catch(error => {
    console.error("Initialization failed:", error);
    process.exit(1);
});