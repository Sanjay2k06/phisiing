import { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import { Mail, MessageSquare, Link as LinkIcon, AlertCircle } from "lucide-react";
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

  const modes = [
    { id: "email", label: "Email", icon: Mail, description: "Email with headers" },
    { id: "sms", label: "SMS", icon: MessageSquare, description: "Text message" },
    { id: "whatsapp", label: "WhatsApp", icon: MessageSquare, description: "WhatsApp message" },
    { id: "url", label: "URL", icon: LinkIcon, description: "Link only" },
    { id: "general", label: "General", icon: AlertCircle, description: "Any message" },
  ];

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
        const headerLines = emailHeaders.split("\n");
        headerLines.forEach(line => {
          const [key, ...valueParts] = line.split(":");
          if (key && valueParts.length > 0) {
            headers[key.trim().toLowerCase()] = valueParts.join(":").trim();
          }
        });
      }

      const response = await axios.post(`${API}/analyze`, {
        content: content,
        mode: selectedMode,
        email_headers: Object.keys(headers).length > 0 ? headers : null,
      });

      setResult(response.data);
      toast.success("Analysis complete!");
    } catch (error) {
      console.error("Analysis error:", error);
      toast.error("Analysis failed. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const examples = {
    email: "From: security@paypa1-support.com\nSubject: Urgent: Your Account Will Be Suspended\n\nDear Customer,\n\nYour PayPal account has been temporarily restricted due to unusual activity. You must verify your account within 24 hours to avoid permanent suspension.\n\nClick here to verify: http://paypal-verify.tk/confirm\n\nThank you,\nPayPal Security Team",
    sms: "URGENT: Your package delivery failed. Confirm your address here: bit.ly/pkg-confirm. Fees pending. Reply STOP to cancel.",
    whatsapp: "Hi! You've been selected to receive a $500 Amazon gift card! Click this link to claim your reward before it expires: http://amazon-gift.xyz/claim?id=8374",
    url: "http://g00gle-security-alert.tk/verify-account?session=83749234",
    general: "Congratulations! You've won $10,000 in our prize draw. To claim your prize, please provide your bank details and pay a small processing fee of $50. This is a limited time offer - act now!",
  };

  return (
    <div id="detection" className="py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="font-heading font-bold text-3xl sm:text-4xl text-foreground mb-4 text-center" data-testid="detection-heading">
            Multi-Channel Detection
          </h2>
          <p className="text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
            Select your message type for channel-specific analysis
          </p>

          {/* Mode Selector */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            {modes.map((mode) => {
              const Icon = mode.icon;
              return (
                <button
                  key={mode.id}
                  onClick={() => {
                    setSelectedMode(mode.id);
                    setResult(null);
                  }}
                  data-testid={`mode-${mode.id}`}
                  className={`p-4 rounded-lg border-2 transition-all duration-300 hover:scale-105 ${
                    selectedMode === mode.id
                      ? "border-accent bg-accent/10 shadow-lg"
                      : "border-border bg-card hover:border-accent/50"
                  }`}
                >
                  <Icon className={`w-6 h-6 mx-auto mb-2 ${selectedMode === mode.id ? "text-accent" : "text-muted-foreground"}`} />
                  <div className="text-sm font-heading font-semibold text-foreground">{mode.label}</div>
                  <div className="text-xs text-muted-foreground mt-1">{mode.description}</div>
                </button>
              );
            })}
          </div>

          {/* Input Area */}
          <div className="bg-card border border-border rounded-lg p-6 mb-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-heading font-semibold text-foreground mb-2" data-testid="content-label">
                  Message Content {selectedMode === "url" && "(URL)"}
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder={`Enter ${selectedMode === "url" ? "URL" : "message content"} to analyze...`}
                  data-testid="content-input"
                  className="w-full h-40 bg-background border border-input rounded px-4 py-3 text-foreground font-mono text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent resize-none"
                />
              </div>

              {selectedMode === "email" && (
                <div>
                  <label className="block text-sm font-heading font-semibold text-foreground mb-2" data-testid="headers-label">
                    Email Headers (Optional)
                  </label>
                  <textarea
                    value={emailHeaders}
                    onChange={(e) => setEmailHeaders(e.target.value)}
                    placeholder="From: sender@example.com\nSPF: pass\nDKIM: pass\nDMARC: pass"
                    data-testid="headers-input"
                    className="w-full h-24 bg-background border border-input rounded px-4 py-3 text-foreground font-mono text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent resize-none"
                  />
                </div>
              )}

              <div className="flex items-center justify-between">
                <button
                  onClick={() => setContent(examples[selectedMode])}
                  data-testid="load-example-btn"
                  className="text-sm text-accent hover:text-accent/80 font-heading font-semibold transition-colors"
                >
                  Load Example
                </button>

                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  data-testid="analyze-btn"
                  className="px-6 py-3 bg-primary text-primary-foreground font-heading font-semibold rounded hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:scale-105 hover:shadow-lg"
                >
                  {isAnalyzing ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    "Analyze Message"
                  )}
                </button>
              </div>
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