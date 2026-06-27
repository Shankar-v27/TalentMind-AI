import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Brain, CheckCircle2, Gauge, Search, Sparkles, UsersRound } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { useTalentMindStore } from "../state/useTalentMindStore";

const stats = [
  { label: "Candidates analyzed", value: "100,000", icon: UsersRound },
  { label: "Semantic retrievals", value: "12,480", icon: Search },
  { label: "Top-ranked matches", value: "1,246", icon: CheckCircle2 },
  { label: "Average match score", value: "86.4%", icon: Gauge },
];

export function Dashboard() {
  const candidates = useTalentMindStore((state) => state.candidates);
  return (
    <div className="space-y-6">
      <section className="grid gap-5 lg:grid-cols-[1.45fr_0.9fr]">
        <Card className="relative overflow-hidden p-7">
          <div className="max-w-3xl">
            <Badge tone="violet" className="mb-4">AI-powered recruitment intelligence</Badge>
            <h1 className="max-w-4xl text-4xl font-extrabold leading-tight sm:text-5xl">
              Discover, rank, and explain the best talent with <span className="text-gradient">TalentMind AI</span>
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-muted-foreground">
              Enterprise-grade candidate intelligence built on semantic search, multi-signal scoring, behavioral analytics, and recruiter-ready explanations.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link to="/job-analysis">
                <Button>Start AI search <ArrowRight size={18} /></Button>
              </Link>
              <Link to="/rankings">
                <Button variant="outline">View ranked candidates</Button>
              </Link>
            </div>
          </div>
          <Brain className="absolute -right-8 bottom-0 text-primary/10" size={260} />
        </Card>
        <Card>
          <div className="mb-4 flex items-center gap-2 font-extrabold"><Sparkles size={18} className="text-primary" /> Recent AI searches</div>
          {["Senior AI Retrieval Engineer", "Founding ML Engineer", "RAG Platform Lead", "Data Engineering Manager"].map((item, index) => (
            <div key={item} className="flex items-center justify-between border-b py-3 last:border-b-0">
              <div>
                <div className="font-semibold">{item}</div>
                <div className="text-xs text-muted-foreground">{240 + index * 38} candidates retrieved</div>
              </div>
              <Badge tone={index === 0 ? "green" : "blue"}>{index === 0 ? "Live" : "Saved"}</Badge>
            </div>
          ))}
        </Card>
      </section>
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat, index) => (
          <motion.div key={stat.label} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.05 }}>
            <Card>
              <stat.icon className="mb-4 text-primary" size={24} />
              <div className="text-3xl font-extrabold">{stat.value}</div>
              <div className="mt-1 text-sm text-muted-foreground">{stat.label}</div>
            </Card>
          </motion.div>
        ))}
      </section>
      <section className="grid gap-5 lg:grid-cols-3">
        {candidates.slice(0, 3).map((candidate) => (
          <Card key={candidate.id}>
            <div className="mb-3 flex items-start justify-between">
              <div>
                <div className="text-sm text-muted-foreground">Rank #{candidate.rank}</div>
                <div className="text-lg font-extrabold">{candidate.name}</div>
              </div>
              <div className="rounded-lg bg-primary/10 px-3 py-2 text-xl font-extrabold text-primary">{candidate.score}</div>
            </div>
            <p className="text-sm font-semibold">{candidate.role}</p>
            <p className="mt-2 line-clamp-2 text-sm leading-6 text-muted-foreground">{candidate.reasoning}</p>
          </Card>
        ))}
      </section>
    </div>
  );
}
