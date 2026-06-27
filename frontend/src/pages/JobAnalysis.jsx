import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle2, FileText, Loader2, UploadCloud, Zap,
  AlertCircle, BrainCircuit, ChevronRight, X, Sparkles,
  Target, MapPin, Briefcase, Monitor, Star
} from "lucide-react";
import { Badge } from "../components/ui/Badge";
import { api } from "../services/api";
import { useTalentMindStore } from "../state/useTalentMindStore";

const RANKING_STAGES = [
  { label: "Understanding Job Requirements",    icon: BrainCircuit },
  { label: "Loading Candidate Profiles",        icon: FileText },
  { label: "Semantic FAISS Retrieval",          icon: Target },
  { label: "Evaluating Skills & Experience",    icon: Star },
  { label: "Analyzing Behavioral Signals",      icon: Sparkles },
  { label: "Generating AI Match Scores",        icon: Zap },
];

export function JobAnalysis() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [ranking, setRanking] = useState(false);
  const [error, setError] = useState("");
  const [rankingStageIndex, setRankingStageIndex] = useState(-1);

  const { setJdAnalysis, clearSession, setCandidates } = useTalentMindStore();
  const jdAnalysis = useTalentMindStore((state) => state.jdAnalysis);
  const { register, handleSubmit, watch } = useForm();
  const descriptionValue = watch("description", "");

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    maxFiles: 1,
    onDrop: ([accepted]) => accepted && setFile(accepted),
  });

  async function submit(values) {
    setAnalyzing(true);
    setError("");

    // Clear previous session (store reset — synchronous)
    clearSession();

    const payload = new FormData();
    payload.append("text", values.description || "");
    if (file) payload.append("file", file);

    try {
      const result = await api.analyzeJobDescription(payload);
      if (result.success) {
        setJdAnalysis(result);
        setError("");
      } else {
        setError(result.error || "Failed to analyze JD. Please try again.");
      }
    } catch (err) {
      const msg = err.response?.data?.detail
        || err.message
        || "Unable to reach backend. Ensure the API server is running on port 8000 and GROQ_API_KEY is set.";
      setError(msg);
    } finally {
      setAnalyzing(false);
    }
  }

  async function startRanking() {
    setRanking(true);
    setError("");
    setRankingStageIndex(0);

    try {
      for (let i = 0; i < RANKING_STAGES.length; i++) {
        setRankingStageIndex(i);
        await new Promise((r) => setTimeout(r, 700));
      }
      const result = await api.rankCandidates();
      if (result.success) {
        setCandidates(result.candidates);
        navigate("/rankings");
      } else {
        setError(result.error || "Failed to rank candidates.");
        setRanking(false);
        setRankingStageIndex(-1);
      }
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Ranking failed. Ensure the backend is running.";
      setError(msg);
      setRanking(false);
      setRankingStageIndex(-1);
    }
  }

  const canSubmit = !!(descriptionValue?.trim() || file);

  return (
    <div className="space-y-5">
      {/* Page Header */}
      <div>
        <h1 className="text-[22px] font-extrabold text-white tracking-tight">JD Intelligence Engine</h1>
        <p className="text-[12px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>
          Paste or upload a job description — AI extracts skills, seniority, and ranking signals
        </p>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1fr_1fr]">

        {/* ── LEFT: Input Card ── */}
        <div className="rounded-xl border p-6 space-y-5"
          style={{ background: "var(--tm-bg-surface)", borderColor: "var(--tm-border)" }}>

          <div className="flex items-center gap-2 pb-4 border-b" style={{ borderColor: "var(--tm-border)" }}>
            <div className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ background: "rgba(37,99,235,0.1)", color: "#60A5FA" }}>
              <BrainCircuit size={15} />
            </div>
            <div>
              <div className="text-[13px] font-bold text-white">Job Description Input</div>
              <div className="text-[10px]" style={{ color: "var(--tm-text-muted)" }}>Upload .docx or paste text</div>
            </div>
          </div>

          <form onSubmit={handleSubmit(submit)} className="space-y-4">
            {/* Dropzone */}
            <div
              {...getRootProps()}
              className="relative flex min-h-[120px] cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed p-6 text-center transition-all duration-200"
              style={{
                background: isDragActive ? "rgba(37,99,235,0.08)" : "rgba(255,255,255,0.02)",
                borderColor: isDragActive ? "rgba(37,99,235,0.5)"
                  : file ? "rgba(16,185,129,0.4)"
                    : "rgba(255,255,255,0.1)",
              }}
            >
              <input {...getInputProps()} />
              {file ? (
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ background: "rgba(16,185,129,0.1)", color: "#6EE7B7" }}>
                    <CheckCircle2 size={18} />
                  </div>
                  <div className="text-left">
                    <div className="text-[13px] font-semibold text-white">{file.name}</div>
                    <div className="text-[10px]" style={{ color: "#6EE7B7" }}>Ready to analyze</div>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                    className="ml-2 p-1 rounded hover:bg-white/10 transition-colors"
                  >
                    <X size={13} style={{ color: "var(--tm-text-muted)" }} />
                  </button>
                </div>
              ) : (
                <>
                  <UploadCloud size={28} style={{ color: "rgba(37,99,235,0.7)" }} className="mb-2" />
                  <div className="text-[13px] font-semibold text-white">
                    {isDragActive ? "Drop it here…" : "Drop a .docx file"}
                  </div>
                  <div className="text-[11px] mt-1" style={{ color: "var(--tm-text-muted)" }}>
                    or click to browse
                  </div>
                </>
              )}
            </div>

            {/* Textarea */}
            <div>
              <div className="text-[11px] font-semibold mb-1.5" style={{ color: "var(--tm-text-secondary)" }}>
                Or paste job description text
              </div>
              <textarea
                {...register("description")}
                placeholder="We are looking for a Senior ML Engineer with expertise in Python, PyTorch, and LLMs. The candidate should have 5+ years of experience building production AI systems…"
                rows={8}
                className="w-full rounded-xl border p-3.5 text-[13px] leading-6 resize-none outline-none transition-all"
                style={{
                  background: "var(--tm-bg-elevated)",
                  borderColor: "var(--tm-border)",
                  color: "var(--tm-text-primary)",
                  caretColor: "#2563EB",
                }}
                onFocus={(e) => e.target.style.borderColor = "rgba(37,99,235,0.5)"}
                onBlur={(e) => e.target.style.borderColor = "var(--tm-border)"}
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={analyzing || ranking || !canSubmit}
              className="btn btn-primary w-full"
              style={{ justifyContent: "center", opacity: (!canSubmit && !analyzing) ? 0.5 : 1 }}
            >
              {analyzing ? (
                <><Loader2 size={15} className="animate-spin" /> Analyzing with Groq AI…</>
              ) : (
                <><Zap size={15} /> Run AI Analysis</>
              )}
            </button>

            {!canSubmit && (
              <p className="text-[11px] text-center" style={{ color: "var(--tm-text-muted)" }}>
                Upload a .docx or paste job description text above
              </p>
            )}
          </form>
        </div>

        {/* ── RIGHT: Results Panel ── */}
        <div className="space-y-4">

          {/* Loading state */}
          <AnimatePresence>
            {analyzing && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="rounded-xl border p-6"
                style={{ background: "var(--tm-bg-surface)", borderColor: "rgba(37,99,235,0.2)" }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center"
                    style={{ background: "rgba(37,99,235,0.1)" }}>
                    <Loader2 size={15} className="animate-spin" style={{ color: "#60A5FA" }} />
                  </div>
                  <div>
                    <div className="text-[13px] font-bold text-white">Processing with Groq AI</div>
                    <div className="text-[10px]" style={{ color: "var(--tm-text-muted)" }}>Extracting requirements…</div>
                  </div>
                </div>
                <div className="space-y-2">
                  {["Parsing job description", "Extracting required skills", "Identifying seniority signals"].map((step, i) => (
                    <motion.div
                      key={step}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.3 }}
                      className="flex items-center gap-2 text-[11px]"
                      style={{ color: "rgba(255,255,255,0.5)" }}
                    >
                      <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "#2563EB" }} />
                      {step}
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Ranking progress */}
          <AnimatePresence>
            {ranking && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="rounded-xl border p-6"
                style={{ background: "var(--tm-bg-surface)", borderColor: "rgba(124,58,237,0.2)" }}
              >
                <div className="text-[13px] font-bold text-white mb-4">AI Recruitment Pipeline</div>
                <div className="space-y-2.5">
                  {RANKING_STAGES.map((stage, i) => {
                    const done = i < rankingStageIndex;
                    const active = i === rankingStageIndex;
                    return (
                      <motion.div
                        key={stage.label}
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.08 }}
                        className="flex items-center gap-3 p-2.5 rounded-lg transition-all"
                        style={{
                          background: done ? "rgba(16,185,129,0.06)"
                            : active ? "rgba(37,99,235,0.08)"
                              : "rgba(255,255,255,0.02)",
                          borderLeft: active ? "2px solid #2563EB" : done ? "2px solid #10B981" : "2px solid transparent",
                        }}
                      >
                        <div className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center"
                          style={{
                            background: done ? "rgba(16,185,129,0.15)" : active ? "rgba(37,99,235,0.15)" : "rgba(255,255,255,0.05)",
                            color: done ? "#6EE7B7" : active ? "#60A5FA" : "rgba(255,255,255,0.25)",
                          }}>
                          {done ? <CheckCircle2 size={12} /> : active ? <Loader2 size={12} className="animate-spin" /> : <stage.icon size={12} />}
                        </div>
                        <span className="text-[12px] font-medium" style={{
                          color: done ? "#6EE7B7" : active ? "#fff" : "rgba(255,255,255,0.35)"
                        }}>
                          {stage.label}
                        </span>
                      </motion.div>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error */}
          <AnimatePresence>
            {error && !analyzing && !ranking && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="rounded-xl border p-4 flex items-start gap-3"
                style={{ background: "rgba(239,68,68,0.06)", borderColor: "rgba(239,68,68,0.2)" }}
              >
                <AlertCircle size={15} className="mt-0.5 flex-shrink-0" style={{ color: "#FCA5A5" }} />
                <div>
                  <div className="text-[12px] font-bold text-white mb-0.5">Analysis failed</div>
                  <p className="text-[11px] leading-5" style={{ color: "rgba(255,255,255,0.5)" }}>{error}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {jdAnalysis && !ranking && !analyzing && (
              <motion.div
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="rounded-xl border overflow-hidden"
                style={{ background: "var(--tm-bg-surface)", borderColor: "rgba(37,99,235,0.2)" }}
              >
                {/* Result header */}
                <div className="p-5 border-b" style={{ borderColor: "var(--tm-border)", background: "rgba(37,99,235,0.04)" }}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="pill pill-emerald">Analysis Complete</span>
                  </div>
                  <h2 className="text-[18px] font-extrabold text-white tracking-tight">
                    {jdAnalysis.analysis?.role ?? "Job Role"}
                  </h2>
                </div>

                <div className="p-5 space-y-5">
                  {/* Meta grid */}
                  <div className="grid grid-cols-2 gap-2.5">
                    {[
                      { label: "Experience",  value: jdAnalysis.analysis?.experienceRange, icon: Briefcase },
                      { label: "Seniority",   value: jdAnalysis.analysis?.seniority,       icon: Star },
                      { label: "Domain",      value: jdAnalysis.analysis?.domain,           icon: Target },
                      { label: "Location",    value: jdAnalysis.analysis?.location,         icon: MapPin },
                      { label: "Work Mode",   value: jdAnalysis.analysis?.workMode,         icon: Monitor },
                    ].filter(i => i.value).map(({ label, value, icon: Icon }) => (
                      <div key={label} className="flex items-start gap-2.5 p-3 rounded-lg"
                        style={{ background: "var(--tm-bg-elevated)", border: "1px solid var(--tm-border)" }}>
                        <Icon size={12} className="mt-0.5 flex-shrink-0" style={{ color: "var(--tm-text-muted)" }} />
                        <div>
                          <div className="text-[9px] font-bold uppercase tracking-widest mb-0.5"
                            style={{ color: "var(--tm-text-muted)" }}>{label}</div>
                          <div className="text-[12px] font-semibold text-white">{value}</div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Required skills */}
                  {jdAnalysis.analysis?.requiredSkills?.length > 0 && (
                    <div>
                      <div className="text-[11px] font-bold mb-2" style={{ color: "var(--tm-text-secondary)" }}>
                        Required Skills
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.analysis.requiredSkills.map((skill) => (
                          <span key={skill} className="pill pill-blue">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Preferred skills */}
                  {jdAnalysis.analysis?.preferredSkills?.length > 0 && (
                    <div>
                      <div className="text-[11px] font-bold mb-2" style={{ color: "var(--tm-text-secondary)" }}>
                        Preferred Skills
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.analysis.preferredSkills.map((skill) => (
                          <span key={skill} className="pill pill-violet">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* CTA */}
                  <button
                    onClick={startRanking}
                    disabled={ranking}
                    className="btn btn-primary w-full"
                    style={{ justifyContent: "center" }}
                  >
                    <Zap size={15} />
                    Start AI Candidate Ranking
                    <ChevronRight size={13} />
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Empty state (no analysis yet, not loading) */}
          {!jdAnalysis && !analyzing && !ranking && !error && (
            <div className="flex flex-col items-center justify-center py-16 text-center rounded-xl border"
              style={{ background: "var(--tm-bg-surface)", borderColor: "var(--tm-border)", borderStyle: "dashed" }}>
              <div className="w-14 h-14 rounded-2xl mb-4 flex items-center justify-center"
                style={{ background: "rgba(37,99,235,0.07)", border: "1px solid rgba(37,99,235,0.15)" }}>
                <BrainCircuit size={22} style={{ color: "#2563EB" }} />
              </div>
              <div className="font-bold text-white mb-2 text-[14px]">No analysis yet</div>
              <p className="text-[12px] max-w-xs" style={{ color: "var(--tm-text-muted)" }}>
                Enter a job description on the left and click <span className="text-white font-semibold">Run AI Analysis</span> to extract requirements and start ranking.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
