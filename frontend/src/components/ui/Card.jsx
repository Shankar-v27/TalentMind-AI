// Enterprise Card component
import { cn } from "../../lib/utils";

export function Card({ className, children, variant = "default", glow = false, ...props }) {
  const base = "card-enterprise";
  const variants = {
    default: "",
    kpi: "card-kpi",
    glass: "glass-card",
    flat: "rounded-xl border p-5",
  };

  return (
    <div
      className={cn(base, variants[variant], glow && "border-gradient", className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children, ...props }) {
  return (
    <div className={cn("flex items-center justify-between mb-4 pb-3 border-b", className)}
      style={{ borderColor: "var(--tm-border)" }}
      {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ className, children, ...props }) {
  return (
    <h3 className={cn("text-[14px] font-700 font-bold text-white tracking-tight", className)} {...props}>
      {children}
    </h3>
  );
}

export function KPICard({ label, value, delta, deltaPositive, icon: Icon, accent = "blue", trend, sublabel }) {
  const accentColors = {
    blue:   { text: "#60A5FA", glow: "rgba(37,99,235,0.2)",   border: "rgba(37,99,235,0.2)" },
    violet: { text: "#C4B5FD", glow: "rgba(124,58,237,0.2)",  border: "rgba(124,58,237,0.2)" },
    cyan:   { text: "#67E8F9", glow: "rgba(14,165,233,0.2)",  border: "rgba(14,165,233,0.2)" },
    emerald:{ text: "#6EE7B7", glow: "rgba(16,185,129,0.2)",  border: "rgba(16,185,129,0.2)" },
    amber:  { text: "#FCD34D", glow: "rgba(245,158,11,0.15)", border: "rgba(245,158,11,0.2)" },
    rose:   { text: "#FCA5A5", glow: "rgba(239,68,68,0.2)",   border: "rgba(239,68,68,0.2)" },
  };
  const c = accentColors[accent] || accentColors.blue;

  return (
    <div
      className="relative overflow-hidden rounded-xl p-5 border transition-all duration-300 hover:-translate-y-0.5 group"
      style={{
        background: `linear-gradient(135deg, var(--tm-bg-surface) 0%, var(--tm-bg-subtle) 100%)`,
        borderColor: "var(--tm-border)",
      }}
    >
      {/* Ambient glow */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
        style={{ background: `radial-gradient(circle at top left, ${c.glow}, transparent 70%)` }}
      />
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-3">
          {Icon && (
            <div
              className="flex items-center justify-center w-9 h-9 rounded-lg"
              style={{ background: c.glow, color: c.text }}
            >
              <Icon size={17} />
            </div>
          )}
          {delta !== undefined && (
            <span
              className="text-[11px] font-semibold px-2 py-0.5 rounded-full"
              style={{
                color: deltaPositive ? "#6EE7B7" : "#FCA5A5",
                background: deltaPositive ? "rgba(16,185,129,0.1)" : "rgba(239,68,68,0.1)",
              }}
            >
              {deltaPositive ? "↑" : "↓"} {delta}
            </span>
          )}
        </div>
        <div className="text-[26px] font-extrabold text-white tracking-tight leading-none mb-1">
          {value}
        </div>
        <div className="text-[12px] font-medium" style={{ color: "var(--tm-text-secondary)" }}>
          {label}
        </div>
        {sublabel && (
          <div className="text-[10px] mt-0.5" style={{ color: "var(--tm-text-muted)" }}>{sublabel}</div>
        )}
      </div>
    </div>
  );
}
