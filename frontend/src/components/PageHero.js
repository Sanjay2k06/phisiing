const PageHero = ({ title, subtitle }) => {
  return (
    <section className="hero-video-wrapper">
      <video autoPlay loop muted playsInline>
        <source src="/videos/bg-hero.mp4" type="video/mp4" />
      </video>

      <div className="hero-video-overlay"></div>

      <div className="hero-content">
        <div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
          <a href="/analysis" className="primary-btn">
            Analyze Now
          </a>
        </div>
      </div>
    </section>
  );
};

export default PageHero;
