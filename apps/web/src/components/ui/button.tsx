import { cn } from "@/lib/cn";

type ButtonVariant =
  | "primary"
  | "secondary"
  | "outline"
  | "ghost"
  | "destructive"
  | "link"
  | "ai";

const variants: Record<ButtonVariant, string> = {
  primary:
    "bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)] shadow-sm",
  secondary:
    "bg-[var(--surface-muted)] text-[var(--ink)] hover:bg-[var(--line)]",
  outline:
    "border border-[var(--line-strong)] bg-[var(--surface)] text-[var(--ink)] hover:bg-[var(--surface-muted)]",
  ghost: "text-[var(--ink)] hover:bg-[var(--surface-muted)]",
  destructive: "bg-[var(--danger)] text-white hover:opacity-90",
  link: "text-[var(--accent)] underline-offset-4 hover:underline px-0",
  ai: "ai-gradient text-white hover:opacity-95 shadow-sm",
};

export function Button({
  className,
  variant = "primary",
  size = "md",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  size?: "sm" | "md" | "lg";
}) {
  const sizes = {
    sm: "h-8 px-3 text-xs",
    md: "h-9 px-3.5 text-sm",
    lg: "h-11 px-4 text-sm",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-[var(--radius-sm)] font-medium transition disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    />
  );
}
