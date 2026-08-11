import { Button } from "@/components/ui/button";
import { cn } from "@/lib/cn";

export function EmptyState({
  title,
  body,
  action,
  secondaryAction,
  icon = "◇",
  className,
}: {
  title: string;
  body: string;
  action?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  icon?: string;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "rounded-[var(--radius-lg)] border border-dashed border-[var(--line-strong)] bg-[var(--surface)] px-6 py-14 text-center",
        className,
      )}
    >
      <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-[var(--surface-muted)] text-xl text-[var(--muted)]">
        {icon}
      </div>
      <h2 className="font-display text-xl tracking-tight">{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-sm text-[var(--muted)]">{body}</p>
      {(action || secondaryAction) && (
        <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
          {action}
          {secondaryAction}
        </div>
      )}
    </div>
  );
}

export function StatusBanner({
  kind,
  children,
}: {
  kind: "info" | "error" | "success" | "warning";
  children: React.ReactNode;
}) {
  const styles = {
    info: "border-[var(--info)]/30 bg-[var(--info-soft)] text-[var(--info)]",
    error: "border-[var(--danger)]/30 bg-[var(--danger-soft)] text-[var(--danger)]",
    success: "border-[var(--success)]/30 bg-[var(--success-soft)] text-[var(--success)]",
    warning: "border-[var(--warning)]/30 bg-[var(--warning-soft)] text-[var(--warning)]",
  } as const;

  return (
    <div role="status" className={`rounded-[var(--radius-sm)] border px-3 py-2 text-sm ${styles[kind]}`}>
      {children}
    </div>
  );
}

export function SkeletonRows({ rows = 5 }: { rows?: number }) {
  return (
    <div className="animate-pulse space-y-3 p-4" aria-busy="true" aria-live="polite">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <div className="h-3 w-1/3 rounded bg-[var(--line)]" />
          <div className="h-3 w-1/4 rounded bg-[var(--line)]" />
          <div className="h-3 w-16 rounded bg-[var(--line)]" />
        </div>
      ))}
    </div>
  );
}

export function PageHeader({
  title,
  description,
  actions,
  sticky = false,
}: {
  title: string;
  description?: string;
  actions?: React.ReactNode;
  /** Stick under the app header inside the main scroll region. */
  sticky?: boolean;
}) {
  return (
    <div
      className={cn(
        "mb-6 flex flex-wrap items-start justify-between gap-4",
        sticky &&
          "sticky top-0 z-20 -mx-4 mb-6 border-b border-[var(--line)] bg-[var(--background)]/95 px-4 py-4 backdrop-blur md:-mx-6 md:px-6",
      )}
    >
      <div>
        <h1 className="font-display text-[28px] leading-tight tracking-tight md:text-[32px]">
          {title}
        </h1>
        {description ? (
          <p className="mt-1 max-w-2xl text-sm text-[var(--muted)]">{description}</p>
        ) : null}
      </div>
      {actions ? <div className="flex flex-wrap items-center gap-2">{actions}</div> : null}
    </div>
  );
}

export { Button };
