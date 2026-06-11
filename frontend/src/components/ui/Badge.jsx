import { cn } from "../../lib/utils";

export function Badge({ className, tone = "blue", ...props }) {
  const tones = {
    blue: "bg-blue-500/12 text-blue-600 dark:text-blue-300",
    violet: "bg-violet-500/12 text-violet-600 dark:text-violet-300",
    cyan: "bg-cyan-500/12 text-cyan-700 dark:text-cyan-300",
    green: "bg-emerald-500/12 text-emerald-700 dark:text-emerald-300",
    amber: "bg-amber-500/14 text-amber-700 dark:text-amber-300",
    slate: "bg-slate-500/12 text-slate-700 dark:text-slate-300",
  };

  return (
    <span
      className={cn("inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold", tones[tone], className)}
      {...props}
    />
  );
}
