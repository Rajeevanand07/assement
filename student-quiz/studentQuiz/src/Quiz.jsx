// src/components/Quiz.jsx
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./styles.css";

function Quiz() {
  const location = useLocation();
  const navigate = useNavigate();

  const { skill, questions, answers, questions_text } = location.state || {};

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData(e.target);
      const userAnswers = [];

      for (let i = 0; i < 5; i++) {
        userAnswers.push(formData.get(`q${i}`));
      }

      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          skill,
          answers,
          questions_text,
          user_answers: userAnswers,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      navigate("/result", { state: result });
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to submit quiz. Please try again.');
    }
  };

  return (
    <div className="quiz-container">
      <h2>Quiz on: {skill}</h2>
      <form onSubmit={handleSubmit}>
        {questions.map((q, qid) => (
          <div className="question" key={qid}>
            <p>
              Q{qid + 1}. {q.question}
            </p>
            {q.options.map((option, index) => (
              <label key={index}>
                <input
                  type="radio"
                  name={`q${qid}`}
                  value={["A", "B", "C", "D"][index]}
                  required
                />
                {["A", "B", "C", "D"][index]}) {option}
              </label>
            ))}
          </div>
        ))}
        <button type="submit">Submit Answers</button>
      </form>
    </div>
  );
}

export default Quiz;
