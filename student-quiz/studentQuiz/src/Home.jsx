// src/components/Home.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles.css";

function Home() {
    const [skill, setSkill] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setIsLoading(true);
      try {
        const response = await fetch("/api/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ skill }),
        });
  
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
  
        const data = await response.json();
        navigate("/quiz", { state: data });
      } catch (error) {
        console.error("Error:", error);
        alert("Failed to generate quiz. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };
  
    if (isLoading) {
      return (
        <div className="loader-container">
          <div className="loader"></div>
          <p>Loading quiz questions...</p>
        </div>
      );
    }

  return (
    <div className="home">
        <div className="box_home" style={{height: "100px", width: "150px", backgroundColor: "#F3F3F3", zIndex: 1,position: "absolute", bottom: 0, right: "1%"}}>

        </div>
      <h2 className="sksp">Skill Sprint</h2>
      <form onSubmit={handleSubmit}>
        <h3>Enter a Skill to Begin</h3>
        <input
          type="text"
          placeholder="Enter skill"
          value={skill}
          onChange={(e) => setSkill(e.target.value)}
          required
        />
        <button type="submit">Start Quiz</button>
      </form>
      <iframe
      style={{position: "absolute", top: 0, left: 0,zIndex: -1,height: "100vh"}}
        src="https://my.spline.design/animatedshapeblend-f5847975823372ed13a6ac31aec13a26/"
        width="100%"
        height="100vh"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>
  );
}

export default Home;
