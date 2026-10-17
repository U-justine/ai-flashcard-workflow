# Stage 1 Prompt — Chat AI (ChatGPT, Gemini, Claude, Copilot Chat, etc.)

Copy everything between the lines into any chat AI. Then paste your notes at the bottom.

---
You are a study assistant. Turn the study notes below into flashcards.

Rules:
1. Output ONLY valid JSON. No explanation, no Markdown, no code fences.
2. Use exactly this structure:
{
  "topic": "<short topic name>",
  "cards": [
    {"id": 1, "question": "<question>", "answer": "<short answer>", "difficulty": "easy"}
  ]
}
3. "id" is a whole number, starting at 1, with no repeats.
4. "difficulty" must be one of: "easy", "medium", "hard".
5. Make 8 to 32 cards. One fact per card. Answers under 25 words.
6. Use only facts from the notes. Do not invent facts.

Save the reply as `data/flashcards.json`.
