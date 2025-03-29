import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import "./styles.css";

function Result() {
  const location = useLocation();
  const { score, weak_topics, learning_content } = location.state || {};
  const lines = learning_content?.split("\n") || [];

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="loader-wrapper">
        <div className="custom-loader"></div>
      </div>
    );
  }

  return (
    <div className="result-wrapper">
      <div className="result-grid">
        <section className="card score-card">
          <h2>Your Score</h2>
          <div className="score-value">{score}/5</div>
        </section>

        <section className="card weak-card">
          <h2>Weak Topics</h2>
          <div className="weak-list">
            {weak_topics.split(",").map((topic, index) => (
              <span key={index} className="weak-item">
                • {topic.trim()}
              </span>
            ))}
          </div>
        </section>
      </div>

      <section className="card learning-card">
        <h2>Recommended Learning</h2>
        <div className="learning-content">
          {lines.map((line, index) => {
            if (line.startsWith("##")) {
              return (
                <h3 key={index} className="section-heading">
                  {line.replace("##", "").trim()}
                </h3>
              );
            } else if (line.startsWith("- ")) {
              return (
                <ul key={index} className="learning-list">
                  <li>{line.slice(2)}</li>
                </ul>
              );
            } else {
              return (
                <p key={index} className="learning-paragraph">
                  {line}
                </p>
              );
            }
          })}
        </div>
      </section>

      <div className="button-wrapper">
        <Link to="/" className="quiz-button">
          Take Another Quiz
        </Link>
      </div>

      {/* Spline animation */}
      <iframe
        style={{
          position: "fixed",
          top: "10%",
          left: 0,
          zIndex: -1,
          height: "100vh",
        }}
        src="https://my.spline.design/animatedshapeblend-f5847975823372ed13a6ac31aec13a26/"
        width="100%"
        height="100vh"
        frameBorder="0"
        allowFullScreen
      ></iframe>
    </div>
  );
}

export default Result;
