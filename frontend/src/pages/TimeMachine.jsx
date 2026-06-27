import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Sparkles, RefreshCw, Sliders, ArrowRight, TrendingUp, ShieldAlert, Zap, 
  HelpCircle, UserCheck, CheckCircle2, AlertTriangle, Play,
  ChevronRight, Compass, DollarSign, Calendar, Star, Users
} from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { ProgressRing } from "../components/ui/ProgressRing";
import { 
  ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Cell, 
  LineChart, Line 
} from "recharts";

// Local mirror of Python ScenarioEngine.SCENARIO_PRESETS
const SCENARIO_PRESETS = {
  high_skill: {
    label: "Scenario A: High Skill Focus",
    description: "Prioritizes deep technical skill alignment over all other parameters."
  },
  fast_hiring: {
    label: "Scenario B: Urgent Backfill",
    description: "Prioritizes fast-onboarding notice periods and immediate availability."
  },
  future_potential: {
    label: "Scenario C: Future Leaders",
    description: "Optimizes for long-term learning velocity and career acceleration profiles."
  },
  leadership_focus: {
    label: "Scenario D: Leadership Capabilities",
    description: "Prioritizes strategic management capabilities and organization DNA fit."
  },
  low_cost: {
    label: "Scenario E: Budget Optimization",
    description: "Prioritizes candidates fitting constrained salary requirements."
  }
};

