import { cn } from "../../lib/utils";

const TONE_MAP = {
  blue:    "pill-blue",
  violet:  "pill-violet",
  cyan:    "pill-cyan",
  green:   "pill-emerald",
  emerald: "pill-emerald",
  amber:   "pill-amber",
  rose:    "pill-rose",
  red:     "pill-rose",
  default: "pill-blue",
};

export function Badge({ children, tone = "default", className, ...props }) {
  return (
    <span className={cn("pill", TONE_MAP[tone] ?? "pill-blue", className)} {...props}>
      {children}
    </span>
  );
}
