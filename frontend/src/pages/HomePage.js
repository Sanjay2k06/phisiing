import { motion } from "framer-motion";
import HeroSection from "../components/HeroSection";
import DetectionInterface from "../components/DetectionInterface";
import HowItWorks from "../components/HowItWorks";
import StatsDisplay from "../components/StatsDisplay";
import Disclaimer from "../components/Disclaimer";
import RefreshButton from "../components/RefreshButton";

const HomePage = () => {
  return (
    <div className="min-h-screen bg-home">
      {/* Hero Section */}
      <section>
        <HeroSection />
      </section>

      {/* Detection Interface */}
      <section>
        <DetectionInterface />
      </section>

      {/* How It Works */}
      <section>
        <HowItWorks />
      </section>

      {/* Stats */}
      <section>
        <StatsDisplay />
      </section>

      {/* Ethical Disclaimer */}
      <section>
        <Disclaimer />
      </section>

      {/* Refresh Option */}
      <section>
        <RefreshButton />
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-border mt-16">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center text-muted-foreground text-sm space-y-2">
            <p className="font-semibold">
              CodeSphere – AI-Assisted Phishing & Scam Detection System
            </p>
            <p>
              Multi-Engine Analysis • Behavioral Signals • Risk-Aware Intelligence
            </p>
            <p className="text-xs opacity-70 mt-2">
              This system provides automated security analysis. Human verification
              is always recommended before taking action.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
