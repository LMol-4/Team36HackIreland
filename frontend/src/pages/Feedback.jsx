import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Send,
  MessageSquare,
  Lightbulb,
  AlertCircle,
  Target,
  ChevronRight,
  RefreshCw,
  Award,
  Brain,
  PlayCircle,
} from "lucide-react";

// Process the feedback into sections. Always return an array.
const processFeedback = (feedback) => {
  if (!feedback) return [];
  const lines = feedback.split("\n").filter((line) => line.trim() !== "");
  const sections = [];
  let currentSection = null;
  let currentItems = [];

  lines.forEach((line) => {
    // If the line ends with a colon, consider it a section title.
    if (line.endsWith(":")) {
      if (currentSection) {
        sections.push({ title: currentSection, items: currentItems });
      }
      currentSection = line.slice(0, -1);
      currentItems = [];
    } else {
      currentItems.push(line.trim());
    }
  });

  if (currentSection && currentItems.length > 0) {
    sections.push({ title: currentSection, items: currentItems });
  }
  return sections;
};

const Feedback = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [attentionScore, setAttentionScore] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [error, setError] = useState(null);

  const file = location.state?.file;

  useState(() => {
    if (!file) {
      navigate("/", { replace: true });
      return;
    }
  }, [file, navigate]);

  React.useEffect(() => {
    if (!file) {
      navigate("/", { replace: true });
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    fetch("http://127.0.0.1:5000/contact-score", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setAttentionScore(data.attention_score);
        setFeedback(data.feedback);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error processing video:", err);
        setError("Error processing video.");
        setLoading(false);
      });
  }, [file, navigate]);

  const handleGetQuestions = () => {
    setLoadingQuestions(true);
    const formData = new FormData();
    formData.append("video", file);

    fetch("http://127.0.0.1:5000/question_generation/generate-questions", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data.questions)) {
          setQuestions(
            data.questions.map((q) =>
              typeof q === "object" && q !== null && q.question ? q.question : q
            )
          );
        } else {
          console.error("Unexpected questions format:", data);
          setError("Unexpected questions format received.");
        }
        setLoadingQuestions(false);
      })
      .catch((err) => {
        console.error("Error generating questions:", err);
        setError("Error generating questions.");
        setLoadingQuestions(false);
      });
  };

  const handleAnswer = (questionText) => {
    navigate("/answer", { state: { question: questionText } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
      <motion.div className="fixed inset-0 overflow-hidden pointer-events-none">
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
        <motion.button
          onClick={() => navigate("/")}
          className="flex items-center gap-2 text-gray-600 hover:text-emerald-600 transition-colors mb-8 group"
          whileHover={{ x: -5 }}
        >
          <ArrowLeft size={20} className="group-hover:animate-pulse" />
          <span>Back to Upload</span>
        </motion.button>

        {loading ? (
          <motion.div
            className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex justify-center mb-4">
              <motion.div
                className="w-16 h-16"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                <RefreshCw size={64} className="text-emerald-500" />
              </motion.div>
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Processing Your Video
            </h2>
            <p className="text-gray-600">
              Analyzing your presentation to provide comprehensive feedback...
            </p>
          </motion.div>
        ) : error ? (
          <motion.div
            className="bg-red-50 rounded-2xl p-8 border border-red-100 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-2xl font-semibold text-red-900 mb-2">
              Error Processing Video
            </h2>
            <p className="text-red-600 mb-4">{error}</p>
            <motion.button
              onClick={() => navigate("/")}
              className="px-6 py-2 bg-red-600 text-white rounded-lg shadow hover:bg-red-700 transition"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Try Again
            </motion.button>
          </motion.div>
        ) : (
          <motion.div
            className="space-y-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {/* Score Card */}
            <motion.div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                    Presentation Analysis
                  </h2>
                  <p className="text-gray-600">
                    Detailed feedback on your pitch performance
                  </p>
                </div>
                <div className="flex items-center gap-3 bg-emerald-50 px-4 py-2 rounded-xl">
                  <Award className="text-emerald-500" size={24} />
                  <div className="text-right">
                    <p className="text-sm text-emerald-600 font-medium">
                      Score
                    </p>
                    <p className="text-2xl font-bold text-emerald-700">
                      {Number(attentionScore).toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <div className="flex items-start gap-4 bg-gradient-to-br from-white to-emerald-50/30 p-6 rounded-xl border border-emerald-100/20">
                  <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
                    <Brain className="text-emerald-600" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">
                      AI Feedback
                    </h3>
                    <p className="text-gray-600 leading-relaxed">{feedback}</p>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Questions Section */}
            <motion.div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                    Practice Questions
                  </h2>
                  <p className="text-gray-600">
                    Answer these questions to strengthen your pitch
                  </p>
                </div>
                <motion.button
                  onClick={handleGetQuestions}
                  className="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl shadow-lg shadow-emerald-100/30 hover:shadow-emerald-100/50 transition-shadow flex items-center gap-2"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  disabled={loadingQuestions}
                >
                  {loadingQuestions ? (
                    <>
                      <RefreshCw size={20} className="animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <Lightbulb size={20} />
                      <span>Generate Questions</span>
                    </>
                  )}
                </motion.button>
              </div>

              {questions.length > 0 && (
                <motion.div className="space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  {questions.map((questionText, index) => (
                    <motion.div
                      key={index}
                      className="group relative bg-gradient-to-br from-white to-emerald-50/30 p-6 rounded-xl border border-emerald-100/20 hover:border-emerald-200/50 shadow-sm hover:shadow-lg transition-all"
                      whileHover={{ y: -2 }}
                    >
                      <div className="flex items-start gap-4">
                        <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
                          <Target className="text-emerald-600" size={24} />
                        </div>
                        <p className="text-gray-800 flex-grow pt-2">{questionText}</p>
                        <motion.button
                          onClick={() => handleAnswer(questionText)}
                          className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg shadow hover:bg-emerald-700 transition"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <span>Answer</span>
                          <ChevronRight size={16} />
                        </motion.button>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </motion.div>

            {/* Action Button */}
            <motion.div className="flex justify-center">
              <motion.button
                onClick={() => navigate("/")}
                className="px-6 py-3 bg-white text-emerald-600 rounded-xl border border-emerald-200 shadow hover:shadow-lg transition-shadow flex items-center gap-2"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <PlayCircle size={20} />
                <span>Analyze Another Video</span>
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </main>
    </div>
  );
};

export default Feedback;
