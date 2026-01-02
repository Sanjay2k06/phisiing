import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import HeroSection from "../components/HeroSection";
import DetectionInterface from "../components/DetectionInterface";
import HowItWorks from "../components/HowItWorks";
import StatsDisplay from "../components/StatsDisplay";

const HomePage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection />

      {/* Detection Interface */}
      <DetectionInterface />

      {/* How It Works */}
      <HowItWorks />

      {/* Stats */}
      <StatsDisplay />

      {/* Footer */}
      <footer className="py-12 border-t border-border">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center text-muted-foreground text-sm">
            <p>CyberSentinel AI - Advanced Phishing Defense System</p>
            <p className="mt-2">Powered by Multi-Engine AI Detection</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;