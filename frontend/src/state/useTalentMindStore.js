import { create } from "zustand";
import { candidates } from "../data/mockData";

export const useTalentMindStore = create((set) => ({
  theme: "dark",
  candidates,
  shortlisted: new Set(candidates.filter((candidate) => candidate.shortlisted).map((candidate) => candidate.id)),
  comparison: [],
  messages: [
    {
      role: "assistant",
      content: "Ask me to compare candidates, find RAG specialists, or explain ranking decisions.",
    },
  ],
  toggleTheme: () =>
    set((state) => ({
      theme: state.theme === "dark" ? "light" : "dark",
    })),
  toggleShortlist: (id) =>
    set((state) => {
      const shortlisted = new Set(state.shortlisted);
      shortlisted.has(id) ? shortlisted.delete(id) : shortlisted.add(id);
      return { shortlisted };
    }),
  toggleComparison: (id) =>
    set((state) => {
      const exists = state.comparison.includes(id);
      return {
        comparison: exists ? state.comparison.filter((item) => item !== id) : [...state.comparison.slice(-2), id],
      };
    }),
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
}));
