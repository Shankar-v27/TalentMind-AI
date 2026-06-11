import { create } from "zustand";
import { candidates } from "../data/mockData";

export const useTalentMindStore = create((set) => ({
  // Theme
  theme: "dark",
  toggleTheme: () =>
    set((state) => ({
      theme: state.theme === "dark" ? "light" : "dark",
    })),

  // JD Analysis State
  jdAnalysis: null,
  setJdAnalysis: (analysis) => set({ jdAnalysis: analysis }),
  clearJdAnalysis: () => set({ jdAnalysis: null }),

  // Candidates and Ranking
  candidates,
  setCandidates: (candidates) =>
    set({
      candidates,
      shortlisted: new Set(candidates.filter((candidate) => candidate.shortlisted).map((candidate) => candidate.id)),
      comparison: [],
    }),

  // Ranking state
  isRanking: false,
  rankingProgress: 0,
  rankingStage: null,
  setIsRanking: (isRanking) => set({ isRanking }),
  setRankingProgress: (progress) => set({ rankingProgress: progress }),
  setRankingStage: (stage) => set({ rankingStage: stage }),

  // Shortlist and Comparison
  shortlisted: new Set(candidates.filter((candidate) => candidate.shortlisted).map((candidate) => candidate.id)),
  toggleShortlist: (id) =>
    set((state) => {
      const shortlisted = new Set(state.shortlisted);
      shortlisted.has(id) ? shortlisted.delete(id) : shortlisted.add(id);
      return { shortlisted };
    }),

  comparison: [],
  toggleComparison: (id) =>
    set((state) => {
      const exists = state.comparison.includes(id);
      return {
        comparison: exists ? state.comparison.filter((item) => item !== id) : [...state.comparison.slice(-2), id],
      };
    }),

  // Copilot Messages
  messages: [
    {
      role: "assistant",
      content: "Ask me to compare candidates, find RAG specialists, or explain ranking decisions.",
    },
  ],
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  // Session Management
  clearSession: () => set({
    jdAnalysis: null,
    candidates,
    shortlisted: new Set(),
    comparison: [],
    isRanking: false,
    rankingProgress: 0,
    rankingStage: null,
  }),
}));
