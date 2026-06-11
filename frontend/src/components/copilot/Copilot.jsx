import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, CornerDownLeft, MessageSquare, X } from "lucide-react";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { api } from "../../services/api";
import { useTalentMindStore } from "../../state/useTalentMindStore";

const prompts = ["Why does Aarav rank higher?", "Find RAG candidates", "Who is relocation friendly?"];

export function Copilot() {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [typing, setTyping] = useState(false);
  const { messages, addMessage } = useTalentMindStore();

  async function send(text = value) {
    if (!text.trim()) return;
    addMessage({ role: "user", content: text });
    setValue("");
    setTyping(true);
    const response = await api.askCopilot(text);
    setTyping(false);
    addMessage({ role: "assistant", content: response.answer });
  }

  return (
    <>
      <Button className="fixed bottom-5 right-5 z-40 rounded-full" size="lg" onClick={() => setOpen(true)}>
        <MessageSquare size={18} /> Copilot
      </Button>
      <AnimatePresence>
        {open && (
          <motion.section
            initial={{ opacity: 0, y: 24, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 24, scale: 0.96 }}
            className="fixed bottom-20 right-4 z-50 flex h-[600px] max-h-[78vh] w-[min(440px,calc(100vw-2rem))] flex-col rounded-lg border bg-card shadow-2xl"
          >
            <div className="flex items-center justify-between border-b p-4">
              <div className="flex items-center gap-2 font-extrabold">
                <Bot className="text-primary" size={20} /> TalentMind AI Copilot
              </div>
              <Button variant="ghost" size="icon" onClick={() => setOpen(false)}>
                <X size={18} />
              </Button>
            </div>
            <div className="scrollbar-thin flex-1 space-y-3 overflow-y-auto p-4">
              {messages.map((message, index) => (
                <div key={`${message.role}-${index}`} className={message.role === "user" ? "text-right" : ""}>
                  <div
                    className={`inline-block max-w-[85%] rounded-lg px-3 py-2 text-sm leading-6 ${
                      message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              {typing && <div className="inline-flex rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">Thinking...</div>}
            </div>
            <div className="space-y-3 border-t p-4">
              <div className="flex flex-wrap gap-2">
                {prompts.map((prompt) => (
                  <button key={prompt} onClick={() => send(prompt)} className="rounded-full bg-muted px-3 py-1 text-xs font-semibold">
                    {prompt}
                  </button>
                ))}
              </div>
              <form
                className="flex gap-2"
                onSubmit={(event) => {
                  event.preventDefault();
                  send();
                }}
              >
                <Input value={value} onChange={(event) => setValue(event.target.value)} placeholder="Ask about ranking, skills, intent..." />
                <Button size="icon" aria-label="Send">
                  <CornerDownLeft size={18} />
                </Button>
              </form>
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </>
  );
}
