import { motion } from "framer-motion";
import { Brain, Search, Zap, Shield, AlertTriangle, CheckCircle } from "lucide-react";

const HowItWorks = () => {
  const engines = [
    {
      icon: Brain,
      name: "NLP Engine",
      description: "Detects psychological manipulation, urgency tactics, authority abuse, and fear appeals using AI-powered natural language processing.",
    },
    {
      icon: Search,
      name: "URL Intelligence",
      description: "Analyzes suspicious domains, look-alike URLs, IP addresses, URL shorteners, and identifies phishing link patterns.",
    },
    {
      icon: AlertTriangle,
      name: "Behavioral Analysis",
      description: "Identifies social engineering tactics, coercion patterns, time pressure, forced actions, and emotional manipulation.",
    },
    {
      icon: Shield,
      name: "Email Header Analysis",
      description: "Checks SPF, DKIM, DMARC authentication, sender domain verification, and detects email spoofing attempts.",
    },
    {
      icon: Zap,
      name: "Scam Pattern Recognition",
      description: "Recognizes real-world fraud scenarios: delivery scams, OTP theft, refund fraud, job scams, and payment traps.",
    },
    {
      icon: CheckCircle,
      name: "Ensemble Scorer",
      description: "Combines all engine signals using weighted confidence scoring to produce final risk score and explainable verdict.",
    },
  ];

  return (
    <div className="py-20 px-4 bg-muted/30">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="font-heading font-bold text-3xl sm:text-4xl text-foreground mb-4 text-center" data-testid="how-it-works-heading">
            Multi-Engine Detection System
          </h2>
          <p className="text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
            Our system uses 6 specialized AI engines working together to detect modern phishing and scam attempts
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {engines.map((engine, index) => {
              const Icon = engine.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-card border border-border rounded-lg p-6 hover:border-accent/50 transition-all duration-300 hover:scale-105"
                  data-testid={`engine-card-${index}`}
                >
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-accent/20 border border-accent/30 mb-4">
                    <Icon className="w-6 h-6 text-accent" />
                  </div>
                  <h3 className="font-heading font-bold text-lg text-foreground mb-2">{engine.name}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{engine.description}</p>
                </motion.div>
              );
            })}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            viewport={{ once: true }}
            className="mt-12 bg-card border border-border rounded-lg p-8 text-center"
          >
            <h3 className="font-heading font-bold text-xl text-foreground mb-3">
              Adaptive Channel Intelligence
            </h3>
            <p className="text-muted-foreground max-w-3xl mx-auto">
              Unlike traditional filters, our system adapts its analysis based on the message channel.
              Email messages receive header authentication checks, SMS/WhatsApp messages are analyzed for mobile scam patterns,
              and URL-only inputs get deeper domain intelligence analysis.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default HowItWorks;