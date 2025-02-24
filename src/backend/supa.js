import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { extractTextFromPdf } from "./pdfreader.js";

// EXPORTS
export { selectData, insertData, getChunkEmbeds };

async function selectData(supabase, table) {
	const { data, error } = await supabase.from(table).select();

	if (error) {
		console.error("Error fetching data:", error);
	} else {
		console.log("Data:", data);
	}
}

async function insertData(supabase, title, content, embedding) {
	const { error } = await supabase
		.from("pdfEmbedding")
		.insert({ title: title, content: content, embedding: embedding });

	if (error) {
		console.error("Error inserting data:", error);
	} else {
		console.log("insertData worked successfully");
	}
}

// Semantic chunking with LangChain's RecursiveCharacterTextSplitter
async function semanticChunkText(text) {
	const splitter = new RecursiveCharacterTextSplitter({
		separator: ["\n\n", "\n", "Chapter", "Section", "---", "###", "."],
		chunkSize: 1000, // Max size per chunk in tokens
		chunkOverlap: 100, // Overlap to provide context between chunks
	});
	// Remove unnecessary whitespace, dots, etc.
	text = text.replace(/\.{3,}/g, " ");
	text = text.replace(/\s{2,}/g, " ");
	text = text.replace(/\s\d+\s/g, " ");
	const retVal = await splitter.splitText(text);
	return retVal;
}

async function getChunkEmbeds(embedding, link) {
	// await getPdfData(filepath).then((x) => storeDoc(x));
	const rawText = await extractTextFromPdf(link).catch((error) =>
		console.error("Error:", error),
	);

	const lotsEmbeds = [];
	const lotsText = [];
	const lotsLinks = [];

	// const myInput = doc.replace(/\n/g, " ");
	const chunks = await semanticChunkText(rawText); // Await here as well

	for (let chunk of chunks) {
		const currEmbed = await embedding.embedDocuments([chunk]);
		lotsEmbeds.push(currEmbed[0]);
		lotsText.push(chunk);
		lotsLinks.push(link);
	}
	return { lotsText, lotsEmbeds, lotsLinks };
}
