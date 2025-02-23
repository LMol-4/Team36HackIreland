import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Answer = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { question } = location.state || {};
  const [answerText, setAnswerText] = useState("");
  const [evaluationFeedback, setEvaluationFeedback] = useState("");
  const [loadingEvaluation, setLoadingEvaluation] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = () => {
    if (!answerText.trim()) {
      setError("Please type an answer before submitting.");
      return;
    }
    setError(null);
    setLoadingEvaluation(true);
    // POST request to the evaluation endpoint
    fetch("http://127.0.0.1:5000/evaluation/judge-responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        questions: [question],
        answers: [answerText],
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        // Expecting data.feedback
        setEvaluationFeedback(data.feedback);
        setLoadingEvaluation(false);
      })
      .catch((err) => {
        console.error("Error evaluating response:", err);
        setError("Error evaluating your answer. Please try again.");
        setLoadingEvaluation(false);
      });
  };

  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>No question provided.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">Answer the Question</h1>
      <div className="max-w-2xl w-full bg-white shadow rounded-lg p-6">
        <p className="text-xl font-semibold mb-4">
          <strong>Question:</strong> {question}
        </p>
        <textarea
          className="w-full border rounded p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="8"
          placeholder="Type your answer here..."
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
        ></textarea>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <button
          onClick={handleSubmit}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition mb-4"
          disabled={loadingEvaluation}
        >
          {loadingEvaluation ? "Evaluating..." : "Submit Answer"}
        </button>
        {evaluationFeedback && (
          <div className="mt-6 p-4 border rounded bg-green-50">
            <h2 className="text-2xl font-semibold mb-2">Evaluator Feedback:</h2>
            <p className="text-lg">{evaluationFeedback}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Answer;
