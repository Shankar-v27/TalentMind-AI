import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  Sparkles, RefreshCw, Eye, ThumbsUp, Trash2, Award, Zap, UserCheck, 
  HelpCircle, UserMinus, Plus, ShieldAlert, BarChart3, Clock, HelpCircle as HelpIcon,
  BookOpen, Network, Database, Layers, ArrowUpRight, Compass, Settings, CheckCircle
} from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { 
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, LineChart, Line
} from "recharts";

export function RecruiterMemory() {
  const [recruiterId, setRecruiterId] = useState("recruiter_alpha");
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  
  // RMG state
  const [preferences, setPreferences] = useState({});
  const [behavior, setBehavior] = useState({});
  const [dna, setDna] = useState(null);
  const [personalizedCands, setPersonalizedCands] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [patterns, setPatterns] = useState([]);
  const [qValues, setQValues] = useState({});
  const [explanation, setExplanation] = useState(null);
  const [visualization, setVisualization] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  
  const [loading, setLoading] = useState(false);
  const [actionSimulating, setActionSimulating] = useState(false);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/recruiter/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recruiter_id: recruiterId })
      });
      const data = await res.json();
      
      setPreferences(data.preferences || {});
      setBehavior(data.behavior || {});
      setDna(data.dna || null);
      setPersonalizedCands(data.personalized_candidates || []);
      setRecommendations(data.recommendations || null);
      setPatterns(data.patterns || []);
      setQValues(data.reinforcement_q_values || {});
      setExplanation(data.explanation || null);
      setVisualization(data.visualization || null);
      
      if (data.personalized_candidates && data.personalized_candidates.length > 0) {
        setSelectedCandidate(data.personalized_candidates[0]);
      }
      
      // Fetch graph relations
      const gRes = await fetch("http://localhost:8000/api/recruiter/graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recruiter_id: recruiterId })
      });
      const gData = await gRes.json();
      setGraphData(gData);

    } catch (e) {
      console.error("RMG profile fetch error", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [recruiterId]);

  // Log action simulator
  const logAction = async (candidateId, actionType) => {
    setActionSimulating(true);
    try {
      await fetch("http://localhost:8000/api/recruiter/memory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          recruiter_id: recruiterId,
          candidate_id: candidateId,
          action: actionType
        })
      });
      
      // Refresh profile data
      await fetchProfile();
    } catch (e) {
      console.error("Action log error", e);
    } finally {
      setActionSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <Card className="relative overflow-hidden border-violet-500/20 bg-gradient-to-r from-slate-900 via-violet-950/20 to-slate-900">
        <div className="absolute top-0 right-0 p-6 opacity-10">
          <Network size={180} className="animate-pulse text-violet-500" />
        </div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge tone="violet" className="py-1">
                <Sparkles size={12} className="mr-1" /> CORE INNOVATION
              </Badge>
              <Badge tone="cyan" className="py-1">RECRUITER MEMORY GRAPH</Badge>
            </div>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">
              Recruiter Memory Graph (RMG)
            </h1>
            <p className="mt-1 max-w-2xl text-sm text-slate-300">
              Personalized recruitment intelligence. RMG learns your unique hiring styles, preferred attributes, and trade-off behavior thresholds dynamically from your actions.
            </p>
          </div>
          <div>
            <div className="flex gap-2">
              <select
                value={recruiterId}
                onChange={(e) => setRecruiterId(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-violet-500"
              >
                <option value="recruiter_alpha">Recruiter Alpha (Tech Focus)</option>
                <option value="recruiter_beta">Recruiter Beta (Cost Focus)</option>
                <option value="recruiter_gamma">Recruiter Gamma (Retention Focus)</option>
              </select>
              <Button className="bg-gradient-to-r from-violet-600 to-indigo-600 text-white" onClick={fetchProfile} disabled={loading}>
                <RefreshCw size={15} className={`mr-2 ${loading ? "animate-spin" : ""}`} /> Sync
              </Button>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-12">
        {/* LEFT COLUMN: PREFERENCES & SIMULATOR */}
        <div className="lg:col-span-4 space-y-6">
          {/* RADAR GRAPH PREFERENCES */}
          <Card className="border-slate-800 bg-slate-900/60 backdrop-blur-xl">
            <h2 className="text-md font-bold text-white mb-4 border-b border-slate-800 pb-3 flex items-center gap-2">
              <Settings size={16} className="text-violet-400" /> Learned Preference Weights
            </h2>
            {visualization && visualization.radar && (
              <div className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" radius="70%" data={visualization.radar}>
                    <PolarGrid stroke="#334155" />
                    <PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={9} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" fontSize={8} />
                    <Radar name={recruiterId} dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            )}
          </Card>

          {/* ACTION SIMULATOR COCKPIT */}
          <Card className="border-slate-800 bg-slate-900/60">
            <h2 className="text-md font-bold text-white mb-3">Simulate Recruiter Action</h2>
            <p className="text-xs text-slate-400 mb-3">Manually log actions below to dynamically shift preference graphs.</p>
            {selectedCandidate && (
              <div className="space-y-3 bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-400">Target Candidate</span>
                  <span className="font-bold text-white">{selectedCandidate.name}</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <Button size="xs" className="bg-emerald-600 hover:bg-emerald-700 text-white text-[10px]" onClick={() => logAction(selectedCandidate.candidate_id, "hired")} disabled={actionSimulating}>
                    Log Hire
                  </Button>
                  <Button size="xs" className="bg-cyan-600 hover:bg-cyan-700 text-white text-[10px]" onClick={() => logAction(selectedCandidate.candidate_id, "shortlisted")} disabled={actionSimulating}>
                    Log Shortlist
                  </Button>
                  <Button size="xs" className="bg-amber-600 hover:bg-amber-700 text-white text-[10px]" onClick={() => logAction(selectedCandidate.candidate_id, "saved")} disabled={actionSimulating}>
                    Log Save
                  </Button>
                  <Button size="xs" className="bg-rose-600 hover:bg-rose-700 text-white text-[10px]" onClick={() => logAction(selectedCandidate.candidate_id, "rejected")} disabled={actionSimulating}>
                    Log Reject
                  </Button>
                </div>
              </div>
            )}
          </Card>
        </div>

        {/* CENTER COLUMN: PERSONALIZED RANKINGS */}
        <div className="lg:col-span-5 space-y-6">
          <Card className="border-slate-800 bg-slate-950/40">
            <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-lg font-bold text-white">Personalized Candidate Feed</h2>
                <p className="text-xs text-slate-400 mt-0.5">Rankings boosted based on historical recruiter preferences</p>
              </div>
              <Badge tone="cyan">BOOSTED FEED</Badge>
            </div>

            <div className="space-y-2.5 max-h-[460px] overflow-y-auto">
              {personalizedCands.map((cand, index) => {
                const isSelected = selectedCandidate?.candidate_id === cand.candidate_id;
                return (
                  <div
                    key={cand.candidate_id}
                    onClick={() => setSelectedCandidate(cand)}
                    className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition ${
                      isSelected 
                        ? "border-violet-500 bg-violet-600/10 shadow-glow" 
                        : "border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/70"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="h-7 w-7 rounded-lg bg-slate-800/80 flex items-center justify-center font-bold text-xs text-violet-400">
                        #{index + 1}
                      </div>
                      <div>
                        <span className="font-bold text-sm text-white">{cand.name}</span>
                        <div className="flex gap-2 text-[10px] text-slate-400 mt-0.5">
                          <span>Global Score: {cand.global_score}</span>
                          <span>•</span>
                          <span className="text-violet-400 font-bold">Personalized: {cand.personalized_score}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      {cand.personalization_boost > 0 && (
                        <Badge tone="violet" className="text-[10px] font-bold">
                          +{cand.personalization_boost}
                        </Badge>
                      )}
                      <ArrowUpRight size={14} className="text-slate-600" />
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* RIGHT COLUMN: PREDICTIVE METERS & EXPLANATIONS */}
        <div className="lg:col-span-3 space-y-6">
          {/* DECISION DNA */}
          {dna && (
            <Card className="border-slate-800 bg-slate-900/60">
              <h2 className="text-md font-bold text-white mb-2 flex items-center gap-1.5">
                <Database size={16} className="text-cyan-400" /> Recruiter DNA profile
              </h2>
              <div className="space-y-2 text-xs">
                {Object.keys(dna.metrics || {}).map((key) => (
                  <div key={key} className="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-slate-850">
                    <span className="text-slate-400 uppercase text-[9px] font-bold">{key.replace("_", " ")}</span>
                    <Badge tone={dna.metrics[key] === "High" ? "cyan" : "violet"}>{dna.metrics[key]}</Badge>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* ACTION PREDICTION PROBABILITIES */}
          {selectedCandidate && selectedCandidate.predictions && (
            <Card className="border-slate-800 bg-slate-900/60">
              <h3 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5">
                <Clock size={14} className="text-violet-400" /> Action Predictions for {selectedCandidate.name}
              </h3>
              <div className="space-y-2">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Hire Probability</span>
                    <span className="text-white font-bold">{Math.round(selectedCandidate.predictions.hire_probability * 100)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1 rounded">
                    <div className="bg-emerald-500 h-1 rounded" style={{ width: `${selectedCandidate.predictions.hire_probability * 100}%` }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Shortlist Probability</span>
                    <span className="text-white font-bold">{Math.round(selectedCandidate.predictions.shortlist_probability * 100)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1 rounded">
                    <div className="bg-cyan-500 h-1 rounded" style={{ width: `${selectedCandidate.predictions.shortlist_probability * 100}%` }} />
                  </div>
                </div>
              </div>
            </Card>
          )}

          {/* PERSONALIZATION EXPLANATION */}
          {explanation && (
            <Card className="border-violet-500/20 bg-violet-950/5">
              <h3 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5">
                <CheckCircle size={14} className="text-violet-400" /> Decision Explainability
              </h3>
              <div className="text-[11px] text-slate-300 leading-relaxed whitespace-pre-line bg-slate-950 p-2.5 rounded-lg border border-slate-850">
                {explanation.explanation}
              </div>
            </Card>
          )}
        </div>
      </div>

      {/* BOTTOM PANEL: PREFERENCE TIMELINES & KNOWLEDGE GRAPH */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* GRAPH RELATIONSHIPS CACHE */}
        <Card className="border-slate-850 bg-slate-900/70">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
            <Network size={16} className="text-violet-400" /> Recruiter Knowledge Graph Relations (NetworkX)
          </h3>
          <div className="space-y-1.5 max-h-[220px] overflow-y-auto">
            {graphData.edges.slice(0, 10).map((edge, idx) => (
              <div key={idx} className="flex justify-between items-center text-xs bg-slate-950 p-2 rounded-lg border border-slate-850">
                <span className="font-bold text-slate-300">{edge.source}</span>
                <Badge tone="violet">{edge.relation.toUpperCase()}</Badge>
                <span className="font-bold text-slate-300">{edge.target}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* PREFERENCE EVOLUTION TIMELINE */}
        {visualization && visualization.timeline && (
          <Card className="border-slate-850 bg-slate-900/70">
            <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
              <Layers size={16} className="text-cyan-400" /> Preference Evolution Timeline
            </h3>
            <div className="space-y-3">
              {visualization.timeline.map((item, idx) => (
                <div key={idx} className="flex items-start gap-3 text-xs">
                  <Badge tone="cyan" className="mt-0.5">{item.year}</Badge>
                  <div className="text-slate-300 font-semibold leading-relaxed">
                    {item.focus}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