export function TimeMachine() {
  // Requirement state
  const [experience, setExperience] = useState(3);
  const [salary, setSalary] = useState(25); // LPA
  const [joining, setJoining] = useState(60); // notice period days
  const [skillWeight, setSkillWeight] = useState(0.3);
  const [expWeight, setExpWeight] = useState(0.2);
  const [leadership, setLeadership] = useState(0.3);
  const [futurePotential, setFuturePotential] = useState(0.3);
  const [retention, setRetention] = useState(0.5);
  const [risk, setRisk] = useState(0.4);
  const [skills, setSkills] = useState(["python", "aws", "docker"]);
  const [newSkillInput, setNewSkillInput] = useState("");

  // Result states
  const [rankings, setRankings] = useState([]);
  const [weights, setWeights] = useState({});
  const [optimization, setOptimization] = useState({});
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [counterfactual, setCounterfactual] = useState(null);
  const [sensitivity, setSensitivity] = useState({});
  const [stability, setStability] = useState([]);
  const [movements, setMovements] = useState([]);
  const [explanation, setExplanation] = useState("");
  const [simWins, setSimWins] = useState({});
  
  const [activeScenario, setActiveScenario] = useState("custom");
  const [isSimulating, setIsSimulating] = useState(false);
  const [loading, setLoading] = useState(false);

  // Load and recalculate rankings based on weights & constraints
  const fetchRankings = async () => {
    setLoading(true);
    try {
      const statePayload = {
        experience,
        salary,
        joining,
        skill_weight: skillWeight,
        experience_weight: expWeight,
        leadership,
        future_potential: futurePotential,
        retention,
        risk,
        skills
      };

      // 1. Fetch State & Rankings
      const resState = await fetch("http://localhost:8000/api/timemachine/state", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(statePayload)
      });
      const dataState = await resState.json();
      
      setRankings(dataState.rankings || []);
      setWeights(dataState.weights || {});
      
      // Auto-select top candidate if none selected
      if (dataState.rankings && dataState.rankings.length > 0 && !selectedCandidate) {
        setSelectedCandidate(dataState.rankings[0]);
      }

      // 2. Fetch Optimization Picks
      const resRank = await fetch("http://localhost:8000/api/timemachine/rank", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: statePayload })
      });
      const dataRank = await resRank.json();
      setOptimization(dataRank.optimization || {});

      // 3. Fetch Sensitivity
      const resSens = await fetch("http://localhost:8000/api/timemachine/sensitivity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: statePayload })
      });
      const dataSens = await resSens.json();
      setSensitivity(dataSens.sensitivity || {});

      // 4. Fetch Stability
      const resStab = await fetch("http://localhost:8000/api/timemachine/stability", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: statePayload })
      });
      const dataStab = await resStab.json();
      setStability(dataStab.stability || []);

      // 5. Fetch Movements (mock baseline offset)
      const resMov = await fetch("http://localhost:8000/api/timemachine/movement", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ baseline_state: statePayload })
      });
      const dataMov = await resMov.json();
      setMovements(dataMov.movement || []);

    } catch (e) {
      console.error("Error fetching simulation rankings", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, [experience, salary, joining, skillWeight, expWeight, leadership, futurePotential, retention, risk, skills]);

  // Fetch candidate counterfactual & explanation when selected candidate changes
  useEffect(() => {
    if (!selectedCandidate) return;
    
    const fetchCandidateDetails = async () => {
      try {
        const statePayload = {
          experience,
          salary,
          joining,
          skill_weight: skillWeight,
          experience_weight: expWeight,
          leadership,
          future_potential: futurePotential,
          retention,
          risk,
          skills
        };

        // Fetch counterfactual
        const resCf = await fetch("http://localhost:8000/api/timemachine/counterfactual", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            candidate_id: selectedCandidate.candidate_id,
            state: statePayload
          })
        });
        const dataCf = await resCf.json();
        setCounterfactual(dataCf);

        // Fetch movement explanation narrative
        const matchedMov = movements.find(m => m.candidate_id === selectedCandidate.candidate_id);
        const oldRank = matchedMov ? matchedMov.old_rank : 5;
        const newRank = matchedMov ? matchedMov.new_rank : 2;
        
        const resExp = await fetch("http://localhost:8000/api/timemachine/explain", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            candidate_name: selectedCandidate.name,
            old_rank: oldRank,
            new_rank: newRank,
            old_state: { ...statePayload, experience: oldRank > newRank ? experience + 2 : experience - 2 },
            new_state: statePayload,
            score_diff: oldRank > newRank ? 8.5 : -4.2
          })
        });
        const dataExp = await resExp.json();
        setExplanation(dataExp.explanation);

      } catch (e) {
        console.error("Error details", e);
      }
    };

    fetchCandidateDetails();
  }, [selectedCandidate, movements]);

  // Apply predefined scenario presets
  const applyPreset = async (scenarioId) => {
    setActiveScenario(scenarioId);
    try {
      const res = await fetch("http://localhost:8000/api/timemachine/scenario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario_id: scenarioId })
      });
      const data = await res.json();
      
      const s = data.state;
      setExperience(s.experience);
      setSalary(s.salary);
      setJoining(s.joining);
      setSkillWeight(s.skill_weight);
      setExpWeight(s.experience_weight);
      setLeadership(s.leadership);
      setFuturePotential(s.future_potential);
      setRetention(s.retention);
      setRisk(s.risk);
    } catch (e) {
      console.error(e);
    }
  };

  // Run 1,000 Monte Carlo Simulation Runs
  const runMonteCarlo = async () => {
    setIsSimulating(true);
    setSimWins({});
    try {
      const statePayload = {
        experience,
        salary,
        joining,
        skill_weight: skillWeight,
        experience_weight: expWeight,
        leadership,
        future_potential: futurePotential,
        retention,
        risk,
        skills
      };

      const res = await fetch("http://localhost:8000/api/timemachine/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: statePayload, runs: 1000 })
      });
      const data = await res.json();
      setSimWins(data.simulation_wins || {});
    } catch (e) {
      console.error(e);
    } finally {
      setIsSimulating(false);
    }
  };

  // Add/remove skills from state
  const handleAddSkill = (e) => {
    e.preventDefault();
    if (newSkillInput && !skills.includes(newSkillInput.toLowerCase())) {
      setSkills([...skills, newSkillInput.toLowerCase()]);
      setNewSkillInput("");
    }
  };

  const handleRemoveSkill = (skill) => {
    setSkills(skills.filter(s => s !== skill));
  };

  // Format Recharts data for sensitivity
  const sensitivityData = Object.keys(sensitivity).map(key => ({
    name: key.toUpperCase(),
    value: sensitivity[key]
  }));

  const colors = ["#3b82f6", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b"];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <Card className="relative overflow-hidden border-violet-500/20 bg-gradient-to-r from-slate-900 via-violet-950/20 to-slate-900">
        <div className="absolute top-0 right-0 p-6 opacity-10">
          <Compass size={180} className="animate-spin-slow text-violet-500" />
        </div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge tone="violet" className="py-1">
                <Sparkles size={12} className="mr-1" /> INNOVATION LAYER
              </Badge>
              <Badge tone="cyan" className="py-1">DECISION INTELLIGENCE</Badge>
            </div>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">
              Recruiter Time Machine
            </h1>
            <p className="mt-1 max-w-2xl text-sm text-slate-300">
              Interactive talent simulation playground. Modify role priorities, weights, and constraints in real-time. Forecast the structural evolution of your hiring universe.
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="border-violet-500/30 text-violet-300 hover:bg-violet-500/10" onClick={fetchRankings}>
              <RefreshCw size={15} className={`mr-2 ${loading ? "animate-spin" : ""}`} /> Recalculate
            </Button>
            <Button className="bg-gradient-to-r from-blue-600 to-violet-600 text-white shadow-glow" onClick={runMonteCarlo} disabled={isSimulating}>
              <Play size={15} className="mr-2" /> {isSimulating ? "Simulating..." : "Run Monte Carlo"}
            </Button>
          </div>
        </div>
      </Card>

      {/* Scenario Presets Selector */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
        {Object.keys(SCENARIO_PRESETS).map((key) => {
          const active = activeScenario === key;
          return (
            <button
              key={key}
              onClick={() => applyPreset(key)}
              className={`rounded-xl border p-3 text-left transition ${
                active 
                  ? "border-violet-500 bg-violet-600/20 text-white shadow-glow" 
                  : "border-slate-800 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400"
              }`}
            >
              <div className="text-xs font-bold uppercase tracking-wider opacity-60">Preset</div>
              <div className="mt-1 font-bold text-sm truncate">{key.replace("_", " ").toUpperCase()}</div>
            </button>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-12">
        {/* LEFT PANEL: REQUIREMENT CONTROLS */}
        <div className="lg:col-span-4 space-y-6">
          <Card className="border-slate-800/60 bg-slate-900/80 backdrop-blur-xl">
            <h2 className="flex items-center gap-2 text-lg font-bold text-white mb-4 border-b border-slate-800 pb-3">
              <Sliders size={18} className="text-blue-400" /> Hiring Constraints
            </h2>
            
            <div className="space-y-5">
              {/* Experience slider */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300 font-medium">Minimum Experience</span>
                  <span className="text-blue-400 font-bold">{experience} Years</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="12"
                  step="1"
                  value={experience}
                  onChange={(e) => setExperience(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>

              {/* Salary slider */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300 font-medium">Max Budget (Salary)</span>
                  <span className="text-emerald-400 font-bold">{salary} LPA</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="60"
                  step="2"
                  value={salary}
                  onChange={(e) => setSalary(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
              </div>

              {/* Joining slider */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300 font-medium">Notice Period Ceiling</span>
                  <span className="text-amber-400 font-bold">{joining} Days</span>
                </div>
                <input
                  type="range"
                  min="15"
                  max="90"
                  step="15"
                  value={joining}
                  onChange={(e) => setJoining(parseInt(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-500"
                />
              </div>
            </div>
          </Card>

          {/* Skill presets addition */}
          <Card className="border-slate-800/60 bg-slate-900/80 backdrop-blur-xl">
            <h2 className="flex items-center gap-2 text-lg font-bold text-white mb-4 border-b border-slate-800 pb-3">
              <Zap size={18} className="text-violet-400" /> Mandatory Skills
            </h2>
            <form onSubmit={handleAddSkill} className="flex gap-2 mb-3">
              <input
                type="text"
                placeholder="e.g. kubernetes, fastapi"
                value={newSkillInput}
                onChange={(e) => setNewSkillInput(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-violet-500"
              />
              <Button type="submit" size="sm" className="bg-violet-600 hover:bg-violet-700 text-white">Add</Button>
            </form>
            <div className="flex flex-wrap gap-1.5">
              {skills.map(s => (
                <Badge key={s} tone="violet" className="py-1 px-2.5 flex items-center gap-1.5">
                  {s.toUpperCase()}
                  <button type="button" onClick={() => handleRemoveSkill(s)} className="hover:text-red-400 font-bold ml-1">×</button>
                </Badge>
              ))}
            </div>
          </Card>

          {/* WEIGHTS SLIDERS */}
          <Card className="border-slate-800/60 bg-slate-900/80 backdrop-blur-xl">
            <h2 className="flex items-center gap-2 text-lg font-bold text-white mb-4 border-b border-slate-800 pb-3">
              <TrendingUp size={18} className="text-cyan-400" /> Dimension Weight Priorities
            </h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Skill Alignment Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round(skillWeight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={skillWeight}
                  onChange={(e) => setSkillWeight(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Experience Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round(expWeight * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={expWeight}
                  onChange={(e) => setExpWeight(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Leadership Fit Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round(leadership * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={leadership}
                  onChange={(e) => setLeadership(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Future Potential Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round(futurePotential * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={futurePotential}
                  onChange={(e) => setFuturePotential(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Retention Likelihood Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round(retention * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={retention}
                  onChange={(e) => setRetention(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400 font-semibold">Risk Safety Weight</span>
                  <span className="text-cyan-400 font-bold">{Math.round((1.0 - risk) * 100)}%</span>
                </div>
                <input
                  type="range"
                  min="0.1"
                  max="0.8"
                  step="0.05"
                  value={risk}
                  onChange={(e) => setRisk(parseFloat(e.target.value))}
                  className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
              </div>
            </div>
          </Card>
        </div>

        {/* CENTER PANEL: LIVE SIMULATION RANKINGS */}
        <div className="lg:col-span-5 space-y-6">
          <Card className="border-slate-800 bg-slate-950/40 p-4">
            <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <UserCheck size={18} className="text-blue-500" /> Recomputed Rankings
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">Showing candidates aligned to current scenario weights</p>
              </div>
              <Badge tone="blue">{rankings.length} Active</Badge>
            </div>

            <div className="space-y-2 max-h-[580px] overflow-y-auto pr-1">
              <AnimatePresence>
                {rankings.map((cand, index) => {
                  const isSelected = selectedCandidate && selectedCandidate.candidate_id === cand.candidate_id;
                  const winRate = simWins[cand.candidate_id] || 0;
                  
                  return (
                    <motion.div
                      key={cand.candidate_id}
                      layoutId={`card-${cand.candidate_id}`}
                      onClick={() => setSelectedCandidate(cand)}
                      className={`relative flex items-center justify-between p-3 rounded-xl border cursor-pointer transition ${
                        isSelected 
                          ? "border-blue-500/50 bg-blue-600/10 shadow-glow" 
                          : "border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/70"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`h-8 w-8 rounded-lg flex items-center justify-center font-bold text-sm ${
                          index === 0 
                            ? "bg-amber-500/20 text-amber-300 border border-amber-500/40" 
                            : index === 1 
                            ? "bg-slate-300/20 text-slate-300 border border-slate-300/40"
                            : "bg-slate-800/60 text-slate-400"
                        }`}>
                          #{index + 1}
                        </div>
                        <div>
                          <div className="font-bold text-sm text-white flex items-center gap-1.5">
                            {cand.name}
                            {!cand.eligible && (
                              <Badge tone="amber" className="text-[10px] py-0 px-1.5">FAIL CONSTRAINTS</Badge>
                            )}
                          </div>
                          <div className="flex gap-2 text-[11px] text-slate-400 mt-0.5">
                            <span>Skills: {cand.breakdown.skill}%</span>
                            <span>•</span>
                            <span>Future: {cand.breakdown.future}%</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        {winRate > 0 && (
                          <div className="text-right">
                            <span className="text-[10px] block uppercase font-bold text-slate-500">MC WIN</span>
                            <span className="text-xs font-extrabold text-violet-400">{winRate}%</span>
                          </div>
                        )}
                        <div className="text-right">
                          <span className="text-lg font-black text-blue-400">{cand.score}</span>
                          <span className="text-[10px] text-slate-500 block">score</span>
                        </div>
                        <ChevronRight size={14} className="text-slate-600" />
                      </div>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
          </Card>
        </div>

        {/* RIGHT PANEL: DETAILS, STABILITY & SENSITIVITY */}
        <div className="lg:col-span-3 space-y-6">
          {/* Selected Candidate & Counterfactual analysis */}
          {selectedCandidate && (
            <Card className="border-violet-500/30 bg-violet-950/10">
              <h2 className="text-md font-bold text-white flex items-center gap-2 mb-2">
                <CheckCircle2 size={16} className="text-violet-400" /> Counterfactual Optimization
              </h2>
              <div className="text-xs text-slate-400 mb-4">
                Target changes for <span className="font-bold text-white">{selectedCandidate.name}</span> to secure Rank 1
              </div>

              {counterfactual && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs border-b border-slate-800 pb-2 mb-2">
                    <span className="text-slate-400">Score Gap to Winner</span>
                    <span className="text-red-400 font-bold">-{counterfactual.score_gap} pts</span>
                  </div>

                  <div className="space-y-2">
                    {counterfactual.rank1_conditions && counterfactual.rank1_conditions.map((cond, i) => (
                      <div key={i} className="flex gap-2 items-start text-[11px] text-slate-300">
                        <span className="text-violet-400 mt-0.5">•</span>
                        <span>{cond}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          )}

          {/* Explainability Narrative */}
          {explanation && (
            <Card className="border-slate-850 bg-slate-900/30">
              <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-1.5">
                <ShieldAlert size={14} className="text-amber-400" /> Simulation Rationale
              </h3>
              <p className="text-[11px] text-slate-300 leading-relaxed whitespace-pre-line bg-slate-950/60 p-2.5 rounded-lg border border-slate-850">
                {explanation}
              </p>
            </Card>
          )}

          {/* SENSITIVITY GRAPH */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h3 className="text-sm font-bold text-white mb-3">Ranking Sensitivity Index</h3>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sensitivityData}>
                  <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} />
                  <Tooltip />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {sensitivityData.map((entry, idx) => (
                      <Cell key={idx} fill={colors[idx % colors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-[10px] text-slate-400 mt-2 text-center">Higher value indicates candidate rankings change more when this slider varies.</p>
          </Card>

          {/* STABILITY LIST */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h3 className="text-sm font-bold text-white mb-3">Rank Stability Score</h3>
            <div className="space-y-2.5 max-h-[220px] overflow-y-auto">
              {stability.map(item => (
                <div key={item.candidate_id} className="text-xs">
                  <div className="flex justify-between mb-1">
                    <span className="font-semibold text-slate-300">{item.name}</span>
                    <span className="text-blue-400 font-bold">{Math.round(item.stability * 100)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-violet-500 h-full rounded-full" 
                      style={{ width: `${item.stability * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* BOTTOM PANEL: TIMELINE & OPTIMIZATION TARGETS */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* OPTIMIZATION TARGETS */}
        <Card className="border-slate-800 bg-slate-900/70">
          <h2 className="text-md font-bold text-white mb-3 flex items-center gap-2">
            <Compass size={16} className="text-cyan-400" /> Scenario Goal Optimization Target Picks
          </h2>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Best Long-term Future Pick</span>
              <span className="font-bold text-white">{optimization.best_future || "Calculating..."}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Lowest Salary Budget Fit</span>
              <span className="font-bold text-white">{optimization.best_cost || "Calculating..."}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Fastest Joining notice</span>
              <span className="font-bold text-white">{optimization.best_joining || "Calculating..."}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Highest Retention Likelihood</span>
              <span className="font-bold text-white">{optimization.best_retention || "Calculating..."}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Most Innovative Candidate</span>
              <span className="font-bold text-white">{optimization.best_innovation || "Calculating..."}</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-850">
              <span className="text-slate-400 block mb-0.5">Strongest Leadership Focus</span>
              <span className="font-bold text-white">{optimization.best_leadership || "Calculating..."}</span>
            </div>
          </div>
        </Card>

        {/* CANDIDATE MOVEMENT */}
        <Card className="border-slate-800 bg-slate-900/70">
          <h2 className="text-md font-bold text-white mb-3 flex items-center gap-2">
            <Users size={16} className="text-blue-400" /> Rank Movement Shifts (Active Timeline)
          </h2>
          <div className="space-y-2 max-h-[160px] overflow-y-auto pr-1">
            {movements.slice(0, 10).map((mov) => {
              const goesUp = mov.delta > 0;
              const goesDown = mov.delta < 0;
              return (
                <div key={mov.candidate_id} className="flex justify-between items-center text-xs p-2 rounded-lg bg-slate-950/60 border border-slate-850">
                  <span className="font-bold text-white">{mov.name}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-slate-400">Rank {mov.old_rank} → {mov.new_rank}</span>
                    <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                      goesUp 
                        ? "bg-emerald-500/20 text-emerald-400" 
                        : goesDown 
                        ? "bg-red-500/20 text-red-400" 
                        : "bg-slate-800 text-slate-400"
                    }`}>
                      {goesUp ? `+${mov.delta}` : mov.delta}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      </div>
    </div>
  );
}
