import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight, Users, Zap, TrendingUp, Shield, Target,
  BrainCircuit, Clock, Sliders, Network, BarChart3,
  ChevronRight, Activity, Star, Sparkles, AlertCircle,
  CheckCircle2, GitBranch
} from "lucide-react";
import { Card, KPICard } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { useTalentMindStore } from "../state/useTalentMindStore";
import {
  ResponsiveContainer, AreaChart, Area, LineChart, Line,
  XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar
} from "recharts";

/* ── Animated counter ── */
function AnimatedNumber({ value, suffix = "", prefix = "", duration = 1800 }) {
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    const start = Date.now();
    const target = parseFloat(String(value).replace(/[^0-9.]/g, "")) || 0;
    const tick = () => {
      const elapsed = Date.now() - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(eased * target * 10) / 10);
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [value, duration]);
  return <span>{prefix}{typeof value === "string" && value.includes(".") ? display.toFixed(1) : Math.round(display)}{suffix}</span>;
}

const KPIS = [
  { label: "Total Candidates", value: "100,000", delta: "12.4%", deltaPositive: true, icon: Users, accent: "blue", sublabel: "In active pipeline" },
  { label: "Avg. Match Score", value: "86.4%", delta: "3.2%", deltaPositive: true, icon: Target, accent: "emerald", sublabel: "AI-weighted scoring" },
  { label: "Retention Forecast", value: "91.2%", delta: "1.8%", deltaPositive: true, icon: Shield, accent: "violet", sublabel: "12-month prediction" },
  { label: "Prediction Accuracy", value: "95%", delta: "0.5%", deltaPositive: true, icon: Zap, accent: "cyan", sublabel: "Model confidence" },
  { label: "Active JD Analysis", value: "47", delta: "8", deltaPositive: true, icon: BrainCircuit, accent: "amber", sublabel: "Jobs running now" },
  { label: "Hiring Risk Score", value: "14.3%", delta: "2.1%", deltaPositive: false, icon: AlertCircle, accent: "rose", sublabel: "Avg. across pipeline" },
];

const TREND_DATA = [
  { month: "Jan", hired: 24, rejected: 12, score: 81 },
  { month: "Feb", hired: 31, rejected: 9,  score: 83 },
  { month: "Mar", hired: 28, rejected: 15, score: 80 },
  { month: "Apr", hired: 42, rejected: 8,  score: 87 },
  { month: "May", hired: 38, rejected: 11, score: 85 },
  { month: "Jun", hired: 55, rejected: 7,  score: 91 },
  { month: "Jul", hired: 61, rejected: 6,  score: 92 },
];

const RETENTION_DATA = [
  { month: "Jan", retention: 88 }, { month: "Feb", retention: 89 },
  { month: "Mar", retention: 87 }, { month: "Apr", retention: 91 },
  { month: "May", retention: 90 }, { month: "Jun", retention: 93 },
  { month: "Jul", retention: 95 },
];

const PIPELINE_DATA = [
  { stage: "Applied",      count: 4820 },
  { stage: "Screened",     count: 1240 },
  { stage: "Technical",    count: 480 },
  { stage: "Interview",    count: 210 },
  { stage: "Offer",        count: 88 },
  { stage: "Hired",        count: 61 },
];

const MODULES = [
  { to: "/job-analysis",     label: "JD Analysis",       desc: "AI-powered job description parsing",    icon: BrainCircuit, accent: "#2563EB", glow: "rgba(37,99,235,0.3)"  },
  { to: "/rankings",         label: "Candidate Ranking",  desc: "Multi-signal scoring & ranking engine", icon: Users,        accent: "#7C3AED", glow: "rgba(124,58,237,0.3)" },
  { to: "/time-machine",     label: "Time Machine",       desc: "Live scenario simulator",               icon: Clock,        accent: "#0EA5E9", glow: "rgba(14,165,233,0.3)"  },
  { to: "/optimizer",        label: "MOHO Optimizer",     desc: "Multi-objective Pareto optimization",   icon: Sliders,      accent: "#10B981", glow: "rgba(16,185,129,0.3)"  },
  { to: "/recruiter-memory", label: "Memory Graph",       desc: "Recruiter behavior intelligence",       icon: Network,      accent: "#F59E0B", glow: "rgba(245,158,11,0.3)"  },
  { to: "/analytics",        label: "Analytics",          desc: "Workforce intelligence reports",        icon: BarChart3,    accent: "#EF4444", glow: "rgba(239,68,68,0.25)"   },
];

