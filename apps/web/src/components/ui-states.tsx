export function StatusBanner({
  kind,
  children,
}: {
  kind: "info" | "error" | "success" | "warning";
  children: React.ReactNode;
}) {
  const styles = {
    info: "border-[var(--line)] bg-white text-[var(--ink)]",
    error: "border-red-300 bg-red-50 text-red-900",
    success: "border-emerald-300 bg-emerald-50 text-emerald-950",
    warning: "border-amber-300 bg-amber-50 text-amber-950",
  } as const;

  return (
    <div role="status" className={`rounded border px-3 py-2 text-sm ${styles[kind]}`}>
      {children}
    </div>
  );
}

export function EmptyState({
  title,
  body,
  action,
}: {
  title: string;
  body: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="rounded border border-dashed border-[var(--line)] bg-white px-6 py-10 text-center">
      <h2 className="font-display text-xl">{title}</h2>
      <p className="mt-2 text-sm text-[var(--muted)]">{body}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}

export function LoadingBlock({ label = "Loading" }: { label?: string }) {
  return (
    <div
      className="animate-pulse rounded border border-[var(--line)] bg-white p-6"
      aria-busy="true"
      aria-live="polite"
    >
      <p className="text-sm text-[var(--muted)]">{label}…</p>
      <div className="mt-4 h-3 w-2/3 rounded bg-slate-200" />
      <div className="mt-2 h-3 w-1/2 rounded bg-slate-200" />
    </div>
  );
}
