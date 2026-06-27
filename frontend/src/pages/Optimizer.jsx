import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Sparkles, RefreshCw, Sliders, ArrowRight, TrendingUp, ShieldAlert, Zap, 
  UserCheck, CheckCircle2, AlertTriangle, Play, ChevronRight, Compass, 
  DollarSign, Calendar, Star, Users, Award, Percent, Activity
} from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { 
  ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Cell, 
  LineChart, Line, ScatterChart, Scatter, LabelList
} from "recharts";

export function Optimizer() {
  // Constraints
  const [maxSalary, setMaxSalary] = useState(35);
  const [maxJoining, setMaxJoining] = useState(60);
  const [minExp, setMinExp] = useState(3);
  const [requiredSkills, setRequiredSkills] = useState(["python", "aws"]);
  const [skillInput, setSkillInput] = useState("");

  // Strategy & Presets
  const [strategy, setStrategy] = useState("future_growth");
  const [scenarioId, setScenarioId] = useState("startup");

  // Output states
  const [recommended, setRecommended] = useState(null);
  const [paretoFrontier, setParetoFrontier] = useState([]);
  const [nsgaOptimal, setNsgaOptimal] = useState([]);
  const [salaryRoi, setSalaryRoi] = useState(null);
  const [joining, setJoining] = useState(null);
  const [futureForecast, setFutureForecast] = useState(null);
  const [retention, setRetention] = useState(null);
  const [learning, setLearning] = useState(null);
  const [team, setTeam] = useState(null);
  const [organization, setOrganization] = useState(null);
  const [risk, setRisk] = useState(null);
  const [diversity, setDiversity] = useState(null);
  const [tradeoffs, setTradeoffs] = useState(null);
  const [sensitivity, setSensitivity] = useState({});
  const [scenarioResults, setScenarioResults] = useState(null);
  const [monteCarlo, setMonteCarlo] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [visualization, setVisualization] = useState(null);

  const [loading, setLoading] = useState(false);
  const [selectedCandidateId, setSelectedCandidateId] = useState(null);

  // Trigger full optimizer run
  const runOptimizer = async () => {
    setLoading(true);
    try {
      const payload = {
        constraints: {
          salary_max: maxSalary,
          joining_max: maxJoining,
          experience_min: minExp,
          required_skills: requiredSkills
        },
        strategy: strategy,
        scenario_id: scenarioId
      };

      const res = await fetch("http://localhost:8000/api/optimizer/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      setRecommended(data.recommended_candidate || null);
      setParetoFrontier(data.pareto_frontier || []);
      setNsgaOptimal(data.nsga2_frontier || []);
      setSalaryRoi(data.salary_roi || null);
      setJoining(data.joining || null);
      setFutureForecast(data.future_forecast || null);
      setRetention(data.retention || null);
      setLearning(data.learning || null);
      setTeam(data.team || null);
      setOrganization(data.organization || null);
      setRisk(data.risk || null);
      setDiversity(data.diversity || null);
      setTradeoffs(data.tradeoffs || null);
      setSensitivity(data.sensitivity || {});
      setScenarioResults(data.scenario_results || null);
      setMonteCarlo(data.monte_carlo || null);
      setExplanation(data.explanation || null);
      setVisualization(data.visualization || null);

      if (data.recommended_candidate) {
        setSelectedCandidateId(data.recommended_candidate.candidate_id);
      }
    } catch (e) {
      console.error("Optimizer fetch error", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runOptimizer();
  }, [maxSalary, maxJoining, minExp, requiredSkills, strategy, scenarioId]);

  const handleAddSkill = (e) => {
    e.preventDefault();
    if (skillInput && !requiredSkills.includes(skillInput.toLowerCase())) {
      setRequiredSkills([...requiredSkills, skillInput.toLowerCase()]);
      setSkillInput("");
    }
  };

  const handleRemoveSkill = (skill) => {
    setRequiredSkills(requiredSkills.filter(s => s !== skill));
  };

  // Sensitivity data mapping
  const sensitivityData = Object.keys(sensitivity).map(key => ({
    name: key.toUpperCase(),
    value: sensitivity[key]
  }));

  const colors = ["#2563eb", "#7c3aed", "#0891b2", "#10b981", "#f59e0b"];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <Card className="relative overflow-hidden border-cyan-500/20 bg-gradient-to-r from-slate-900 via-cyan-950/20 to-slate-900">
        <div className="absolute top-0 right-0 p-6 opacity-10">
          <Compass size={180} className="animate-spin-slow text-cyan-500" />
        </div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge tone="cyan" className="py-1">
                <Sparkles size={12} className="mr-1" /> CORE INNOVATION
              </Badge>
              <Badge tone="violet" className="py-1">MULTI-OBJECTIVE OPTIMIZER</Badge>
            </div>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">
              Multi-Objective Hiring Optimizer (MOHO)
            </h1>
            <p className="mt-1 max-w-2xl text-sm text-slate-300">
              Go beyond simple candidate scoring. Balance conflicting hiring goals (Quality, Budget, Notice, Retention) dynamically using NSGA-II Evolutionary Algorithms and Pareto Frontiers.
            </p>
          </div>
          <div>
            <Button className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-glow" onClick={runOptimizer} disabled={loading}>
              <RefreshCw size={15} className={`mr-2 ${loading ? "animate-spin" : ""}`} /> 
              {loading ? "Optimizing..." : "Recalculate Pareto"}
            </Button>
          </div>
        </div>
      </Card>

      {/* Preset Scenarios selector */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { id: "startup", label: "Startup Mode", desc: "Prioritizes Innovation & Learning" },
          { id: "corporate", label: "Corporate Mode", desc: "Prioritizes Retention & Leadership" },
          { id: "government", label: "Government Mode", desc: "Prioritizes Compliance & Risk safety" },
          { id: "research", label: "Research Mode", desc: "Prioritizes Skill & Domain Diversity" }
        ].map((item) => (
          <button
            key={item.id}
            onClick={() => setScenarioId(item.id)}
            className={`rounded-xl border p-3 text-left transition ${
              scenarioId === item.id 
                ? "border-cyan-500 bg-cyan-600/10 text-white shadow-glow" 
                : "border-slate-800 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400"
            }`}
          >
            <span className="text-[10px] uppercase tracking-wider block font-bold text-cyan-400">Preset Scenario</span>
            <span className="font-bold text-sm block mt-1 text-white">{item.label}</span>
            <span className="text-xs text-slate-400 block mt-0.5">{item.desc}</span>
          </button>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-12">
        {/* LEFT COLUMN: EDIT CONSTRAINTS & STRATEGY */}
        <div className="lg:col-span-3 space-y-6">
          {/* HARD CONSTRAINTS */}
          <Card className="border-slate-800 bg-slate-900/60 backdrop-blur-xl">
            <h2 className="text-md font-bold text-white mb-4 border-b border-slate-800 pb-3 flex items-center gap-2">
              <Sliders size={16} className="text-cyan-400" /> Constraint thresholds
            </h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300 font-semibold">Max Salary Cap</span>
                  <span className="text-cyan-400 font-bold">{maxSalary} LPA</span>
                </div>
                <input
                  type="range"
                  min="15"
                  max="50"
                  step="2"
                  value={maxSalary}
                  onChange={(e) => setMaxSalary(parseInt(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded accent-cyan-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300 font-semibold">Notice Period ceiling</span>
                  <span className="text-amber-400 font-bold">{maxJoining} Days</span>
                </div>
                <input
                  type="range"
                  min="15"
                  max="90"
                  step="15"
                  value={maxJoining}
                  onChange={(e) => setMaxJoining(parseInt(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded accent-amber-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300 font-semibold">Minimum Experience</span>
                  <span className="text-emerald-400 font-bold">{minExp} Years</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  step="1"
                  value={minExp}
                  onChange={(e) => setMinExp(parseInt(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded accent-emerald-500 cursor-pointer"
                />
              </div>
            </div>
          </Card>

          {/* REQUIRED SKILLS */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h2 className="text-md font-bold text-white mb-3 flex items-center gap-1.5">
              <Zap size={16} className="text-violet-400" /> Mandatory Skills
            </h2>
            <form onSubmit={handleAddSkill} className="flex gap-2 mb-3">
              <input
                type="text"
                placeholder="fastapi, kubernetes"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-500"
              />
              <Button type="submit" size="sm" className="bg-cyan-600 hover:bg-cyan-700 text-white text-xs">Add</Button>
            </form>
            <div className="flex flex-wrap gap-1.5">
              {requiredSkills.map(s => (
                <Badge key={s} tone="cyan" className="py-0.5 px-2 flex items-center gap-1">
                  {s.toUpperCase()}
                  <button type="button" onClick={() => handleRemoveSkill(s)} className="hover:text-red-400 font-extrabold ml-1">×</button>
                </Badge>
              ))}
            </div>
          </Card>

          {/* CHOOSE OPTIMIZATION STRATEGY */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h2 className="text-md font-bold text-white mb-3">Strategic Goal</h2>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
            >
              <option value="future_growth">Best Future Potential</option>
              <option value="best_quality">Maximum Candidate Quality</option>
              <option value="best_value">Best Value (ROI)</option>
              <option value="fastest_joining">Fastest Notice Period</option>
              <option value="lowest_risk">Lowest Resignation Risk</option>
              <option value="highest_innovation">Highest Innovation</option>
              <option value="best_leadership">Strongest Leadership</option>
              <option value="highest_retention">Highest Long-term Retention</option>
              <option value="best_team_fit">Best Team Compatibility</option>
              <option value="best_organization_fit">Best Organizational Alignment</option>
            </select>
          </Card>
        </div>

        {/* CENTER COLUMN: PARETO FRONTIER & CANDIDATE SELECTOR */}
        <div className="lg:col-span-6 space-y-6">
          {/* PARETO FRONTIER GRAPH */}
          <Card className="border-slate-800 bg-slate-950/40">
            <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-lg font-bold text-white">Pareto Frontier (Salary vs Quality)</h2>
                <p className="text-xs text-slate-400 mt-0.5">Top-right candidates represent non-dominated optimal choices</p>
              </div>
              <Badge tone="violet">PARETO-OPTIMAL</Badge>
            </div>

            {visualization && visualization.pareto_frontier && (
              <div className="h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                    <XAxis type="number" dataKey="salary" name="Salary" unit=" LPA" stroke="#64748b" fontSize={10} />
                    <YAxis type="number" dataKey="quality" name="Quality" unit="%" stroke="#64748b" fontSize={10} domain={[60, 100]} />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Candidates" data={visualization.pareto_frontier} fill="#06b6d4">
                      <LabelList dataKey="name" position="top" style={{ fill: '#94a3b8', fontSize: 10, fontWeight: 700 }} />
                    </Scatter>
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            )}
          </Card>

          {/* NSGA-II ELITE LIST */}
          <Card className="border-slate-800 bg-slate-950/20">
            <h2 className="text-md font-bold text-white mb-3">NSGA-II Multi-Objective Elite Candidates</h2>
            <div className="space-y-2 max-h-[380px] overflow-y-auto">
              {nsgaOptimal.map((cand, index) => {
                const isSelected = selectedCandidateId === cand.candidate_id;
                return (
                  <div
                    key={cand.candidate_id}
                    onClick={() => setSelectedCandidateId(cand.candidate_id)}
                    className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition ${
                      isSelected 
                        ? "border-cyan-500 bg-cyan-600/10 shadow-glow" 
                        : "border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/70"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="h-7 w-7 rounded-lg bg-slate-800/80 flex items-center justify-center font-bold text-xs text-cyan-400">
                        #{index + 1}
                      </div>
                      <div>
                        <span className="font-bold text-sm text-white">{cand.name}</span>
                        <div className="flex gap-2 text-[10px] text-slate-400 mt-0.5">
                          <span>Quality: {cand.objectives.quality}%</span>
                          <span>•</span>
                          <span>Salary: {cand.objectives.salary} LPA</span>
                          <span>•</span>
                          <span>Notice: {cand.objectives.joining} Days</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <div className="text-right">
                        <span className="text-[10px] block uppercase text-slate-500 font-bold">Retention</span>
                        <span className="text-xs font-bold text-emerald-400">{cand.objectives.retention}%</span>
                      </div>
                      <ChevronRight size={14} className="text-slate-600" />
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* RIGHT COLUMN: TRADEOFFS & RATIO EXPLANATIONS */}
        <div className="lg:col-span-3 space-y-6">
          {/* RECRUITER STRATEGIC RECOMMENDATION */}
          {recommended && (
            <Card className="border-cyan-500/30 bg-cyan-950/10">
              <h2 className="text-md font-bold text-white mb-2 flex items-center gap-2">
                <CheckCircle2 size={16} className="text-cyan-400" /> Strategic Match
              </h2>
              <div className="text-sm font-extrabold text-white">{recommended.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5 uppercase tracking-wider font-bold">
                Selected for Strategy: {strategy.replace("_", " ")}
              </div>
              
              {explanation && (
                <div className="mt-3 bg-slate-950/70 p-3 rounded-lg border border-slate-800">
                  <div className="text-[11px] text-slate-300 leading-relaxed whitespace-pre-line">
                    {explanation.explanation}
                  </div>
                  <div className="mt-2.5 flex justify-between items-center text-xs pt-2 border-t border-slate-850">
                    <span className="text-slate-400 font-semibold">Decision Confidence</span>
                    <span className="text-cyan-400 font-black">{explanation.decision_confidence}%</span>
                  </div>
                </div>
              )}
            </Card>
          )}

          {/* SENSITIVITY INDEX */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h3 className="text-xs font-bold text-white mb-3">Objective Sensitivity Analysis</h3>
            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sensitivityData}>
                  <XAxis dataKey="name" stroke="#64748b" fontSize={9} tickLine={false} />
                  <Tooltip />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {sensitivityData.map((entry, idx) => (
                      <Cell key={idx} fill={colors[idx % colors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-[9px] text-slate-400 mt-2 text-center">Variance contribution indicating critical decision points</p>
          </Card>

          {/* MONTE CARLO STABILITY */}
          {monteCarlo && (
            <Card className="border-slate-800 bg-slate-900/60">
              <h3 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5">
                <Activity size={14} className="text-emerald-400" /> 10,000 workforce simulations
              </h3>
              <div className="space-y-2 max-h-[160px] overflow-y-auto">
                {Object.keys(monteCarlo.strategy_distribution || {}).map((key) => {
                  const val = monteCarlo.strategy_distribution[key];
                  return (
                    <div key={key} className="text-xs">
                      <div className="flex justify-between mb-1">
                        <span className="text-slate-400 uppercase font-semibold text-[10px]">{key.replace("_", " ")}</span>
                        <span className="text-white font-bold">{val}%</span>
                      </div>
                      <div className="w-full bg-slate-800 h-1 rounded">
                        <div className="bg-cyan-500 h-1 rounded" style={{ width: `${val}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}
        </div>
      </div>

      {/* BOTTOM PANEL: SYNERGY & DIVERSITY DETAIL CARD */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* COGNITIVE DIVERSITY */}
        {diversity && (
          <Card className="border-slate-850 bg-slate-900/70">
            <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
              <Users size={16} className="text-violet-400" /> Cognitive Team Diversity Fit
            </h3>
            <div className="flex justify-between items-center text-xs mb-2">
              <span className="text-slate-400">Diversity Balance index</span>
              <span className="font-bold text-violet-400 text-sm">{Math.round(diversity.diversity_score * 100)}%</span>
            </div>
            <div className="text-[11px] text-slate-300 leading-relaxed bg-slate-950 p-2.5 rounded-lg border border-slate-850">
              {diversity.recommendation}
            </div>
          </Card>
        )}

        {/* TEAM SYNERGY METRICS */}
        {team && (
          <Card className="border-slate-850 bg-slate-900/70">
            <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
              <Star size={16} className="text-amber-400" /> Team Impact Forecast
            </h3>
            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Team Happiness Contribution</span>
                <span className="font-bold text-white">{Math.round(team.metrics.team_happiness * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Productivity Synergy Increment</span>
                <span className="font-bold text-white">{Math.round(team.metrics.team_productivity * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Conflict Mitigation Index</span>
                <span className="font-bold text-white">{Math.round(team.metrics.conflict_reduction * 100)}%</span>
              </div>
            </div>
          </Card>
        )}

        {/* ORGANIZATIONAL BUSINESS VALUE */}
        {organization && (
          <Card className="border-slate-850 bg-slate-900/70">
            <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
              <Award size={16} className="text-cyan-400" /> Organization Fit Score
            </h3>
            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Business Value Contribution</span>
                <span className="font-bold text-white">{Math.round(organization.breakdown.business_value * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Innovation Capital Growth</span>
                <span className="font-bold text-white">{Math.round(organization.breakdown.innovation_contribution * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Leadership Capital Addition</span>
                <span className="font-bold text-white">{Math.round(organization.breakdown.leadership_capital * 100)}%</span>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
