import axios from "axios";
import { analytics, candidates, jdAnalysis } from "../data/mockData";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 18000,
});

async function withFallback(request, fallback) {
  try {
    const response = await request();
    return response.data;
  } catch {
    return new Promise((resolve) => {
      window.setTimeout(() => resolve(fallback), 450);
    });
  }
}

export const api = {
  analyzeJobDescription: (payload) => withFallback(() => client.post("/jobs/analyze", payload), jdAnalysis),
  rankCandidates: (payload) => withFallback(() => client.post("/candidates/rank", payload), candidates),
  getCandidate: (id) =>
    withFallback(
      () => client.get(`/candidates/${id}`),
      candidates.find((candidate) => candidate.id === id) || candidates[0],
    ),
  getAnalytics: () => withFallback(() => client.get("/analytics"), analytics),
  askCopilot: (message) =>
    withFallback(() => client.post("/copilot/chat", { message }), {
      answer:
        message.toLowerCase().includes("relocate")
          ? "Mira Kapoor and Neha Rao are the strongest relocation-friendly matches based on behavioral intent and response reliability."
          : "Aarav ranks higher because his skills map directly to RAG, embeddings, FAISS, and production FastAPI systems while maintaining a 91 trust score.",
    }),
};
