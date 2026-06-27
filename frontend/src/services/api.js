import axios from "axios";
import { analytics, candidates } from "../data/mockData";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  timeout: 120000,
});

async function withFallback(request, fallback) {
  try {
    const response = await request();
    return response.data;
  } catch (error) {
    console.error("API request failed:", error);
    return new Promise((resolve) => {
      window.setTimeout(() => resolve(fallback), 450);
    });
  }
}

export const api = {
  /**
   * Analyze a job description using Groq AI.
   * Returns structured JD analysis (required skills, seniority, location, etc).
   */
  analyzeJobDescription: async (payload) => {
    try {
      const response = await client.post("/jobs/analyze", payload);
      return response.data;
    } catch (error) {
      console.error("Job analysis failed:", error);
      throw error;
    }
  },

  /**
   * Rank candidates using the analyzed JD.
   * Must be called after successful JD analysis.
   */
  rankCandidates: async (jdData = null) => {
    try {
      const response = await client.post("/candidates/rank", jdData ? { jd_data: jdData } : {});
      return response.data;
    } catch (error) {
      console.error("Candidate ranking failed:", error);
      throw error;
    }
  },

  /**
   * Get a specific candidate from the current ranking results.
   */
  getCandidate: (id) =>
    withFallback(
      () => client.get(`/candidates/${id}`),
      candidates.find((candidate) => candidate.id === id) || candidates[0],
    ),

  /**
   * Get analytics data.
   */
  getAnalytics: () => withFallback(() => client.get("/analytics"), analytics),

  /**
   * Ask Copilot for analysis help.
   */
  askCopilot: (message) =>
    withFallback(() => client.post("/copilot/chat", { message }), {
      answer:
        message.toLowerCase().includes("relocate")
          ? "Mira Kapoor and Neha Rao are the strongest relocation-friendly matches based on behavioral intent and response reliability."
          : "Aarav ranks higher because his skills map directly to RAG, embeddings, FAISS, and production FastAPI systems while maintaining a 91 trust score.",
    }),

  /**
   * Clear current session (JD analysis and rankings).
   */
  clearSession: async () => {
    try {
      const response = await client.post("/clear-session");
      return response.data;
    } catch (error) {
      console.error("Failed to clear session:", error);
    }
  },
};
