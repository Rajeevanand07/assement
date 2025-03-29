import google.generativeai as genai
import re

# Set up API key
API_KEY = "AIzaSyBoNbbZTVTv3n4NKdozLWRVovi8udw7lDA"
genai.configure(api_key=API_KEY)

def generate_mcqs(skill, num_questions=10):
    """Generate MCQs using Google's Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-flash")
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
    return response.text if response else "Failed to generate MCQs."

def parse_mcqs(mcq_text):
    """Parse generated MCQs into structured format."""
    questions = []
    answer_key = []
    mcq_pattern = re.findall(r"Q\d+\.\s(.+?)\nA\)\s(.+?)\nB\)\s(.+?)\nC\)\s(.+?)\nD\)\s(.+?)\nAnswer:\s([A-D])", mcq_text, re.DOTALL)
    
    for match in mcq_pattern:
        question, opt_a, opt_b, opt_c, opt_d, correct_answer = match
        questions.append({
            "question": question.strip(),
            "options": [opt_a.strip(), opt_b.strip(), opt_c.strip(), opt_d.strip()]
        })
        answer_key.append(correct_answer.strip())
    
    return questions, answer_key

def extract_subtopics(mistakes):
    """Extract weak subtopics based on incorrect answers."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    topics = ", ".join(set(mistakes))
    prompt = f"""
    A user struggled with the following questions:
    {topics}.
    Identify specific subtopics related to these questions.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "Failed to identify weak subtopics."

def generate_learning_topic(skill, weak_subtopics):
    """Generate a specific learning topic based on weaknesses."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    topics = ", ".join(set(weak_subtopics))
    prompt = f"""
    A user took a quiz on {skill} and struggled with the following subtopics: {topics}.
    Generate a structured learning topic with explanations, practical exercises, and useful resources.
    """
    response = model.generate_content(prompt)
    return response.text if response else "Failed to generate learning content."

def conduct_quiz(skill, num_questions=10):
    """Conducts a quiz and returns user score and weak subtopics."""
    mcq_text = generate_mcqs(skill, num_questions)
    questions, answer_key = parse_mcqs(mcq_text)
    
    if not questions:
        print("Failed to parse MCQs. Please try again.")
        return None, None
    
    score = 0
    mistakes = []
    
    for idx, mcq in enumerate(questions):
        print(f"\nQuestion {idx + 1}: {mcq['question']}")
        for i, option in enumerate(mcq["options"], start=1):
            print(f"{chr(64 + i)}) {option}")
        
        user_choice = input("Your answer (A/B/C/D): ").strip().upper()
        
        if user_choice in ["A", "B", "C", "D"]:
            if user_choice == answer_key[idx]:
                score += 1
            else:
                mistakes.append(mcq["question"])
        else:
            print("Invalid choice! Moving to the next question.")
    
    weak_subtopics = extract_subtopics(mistakes)
    return score, weak_subtopics

def adaptive_learning(skill):
    """Adaptive learning system that continues until user achieves a perfect score."""
    phase = 1
    while True:
        print(f"\n===== ASSESSMENT {phase} =====")
        score, weak_subtopics = conduct_quiz(skill, num_questions=5)
        
        if score == 5:
            print("\nCongratulations! You have mastered this skill.")
            break
        
        print(f"\nYour Score: {score}/5")
        print("\nWeak Topics:")
        print(weak_subtopics)
        
        print("\nGenerating new learning topic...")
        learning_content = generate_learning_topic(skill, weak_subtopics)
        print(f"\n--- RECOMMENDED LEARNING SECTION ---\n")
        print(learning_content)
        
        input("\nPress Enter to take the next assessment...")
        phase += 1
        if phase > 5:
            print("Maximum learning phases reached. Keep practicing!")
            break

# Run the adaptive learning system
skill = input("Enter a skill: ")
adaptive_learning(skill)