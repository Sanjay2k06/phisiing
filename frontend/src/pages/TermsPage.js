import Navbar from "../components/Navbar";
import PageHero from "../components/PageHero";

const TermsPage = () => {
  return (
    <div className="page-wrapper">
      <div className="page-bg-video">
        <video autoPlay loop muted playsInline>
          <source src="/videos/bg-terms.mp4" type="video/mp4" />
        </video>
      </div>
      <div className="page-overlay" />

      <Navbar />

      <PageHero
        title="Terms & Conditions"
        subtitle="Usage guidelines and responsibilities"
      />

      <section className="page-content">
        <ol>
          <li>This system provides advisory analysis only</li>
          <li>No guarantee of complete accuracy</li>
          <li>User decisions remain their responsibility</li>
          <li>Not a replacement for enterprise security tools</li>
          <li>False positives and negatives may occur</li>
          <li>Results should be verified manually</li>
          <li>No permanent storage of sensitive data</li>
          <li>Designed for awareness and education</li>
          <li>No liability for financial loss</li>
          <li>Scam techniques evolve continuously</li>
          <li>Analysis depends on provided input</li>
          <li>Users must practice cyber hygiene</li>
          <li>System output is context-based</li>
          <li>Unauthorized misuse is prohibited</li>
          <li>Usage implies acceptance of terms</li>
        </ol>
      </section>
    </div>
  );
};

export default TermsPage;
