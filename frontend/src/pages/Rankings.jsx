import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Filter, SortAsc, ChevronRight, Star, Shield, Zap,
  TrendingUp, Users, RefreshCw, Search, BarChart2,
  ArrowUpRight, Check, AlertCircle, Clock, Target
} from "lucide-react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { useTalentMindStore } from "../state/useTalentMindStore";
import { api } from "../services/api";
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from "recharts";

const SCORE_COLOR = (s) => {
  if (s >= 90) return "#10B981";
  if (s >= 80) return "#2563EB";
  if (s >= 70) return "#F59E0B";
  return "#EF4444";
};

const SCORE_TONE = (s) => {
  if (s >= 90) return "emerald";
  if (s >= 80) return "blue";
  if (s >= 70) return "amber";
  return "rose";
};

function ScoreRing({ score, size = 48 }) {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const fill = circ - (score / 100) * circ;
  const color = SCORE_COLOR(score);
  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={5} />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color}
          strokeWidth={5} strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" style={{ transition: "stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)" }} />
      </svg>
      <span className="absolute text-[11px] font-extrabold" style={{ color }}>{score}</span>
    </div>
  );
}

function StatPill({ icon: Icon, value, label, color }) {
  return (
    <div className="flex items-center gap-1.5">
      <Icon size={10} style={{ color }} />
      <span className="text-[11px] font-semibold" style={{ color }}>{value}</span>
      <span className="text-[10px]" style={{ color: "var(--tm-text-muted)" }}>{label}</span>
    </div>
  );
}

