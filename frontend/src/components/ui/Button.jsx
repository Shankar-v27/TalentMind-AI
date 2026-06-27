import { cn } from "../../lib/utils";

export function Button({
  children, className, variant = "primary", size = "md",
  disabled, onClick, type = "button", ...props
}) {
  const sizes = { sm: "btn-sm", md: "", lg: "btn-lg", icon: "btn-icon" };
  const variants = {
    primary: "btn-primary",
    ghost:   "btn-ghost",
    outline: "btn-ghost",
    danger:  "btn btn-sm",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={cn("btn", variants[variant], sizes[size], disabled && "opacity-50 cursor-not-allowed", className)}
      {...props}
    >
      {children}
    </button>
  );
}
