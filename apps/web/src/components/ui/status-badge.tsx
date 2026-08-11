import { cn } from "@/lib/cn";

const tones: Record<string, string> = {
  draft: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200",
  backlog: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200",
  open: "bg-[var(--info-soft)] text-[var(--info)]",
  new: "bg-[var(--info-soft)] text-[var(--info)]",
  received: "bg-[var(--info-soft)] text-[var(--info)]",
  classified: "bg-[var(--accent-soft)] text-[var(--accent)]",
  qualifying: "bg-[var(--warning-soft)] text-[var(--warning)]",
  qualified: "bg-[var(--success-soft)] text-[var(--success)]",
  breached: "bg-[var(--danger-soft)] text-[var(--danger)]",
  in_progress: "bg-[var(--accent-soft)] text-[var(--accent)]",
  active: "bg-[var(--success-soft)] text-[var(--success)]",
  ready: "bg-cyan-100 text-cyan-800 dark:bg-cyan-950 dark:text-cyan-200",
  waiting: "bg-[var(--warning-soft)] text-[var(--warning)]",
  pending: "bg-[var(--warning-soft)] text-[var(--warning)]",
  pending_approval: "bg-[var(--warning-soft)] text-[var(--warning)]",
  approved: "bg-[var(--success-soft)] text-[var(--success)]",
  completed: "bg-[var(--success-soft)] text-[var(--success)]",
  done: "bg-[var(--success-soft)] text-[var(--success)]",
  passed_qa: "bg-[var(--success-soft)] text-[var(--success)]",
  blocked: "bg-[var(--danger-soft)] text-[var(--danger)]",
  failed: "bg-[var(--danger-soft)] text-[var(--danger)]",
  rejected: "bg-[var(--danger-soft)] text-[var(--danger)]",
  at_risk: "bg-[var(--warning-soft)] text-[var(--warning)]",
  cancelled: "bg-slate-100 text-slate-500",
  sent: "bg-[var(--success-soft)] text-[var(--success)]",
  confidential: "bg-violet-100 text-violet-800 dark:bg-violet-950 dark:text-violet-200",
};

function normalize(status: string) {
  return status.trim().toLowerCase().replace(/\s+/g, "_");
}

export function StatusBadge({
  status,
  className,
}: {
  status: string;
  className?: string;
}) {
  const key = normalize(status);
  const label = status.replace(/_/g, " ");
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium capitalize",
        tones[key] ?? "bg-[var(--surface-muted)] text-[var(--muted)]",
        className,
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current opacity-80" />
      {label}
    </span>
  );
}
