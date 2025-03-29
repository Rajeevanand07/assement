from flask import Flask, request, jsonify
import google.generativeai as genai
import re
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow requests from React dev server

# Configure Gemini API
API_KEY = "AIzaSyBTtDz32piqrGLnWv0XhX-HuHwW7CskTFw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_mcqs(skill, num_questions=5):
    prompt = f"""
    Generate {num_questions} multiple-choice questions about {skill}. 
    Each question should have 4 options labeled (A, B, C, D) and one correct answer.
    Format:
    Q1. Question text?
    A) Option 1
    B) Option 2
    C) Option 3
    D) Option 4
    Answer: Correct option letter (A/B/C/D)
    """
    response = model.generate_content(prompt)
    return response.text if response else ""


def parse_mcqs(mcq_text):
    questions = []
    matches = re.findall(
        r"Q\d+\.\s(.+?)\nA\)\s(.+?)\nB\)\s(.+?)\nC\)\s(.+?)\nD\)\s(.+?)\nAnswer:\s([A-D])",
        mcq_text, re.DOTALL
    )
    for match in matches:
        q, a, b, c, d, ans = match
        questions.append({
            "question": q.strip(),
            "options": [a.strip(), b.strip(), c.strip(), d.strip()],
            "answer": ans.strip()
        })
    return questions


def extract_subtopics(mistakes):
    if not mistakes:
        return "None"
    
    combined = "\n".join([f"- {q}" for q in mistakes])
    prompt = f"""
    The following questions were answered incorrectly in a quiz:

    {combined}

    Based on the content and intent of these questions, identify the specific subtopics or concepts the user is weak in.
    Just list the core subtopics clearly, separated by commas. Avoid full sentences.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "N/A"


def generate_learning_topic(skill, weak_subtopics):
    topics = ", ".join(set(weak_subtopics))
    prompt = f"""
    A user took a quiz on {skill} and struggled with the following subtopics: {topics}.

    Create a structured learning module that includes:
    - Short explanations for each subtopic
    - 2–3 practical exercises or coding tasks
    - A list of at least 3 helpful resources (links to articles, tutorials, or videos)

    Format the response clearly using headings.
    """
    response = model.generate_content(prompt)
    return response.text if response else "N/A"


@app.route("/", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    skill = data.get("skill")

    mcq_text = generate_mcqs(skill)
    questions = parse_mcqs(mcq_text)
    answers = [q["answer"] for q in questions]
    questions_text = [q["question"] for q in questions]

    return jsonify({
        "skill": skill,
        "questions": questions,
        "answers": answers,
        "questions_text": questions_text
    })


@app.route("/submit", methods=["POST"])
def submit_answers():
    data = request.get_json()
    skill = data.get("skill")
    answers = data.get("answers")
    questions_text = data.get("questions_text")
    user_answers = data.get("user_answers")

    score = 0
    mistakes = []

    for i in range(5):
        user_ans = user_answers[i].strip().upper()
        correct_ans = answers[i].strip().upper()
        if user_ans == correct_ans:
            score += 1
        else:
            mistakes.append(questions_text[i])

    weak_topics = extract_subtopics(mistakes)
    learning_content = generate_learning_topic(skill, [weak_topics])

    return jsonify({
        "score": score,
        "weak_topics": weak_topics,
        "learning_content": learning_content
    })


if __name__ == "__main__":
    app.run(debug=True)
