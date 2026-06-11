import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import { CheckCircle2, FileText, Loader2, UploadCloud, Zap } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Textarea } from "../components/ui/Input";
import { Badge } from "../components/ui/Badge";
import { api } from "../services/api";
import { useTalentMindStore } from "../state/useTalentMindStore";

const RANKING_STAGES = [
  "Understanding Job Requirements",
  "Loading 100,000 Candidate Profiles",
  "Semantic FAISS Retrieval",
  "Evaluating Skills & Experience",
  "Analyzing Behavioral Signals",
  "Generating AI Match Scores",
];

export function JobAnalysis() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [ranking, setRanking] = useState(false);
  const [error, setError] = useState("");
  const [rankingStageIndex, setRankingStageIndex] = useState(0);

  const { setJdAnalysis, clearSession, setCandidates } = useTalentMindStore();
  const jdAnalysis = useTalentMindStore((state) => state.jdAnalysis);
  const { register, handleSubmit } = useForm();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    maxFiles: 1,
    onDrop: ([accepted]) => setFile(accepted),
  });

  async function submit(values) {
    setAnalyzing(true);
    setError("");
    setFile(null); // Clear file after submit

    // Clear previous session when analyzing new JD
    await clearSession();

    const payload = new FormData();
    payload.append("text", values.description || "");

    if (file) {
      payload.append("file", file);
    }

    try {
      const result = await api.analyzeJobDescription(payload);
      if (result.success) {
        setJdAnalysis(result);
        setError("");
      } else {
        setError(result.error || "Failed to analyze JD");
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Unable to analyze this JD. Check that the backend is running and GROQ_API_KEY is set.";
      setError(errorMsg);
      console.error("Analysis error:", err);
    } finally {
      setAnalyzing(false);
    }
  }

  async function startRanking() {
    setRanking(true);
    setError("");
    setRankingStageIndex(0);

    try {
      // Simulate progressive stages
      for (let i = 0; i < RANKING_STAGES.length; i++) {
        setRankingStageIndex(i);
        await new Promise((resolve) => setTimeout(resolve, 800));
      }

      // Fetch ranking results
      const result = await api.rankCandidates();
      if (result.success) {
        setCandidates(result.candidates);
        navigate("/rankings");
      } else {
        setError(result.error || "Failed to rank candidates");
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to rank candidates";
      setError(errorMsg);
      console.error("Ranking error:", err);
      setRanking(false);
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
      {/* Upload Form Card */}
      <Card>
        <h2 className="mb-2 text-2xl font-extrabold">Analyze a job description</h2>
        <p className="mb-5 text-sm leading-6 text-muted-foreground">
          Upload a `.docx` JD or paste requirements to extract skills, seniority, location, and ranking signals.
        </p>
        <form onSubmit={handleSubmit(submit)} className="space-y-4">
          <div
            {...getRootProps()}
            className={`flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed p-6 text-center transition ${
              isDragActive ? "border-primary bg-primary/10" : "bg-muted/40"
            }`}
          >
            <input {...getInputProps()} />
            <UploadCloud className="mb-3 text-primary" size={34} />
            <div className="font-bold">{file ? file.name : "Drop a .docx job description"}</div>
            <div className="mt-1 text-sm text-muted-foreground">or click to browse</div>
          </div>
          <Textarea
            {...register("description")}
            placeholder="Paste job description, responsibilities, required skills, and hiring preferences..."
          />
          <Button disabled={analyzing || ranking} className="w-full">
            {analyzing ? <Loader2 className="animate-spin" size={18} /> : <FileText size={18} />}
            {analyzing ? "Analyzing..." : "Run AI analysis"}
          </Button>
        </form>
      </Card>

      {/* Results Panel */}
      <div className="space-y-6">
        {/* Analyzing Stage */}
        {analyzing && (
          <Card>
            <div className="mb-4 text-lg font-extrabold">Analyzing job description with Groq AI...</div>
            <motion.div
              animate={{ opacity: [0.5, 1] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className="flex items-center gap-3 rounded-lg bg-primary/10 p-4"
            >
              <Loader2 className="animate-spin text-primary" size={20} />
              <span className="font-semibold">Processing with Groq LLM</span>
            </motion.div>
          </Card>
        )}

        {/* Ranking Stage */}
        {ranking && (
          <Card>
            <div className="mb-4 text-lg font-extrabold">AI recruitment pipeline running</div>
            <div className="space-y-3">
              {RANKING_STAGES.map((stage, index) => (
                <motion.div
                  key={stage}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: Math.max(0, index - rankingStageIndex) * 0.1 }}
                  className={`flex items-center gap-3 rounded-lg p-3 transition ${
                    index < rankingStageIndex
                      ? "bg-green-500/10"
                      : index === rankingStageIndex
                        ? "bg-primary/15"
                        : "bg-muted/45"
                  }`}
                >
                  <div className={`flex h-8 w-8 items-center justify-center rounded-full ${index < rankingStageIndex ? "bg-green-500/20 text-green-400" : "bg-primary/15 text-primary"}`}>
                    {index < rankingStageIndex ? <CheckCircle2 size={17} /> : <Loader2 className={index === rankingStageIndex ? "animate-spin" : ""} size={17} />}
                  </div>
                  <span className="text-sm font-semibold">{stage}</span>
                </motion.div>
              ))}
            </div>
          </Card>
        )}

        {/* Error Display */}
        {error && !analyzing && !ranking && (
          <Card>
            <div className="font-bold text-red-400">Analysis failed</div>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">{error}</p>
          </Card>
        )}

        {/* Analysis Results */}
        {jdAnalysis && !ranking && (
          <Card>
            <div className="mb-5">
              <Badge tone="green">Analysis complete</Badge>
              <h2 className="mt-3 text-2xl font-extrabold">{jdAnalysis.analysis.role}</h2>
            </div>

            {/* Job Details Grid */}
            <div className="grid gap-4 sm:grid-cols-2">
              {[
                ["Experience", jdAnalysis.analysis.experienceRange],
                ["Seniority", jdAnalysis.analysis.seniority],
                ["Domain", jdAnalysis.analysis.domain],
                ["Location", jdAnalysis.analysis.location],
                ["Work mode", jdAnalysis.analysis.workMode],
              ].map(([label, value]) => (
                <div key={label} className="rounded-lg bg-muted/45 p-4">
                  <div className="text-xs font-bold uppercase text-muted-foreground">{label}</div>
                  <div className="mt-1 font-bold">{value}</div>
                </div>
              ))}
            </div>

            {/* Required Skills */}
            <div className="mt-5">
              <div className="mb-2 font-bold">Required skills</div>
              <div className="flex flex-wrap gap-2">
                {jdAnalysis.analysis.requiredSkills.map((skill) => (
                  <Badge key={skill}>{skill}</Badge>
                ))}
              </div>
            </div>

            {/* Preferred Skills */}
            <div className="mt-5">
              <div className="mb-2 font-bold">Preferred skills</div>
              <div className="flex flex-wrap gap-2">
                {jdAnalysis.analysis.preferredSkills.map((skill) => (
                  <Badge key={skill} tone="violet">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Ranking Button */}
            <Button
              onClick={startRanking}
              disabled={ranking}
              className="mt-6 w-full bg-gradient-to-r from-primary to-primary/80"
            >
              <Zap size={18} />
              Start AI Candidate Ranking
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
}
