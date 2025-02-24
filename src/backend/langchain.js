export { runQuery };

async function runQuery(query, chat, embeddings, supabase) {
	// Create vector embedding for the query
	const queryEmbed = await embeddings.embedQuery(query);

	// Find the closest vector in the Supabase
	const { data, error } = await supabase.rpc("find_closest_embedding", {
		query_embedding: queryEmbed,
	});

	if (error) {
		console.error("Error fetching closest vector:", error);
		return null;
	}

	// Now using info from the closest vector, we can pass it into ChatGPT to get response
	let vectorData = data[0].content;
	let dataLink = data[0].title;
	const prompt = `Here is background information from which the question will be asked: ${vectorData}.\n Also add this link to the end of the answer: ${dataLink}. \n Please now answer the following question using only this data: ${query}`;
	// Pass prompt to OpenAI and print out
	const gptResp = await chat.invoke(prompt);
	const response = gptResp.content;
	console.log("ChatGPT: " + response);
	return response;
}
