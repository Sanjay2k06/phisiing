import { motion } from "framer-motion";
import { Shield, AlertTriangle, XCircle, CheckCircle } from "lucide-react";

const ResultsDashboard = ({ result }) => {
  const getVerdictColor = (verdict) => {
    if (verdict === "Safe") return "text-safe";
    if (verdict === "Suspicious") return "text-suspicious";
    if (verdict === "Scam Detected") return "text-scam";
    if (verdict === "Phishing Detected") return "text-destructive";
    return "text-neutral";
  };

  const getVerdictBg = (verdict) => {
    if (verdict === "Safe") return "bg-safe/20 border-safe/30";
    if (verdict === "Suspicious") return "bg-suspicious/20 border-suspicious/30";
    if (verdict === "Scam Detected") return "bg-scam/20 border-scam/30";
    if (verdict === "Phishing Detected") return "bg-destructive/20 border-destructive/30";
    return "bg-neutral/20 border-neutral/30";
  };

  const getVerdictIcon = (verdict) => {
    if (verdict === "Safe") return <CheckCircle className="w-12 h-12" />;
    if (verdict === "Suspicious") return <AlertTriangle className="w-12 h-12" />;
    if (verdict === "Scam Detected" || verdict === "Phishing Detected") return <XCircle className="w-12 h-12" />;
    return <Shield className="w-12 h-12" />;
  };

  const getRiskLevel = (score) => {
    if (score >= 70) return "Critical";
    if (score >= 50) return "High";
    if (score >= 30) return "Medium";
    return "Low";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
      data-testid="results-dashboard"
    >
      {/* Main Verdict */}
      <div className={`border-2 rounded-lg p-8 ${getVerdictBg(result.verdict)}`}>
        <div className="flex items-center gap-6">
          <div className={getVerdictColor(result.verdict)}>
            {getVerdictIcon(result.verdict)}
          </div>
          <div className="flex-1">
            <h3 className="font-heading font-bold text-2xl text-foreground mb-2" data-testid="verdict">
              {result.verdict}
            </h3>
            <div className="flex items-center gap-4">
              <div>
                <div className="text-sm text-muted-foreground">Risk Score</div>
                <div className={`text-3xl font-mono font-bold ${getVerdictColor(result.verdict)}`} data-testid="risk-score">
                  {result.risk_score}/100
                </div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Risk Level</div>
                <div className={`text-xl font-heading font-bold ${getVerdictColor(result.verdict)}`}>
                  {getRiskLevel(result.risk_score)}
                </div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Mode</div>
                <div className="text-xl font-heading font-bold text-foreground uppercase">
                  {result.mode}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Progress Bar */}
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="text-sm font-heading font-semibold text-foreground mb-3">Risk Assessment</div>
        <div className="w-full h-4 bg-background rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${result.risk_score}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className={`h-full ${
              result.risk_score >= 70 ? "bg-destructive" :
              result.risk_score >= 50 ? "bg-scam" :
              result.risk_score >= 30 ? "bg-suspicious" :
              "bg-safe"
            }`}
          />
        </div>
        <div className="flex justify-between text-xs text-muted-foreground mt-2">
          <span>0 - Safe</span>
          <span>30 - Suspicious</span>
          <span>50 - Scam</span>
          <span>70+ - Phishing</span>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h4 className="font-heading font-bold text-lg text-foreground mb-3" data-testid="summary-heading">
          Analysis Summary
        </h4>
        <p className="text-muted-foreground leading-relaxed" data-testid="summary-text">
          {result.summary}
        </p>
      </div>

      {/* Engine Results */}
      <div className="space-y-4">
        <h4 className="font-heading font-bold text-lg text-foreground" data-testid="engine-results-heading">
          Detection Engine Results
        </h4>
        <div className="grid md:grid-cols-2 gap-4">
          {result.engine_results.map((engine, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-card border border-border rounded-lg p-5"
              data-testid={`engine-result-${index}`}
            >
              <div className="flex items-center justify-between mb-3">
                <h5 className="font-heading font-semibold text-foreground">{engine.engine_name}</h5>
                <span className={`text-lg font-mono font-bold ${
                  engine.risk_score >= 50 ? "text-destructive" :
                  engine.risk_score >= 30 ? "text-suspicious" :
                  "text-safe"
                }`}>
                  {engine.risk_score.toFixed(1)}
                </span>
              </div>
              <div className="space-y-2">
                {engine.findings.slice(0, 3).map((finding, fIndex) => (
                  <div key={fIndex} className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                    <p className="text-sm text-muted-foreground">{finding}</p>
                  </div>
                ))}
              </div>
              <div className="mt-3 text-xs text-muted-foreground">
                Confidence: {(engine.confidence * 100).toFixed(0)}%
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h4 className="font-heading font-bold text-lg text-foreground mb-4" data-testid="recommendations-heading">
            Recommended Actions
          </h4>
          <div className="space-y-3">
            {result.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-3" data-testid={`recommendation-${index}`}>
                <div className="w-6 h-6 rounded-full bg-accent/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-xs font-bold text-accent">{index + 1}</span>
                </div>
                <p className="text-muted-foreground">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default ResultsDashboard;