import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: process.env.VECTOR_ENGINE_MODEL ?? "gpt-4o-mini",
  messages: [
    {
      role: "user",
      content: "Write one sentence about building with Vector Engine API.",
    },
  ],
});

console.log(response.choices[0].message.content);
