import { formatPercent } from "../../lib/utils";

export function ProgressRing({ value = 0, size = 112, stroke = 10, label = "Match" }) {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} strokeWidth={stroke} className="fill-none stroke-muted" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="fill-none stroke-primary transition-all duration-700"
        />
      </svg>
      <div className="absolute text-center">
        <div className="text-2xl font-extrabold">{formatPercent(value)}</div>
        <div className="text-[11px] font-semibold uppercase text-muted-foreground">{label}</div>
      </div>
    </div>
  );
}
