import readline from 'readline';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import { createClient } from '@supabase/supabase-js';
import OpenAI from 'openai';
import { OpenAIEmbeddings } from '@langchain/openai';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import dotenv from 'dotenv';

dotenv.config();

const s3 = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function queryRAG(question) {
  try {
    console.log(`\n🔍 Searching for relevant context...\n`);

    const embeddings = new OpenAIEmbeddings({
        apiKey: process.env.OPENAI_API_KEY,  // Note 'apiKey' instead of 'openAIApiKey'
        modelName: "text-embedding-ada-002"   // Explicitly specify the model
      });    
    const vectorStore = new SupabaseVectorStore(supabase, embeddings.embedQuery.bind(embeddings), { tableName: 'vectors' });
    const results = await vectorStore.similaritySearch(question, 3); // Get top 3 relevant chunks

    if (results.length === 0) {
      console.log("⚠️ No relevant information found. Try rephrasing your question.");
      return;
    }

    const context = results.map(doc => doc.content).join('\n');
    console.log(`📖 Found Context:\n${context}\n`);

    const completion = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a helpful AI assistant.' },
        { role: 'user', content: question + '\nContext:\n' + context }
      ],
    });

    console.log(`🤖 AI Response:\n${completion.choices[0].message.content}\n`);
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question("❓ Enter your question: ", async (question) => {
  await queryRAG(question);
  rl.close();
});
