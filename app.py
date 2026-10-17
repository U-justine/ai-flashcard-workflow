from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

# Load the flashcards
with open("data/flashcards.json", "r") as f:
    deck = json.load(f)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Flashcard Quiz</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { border: 2px solid #333; padding: 20px; border-radius: 8px; background: #f9f9f9; }
        input[type="text"] { width: 100%; padding: 10px; margin-top: 10px; box-sizing: border-box; }
        button { padding: 10px 20px; margin-top: 10px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 4px; }
        .correct { color: green; font-weight: bold; }
        .wrong { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>{{ topic }}</h1>
    
    {% if feedback %}
        <h2 class="{{ feedback_class }}">{{ feedback }}</h2>
    {% endif %}

    <div class="card">
        <h2>Question {{ index + 1 }}:</h2>
        <p>{{ card.question }}</p>
        
        {% if not feedback %}
            <form method="POST">
                <input type="text" name="user_answer" placeholder="Type your answer here..." required>
                <input type="hidden" name="card_index" value="{{ index }}">
                <button type="submit">Submit Answer</button>
            </form>
        {% else %}
            <p><strong>Correct Answer:</strong> {{ card.answer }}</p>
            <a href="/?index={{ next_index }}"><button>Next Question</button></a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    index = request.args.get("index", default=0, type=int)
    if index >= len(deck["cards"]):
        return "<h1>Quiz Complete!</h1><p>You have finished all cards.</p>"

    card = deck["cards"][index]
    feedback = None
    feedback_class = ""

    if request.method == "POST":
        user_answer = request.form.get("user_answer", "").strip().lower()
        correct_answer = card["answer"].lower()
        
        # Simple check: does the user's answer match a chunk of the correct answer?
        if user_answer in correct_answer or correct_answer in user_answer:
            feedback = "Correct!"
            feedback_class = "correct"
        else:
            feedback = "Incorrect."
            feedback_class = "wrong"

    return render_template_string(
        HTML, 
        topic=deck["topic"], 
        card=card, 
        index=index, 
        next_index=index + 1,
        feedback=feedback,
        feedback_class=feedback_class
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)