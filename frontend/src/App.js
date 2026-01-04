import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import IntroPage from "./pages/IntroPage";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      {/* GLOBAL BACKGROUND VIDEO */}
      <div className="app-bg-video">
        <video
          autoPlay
          loop
          muted
          playsInline
        >
          <source src="/videos/bg-global.mp4" type="video/mp4" />
        </video>
      </div>

      {/* GLOBAL OVERLAY */}
      <div className="app-bg-overlay" />

      {/* APP CONTENT */}
      <BrowserRouter>
        <Routes>
          <Route path="/intro" element={<IntroPage />} />
          <Route path="/" element={<HomePage />} />
        </Routes>
      </BrowserRouter>

      <Toaster position="top-right" theme="dark" />
    </div>
  );
}

export default App;
