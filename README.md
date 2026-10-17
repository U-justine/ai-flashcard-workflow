# AI Flashcard Workflow: Chat AI → CLI/IDE AI

**By Justine Umutoni**
<<<<<<< HEAD
**Course:** Applied AI & Prompt Engineering

=======

**Course:** Applied AI & Prompt Engineering

>>>>>>> 5ca483f156fbca65276cd67b2bde5bcf43c3a212
## 1. The Problem I Solved
Making flashcards by hand from my lecture notes was taking too much time, and building a custom tool to study them was even slower. I realized this task splits perfectly into two stages: understanding text (which Chat AI is great at) and writing code inside a project (which CLI/IDE AI is great at). 

I built a workflow that takes raw, messy text and turns it into a working terminal quiz app using two different AI UX types.

## 2. The Architecture (How it Works)
My workflow chains two different AI tools together, with a safety gate in the middle:

| Stage | UX Type | Input | Output |
|-------|---------|-------|--------|
| 1 | **Chat** (Claude, ChatGPT, etc.) | Raw notes (`data/sample_notes.txt`) | `data/flashcards.json` |
| Gate | Plain Python (no AI) | `flashcards.json` | PASS or a list of errors |
| 2 | **CLI or IDE** (Copilot, Claude Code, etc.) | `flashcards.json` | `quiz.py` + automated tests |

**The Workflow Diagram:**

```mermaid
flowchart LR
    A[Raw study notes] --> B[Stage 1: Chat AI<br/>prompts/stage1_chat_prompt.md]
    B --> C[data/flashcards.json]
    C --> D{Gate: validate.py}
    D -- FAIL: errors --> B
    D -- PASS --> E[Stage 2: CLI or IDE AI<br/>prompts/stage2_cli_prompt.md]
    E --> F[quiz.py + tests/]
    F --> G{Tests pass?}
    G -- No --> E
<<<<<<< HEAD
    G -- Yes --> H[run_workflow.sh<br/>Interactive quiz]
=======
    G -- Yes --> H[run_workflow.sh<br/>Interactive quiz]
>>>>>>> 5ca483f156fbca65276cd67b2bde5bcf43c3a212
