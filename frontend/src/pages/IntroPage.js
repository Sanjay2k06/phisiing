import { useNavigate } from "react-router-dom";

const IntroPage = () => {
  const navigate = useNavigate();

  return (
    <div className="hero-video-wrapper">
      <video autoPlay loop muted playsInline>
        <source src="/videos/bg-intro.mp4" type="video/mp4" />
      </video>

      <div className="hero-video-overlay" />

      <div className="hero-content text-center">
        <h1 className="text-5xl font-bold mb-6">CodeSphere</h1>

        <p className="text-muted-foreground max-w-xl mx-auto mb-8">
          An AI-assisted cybersecurity platform designed to analyze phishing,
          scam messages, and malicious links before users interact with them.
        </p>

        <button
          onClick={() => navigate("/")}
          className="px-10 py-4 bg-primary text-primary-foreground rounded hover:scale-105 transition-all"
        >
          Enter System
        </button>
      </div>
    </div>
  );
};

export default IntroPage;
