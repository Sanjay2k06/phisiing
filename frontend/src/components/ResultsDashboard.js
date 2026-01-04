import { motion } from "framer-motion";
import { Shield, AlertTriangle, XCircle, CheckCircle } from "lucide-react";

const safeArray = (v) => (Array.isArray(v) ? v : []);
const safeObject = (v) => (v && typeof v === "object" ? v : {});

const ResultsDashboard = ({ result }) => {
  // -------- HARD GUARDS (CRASH PROOF) --------
  if (!result) {
    return (
      <div className="p-6 bg-card border rounded text-muted-foreground">
        No analysis result available.
      </div>
    );
  }

  const verdict = result.verdict ?? "Unknown";
  const riskScore = Number(result.risk_score ?? 0);
  const mode = result.mode ?? "general";
  const engineResults = safeArray(result.engine_results);
  const recommendations = safeArray(result.recommendations);
  const summary = safeObject(result.summary);

  // -------- UI HELPERS --------
  const getVerdictColor = () => {
    if (verdict === "Safe") return "text-safe";
    if (verdict === "Suspicious") return "text-suspicious";
    if (verdict === "Scam Detected") return "text-scam";
    if (verdict === "Phishing Detected") return "text-destructive";
    return "text-neutral";
  };

  const getVerdictBg = () => {
    if (verdict === "Safe") return "bg-safe/20 border-safe/30";
    if (verdict === "Suspicious") return "bg-suspicious/20 border-suspicious/30";
    if (verdict === "Scam Detected") return "bg-scam/20 border-scam/30";
    if (verdict === "Phishing Detected") return "bg-destructive/20 border-destructive/30";
    return "bg-neutral/20 border-neutral/30";
  };

  const getVerdictIcon = () => {
    if (verdict === "Safe") return <CheckCircle className="w-12 h-12" />;
    if (verdict === "Suspicious") return <AlertTriangle className="w-12 h-12" />;
    if (verdict === "Scam Detected" || verdict === "Phishing Detected")
      return <XCircle className="w-12 h-12" />;
    return <Shield className="w-12 h-12" />;
  };

  const getRiskLevel = () => {
    if (riskScore >= 70) return "Critical";
    if (riskScore >= 50) return "High";
    if (riskScore >= 30) return "Medium";
    return "Low";
  };

  // -------- RENDER --------
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Verdict */}
      <div className={`border-2 rounded-lg p-8 ${getVerdictBg()}`}>
        <div className="flex gap-6 items-center">
          <div className={getVerdictColor()}>{getVerdictIcon()}</div>
          <div>
            <h3 className="text-2xl font-bold">{verdict}</h3>
            <p className="text-muted-foreground">
              Risk Score: <span className="font-mono">{riskScore}/100</span>
            </p>
            <p className="text-muted-foreground">
              Risk Level: <strong>{getRiskLevel()}</strong>
            </p>
            <p className="text-muted-foreground">
              Mode: <strong>{mode.toUpperCase()}</strong>
            </p>
          </div>
        </div>
      </div>

      {/* Progress */}
      <div className="bg-card border rounded p-5">
        <div className="w-full h-3 bg-background rounded overflow-hidden">
          <div
            className={`h-full transition-all ${
              riskScore >= 70
                ? "bg-destructive"
                : riskScore >= 50
                ? "bg-scam"
                : riskScore >= 30
                ? "bg-suspicious"
                : "bg-safe"
            }`}
            style={{ width: `${riskScore}%` }}
          />
        </div>
      </div>

      {/* Summary */}
      <div className="bg-card border rounded p-5 text-sm text-muted-foreground space-y-1">
        <p><strong>Overall Intent:</strong> {summary.overall_intent ?? "N/A"}</p>
        <p><strong>ML Probability:</strong> {summary.ml_probability ?? "N/A"}</p>
        <p><strong>Threat Confidence:</strong> {summary.threat_confidence ?? "N/A"}</p>
        <p><strong>Engines Used:</strong> {summary.analysis_engines_used ?? engineResults.length}</p>
        {summary.ai_disagreement && (
          <p className="text-yellow-500 font-semibold">
            ⚠ AI vs AI disagreement detected
          </p>
        )}
      </div>

      {/* Engine Results */}
      <div className="space-y-4">
        <h4 className="font-bold text-lg">Detection Engine Results</h4>

        {engineResults.length === 0 ? (
          <p className="text-muted-foreground text-sm">
            No engine details available.
          </p>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {engineResults.map((engine, index) => (
              <div key={index} className="bg-card border rounded p-4">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">
                    {engine.engine_name ?? "Unknown Engine"}
                  </span>
                  <span className="font-mono">
                    {Number(engine.risk_score ?? 0)}
                  </span>
                </div>

                {safeArray(engine.findings).slice(0, 3).map((f, i) => (
                  <p key={i} className="text-xs text-muted-foreground">
                    • {f}
                  </p>
                ))}

                <p className="text-xs mt-2 text-muted-foreground">
                  Confidence: {Math.round((engine.confidence ?? 0) * 100)}%
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div className="bg-card border rounded p-5">
          <h4 className="font-bold mb-3">Recommended Actions</h4>
          {recommendations.map((r, i) => (
            <p key={i} className="text-sm text-muted-foreground">
              {i + 1}. {r}
            </p>
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default ResultsDashboard;
