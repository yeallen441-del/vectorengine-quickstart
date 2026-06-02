import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTORNODE_API_KEY,
  baseURL: process.env.VECTORNODE_BASE_URL ?? "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: process.env.VECTORNODE_MODEL ?? "gpt-4o-mini",
  messages: [
    {
      role: "user",
      content: "Write one sentence about building with VectorNode.",
    },
  ],
});

console.log(response.choices[0].message.content);
