import { motion } from "framer-motion";
import { BarChart3, TrendingUp, Users, Shield, Zap, Activity } from "lucide-react";
import { Card, KPICard } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import {
  ResponsiveContainer, AreaChart, Area, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, Tooltip, CartesianGrid, RadarChart, PolarGrid,
  PolarAngleAxis, Radar, PieChart, Pie, Cell
} from "recharts";

const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const PERF_DATA = MONTHS.slice(0, 8).map((m, i) => ({
  month: m,
  candidates: 200 + i * 40 + Math.round(Math.random() * 30),
  hires: 18 + i * 3,
  quality: 78 + i * 2,
}));

const SKILL_DATA = [
  { skill: "Python",     count: 820 },
  { skill: "React",      count: 640 },
  { skill: "AWS",        count: 590 },
  { skill: "Docker",     count: 510 },
  { skill: "ML/AI",      count: 480 },
  { skill: "Kubernetes", count: 380 },
  { skill: "FastAPI",    count: 320 },
  { skill: "LLMs",       count: 290 },
];

const RISK_DATA = [
  { name: "Low Risk",    value: 58, color: "#10B981" },
  { name: "Medium Risk", value: 27, color: "#F59E0B" },
  { name: "High Risk",   value: 15, color: "#EF4444" },
];

const FUNNEL_DATA = [
  { stage: "Screened",   value: 100 },
  { stage: "Qualified",  value: 72 },
  { stage: "Technical",  value: 48 },
  { stage: "Interview",  value: 31 },
  { stage: "Offer",      value: 18 },
  { stage: "Hired",      value: 12 },
];

const RADAR_ORG = [
  { subject: "Innovation",   A: 88 },
  { subject: "Stability",    A: 76 },
  { subject: "Leadership",   A: 82 },
  { subject: "Collaboration",A: 91 },
  { subject: "Speed",        A: 74 },
  { subject: "Diversity",    A: 69 },
];

const TT = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border p-3 text-xs"
      style={{ background: "var(--tm-bg-elevated)", borderColor: "var(--tm-border)", color: "white", minWidth: 120 }}>
      <div className="font-semibold mb-1.5">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="flex items-center gap-1.5 mb-0.5">
          <div className="w-2 h-2 rounded-full" style={{ background: p.color }} />
          <span style={{ color: "rgba(255,255,255,0.5)" }}>{p.name}:</span>
          <span className="font-semibold">{p.value}</span>
        </div>
      ))}
    </div>
  );
};

export function Analytics() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-[22px] font-extrabold text-white tracking-tight">Workforce Analytics</h1>
        <p className="text-[12px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>
          8-month performance intelligence · 50 candidates active
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "Total Analyzed",    value: "50",   delta: "12%",  deltaPositive: true,  icon: Users,      accent: "blue"   },
          { label: "Avg Quality Score", value: "86.4", delta: "3.2%", deltaPositive: true,  icon: TrendingUp, accent: "emerald"},
          { label: "Retention Forecast",value: "91%",  delta: "1.8%", deltaPositive: true,  icon: Shield,     accent: "violet" },
          { label: "High-Risk Flags",   value: "7",    delta: "2",    deltaPositive: false, icon: Zap,        accent: "rose"   },
        ].map((kpi, i) => (
          <motion.div key={kpi.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}>
            <KPICard {...kpi} />
          </motion.div>
        ))}
      </div>

      {/* Charts row 1 */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Performance trend */}
        <div className="lg:col-span-2 card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="text-[13px] font-bold text-white">Hiring Performance</div>
              <div className="text-[11px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>Candidates vs. quality score</div>
            </div>
            <Badge tone="blue">8M</Badge>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={PERF_DATA} margin={{ top: 4, right: 4, left: -28, bottom: 0 }}>
                <defs>
                  <linearGradient id="aCand" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#2563EB" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="aQual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#7C3AED" stopOpacity={0.25} />
                    <stop offset="100%" stopColor="#7C3AED" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="month" tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip content={<TT />} />
                <Area type="monotone" dataKey="candidates" stroke="#2563EB" strokeWidth={2} fill="url(#aCand)" name="Candidates" />
                <Area type="monotone" dataKey="quality"    stroke="#7C3AED" strokeWidth={2} fill="url(#aQual)" name="Quality %" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution Pie */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Risk Distribution</div>
            <Badge tone="amber">Attrition</Badge>
          </div>
          <div className="h-40 mb-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={RISK_DATA} cx="50%" cy="50%" innerRadius={44} outerRadius={68}
                  paddingAngle={3} dataKey="value">
                  {RISK_DATA.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: "var(--tm-bg-elevated)", border: "1px solid var(--tm-border)", borderRadius: 8, fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2">
            {RISK_DATA.map((item) => (
              <div key={item.name} className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: item.color }} />
                <span className="text-[11px] flex-1" style={{ color: "var(--tm-text-secondary)" }}>{item.name}</span>
                <span className="text-[12px] font-bold text-white">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Skill Demand */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Top Skills</div>
            <Badge tone="cyan">Demand</Badge>
          </div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={SKILL_DATA} layout="vertical" margin={{ top: 0, right: 8, left: 0, bottom: 0 }}>
                <XAxis type="number" tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 9 }} axisLine={false} tickLine={false} />
                <YAxis dataKey="skill" type="category" tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 10 }} axisLine={false} tickLine={false} width={72} />
                <Tooltip content={<TT />} />
                <Bar dataKey="count" fill="#0EA5E9" radius={[0, 4, 4, 0]} name="Candidates" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Hiring Funnel */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Conversion Funnel</div>
            <Badge tone="violet">Stages</Badge>
          </div>
          <div className="space-y-2.5">
            {FUNNEL_DATA.map((item, i) => (
              <div key={item.stage}>
                <div className="flex justify-between text-[11px] mb-1">
                  <span style={{ color: "var(--tm-text-secondary)" }}>{item.stage}</span>
                  <span className="font-bold text-white">{item.value}%</span>
                </div>
                <div className="progress-bar">
                  <motion.div
                    className="progress-fill"
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value}%` }}
                    transition={{ duration: 0.8, delay: i * 0.1 }}
                    style={{ background: `hsl(${230 + i * 15} 70% 55%)` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Org DNA Radar */}
        <div className="card-enterprise">
          <div className="flex items-center justify-between mb-4">
            <div className="text-[13px] font-bold text-white">Org DNA Profile</div>
            <Badge tone="emerald">Culture</Badge>
          </div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={RADAR_ORG}>
                <PolarGrid stroke="rgba(255,255,255,0.06)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 9 }} />
                <Radar dataKey="A" stroke="#10B981" fill="#10B981" fillOpacity={0.2} strokeWidth={2} />
                <Tooltip contentStyle={{ background: "var(--tm-bg-elevated)", border: "1px solid var(--tm-border)", borderRadius: 8, fontSize: 11 }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
