import { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import {
  Mail,
  MessageSquare,
  Link as LinkIcon,
  AlertCircle,
  TrendingUp
} from "lucide-react";
import { toast } from "sonner";
import ResultsDashboard from "./ResultsDashboard";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DetectionInterface = () => {
  const [selectedMode, setSelectedMode] = useState("general");
  const [content, setContent] = useState("");
  const [emailHeaders, setEmailHeaders] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  /* ---------------- MODES ---------------- */
  const modes = [
    { id: "email", label: "Email", icon: Mail, description: "Email body + headers" },
    { id: "sms", label: "SMS", icon: MessageSquare, description: "Text message scams" },
    { id: "whatsapp", label: "WhatsApp", icon: MessageSquare, description: "Chat-based fraud" },
    { id: "url", label: "URL", icon: LinkIcon, description: "Suspicious links" },
    { id: "market", label: "Market Scam", icon: TrendingUp, description: "Investment / trading fraud" },
    { id: "general", label: "General", icon: AlertCircle, description: "Any suspicious message" },
  ];

  /* ---------------- EXAMPLES ---------------- */
  const examples = {
    email:
      "From: security@paypa1-support.com\nSubject: Urgent: Account Verification Required\n\nDear Customer,\n\nWe detected unusual activity in your account. Please verify your identity within 24 hours to avoid suspension.\n\nVerify now: http://paypal-secure-login.tk/confirm\n\nPayPal Security Team",

    sms:
      "ALERT: Your bank account is temporarily blocked. Verify immediately at bit.ly/bank-verify",

    whatsapp:
      "Hi! You’ve won a ₹50,000 reward from Amazon. Click here to claim before it expires: http://amazon-reward.xyz",

    url:
      "http://secure-google-login.verify-now.tk/session?id=928374",

    market:
      "🔥 GUARANTEED PROFIT 🔥\nInvest ₹5,000 today and get ₹50,000 in 7 days.\nLimited slots only. Contact now on WhatsApp.",

    general:
      "Urgent notice: Your account will be permanently closed unless you act immediately. Click the link and confirm your details."
  };

  /* ---------------- ANALYZE ---------------- */
  const handleAnalyze = async () => {
    if (!content.trim()) {
      toast.error("Please enter content to analyze");
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    try {
      const headers = {};
      if (selectedMode === "email" && emailHeaders.trim()) {
        emailHeaders.split("\n").forEach((line) => {
          const [key, ...value] = line.split(":");
          if (key && value.length) {
            headers[key.trim().toLowerCase()] = value.join(":").trim();
          }
        });
      }

      const response = await axios.post(`${API}/analyze`, {
        content: content,
        mode: selectedMode,
        email_headers: Object.keys(headers).length ? headers : null,
      });

      setResult(response.data);
      toast.success("Analysis completed successfully");
    } catch (err) {
      console.error(err);
      toast.error("Analysis failed. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  /* ---------------- UI ---------------- */
  return (
    <div id="detection" className="py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-4">
            Multi-Channel Scam & Phishing Analysis
          </h2>

          <p className="text-muted-foreground text-center max-w-2xl mx-auto mb-12">
            Choose the type of input. Each channel is analyzed using specialized
            detection logic to identify manipulation, deception, and fraud risk.
          </p>

          {/* Mode Selector */}
          <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-10">
            {modes.map((mode) => {
              const Icon = mode.icon;
              return (
                <button
                  key={mode.id}
                  onClick={() => {
                    setSelectedMode(mode.id);
                    setContent("");
                    setEmailHeaders("");
                    setResult(null);
                  }}
                  className={`p-4 rounded-lg border-2 transition-all hover:scale-105 ${
                    selectedMode === mode.id
                      ? "border-accent bg-accent/10 shadow-lg"
                      : "border-border bg-card"
                  }`}
                >
                  <Icon className="w-6 h-6 mx-auto mb-2 text-accent" />
                  <div className="text-sm font-semibold">{mode.label}</div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {mode.description}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Input */}
          <div className="bg-card border rounded-lg p-6 mb-6">
            <label className="block text-sm font-semibold mb-2">
              {selectedMode === "url" ? "Suspicious URL" : "Message Content"}
            </label>

            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Paste content here for analysis…"
              className="w-full h-40 bg-background border rounded px-4 py-3 font-mono text-sm resize-none"
            />

            {selectedMode === "email" && (
              <div className="mt-4">
                <label className="block text-sm font-semibold mb-2">
                  Email Headers (optional)
                </label>
                <textarea
                  value={emailHeaders}
                  onChange={(e) => setEmailHeaders(e.target.value)}
                  placeholder="From: sender@example.com\nSPF: pass\nDKIM: pass"
                  className="w-full h-24 bg-background border rounded px-4 py-3 font-mono text-sm resize-none"
                />
              </div>
            )}

            <div className="flex justify-between items-center mt-4">
              <button
                onClick={() => setContent(examples[selectedMode])}
                className="text-sm text-accent underline"
              >
                Load Example
              </button>

              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                className="px-6 py-3 bg-primary text-primary-foreground rounded hover:scale-105 transition-all disabled:opacity-50"
              >
                {isAnalyzing ? "Analyzing…" : "Analyze"}
              </button>
            </div>
          </div>

          {/* Results */}
          {result && <ResultsDashboard result={result} />}
        </motion.div>
      </div>
    </div>
  );
};

export default DetectionInterface;
