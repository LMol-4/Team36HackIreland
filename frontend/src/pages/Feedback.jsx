import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useLocation, useNavigate } from "react-router-dom";
import { PlayCircle } from "lucide-react";

const Feedback = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [attentionScore, setAttentionScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState(null);
  const [loadingQuestions, setLoadingQuestions] = useState(false);

  // Retrieve the uploaded file passed from the Home page
  const file = location.state?.file;

  useEffect(() => {
    if (!file) {
      // If no file exists in state, redirect back to Home
      navigate("/", { replace: true });
      return;
    }

    // Prepare form data with the video file for attention score calculation
    const formData = new FormData();
    formData.append("video", file);

    // POST request to calculate the attention score
    fetch("http://127.0.0.1:5000/contact-score", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setAttentionScore(data.attention_score);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error processing video:", err);
        setLoading(false);
      });
  }, [file, navigate]);

  const handleGetQuestions = () => {
    setLoadingQuestions(true);
    const formData = new FormData();
    formData.append("video", file);

    // POST request to your question-generation endpoint
    fetch("http://127.0.0.1:5000/question_generation/generate-questions", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setQuestions(data.questions);
        setLoadingQuestions(false);
      })
      .catch((err) => {
        console.error("Error generating questions:", err);
        setLoadingQuestions(false);
      });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
      {/* Background Decorative Elements */}
      <motion.div
        className="fixed inset-0 overflow-hidden pointer-events-none"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
      >
        <motion.div
          className="absolute -top-40 -right-40 w-96 h-96 bg-emerald-100/30 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.3, 0.4, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-1/2 -left-40 w-96 h-96 bg-cyan-100/30 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
        />
      </motion.div>

      <main className="relative max-w-4xl mx-auto px-6 pt-24 pb-20">
        {/* Feedback Content */}
        <motion.div
          className="flex flex-col items-center text-center mb-20"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <motion.h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700">
            Video Analysis Feedback
          </motion.h1>
          {loading ? (
            <motion.p className="text-lg text-gray-600">
              Processing your video, please wait...
            </motion.p>
          ) : (
            <motion.div>
              <motion.p className="text-xl text-gray-800 mb-4">
                Your Attention Score: <strong>{attentionScore}</strong>
              </motion.p>
              <motion.button
                onClick={() => navigate("/")}
                className="px-6 py-2 bg-emerald-600 text-white rounded-lg shadow hover:bg-emerald-700 transition mb-4"
              >
                Analyze Another Video
              </motion.button>
              <motion.button
                onClick={handleGetQuestions}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
              >
                {loadingQuestions ? "Loading Questions..." : "Get Questions"}
              </motion.button>
              {questions && (
                <motion.div className="mt-6 bg-white p-4 rounded-lg shadow max-w-xl">
                  <h2 className="text-2xl font-semibold mb-2">Generated Questions:</h2>
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {JSON.stringify(questions, null, 2)}
                  </pre>
                </motion.div>
              )}
            </motion.div>
          )}
        </motion.div>
      </main>
    </div>
  );
};

export default Feedback;
