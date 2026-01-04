// frontend/src/services/api.js

const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function analyzeMessage(content, mode = "email") {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
      mode,
    }),
  });

  if (!response.ok) {
    throw new Error("Backend API error");
  }

  return response.json();
}
