import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Upload, FileText, HelpCircle, Hand, Sparkles, PlayCircle, Zap } from "lucide-react";

const Home = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setUploadedFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "video/*": [] // Accept any video file
    },
    maxSize: 1 * 1024 * 1024 * 1024,
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: "easeOut",
      },
    },
  };

  const featureCardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut",
      },
    },
    hover: {
      y: -5,
      transition: {
        duration: 0.2,
        ease: "easeInOut",
      },
    },
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
            ease: "easeInOut"
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
            delay: 1
          }}
        />
      </motion.div>

      <main className="relative max-w-6xl mx-auto px-6 pt-24 pb-20">
        {/* Hero Section */}
        <motion.div 
          className="flex flex-col items-center text-center mb-20"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div 
            className="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full border-2 border-emerald-100 text-emerald-800 mb-6 hover:border-emerald-200 transition-colors"
            variants={itemVariants}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Sparkles size={16} className="text-emerald-600" />
            <span className="text-sm font-medium">AI-Powered Pitch Analysis</span>
          </motion.div>
          
          <div className="max-w-4xl">
            <motion.h1 
              className="text-6xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700"
              variants={itemVariants}
            >
              Perfect Your Pitch with
              <br />
              Personalised Feedback
            </motion.h1>
            <motion.p 
              className="text-lg text-gray-600 max-w-2xl mx-auto mb-8"
              variants={itemVariants}
            >
              Upload a pitch and get instant insights on your presentation skills, <br />
              including your script and body language.
            </motion.p>
            <motion.div 
              className="flex items-center justify-center gap-4 text-sm"
              variants={itemVariants}
            >
              {/* Feature points with animation */}
              <motion.div 
                className="flex items-center gap-2 text-emerald-700"
                whileHover={{ scale: 1.05 }}
              >
                <Zap size={16} className="text-emerald-500" />
                <span>Instant Analysis</span>
              </motion.div>
              <div className="w-1 h-1 bg-gray-300 rounded-full"></div>
              <motion.div 
                className="flex items-center gap-2 text-emerald-700"
                whileHover={{ scale: 1.05 }}
              >
                <Zap size={16} className="text-emerald-500" />
                <span>AI-Powered Insights</span>
              </motion.div>
              <div className="w-1 h-1 bg-gray-300 rounded-full"></div>
              <motion.div 
                className="flex items-center gap-2 text-emerald-700"
                whileHover={{ scale: 1.05 }}
              >
                <Zap size={16} className="text-emerald-500" />
                <span>Detailed Feedback</span>
              </motion.div>
            </motion.div>
          </div>
        </motion.div>

        {/* Upload Section */}
        <motion.div 
          className="max-w-4xl mx-auto mb-32 relative"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-100/20 via-teal-100/20 to-cyan-100/20 rounded-3xl blur-2xl"></div>
          <motion.div 
            className="relative bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-emerald-100/20 shadow-xl"
            whileHover={{ boxShadow: "0 25px 50px -12px rgba(16, 185, 129, 0.15)" }}
          >
            <motion.div 
              className="mb-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
            >
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Upload Your Pitch</h2>
              <p className="text-gray-600">Start improving your presentation skills with AI-powered feedback</p>
            </motion.div>
            <motion.div
              {...getRootProps()}
              className={`aspect-video rounded-xl border-2 border-dashed ${
                isDragActive 
                  ? "border-emerald-500 bg-emerald-50" 
                  : "border-emerald-200 hover:border-emerald-300 bg-gradient-to-br from-white to-emerald-50/30"
              } flex items-center justify-center cursor-pointer transition-all`}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              <input {...getInputProps()} />
              <motion.div 
                className="text-center"
                initial={false}
                animate={uploadedFile ? "uploaded" : "initial"}
                variants={{
                  initial: { scale: 1 },
                  uploaded: { scale: 1.05 }
                }}
              >
                {uploadedFile ? (
                  <div className="space-y-3">
                    <motion.div 
                      className="w-20 h-20 rounded-full bg-emerald-100 flex items-center justify-center mx-auto"
                      initial={{ rotate: 0 }}
                      animate={{ rotate: 360 }}
                      transition={{ duration: 0.6 }}
                    >
                      <PlayCircle className="w-10 h-10 text-emerald-600" />
                    </motion.div>
                    <p className="text-gray-700 font-medium">{uploadedFile.name}</p>
                    {/* Redirection Button using useNavigate */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("/feedback", { state: { file: uploadedFile } });
                      }}
                      className="mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg shadow hover:bg-emerald-700 transition"
                    >
                      Get Feedback
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <motion.div 
                      className="w-20 h-20 rounded-full bg-emerald-100 flex items-center justify-center mx-auto"
                      whileHover={{ y: -5 }}
                    >
                      <Upload className="w-10 h-10 text-emerald-600" />
                    </motion.div>
                    <p className="text-gray-600 font-medium">Drag & drop a video here, or click to upload</p>
                    <p className="text-sm text-gray-500">Supports video files up to 1GB</p>
                  </div>
                )}
              </motion.div>
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
        >
          <motion.div 
            className="text-center mb-12"
            variants={itemVariants}
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Comprehensive Analysis</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">Get detailed insights into every aspect of your presentation</p>
          </motion.div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: FileText,
                title: "Smart Transcription",
                description: "Get an accurate transcript with highlighted points of improvement.",
                gradient: "from-emerald-500 to-teal-600",
                shadow: "shadow-emerald-200/50"
              },
              {
                icon: Hand,
                title: "Body Language",
                description: "Appear confident with personalized recommendations on your body language.",
                gradient: "from-teal-500 to-cyan-600",
                shadow: "shadow-cyan-200/50"
              },
              {
                icon: HelpCircle,
                title: "Q&A",
                description: "Practice responding to thoughtful questions.",
                gradient: "from-cyan-500 to-teal-600",
                shadow: "shadow-teal-200/50"
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg shadow-emerald-100/20 border border-emerald-100/20"
                variants={featureCardVariants}
                whileHover="hover"
                custom={index}
              >
                <motion.div 
                  className={`bg-gradient-to-br ${feature.gradient} w-16 h-16 rounded-xl flex items-center justify-center mb-6 shadow-lg ${feature.shadow}`}
                  whileHover={{ scale: 1.1 }}
                >
                  <feature.icon className="text-white" size={28} />
                </motion.div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default Home;
