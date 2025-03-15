import { createClient } from "@supabase/supabase-js";
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import dotenv from "dotenv";
import { getChunkEmbeds, insertData } from "./src/backend/supa.js";

dotenv.config(); // Load environment variables from .env file

export { loadingEnv, insertAllPdfs };

// Function to load environment variables and initialize clients
function loadingEnv() {
    // Load environment variables
    const SUPABASE_URL = process.env.SUPABASE_URL;
    const SUPABASE_API_KEY = process.env.SUPABASE_KEY;
    const openaikey = process.env.OPENAI_API_KEY;

    if (!SUPABASE_URL || !SUPABASE_API_KEY || !openaikey) {
        throw new Error("Missing required environment variables");
    }

    // Chat client
    const openai = new ChatOpenAI({
        apiKey: openaikey,
        model: "gpt-3.5-turbo",
        temperature: 0.3,
    });

    // Embedding client
    const embeddings = new OpenAIEmbeddings({
        apiKey: openaikey,
        model: "text-embedding-ada-002",
    });

    // Supabase client with custom timeout setting
    const supabase = createClient(SUPABASE_URL, SUPABASE_API_KEY, {
        db: {
            timeout: 60000, // Set timeout to 60 seconds
        },
    });

    return {
        supa: supabase,
        chat: openai,
        embeddings: embeddings,
    };
}

// Function to process all PDFs in a specific Supabase bucket
async function insertAllPdfs(supa, embeddings, bucketName) {
    try {
        // List all files in the specified bucket
        const { data: files, error } = await supa.storage.from(bucketName).list();
        
        if (error) {
            console.error(`Error listing files in bucket ${bucketName}:`, error);
            return;
        }
        
        console.log(`Found ${files.length} files in bucket ${bucketName}`);
        
        // Process each PDF in the bucket
        let counter = 0;
        for (const file of files) {
            if (!file.name.toLowerCase().endsWith('.pdf')) {
                console.log(`Skipping non-PDF file: ${file.name}`);
                continue;
            }
            
            // Get chunks and embeddings
            const resp = await getChunkEmbeds(embeddings, supa, bucketName, file.name);
            if (!resp) {
                console.error(`Failed to process PDF: ${file.name}`);
                continue;
            }
            
            // Store each chunk in the database
            for (let i = 0; i < resp.lotsText.length; i++) {
                await insertData(
                    supa, 
                    bucketName,
                    file.name, 
                    file.name.replace('.pdf', ''), // Use filename as title
                    resp.lotsText[i],
                    resp.lotsEmbeds[i]
                );
                console.log(`Stored chunk ${i+1}/${resp.lotsText.length} from ${file.name}`);
            }
            
            counter++;
            console.log(`Processed file ${counter}/${files.length}: ${file.name}`);
        }
        
        console.log(`Completed processing all PDFs in bucket ${bucketName}`);
    } catch (error) {
        console.error("Error in insertAllPdfs:", error);
    }
}