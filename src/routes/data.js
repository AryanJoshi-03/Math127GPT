import express from "express";
const { createClient } = require("@supabase/supabase-js");
const router = express.Router();

// Initialize Supabase client
const supabaseUrl = "__";
const supabaseKey =
	"__"; // or service key if needed
const supabase = createClient(supabaseUrl, supabaseKey);

// Endpoint to fetch limited data
router.get("/data", async (req, res) => {
	try {
		// Fetch data with limit and range
		const { data, error } = await supabase
			.from("your_table")
			.select("*")
			.limit(100) // Limit to 100 rows
			.range(0, 100); // Fetch rows from 0 to 100

		if (error) {
			throw error;
		}

		// Return the fetched data
		res.json(data);
	} catch (err) {
		console.error("Error fetching data:", err);
		res.status(500).json({ error: "Error fetching data" });
	}
});

module.exports = router;
