import Navbar from "../components/Navbar";
import PageHero from "../components/PageHero";
import DetectionInterface from "../components/DetectionInterface";
import Disclaimer from "../components/Disclaimer";
import RefreshButton from "../components/RefreshButton";

const AnalysisPage = () => {
  return (
    <>
      <Navbar />
      <PageHero
        title="Message & Link Analysis"
        subtitle="Submit content for automated multi-engine risk evaluation"
      />

      <DetectionInterface />
      <Disclaimer />
      <RefreshButton />
    </>
  );
};

export default AnalysisPage;
