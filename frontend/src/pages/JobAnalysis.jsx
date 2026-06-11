import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import { CheckCircle2, FileText, Loader2, UploadCloud } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Textarea } from "../components/ui/Input";
import { Badge } from "../components/ui/Badge";
import { api } from "../services/api";
import { pipelineSteps } from "../data/mockData";

export function JobAnalysis() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [processing, setProcessing] = useState(false);
  const { register, handleSubmit } = useForm();
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    maxFiles: 1,
    onDrop: ([accepted]) => setFile(accepted),
  });

  async function submit(values) {
    setProcessing(true);
    const result = await api.analyzeJobDescription({ text: values.description, fileName: file?.name });
    setTimeout(() => {
      setAnalysis(result);
      setProcessing(false);
    }, 900);
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
      <Card>
        <h2 className="mb-2 text-2xl font-extrabold">Analyze a job description</h2>
        <p className="mb-5 text-sm leading-6 text-muted-foreground">Upload a `.docx` JD or paste requirements to extract skills, seniority, location, and ranking signals.</p>
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
          <Textarea {...register("description")} placeholder="Paste job description, responsibilities, required skills, and hiring preferences..." />
          <Button disabled={processing} className="w-full">
            {processing ? <Loader2 className="animate-spin" size={18} /> : <FileText size={18} />} Run AI analysis
          </Button>
        </form>
      </Card>
      <div className="space-y-6">
        {processing && (
          <Card>
            <div className="mb-4 text-lg font-extrabold">AI recruitment pipeline running</div>
            <div className="space-y-3">
              {pipelineSteps.map((step, index) => (
                <motion.div key={step} initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.1 }} className="flex items-center gap-3 rounded-lg bg-muted/45 p-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/15 text-primary">
                    {index < 5 ? <CheckCircle2 size={17} /> : <Loader2 className="animate-spin" size={17} />}
                  </div>
                  <span className="text-sm font-semibold">{step}</span>
                </motion.div>
              ))}
            </div>
          </Card>
        )}
        {analysis && (
          <Card>
            <div className="mb-5">
              <Badge tone="green">Analysis complete</Badge>
              <h2 className="mt-3 text-2xl font-extrabold">{analysis.role}</h2>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {[
                ["Experience", analysis.experienceRange],
                ["Seniority", analysis.seniority],
                ["Domain", analysis.domain],
                ["Location", analysis.location],
                ["Work mode", analysis.workMode],
              ].map(([label, value]) => (
                <div key={label} className="rounded-lg bg-muted/45 p-4">
                  <div className="text-xs font-bold uppercase text-muted-foreground">{label}</div>
                  <div className="mt-1 font-bold">{value}</div>
                </div>
              ))}
            </div>
            <div className="mt-5">
              <div className="mb-2 font-bold">Required skills</div>
              <div className="flex flex-wrap gap-2">{analysis.requiredSkills.map((skill) => <Badge key={skill}>{skill}</Badge>)}</div>
            </div>
            <div className="mt-5">
              <div className="mb-2 font-bold">Preferred skills</div>
              <div className="flex flex-wrap gap-2">{analysis.preferredSkills.map((skill) => <Badge key={skill} tone="violet">{skill}</Badge>)}</div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