function CandidateCard({ candidate, index, selected, onSelect }) {
  const score = candidate.score ?? 85;
  const scoreColor = SCORE_COLOR(score);
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ delay: index * 0.04, duration: 0.28 }}
      onClick={() => onSelect(candidate)}
      className="group relative rounded-xl border cursor-pointer transition-all duration-250"
      style={{
        background: selected
          ? "linear-gradient(135deg, rgba(37,99,235,0.08), rgba(124,58,237,0.05))"
          : "var(--tm-bg-surface)",
        borderColor: selected ? "rgba(37,99,235,0.45)" : "var(--tm-border)",
        boxShadow: selected ? "0 4px 24px rgba(37,99,235,0.15)" : "none",
      }}
    >
      {selected && (
        <div className="absolute left-0 top-3 bottom-3 w-0.5 rounded-r" style={{ background: "#2563EB" }} />
      )}
      <div className="p-4">
        <div className="flex items-start gap-3">
          {/* Rank */}
          <div className="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-bold"
            style={{
              background: index < 3 ? `${scoreColor}18` : "rgba(255,255,255,0.04)",
              color: index < 3 ? scoreColor : "rgba(255,255,255,0.35)",
            }}>
            #{index + 1}
          </div>

          {/* Avatar */}
          <div
            className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold text-white"
            style={{ background: `hsl(${(index * 53 + 210) % 360} 65% 45%)` }}
          >
            {(candidate.name ?? "C").charAt(0)}
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-[13px] font-bold text-white truncate">{candidate.name ?? `Candidate ${index + 1}`}</span>
              {index < 3 && <Star size={10} style={{ color: "#F59E0B" }} fill="#F59E0B" />}
            </div>
            <div className="text-[11px] mt-0.5 truncate" style={{ color: "var(--tm-text-muted)" }}>
              {candidate.role ?? "Software Engineer"} · {candidate.experience ?? (3 + index)} yrs
            </div>
          </div>

          {/* Score */}
          <ScoreRing score={score} size={44} />
        </div>

        {/* Stats row */}
        <div className="mt-3 grid grid-cols-3 gap-2 pt-3 border-t" style={{ borderColor: "var(--tm-border)" }}>
          <StatPill icon={Shield}   value={`${candidate.retention_probability ? Math.round(candidate.retention_probability * 100) : 88}%`}  label="retain"  color="#6EE7B7" />
          <StatPill icon={TrendingUp} value={`${candidate.future_score ?? 86}%`} label="future" color="#C4B5FD" />
          <StatPill icon={Zap}      value={`${candidate.learning_velocity ? Math.round(candidate.learning_velocity * 100) : 74}%`} label="velocity" color="#67E8F9" />
        </div>

        {/* Skills */}
        {candidate.skills_matched && candidate.skills_matched.length > 0 && (
          <div className="mt-2.5 flex flex-wrap gap-1">
            {candidate.skills_matched.slice(0, 3).map((sk) => (
              <span key={sk} className="pill pill-blue" style={{ fontSize: 9, padding: "1px 5px" }}>
                {sk}
              </span>
            ))}
            {candidate.skills_matched.length > 3 && (
              <span className="text-[9px] font-semibold" style={{ color: "var(--tm-text-muted)" }}>
                +{candidate.skills_matched.length - 3}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Hover action */}
      <div
        className="absolute right-3 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity"
      >
        <ChevronRight size={14} style={{ color: "#2563EB" }} />
      </div>
    </motion.div>
  );
}

function RightPanel({ candidate }) {
  if (!candidate) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <div className="w-16 h-16 rounded-2xl mb-5 flex items-center justify-center"
          style={{ background: "rgba(37,99,235,0.08)", border: "1px solid rgba(37,99,235,0.15)" }}>
          <Users size={24} style={{ color: "#2563EB" }} />
        </div>
        <div className="font-semibold text-white mb-2">Select a candidate</div>
        <p className="text-sm" style={{ color: "var(--tm-text-muted)" }}>
          Click any candidate to view their AI analysis, scores, and recommendations.
        </p>
      </div>
    );
  }

  const score = candidate.score ?? 85;
  const radarData = [
    { subject: "Skills",     A: candidate.skill_match_score ?? 88 },
    { subject: "Experience", A: Math.min((candidate.experience ?? 4) * 10, 100) },
    { subject: "Leadership", A: candidate.leadership_score ?? 72 },
    { subject: "Future",     A: candidate.future_score ?? 85 },
    { subject: "Retention",  A: candidate.retention_probability ? Math.round(candidate.retention_probability * 100) : 89 },
    { subject: "Culture",    A: candidate.culture_fit ?? 80 },
  ];

  return (
    <motion.div
      key={candidate.candidate_id}
      initial={{ opacity: 0, x: 12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.24 }}
      className="h-full overflow-y-auto p-5 space-y-4"
      style={{ scrollbarWidth: "none" }}
    >
      {/* Header */}
      <div className="flex items-start gap-4">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center text-xl font-extrabold text-white flex-shrink-0"
          style={{ background: "linear-gradient(135deg, #2563EB, #7C3AED)" }}
        >
          {(candidate.name ?? "C").charAt(0)}
        </div>
        <div className="flex-1">
          <div className="font-extrabold text-white text-[17px] tracking-tight">{candidate.name}</div>
          <div className="text-[12px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>
            {candidate.role ?? "Engineer"} · {candidate.location ?? "India"}
          </div>
          <div className="flex items-center gap-2 mt-2">
            <Badge tone={SCORE_TONE(score)}>{score} / 100</Badge>
            <span className="status-dot live" />
            <span className="text-[11px]" style={{ color: "#6EE7B7" }}>Active</span>
          </div>
        </div>
      </div>

      {/* Radar */}
      <div className="rounded-xl border p-4" style={{ background: "var(--tm-bg-elevated)", borderColor: "var(--tm-border)" }}>
        <div className="text-[12px] font-bold text-white mb-3">Competency Radar</div>
        <div className="h-44">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(255,255,255,0.06)" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 10 }} />
              <Radar dataKey="A" stroke="#2563EB" fill="#2563EB" fillOpacity={0.2} strokeWidth={2} />
              <Tooltip contentStyle={{ background: "var(--tm-bg-elevated)", border: "1px solid var(--tm-border)", borderRadius: 8 }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Reasoning */}
      {candidate.reasoning && (
        <div className="rounded-xl border p-4" style={{ background: "rgba(37,99,235,0.05)", borderColor: "rgba(37,99,235,0.15)" }}>
          <div className="flex items-center gap-2 mb-2">
            <Zap size={12} style={{ color: "#60A5FA" }} />
            <div className="text-[11px] font-bold" style={{ color: "#60A5FA" }}>AI Reasoning</div>
          </div>
          <p className="text-[12px] leading-5" style={{ color: "rgba(255,255,255,0.7)" }}>
            {candidate.reasoning}
          </p>
        </div>
      )}

      {/* Score breakdown */}
      <div className="space-y-2.5">
        {[
          { label: "Skill Match",   value: candidate.skill_match_score ?? 88, color: "#2563EB" },
          { label: "Future Potential", value: candidate.future_score ?? 85,   color: "#7C3AED" },
          { label: "Retention",     value: candidate.retention_probability ? Math.round(candidate.retention_probability * 100) : 89, color: "#10B981" },
          { label: "Leadership",    value: candidate.leadership_score ?? 72,  color: "#0EA5E9" },
        ].map((item) => (
          <div key={item.label}>
            <div className="flex justify-between text-[11px] mb-1">
              <span style={{ color: "var(--tm-text-secondary)" }}>{item.label}</span>
              <span className="font-bold text-white">{item.value}%</span>
            </div>
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${item.value}%` }}
                transition={{ duration: 0.8, delay: 0.1 }}
                style={{ background: item.color }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* View full profile CTA */}
      <Link to={`/candidates/${candidate.candidate_id ?? candidate.id ?? "1"}`} className="block">
        <button className="btn btn-primary w-full text-sm">
          Full Profile <ArrowUpRight size={13} />
        </button>
      </Link>
    </motion.div>
  );
}

export function Rankings() {
  const { candidates, jdAnalysis, setRankedCandidates } = useTalentMindStore();
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);
  const [search, setSearch] = useState("");

  const filtered = candidates.filter(c =>
    !search || (c.name ?? "").toLowerCase().includes(search.toLowerCase()) ||
    (c.role ?? "").toLowerCase().includes(search.toLowerCase())
  );

  const handleRank = async () => {
    setLoading(true);
    try {
      const data = await api.rankCandidates(jdAnalysis);
      setRankedCandidates(data.ranked_candidates ?? []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-[22px] font-extrabold text-white tracking-tight">Candidate Rankings</h1>
          <p className="text-[12px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>
            {filtered.length} candidates · AI-ranked by multi-signal scoring
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="btn btn-ghost btn-sm">
            <Filter size={13} /> Filter
          </button>
          <button className="btn btn-ghost btn-sm">
            <SortAsc size={13} /> Sort
          </button>
          <button
            className="btn btn-primary btn-sm"
            onClick={handleRank}
            disabled={loading}
          >
            <RefreshCw size={13} className={loading ? "animate-spin" : ""} />
            {loading ? "Ranking…" : "Re-rank AI"}
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: "var(--tm-text-muted)" }} />
        <input
          className="input-enterprise pl-8"
          placeholder="Search candidates by name, role, skills…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Empty state */}
      {filtered.length === 0 && !loading && (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="w-16 h-16 rounded-2xl mb-5 flex items-center justify-center"
            style={{ background: "rgba(37,99,235,0.08)", border: "1px solid rgba(37,99,235,0.15)" }}>
            <Users size={24} style={{ color: "#2563EB" }} />
          </div>
          <div className="font-bold text-white mb-2">No candidates ranked yet</div>
          <p className="text-sm mb-5" style={{ color: "var(--tm-text-muted)" }}>
            Run a JD analysis first, then click Re-rank AI.
          </p>
          <Link to="/job-analysis">
            <button className="btn btn-primary">Start JD Analysis <ArrowUpRight size={13} /></button>
          </Link>
        </div>
      )}

      {/* Main split layout */}
      {filtered.length > 0 && (
        <div className="grid gap-4 lg:grid-cols-[1fr_340px] flex-1 min-h-0">
          {/* Left: candidate list */}
          <div className="space-y-2 overflow-y-auto" style={{ maxHeight: "72vh", scrollbarWidth: "none" }}>
            <AnimatePresence>
              {filtered.map((c, i) => (
                <CandidateCard
                  key={c.candidate_id ?? i}
                  candidate={c}
                  index={i}
                  selected={selected?.candidate_id === c.candidate_id}
                  onSelect={setSelected}
                />
              ))}
            </AnimatePresence>
          </div>

          {/* Right: detail panel */}
          <div
            className="rounded-xl border sticky top-4"
            style={{
              background: "var(--tm-bg-surface)",
              borderColor: "var(--tm-border)",
              height: "fit-content",
              maxHeight: "72vh",
              overflowY: "auto",
            }}
          >
            <RightPanel candidate={selected} />
          </div>
        </div>
      )}
    </div>
  );
}
