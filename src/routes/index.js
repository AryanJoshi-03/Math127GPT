import { loadingEnv, insertAllPdfs } from "./helper.js";
import { runQuery } from "../backend/langchain.js";
import express from "express";
/* INITIALIZATION */
// Used to load Supabase client and OpenAI API
const { supa, chat, embeddings } = loadingEnv();

const app = express();
const port = process.env.PORT || 8080;

app.use(express.json());

app.post('/chat', async(req, res) => {
    try {
        const input = req.body.input;
		console.log(input);
        if (!input) {
            return res.status(400).json({ error: "Message is required"});
        }
        const result = await runQuery(input, chat, embeddings, supa);
		console.log(`result is ${result}`);
        res.status(200).json({ reply: result });
    }
    catch(error) {
        res.status(500).json({error: "Server Error"});
    }

});

app.listen(port, () => {
    console.log(`Server is running on Port:${port}`);
});