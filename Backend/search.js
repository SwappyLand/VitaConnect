// Function to search for doctors
async function searchDoctors(searchTerm) {
  // 1. Your Setup
  const searchServiceName = "YOUR_SERVICE_NAME"; // e.g., vitaconnect-search
  const indexName = "YOUR_INDEX_NAME";           // e.g., azureblob-index
  const apiKey = "YOUR_API_KEY";                 // Paste from Step 2

  const url = `https://${searchServiceName}.search.windows.net/indexes/${indexName}/docs/search?api-version=2021-04-30-Preview`;

  // 2. The Search Logic
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-key": apiKey,
    },
    body: JSON.stringify({
      search: searchTerm,       // What the user typed (e.g., "Heart doctor")
      queryType: "simple",    // The "AI" part (understands intent)
      semanticConfiguration: "default", // Only if you set up semantic ranking
      top: 10,                  // How many results to return
    }),
  });

  const data = await response.json();
  return data.value; // This is the array of doctors!
}

// Usage Example:
// searchDoctors("skin rash specialist").then(doctors => console.log(doctors));