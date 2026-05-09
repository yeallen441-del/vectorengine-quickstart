const response = await fetch("https://www.vectronode.com/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.VECTOR_ENGINE_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "user",
        content: "Hello from Vector Engine API"
      }
    ]
  })
});

const data = await response.json();
console.log(data);
