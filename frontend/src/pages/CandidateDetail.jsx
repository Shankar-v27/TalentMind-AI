import { useParams } from "react-router-dom";
import { Download, Hash, Mail, MapPin, ShieldCheck } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { ProgressRing } from "../components/ui/ProgressRing";
import { scoreBreakdown, timeline } from "../data/mockData";
import { useTalentMindStore } from "../state/useTalentMindStore";

export function CandidateDetail() {
  const { id } = useParams();
  const candidates = useTalentMindStore((state) => state.candidates);
  const candidate = candidates.find((item) => item.id === id) || candidates[0];

  return (
    <div className="space-y-6">
      <Card className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
          <ProgressRing value={candidate.score} label="Overall" />
          <div>
            <Badge tone="green">AI Candidate Intelligence Report</Badge>
            <h2 className="mt-3 text-3xl font-extrabold">{candidate.name}</h2>
            <p className="mt-1 font-semibold text-muted-foreground">{candidate.role} · {candidate.company}</p>
            <div className="mt-3 flex flex-wrap gap-3 text-sm text-muted-foreground">
              <span className="inline-flex items-center gap-1"><Hash size={15} /> Candidate ID {candidate.id}</span>
              <span className="inline-flex items-center gap-1"><MapPin size={15} /> {candidate.location}</span>
              <span className="inline-flex items-center gap-1"><ShieldCheck size={15} /> Trust {candidate.trust}</span>
              <span className="inline-flex items-center gap-1"><Mail size={15} /> Response ready</span>
            </div>
          </div>
        </div>
        <Button onClick={() => window.print()}><Download size={18} /> Export PDF</Button>
      </Card>
      <section className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr]">
        <Card>
          <h3 className="mb-4 text-lg font-extrabold">Score breakdown</h3>
          <div className="space-y-4">
            {scoreBreakdown.map((item) => (
              <div key={item.name}>
                <div className="mb-1 flex justify-between text-sm font-semibold"><span>{item.name}</span><span>{item.value}%</span></div>
                <div className="h-2 rounded-full bg-muted"><div className="h-2 rounded-full bg-gradient-to-r from-blue-600 to-violet-600" style={{ width: `${item.value}%` }} /></div>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <h3 className="mb-3 text-lg font-extrabold">AI-generated reasoning</h3>
          <p className="leading-7 text-muted-foreground">{candidate.reasoning} The candidate demonstrates a balanced mix of technical depth, recent activity, verification quality, and recruiter-friendly responsiveness.</p>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            {["Open to work", "Hybrid / Remote", "Willing to relocate"].map((signal) => <div key={signal} className="rounded-lg bg-muted/45 p-3 text-sm font-bold">{signal}</div>)}
          </div>
        </Card>
      </section>
      <section className="grid gap-5 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <h3 className="mb-4 text-lg font-extrabold">Career timeline</h3>
          <div className="space-y-4">
            {timeline.map((item) => (
              <div key={item.company} className="border-l-2 border-primary/40 pl-4">
                <div className="font-bold">{item.title}</div>
                <div className="text-sm text-muted-foreground">{item.company} · {item.period}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <h3 className="mb-4 text-lg font-extrabold">Education</h3>
          <div className="font-bold">B.Tech, Computer Science</div>
          <div className="text-sm text-muted-foreground">Indian Institute of Technology · Tier 1</div>
          <h3 className="mb-3 mt-6 text-lg font-extrabold">Skills</h3>
          <div className="flex flex-wrap gap-2">{candidate.skills.map((skill) => <Badge key={skill} tone="violet">{skill}</Badge>)}</div>
        </Card>
      </section>
      <Card>
        <h3 className="mb-4 text-lg font-extrabold">Behavioral intelligence</h3>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {[
            ["Recruiter response", "92%"],
            ["Interview completion", "88%"],
            ["Offer acceptance", "74%"],
            ["Profile activity", "High"],
            ["Open-to-work", "Verified"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-lg bg-muted/45 p-4">
              <div className="text-xs font-bold uppercase text-muted-foreground">{label}</div>
              <div className="mt-1 text-xl font-extrabold">{value}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
