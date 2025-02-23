import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, Send, MessageSquare, Lightbulb, AlertCircle, ThumbsUp, ArrowUpCircle, Star } from "lucide-react";

const FeedbackItem = ({ icon: Icon, content }) => (
  <div className="flex items-start gap-3 pl-4 mb-4">
    <div className="w-6 h-6 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0 mt-1">
      <Icon className="text-emerald-600" size={16} />
    </div>
    <p className="text-gray-700 leading-relaxed">{content}</p>
  </div>
);

const FeedbackSection = ({ title, items }) => (
  <div className="mb-8">
    <h3 className="text-xl font-semibold text-gray-800 border-b border-emerald-100 pb-2 mb-4">
      {title}
    </h3>
    <div className="space-y-3">
      {items.map((item, index) => {
        let Icon = AlertCircle;
        
        if (item.toLowerCase().includes("improve") || item.toLowerCase().includes("consider")) {
          Icon = ArrowUpCircle;
        } else if (item.toLowerCase().includes("strength") || item.toLowerCase().includes("good") || item.toLowerCase().includes("well done")) {
          Icon = Star;
        } else if (item.toLowerCase().includes("example") || item.toLowerCase().includes("instance")) {
          Icon = Lightbulb;
        }
        
        return <FeedbackItem key={index} icon={Icon} content={item} />;
      })}
    </div>
  </div>
);

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

    fetch("http://127.0.0.1:5000/answer-feedback/judge-responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        answer: answerText,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setEvaluationFeedback(data.feedback);
        setLoadingEvaluation(false);
      })
      .catch((err) => {
        console.error("Error evaluating response:", err);
        setError("Error evaluating your answer. Please try again.");
        setLoadingEvaluation(false);
      });
  };

  const processFeedback = (feedback) => {
    if (!feedback) return [];
    
    const lines = feedback.split("\n").filter(line => line.trim() !== "");
    const sections = [];
    let currentSection = null;
    let currentItems = [];
  
    lines.forEach(line => {
      if (line.endsWith(":")) {
        if (currentSection) {
          sections.push({
            title: currentSection,
            items: currentItems
          });
        }
        currentSection = line.slice(0, -1);
        currentItems = [];
      } else if (line.trim()) {
        currentItems.push(line.trim());
      }
    });
  
    if (currentSection && currentItems.length > 0) {
      sections.push({
        title: currentSection,
        items: currentItems
      });
    }
  
    return sections;
  };

  if (!question) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-red-100/20 shadow-xl text-center"
        >
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-lg text-gray-800">No question provided.</p>
          <motion.button
            onClick={() => navigate("/feedback")}
            className="mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg shadow hover:bg-emerald-700 transition flex items-center gap-2 mx-auto"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <ArrowLeft size={20} />
            <span>Go Back</span>
          </motion.button>
        </motion.div>
      </div>
    );
  }

  // Split the feedback text into paragraphs
  const feedbackParagraphs = evaluationFeedback
    ? evaluationFeedback.split("\n").filter((line) => line.trim() !== "")
    : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
      {/* Background Elements */}
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
        {/* Top Back Button */}
        <motion.button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-emerald-600 transition-colors mb-8 group"
          whileHover={{ x: -5 }}
        >
          <ArrowLeft size={20} className="group-hover:animate-pulse" />
          <span>Back to Questions</span>
        </motion.button>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          {/* Question Card */}
          <motion.div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
                <MessageSquare className="text-emerald-600" size={24} />
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">Practice Question</h2>
                <p className="text-lg text-gray-700">{question}</p>
              </div>
            </div>
          </motion.div>

          {/* Answer Section */}
          <motion.div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">Your Answer</h2>
              <motion.button
                onClick={handleSubmit}
                className="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl shadow-lg shadow-emerald-100/30 hover:shadow-emerald-100/50 transition-shadow flex items-center gap-2"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={loadingEvaluation}
              >
                {loadingEvaluation ? (
                  <>
                    <motion.div
                    >
                      <Send size={20} />
                    </motion.div>
                    <span>Evaluating...</span>
                  </>
                ) : (
                  <>
                    <Send size={20} />
                    <span>Submit Answer</span>
                  </>
                )}
              </motion.button>
            </div>

            <textarea
              className="w-full bg-white/50 border border-emerald-100 rounded-xl p-4 mb-4 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-shadow text-gray-700 placeholder-gray-400 min-h-[200px] resize-y"
              placeholder="Type your answer here..."
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
            />

            {error && (
              <motion.div 
                className="flex items-center gap-2 text-red-600 mb-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <AlertCircle size={20} />
                <p>{error}</p>
              </motion.div>
            )}
          </motion.div>

          {/* Feedback Section */}
          {evaluationFeedback && (
            <motion.div 
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-start gap-4 mb-8">
                <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
                  <Lightbulb className="text-emerald-600" size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-semibold text-gray-900">AI Feedback</h2>
                  <p className="text-gray-600">Comprehensive analysis of your response</p>
                </div>
              </div>

              <div className="space-y-2">
                {processFeedback(evaluationFeedback).map((section, index) => (
                  <FeedbackSection
                    key={index}
                    title={section.title}
                    items={section.items}
                  />
                ))}
              </div>

              <div className="mt-8 p-4 bg-emerald-50/50 rounded-xl border border-emerald-100/20">
                <div className="flex items-center gap-2 text-emerald-700 mb-2">
                  <MessageSquare size={16} />
                  <span className="font-medium">Pro Tip</span>
                </div>
                <p className="text-gray-600 text-sm">
                  Take note of the suggestions above and try incorporating them in your next response. 
                  Practice makes perfect!
                </p>
              </div>
            </motion.div>
          )}

          {/* Bottom Back Button */}
          <div className="flex justify-between">
            <motion.button
              onClick={() => navigate(-1)}
              className="px-6 py-3 bg-white text-emerald-600 rounded-xl border border-emerald-200 shadow hover:shadow-lg transition-shadow flex items-center gap-2"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <ArrowLeft size={20} />
              <span>Back to Questions</span>
            </motion.button>
            {evaluationFeedback && (
              <motion.button
                onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                className="px-6 py-3 bg-white text-emerald-600 rounded-xl border border-emerald-200 shadow hover:shadow-lg transition-shadow"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Back to Top
              </motion.button>
            )}
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default Answer;