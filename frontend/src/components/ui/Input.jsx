import { cn } from "../../lib/utils";

export function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        "h-11 w-full rounded-lg border bg-card/70 px-3 text-sm outline-none transition placeholder:text-muted-foreground focus:ring-2 focus:ring-primary/35",
        className,
      )}
      {...props}
    />
  );
}

export function Textarea({ className, ...props }) {
  return (
    <textarea
      className={cn(
        "min-h-36 w-full resize-none rounded-lg border bg-card/70 p-3 text-sm outline-none transition placeholder:text-muted-foreground focus:ring-2 focus:ring-primary/35",
        className,
      )}
      {...props}
    />
  );
}
