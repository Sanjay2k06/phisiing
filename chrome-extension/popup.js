document.addEventListener("DOMContentLoaded", () => {
  const analyzeBtn = document.getElementById("analyzeBtn");
  const resultBox = document.getElementById("result");

  if (!analyzeBtn) {
    resultBox.textContent = "Button not found!";
    return;
  }

  analyzeBtn.addEventListener("click", async () => {
    resultBox.textContent = "Analyzing...";

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      if (!tabs || !tabs[0]) {
        resultBox.textContent = "No active tab";
        return;
      }

      const url = tabs[0].url;

      try {
        const res = await fetch("http://127.0.0.1:8000/api/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            content: url,
            mode: "url"
          })
        });

        const data = await res.json();

        resultBox.textContent =
          `Verdict: ${data.verdict}\n` +
          `Risk Score: ${data.risk_score}\n\n` +
          `Summary:\n${JSON.stringify(data.summary, null, 2)}`;

      } catch (err) {
        resultBox.textContent = "Error: " + err.message;
      }
    });
  });
});
