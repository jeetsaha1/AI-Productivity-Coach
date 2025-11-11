import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send } from "lucide-react";

export default function Chat() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "👋 Hello! I'm your AI Productivity Coach. What’s your focus today?" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages([...messages, { from: "user", text: userMessage }]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      setTimeout(() => {
        setMessages((prev) => [...prev, { from: "bot", text: data.reply }]);
        setIsTyping(false);
      }, 1000);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "⚠️ Server not reachable. Try again later." },
      ]);
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-pink-200 via-purple-200 to-indigo-200 p-4">
      <motion.div
        className="w-full max-w-lg bg-white/70 backdrop-blur-md rounded-2xl shadow-2xl p-5 border border-white/40"
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", duration: 0.5 }}
      >
        <h1 className="text-2xl font-bold text-center mb-4 bg-gradient-to-r from-purple-600 to-indigo-500 text-transparent bg-clip-text">
          🌟 AI Productivity Coach
        </h1>

        <div className="h-[450px] overflow-y-auto rounded-xl bg-gradient-to-t from-white/70 to-white/40 p-3 shadow-inner">
          <AnimatePresence>
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                className={`flex ${
                  msg.from === "user" ? "justify-end" : "justify-start"
                } mb-3`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <div
                  className={`px-4 py-2 rounded-2xl max-w-[80%] text-sm shadow-md ${
                    msg.from === "user"
                      ? "bg-gradient-to-r from-blue-500 to-indigo-500 text-white"
                      : "bg-gradient-to-r from-pink-400 to-purple-400 text-white"
                  }`}
                >
                  {msg.text}
                </div>
              </motion.div>
            ))}

            {isTyping && (
              <motion.div
                className="flex justify-start mb-3"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ repeat: Infinity, duration: 1 }}
              >
                <div className="px-4 py-2 rounded-2xl bg-gradient-to-r from-purple-400 to-pink-400 text-white text-sm shadow-md">
                  <span className="animate-pulse">💬 Typing...</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={chatEndRef} />
        </div>

        <div className="mt-4 flex items-center bg-white/70 rounded-full shadow-lg border border-white/50 p-2">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-grow bg-transparent outline-none px-4 text-gray-700"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleSend}
            className="p-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full shadow-md hover:shadow-lg transition-all"
          >
            <Send size={18} />
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