const RECENT_ACTIVITY = [
  { action: "Candidate ranked #1", subject: "Aarav Sharma", time: "2m ago", type: "success" },
  { action: "JD analyzed",          subject: "Senior ML Engineer", time: "8m ago", type: "info" },
  { action: "High retention alert", subject: "Meera Kapoor — 94%", time: "15m ago", type: "success" },
  { action: "Risk flag raised",      subject: "Ghosting risk: Raj Verma", time: "23m ago", type: "warning" },
  { action: "Optimization run",     subject: "MOHO → 3 Pareto solutions", time: "41m ago", type: "info" },
];

const TYPE_COLORS = {
  success: { color: "#6EE7B7", icon: CheckCircle2 },
  info:    { color: "#60A5FA", icon: Activity },
  warning: { color: "#FCD34D", icon: AlertCircle },
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border p-3 text-xs"
      style={{ background: "var(--tm-bg-elevated)", borderColor: "var(--tm-border)", color: "white" }}>
      <div className="font-semibold mb-1">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full" style={{ background: p.color }} />
          <span style={{ color: "rgba(255,255,255,0.6)" }}>{p.name}:</span>
          <span className="font-semibold">{p.value}</span>
        </div>
      ))}
    </div>
  );
};

export function Dashboard() {
  const candidates = useTalentMindStore((state) => state.candidates);

  return (
    <div className="space-y-6">

      {/* ─── PAGE HEADER ─── */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="status-dot live" />
            <span className="text-xs font-semibold" style={{ color: "#6EE7B7" }}>All systems operational</span>
          </div>
          <h1 className="text-[28px] font-extrabold text-white tracking-tight leading-tight">
            Command Center
          </h1>
          <p className="mt-1 text-sm" style={{ color: "var(--tm-text-secondary)" }}>
            Human capital intelligence at a glance
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link to="/job-analysis">
            <button className="btn btn-ghost btn-sm">
              New Analysis
            </button>
          </Link>
          <Link to="/rankings">
            <button className="btn btn-primary btn-sm">
              View Rankings <ArrowRight size={13} />
            </button>
          </Link>
        </div>
      </div>

      {/* ─── KPI GRID ─── */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
        {KPIS.map((kpi, i) => (
          <motion.div
            key={kpi.label}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06, duration: 0.35 }}
          >
            <KPICard {...kpi} />
          </motion.div>
        ))}
      </div>

      {/* ─── CHARTS ROW ─── */}
      <div className="grid gap-4 lg:grid-cols-3">

        {/* Hiring Trends */}
        <div className="lg:col-span-2 card-enterprise">
          <div className="flex items-center justify-between mb-5">
            <div>
              <div className="text-[13px] font-bold text-white">Hiring Trends</div>
              <div className="text-[11px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>Monthly hired vs. rejected</div>
            </div>
            <Badge tone="emerald">7-month</Badge>
          </div>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={TREND_DATA} margin={{ top: 4, right: 4, left: -24, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradHired" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#2563EB" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gradRejected" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#EF4444" stopOpacity={0.2} />
                    <stop offset="100%" stopColor="#EF4444" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="month" tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="hired"    stroke="#2563EB" strokeWidth={2} fill="url(#gradHired)"    name="Hired" />
                <Area type="monotone" dataKey="rejected" stroke="#EF4444" strokeWidth={2} fill="url(#gradRejected)" name="Rejected" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Retention */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-5">
            <div>
              <div className="text-[13px] font-bold text-white">Retention Rate</div>
              <div className="text-[11px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>AI-predicted 12-mo</div>
            </div>
            <Badge tone="violet">Forecast</Badge>
          </div>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={RETENTION_DATA} margin={{ top: 4, right: 4, left: -24, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="month" tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis domain={[80, 100]} tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="retention" stroke="#7C3AED" strokeWidth={2.5}
                  dot={{ fill: "#7C3AED", strokeWidth: 0, r: 4 }} name="Retention %" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* ─── PIPELINE + ACTIVITY ─── */}
      <div className="grid gap-4 lg:grid-cols-3">

        {/* Pipeline Funnel */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Hiring Pipeline</div>
            <Badge tone="blue">Funnel</Badge>
          </div>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={PIPELINE_DATA} layout="vertical" margin={{ top: 0, right: 8, left: 0, bottom: 0 }}>
                <XAxis type="number" tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 9 }} axisLine={false} tickLine={false} />
                <YAxis dataKey="stage" type="category" tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 10 }} axisLine={false} tickLine={false} width={66} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" fill="#2563EB" radius={[0, 4, 4, 0]} name="Candidates" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Activity Feed */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Recent Activity</div>
            <span className="status-dot live" />
          </div>
          <div className="space-y-3">
            {RECENT_ACTIVITY.map((item, i) => {
              const meta = TYPE_COLORS[item.type];
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.07 }}
                  className="flex items-start gap-3"
                >
                  <div
                    className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center"
                    style={{ background: `${meta.color}18` }}
                  >
                    <meta.icon size={11} style={{ color: meta.color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-[11px] font-semibold text-white truncate">{item.action}</div>
                    <div className="text-[10px] mt-0.5 truncate" style={{ color: "var(--tm-text-muted)" }}>{item.subject}</div>
                  </div>
                  <div className="text-[10px] flex-shrink-0" style={{ color: "var(--tm-text-muted)" }}>{item.time}</div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Top Candidates quick list */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Top Candidates</div>
            <Link to="/rankings">
              <button className="btn btn-ghost btn-sm text-[11px]">View all <ChevronRight size={11} /></button>
            </Link>
          </div>
          <div className="space-y-2">
            {(candidates.length > 0 ? candidates.slice(0, 5) : FALLBACK_CANDIDATES).map((c, i) => (
              <motion.div
                key={c.candidate_id ?? i}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="flex items-center gap-3 p-2.5 rounded-lg border transition-all hover:border-blue-500/20 cursor-pointer"
                style={{ borderColor: "var(--tm-border)", background: "rgba(255,255,255,0.02)" }}
              >
                <div
                  className="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                  style={{ background: `hsl(${(i * 47 + 210) % 360} 70% 50%)` }}
                >
                  {(c.name ?? "C").charAt(0)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[12px] font-semibold text-white truncate">{c.name ?? `Candidate ${i + 1}`}</div>
                  <div className="text-[10px] truncate" style={{ color: "var(--tm-text-muted)" }}>{c.role ?? "Engineer"}</div>
                </div>
                <div
                  className="text-[13px] font-extrabold flex-shrink-0"
                  style={{ color: "#60A5FA" }}
                >
                  {c.score ?? (88 - i * 2)}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* ─── MODULE GRID ─── */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-[14px] font-bold text-white">Intelligence Modules</h2>
          <span className="text-[11px]" style={{ color: "var(--tm-text-muted)" }}>6 AI engines active</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
          {MODULES.map((mod, i) => (
            <Link key={mod.to} to={mod.to}>
              <motion.div
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className="group p-4 rounded-xl border cursor-pointer transition-all duration-300 hover:-translate-y-1"
                style={{
                  background: "var(--tm-bg-surface)",
                  borderColor: "var(--tm-border)",
                }}
                whileHover={{ boxShadow: `0 8px 32px ${mod.glow}` }}
              >
                <div
                  className="w-9 h-9 rounded-lg flex items-center justify-center mb-3 transition-transform duration-300 group-hover:scale-110"
                  style={{ background: `${mod.accent}18`, color: mod.accent }}
                >
                  <mod.icon size={17} />
                </div>
                <div className="text-[12px] font-bold text-white leading-tight mb-1">{mod.label}</div>
                <div className="text-[10px] leading-tight" style={{ color: "var(--tm-text-muted)" }}>{mod.desc}</div>
              </motion.div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

const FALLBACK_CANDIDATES = [
  { name: "Aarav Sharma",   role: "ML Engineer",       score: 94 },
  { name: "Meera Kapoor",   role: "Backend Engineer",  score: 91 },
  { name: "Neha Rao",       role: "Data Scientist",    score: 89 },
  { name: "Vikram Singh",   role: "DevOps Lead",       score: 87 },
  { name: "Divya Menon",    role: "AI Researcher",     score: 85 },
];
