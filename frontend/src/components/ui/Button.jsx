import { cn } from "../../lib/utils";

const variants = {
  primary: "bg-primary text-primary-foreground shadow-glow hover:brightness-110",
  secondary: "bg-muted text-foreground hover:bg-muted/80",
  outline: "border bg-card/60 hover:bg-muted",
  ghost: "hover:bg-muted",
  danger: "bg-rose-600 text-white hover:bg-rose-500",
};

export function Button({ className, variant = "primary", size = "md", ...props }) {
  const sizes = {
    sm: "h-9 px-3 text-sm",
    md: "h-11 px-4 text-sm",
    lg: "h-12 px-5 text-base",
    icon: "h-10 w-10 p-0",
  };

  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:cursor-not-allowed disabled:opacity-60",
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    />
  );
}
