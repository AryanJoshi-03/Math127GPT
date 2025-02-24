import path from "path";
import { createClient } from "@supabase/supabase-js";
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import dotenv from "dotenv";
dotenv.config(); // Load environment variables from .env file

import { getChunkEmbeds, insertData } from "../backend/supa.js";
import { extractLinks } from "../backend/pdfreader.js";

export { loadingEnv, insertAllPdfs };

// Function to load environment variables
function loadingEnv() {
	// Load environment variables using dotenv
	const SUPABASE_URL = process.env.SUPABASE_URL;
	const SUPABASE_API_KEY = process.env.SUPABASE_KEY;
	const openaikey = process.env.OPENAI_API_KEY;

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
			timeout: 60000, // Set timeout to 60 seconds (adjust as needed)
		},
	});

	// Create the Supabase client and OpenAI key
	return {
		supa: supabase,
		chat: openai,
		embeddings: embeddings,
	};
}

// Add all pdfs from .txt to database
async function insertAllPdfs(supa, embeddings, filename) {
	// Used to load every link from .txt into array
	// const links = path.resolve("./pdflinks.txt");
	const links = path.resolve(filename);
	let linksArr = await extractLinks(links);
	// Go through linksArr and add each link to db
	let lotsText = [];
	let lotsEmbed = [];
	let lotsLink = [];
	// let { currLink, currText, currEmbed };
	let counter = 0;

	for (const link of linksArr) {
		const resp = await getChunkEmbeds(embeddings, link);
		resp.lotsText.forEach((text) => lotsText.push(text));
		resp.lotsEmbeds.forEach((embed) => lotsEmbed.push(embed));
		resp.lotsLinks.forEach((link) => lotsLink.push(link));

		// Error handling
		if (lotsText.length != lotsEmbed.length) {
			throw error("text and embeds dont match");
		}
		if (lotsLink.length != lotsEmbed.length) {
			throw error("links and embeds dont match");
		}

		// Increment counter for debugging purposes
		counter = counter + 1;
		console.log("Saved link - " + counter + " / " + linksArr.length);
	}

	// Double checking my error handling
	if (lotsText.length != lotsEmbed.length) {
		throw error("text and embeds dont match");
	}
	if (lotsLink.length != lotsEmbed.length) {
		throw error("links and embeds dont match");
	}

	// Now proceed to uploading all chunks to DB
	console.log("Finished processing PDFs");
	for (let i = 0; i < lotsEmbed.length; i++) {
		await insertData(supa, lotsLink[i], lotsText[i], lotsEmbed[i]);
		console.log(
			"Chunk added to DB " + i + " / " + lotsEmbed.length + " : " + lotsLink[i],
		);
	}
	console.log("Uploading finished - " + lotsEmbed.length);
}
