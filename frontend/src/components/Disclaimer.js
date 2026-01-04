import { motion } from "framer-motion";

const Disclaimer = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      viewport={{ once: true }}
      className="max-w-4xl mx-auto my-14 bg-card border border-yellow-500/30 rounded-lg p-6"
    >
      <h4 className="font-semibold text-yellow-500 mb-3 flex items-center gap-2">
        ⚠ Important Security Notice
      </h4>

      <p className="text-sm text-muted-foreground leading-relaxed">
        This analysis is produced by an automated, multi-engine detection system.
        The system evaluates linguistic patterns, behavioral signals, contextual
        intent, and known scam indicators to estimate potential risk.
      </p>

      <p className="text-sm text-muted-foreground mt-3 leading-relaxed">
        While the system is designed to assist users in identifying phishing and
        scam attempts, <strong>no automated security solution is infallible</strong>.
        False positives and false negatives may occur, especially in edge cases
        involving ambiguous or incomplete information.
      </p>

      <p className="text-sm text-muted-foreground mt-3 leading-relaxed">
        Users are strongly advised to review the content carefully and apply
        human judgment before clicking links, sharing credentials, or performing
        financial actions.
      </p>

      <p className="text-xs text-muted-foreground mt-4 opacity-70">
        This tool is intended for awareness and educational purposes and should
        not be considered a replacement for professional cybersecurity controls.
      </p>
    </motion.div>
  );
};

export default Disclaimer;
