import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUpDown, Eye, GitCompare, Search, Star, Zap, Clock, Shield } from "lucide-react";
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
      .filter((candidate) => {
        const skillsString = (candidate.skills || []).join(" ");
        const searchPool = `${candidate.name || ""} ${candidate.role || ""} ${skillsString}`.toLowerCase();
        return searchPool.includes(query.toLowerCase());
      })
      .sort((a, b) => {
        if (sort === "experience") {
          return (b.experience || 0) - (a.experience || 0);
        }
        // Default sort by Future Score / Score
        const scoreA = a.future_score || a.score || 0;
        const scoreB = b.future_score || b.score || 0;
        return scoreB - scoreA;
      });
  }, [candidates, query, sort]);

  return (
    <div className="space-y-5">
      <Card className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-primary/20 bg-gradient-to-r from-card to-primary/5">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight">Future Workforce Rankings</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Analyze candidates ranked by multi-year workforce utility, growth velocity, and cultural alignment.
          </p>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-muted-foreground" size={16} />
            <Input 
              className="pl-9 sm:w-72" 
              value={query} 
              onChange={(event) => setQuery(event.target.value)} 
              placeholder="Search skills, titles, locations..." 
            />
          </div>
          <Button variant="outline" onClick={() => setSort(sort === "score" ? "experience" : "score")}>
            <ArrowUpDown size={16} /> Sort by {sort === "score" ? "Future Score" : "Experience"}
          </Button>
        </div>
      </Card>
      
      {comparison.length > 0 && (
        <Card className="flex flex-wrap items-center justify-between gap-3 border-violet-500/20 bg-violet-500/5">
          <div className="font-bold text-violet-300">Comparison Queue: {comparison.join(" vs ")}</div>
          <Badge tone="violet">{comparison.length}/3 selected</Badge>
        </Card>
      )}

      <div className="overflow-hidden rounded-lg border bg-card/80">
        <div className="hidden grid-cols-[72px_1.4fr_0.9fr_1fr_130px_160px] gap-4 border-b bg-muted/40 px-4 py-3 text-xs font-bold uppercase text-muted-foreground lg:grid">
          <div>Rank</div>
          <div>Candidate Profile</div>
          <div>Future Score</div>
          <div>AI Explainability Rationale</div>
          <div>Future Vectors</div>
          <div>Actions</div>
        </div>
        
        {filtered.map((candidate, index) => {
          // Resolve scores and twin defaults
          const dna = candidate.candidate_dna || { learning: 0.75, stability: 0.85, leadership: 0.70 };
          const dnaMatch = candidate.dna_match || { organization_match: 0.80 };
          
          const fScore = candidate.score || 85;
          const currFit = candidate.current_fit || candidate.score || 80;
          const futFit = Math.round(dnaMatch.organization_match * 100);
          
          const learnVel = dna.learning;
          const learnLabel = learnVel >= 0.75 ? "FAST" : "STEADY";
          const promoProb = Math.round(dna.leadership * 100);
          const retentionProb = Math.round(dna.stability * 100);

          return (
            <div 
              key={candidate.id} 
              className="grid gap-4 border-b p-4 last:border-b-0 lg:grid-cols-[72px_1.4fr_0.9fr_1fr_130px_160px] lg:items-center hover:bg-muted/10 transition-colors"
            >
              <div className="text-2xl font-extrabold text-primary">#{index + 1}</div>
              
              <div>
                <div className="text-lg font-extrabold">{candidate.name}</div>
                <div className="text-sm font-semibold text-muted-foreground">
                  {candidate.role} · <span className="text-primary">{candidate.company}</span>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {(candidate.skills || []).slice(0, 5).map((skill) => (
                    <Badge key={skill} tone="blue" className="text-[10px]">{skill}</Badge>
                  ))}
                </div>
              </div>
              
              <div>
                <div className="text-3xl font-extrabold text-white">{fScore}%</div>
                <div className="text-xs text-muted-foreground mt-0.5">
                  Fit: {currFit}% → Proj: {futFit}%
                </div>
              </div>
              
              <p className="text-xs leading-5 text-muted-foreground font-medium">
                {candidate.reasoning}
              </p>
              
              <div className="space-y-1.5 text-xs text-muted-foreground font-semibold">
                <div className="flex items-center gap-1.5">
                  <Zap size={12} className="text-yellow-400" />
                  <span>Learn: <b className="text-white">{learnLabel}</b></span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Clock size={12} className="text-emerald-400" />
                  <span>Retain: <b className="text-white">{retentionProb}%</b></span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Shield size={12} className="text-indigo-400" />
                  <span>Promo: <b className="text-white">{promoProb}%</b></span>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                <Button 
                  variant="outline" 
                  size="icon" 
                  onClick={() => toggleShortlist(candidate.id)} 
                  aria-label="Shortlist"
                >
                  <Star size={17} className={shortlisted.has(candidate.id) ? "fill-amber-400 text-amber-400" : ""} />
                </Button>
                <Button 
                  variant="outline" 
                  size="icon" 
                  onClick={() => toggleComparison(candidate.id)} 
                  aria-label="Compare"
                >
                  <GitCompare size={17} className={comparison.includes(candidate.id) ? "text-primary" : ""} />
                </Button>
                <Link to={`/candidates/${candidate.id}`}>
                  <Button size="icon" aria-label="View profile"><Eye size={17} /></Button>
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
