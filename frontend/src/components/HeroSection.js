import { motion } from "framer-motion";
import { Shield } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="hero-video-wrapper">
      {/* HERO VIDEO */}
      <video
        autoPlay
        loop
        muted
        playsInline
      >
        <source src="/videos/bg-hero.mp4" type="video/mp4" />
      </video>

      {/* HERO OVERLAY */}
      <div className="hero-video-overlay" />

      {/* HERO CONTENT */}
      <div className="hero-content">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-6 max-w-4xl"
        >
          {/* Team Name */}
          <div className="absolute top-6 left-6 text-sm tracking-widest text-muted-foreground">
            CodeSphere
          </div>

          {/* Icon */}
          <div className="flex justify-center">
            <div className="w-20 h-20 flex items-center justify-center rounded-full border border-accent bg-accent/10">
              <Shield className="w-10 h-10 text-accent" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-4xl md:text-6xl font-bold">
            AI-Assisted Phishing & Scam Detection
          </h1>

          {/* Subtitle */}
          <p className="text-muted-foreground text-lg max-w-3xl mx-auto">
            A multi-engine cybersecurity system that analyzes intent,
            psychological manipulation, and threat signals before users interact
            with suspicious content.
          </p>

          {/* CTA */}
          <a
            href="#detection"
            className="inline-block px-8 py-4 bg-primary text-primary-foreground rounded
            hover:scale-105 transition-all"
          >
            Analyze a Message
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
