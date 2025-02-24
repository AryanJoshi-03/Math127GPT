import axios from "axios";
import { PdfReader } from "pdfreader";
import fs from "fs/promises";

export { extractLinks, extractTextFromPdf };

// Function to read pdflinks.txt
async function extractLinks(file) {
	try {
		const fileContent = await fs.readFile(file, "utf-8");
		const lines = fileContent
			.split("\n")
			.map((line) => line.trim())
			.filter((line) => line);
		return lines;
	} catch (error) {
		console.error("Error reading file:", error);
		throw error;
	}
}

// Function to fetch and parse PDF text
async function extractTextFromPdf(url) {
	try {
		// Fetch the PDF as a binary array
		const response = await axios.get(url, { responseType: "arraybuffer" });
		const pdfData = Buffer.from(response.data);

		let extractedText = "";

		// Initialize PdfReader
		const pdfReader = new PdfReader();

		// Use a Promise to handle the asynchronous parsing
		await new Promise((resolve, reject) => {
			pdfReader.parseBuffer(pdfData, (err, item) => {
				if (err) {
					reject("pdf: " + url + " - " + err);
				} else if (!item) {
					// End of the PDF
					resolve();
				} else if (item.text) {
					// Append text content
					extractedText += `${item.text} `;
				}
			});
		});

		return extractedText;
	} catch (error) {
		console.error("Error extracting text from PDF:", error);
	}
}
