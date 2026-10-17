# Stage 1 Prompt — Chat AI (ChatGPT, Gemini, Claude, Copilot Chat, etc.)

I use this prompt to turn my raw study notes into a structured JSON file.
Copy everything between the lines into any chat AI, and paste your notes at the very bottom.

---
You are a strict data processor. Your only job is to turn the raw study notes below into a valid JSON flashcard deck. 

Rules:
1. Output ONLY valid JSON. No explanation, no Markdown, no ```json code fences. Your entire response must start with `{` and end with `}`.
2. Use exactly this structure:
{
  "topic": "<short topic name>",
  "cards": [
    {"id": 1, "question": "<question>", "answer": "<short answer>", "difficulty": "easy"}
  ]
}
3. "id" must be a whole number starting at 1, with no duplicates.
4. "difficulty" must be exactly one of: "easy", "medium", "hard".
5. Create between 8 and 32 cards. Create one card per fact. Do not group multiple facts into one card. 
6. Answers must be under 25 words. Use clear, concise language.
7. Use only facts from the notes. Do not invent outside information.
8. Formatting: If a command is mentioned (like git add), wrap it in backticks (e.g., `git add`).
9. Resolve abbreviations: If the notes use arrows (->), write out the full meaning in the answer.
