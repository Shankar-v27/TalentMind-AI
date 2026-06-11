import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUpDown, Eye, GitCompare, Search, Star } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { Input } from "../components/ui/Input";
import { useTalentMindStore } from "../state/useTalentMindStore";

export function Rankings() {
  const { candidates, shortlisted, comparison, toggleShortlist, toggleComparison } = useTalentMindStore();
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("score");

  const filtered = useMemo(() => {
    return candidates
      .filter((candidate) => `${candidate.name} ${candidate.role} ${candidate.skills.join(" ")}`.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => (sort === "experience" ? b.experience - a.experience : b.score - a.score));
  }, [candidates, query, sort]);

  return (
    <div className="space-y-5">
      <Card className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-2xl font-extrabold">Candidate ranking dashboard</h2>
          <p className="mt-1 text-sm text-muted-foreground">Search, filter, compare, shortlist, and inspect AI-generated ranking rationale.</p>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-muted-foreground" size={16} />
            <Input className="pl-9 sm:w-72" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search skill, role, candidate" />
          </div>
          <Button variant="outline" onClick={() => setSort(sort === "score" ? "experience" : "score")}>
            <ArrowUpDown size={16} /> Sort by {sort === "score" ? "score" : "experience"}
          </Button>
        </div>
      </Card>
      {comparison.length > 0 && (
        <Card className="flex flex-wrap items-center justify-between gap-3">
          <div className="font-bold">Comparison queue: {comparison.join(" vs ")}</div>
          <Badge tone="violet">{comparison.length}/3 selected</Badge>
        </Card>
      )}
      <div className="overflow-hidden rounded-lg border bg-card/80">
        <div className="hidden grid-cols-[72px_1.4fr_0.8fr_1fr_120px_160px] gap-4 border-b bg-muted/40 px-4 py-3 text-xs font-bold uppercase text-muted-foreground lg:grid">
          <div>Rank</div><div>Candidate</div><div>Score</div><div>Signals</div><div>Trust</div><div>Actions</div>
        </div>
        {filtered.map((candidate) => (
          <div key={candidate.id} className="grid gap-4 border-b p-4 last:border-b-0 lg:grid-cols-[72px_1.4fr_0.8fr_1fr_120px_160px] lg:items-center">
            <div className="text-2xl font-extrabold text-primary">#{candidate.rank}</div>
            <div>
              <div className="text-lg font-extrabold">{candidate.name}</div>
              <div className="text-sm font-semibold text-muted-foreground">{candidate.role} at {candidate.company}</div>
              <div className="mt-2 flex flex-wrap gap-1.5">{candidate.skills.slice(0, 5).map((skill) => <Badge key={skill} tone="blue">{skill}</Badge>)}</div>
            </div>
            <div>
              <div className="text-3xl font-extrabold">{candidate.score}</div>
              <div className="text-xs text-muted-foreground">{candidate.experience} yrs · {candidate.location}</div>
            </div>
            <p className="text-sm leading-6 text-muted-foreground">{candidate.reasoning}</p>
            <div className="space-y-1 text-sm">
              <div>Trust <b>{candidate.trust}</b></div>
              <div>Behavior <b>{candidate.behavioral}</b></div>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" size="icon" onClick={() => toggleShortlist(candidate.id)} aria-label="Shortlist">
                <Star size={17} className={shortlisted.has(candidate.id) ? "fill-amber-400 text-amber-400" : ""} />
              </Button>
              <Button variant="outline" size="icon" onClick={() => toggleComparison(candidate.id)} aria-label="Compare">
                <GitCompare size={17} className={comparison.includes(candidate.id) ? "text-primary" : ""} />
              </Button>
              <Link to={`/candidates/${candidate.id}`}>
                <Button size="icon" aria-label="View profile"><Eye size={17} /></Button>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
