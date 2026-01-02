import { motion } from "framer-motion";
import { Shield, Brain, Lock } from "lucide-react";

const HeroSection = () => {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23DFD0B8' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="container mx-auto px-4 max-w-6xl relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center space-y-8"
        >
          {/* Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-accent/20 border-2 border-accent"
            data-testid="hero-icon"
          >
            <Shield className="w-10 h-10 text-accent" />
          </motion.div>

          {/* Heading */}
          <div className="space-y-4">
            <motion.h1
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="font-heading font-bold text-4xl sm:text-5xl lg:text-6xl text-foreground tracking-tight"
              data-testid="hero-heading"
            >
              AI vs AI Phishing Defense
            </motion.h1>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto font-body"
              data-testid="hero-subheading"
            >
              Modern phishing attacks use generative AI to bypass traditional filters.
              Our multi-engine detection system analyzes messages like a cybersecurity expert—detecting
              psychological manipulation, malicious URLs, and social engineering tactics in real-time.
            </motion.p>
          </div>

          {/* Problem Statement */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-card border border-border rounded-lg p-8 max-w-4xl mx-auto"
            data-testid="problem-statement"
          >
            <div className="grid md:grid-cols-3 gap-6">
              <div className="space-y-3">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-destructive/20 border border-destructive/30">
                  <Brain className="w-6 h-6 text-destructive" />
                </div>
                <h3 className="font-heading font-bold text-lg text-foreground">AI-Generated Scams</h3>
                <p className="text-sm text-muted-foreground">
                  Attackers use ChatGPT & AI to create convincing, personalized phishing messages
                </p>
              </div>
              <div className="space-y-3">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-destructive/20 border border-destructive/30">
                  <Lock className="w-6 h-6 text-destructive" />
                </div>
                <h3 className="font-heading font-bold text-lg text-foreground">Bypassing Filters</h3>
                <p className="text-sm text-muted-foreground">
                  Traditional spam filters fail against well-written, context-aware attacks
                </p>
              </div>
              <div className="space-y-3">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-safe/20 border border-safe/30">
                  <Shield className="w-6 h-6 text-safe" />
                </div>
                <h3 className="font-heading font-bold text-lg text-foreground">Our Solution</h3>
                <p className="text-sm text-muted-foreground">
                  Multi-engine AI detection analyzing behavior, psychology, and intent
                </p>
              </div>
            </div>
          </motion.div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="pt-4"
          >
            <a
              href="#detection"
              data-testid="cta-button"
              className="inline-block px-8 py-4 bg-primary text-primary-foreground font-heading font-semibold rounded hover:bg-primary/90 hover:scale-105 hover:shadow-lg transition-all duration-300"
            >
              Analyze a Message
            </a>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default HeroSection;