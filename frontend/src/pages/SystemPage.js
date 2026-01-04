import Navbar from "../components/Navbar";
import PageHero from "../components/PageHero";

const SystemPage = () => {
  return (
    <div className="page-wrapper">
      <div className="page-bg-video">
        <video autoPlay loop muted playsInline>
          <source src="/videos/bg-system.mp4" type="video/mp4" />
        </video>
      </div>
      <div className="page-overlay" />

      <Navbar />

      <PageHero
        title="Multi-Engine Detection System"
        subtitle="How CodeSphere evaluates threats using layered intelligence"
      />

      <section className="page-content">
        <p>
          CodeSphere is built using a multi-engine analysis architecture. Each
          engine focuses on a different aspect of threat detection, allowing the
          system to reduce bias and increase confidence.
        </p>

        <ul>
          <li>Linguistic analysis of urgency and fear patterns</li>
          <li>Intent recognition and behavioral scoring</li>
          <li>Pattern matching against known scam templates</li>
          <li>Confidence aggregation across engines</li>
          <li>Explainable output for human understanding</li>
        </ul>

        <p>
          Instead of relying on a single rule or model, CodeSphere correlates
          multiple weak signals to form a stronger risk assessment. This approach
          mirrors how cybersecurity professionals analyze threats.
        </p>
      </section>
    </div>
  );
};

export default SystemPage;
