"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";

import { useSession } from "@/components/session-provider";
import { LoadingBlock, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  formatUtc,
  getBaseline,
  listBaselineHistory,
  transitionBaseline,
  updateBaseline,
  type AuditEvent,
  type Baseline,
} from "@/lib/api";
import { can, isDisabled, isHidden } from "@/lib/roles";

const MUTABLE = new Set(["draft", "more_info_required", "rejected"]);

export function BaselineDetailPage({ baselineId }: { baselineId: string }) {
  const { session } = useSession();
  const [baseline, setBaseline] = useState<Baseline | null>(null);
  const [history, setHistory] = useState<AuditEvent[]>([]);
  const [tab, setTab] = useState<"summary" | "history">("summary");
  const [title, setTitle] = useState("");
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [row, hist] = await Promise.all([
        getBaseline(session, baselineId),
        listBaselineHistory(session, baselineId),
      ]);
      setBaseline(row);
      setTitle(row.title);
      setHistory(hist.items);
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setError("Baseline not found.");
      } else if (err instanceof ApiError && err.status === 403) {
        setError("Forbidden.");
      } else if (err instanceof ApiError) {
        setError(err.problem.message);
      } else {
        setError("Unable to load baseline.");
      }
      setBaseline(null);
    } finally {
      setLoading(false);
    }
  }, [session, baselineId]);

  useEffect(() => {
    void load();
  }, [load]);

  async function saveTitle(event: FormEvent) {
    event.preventDefault();
    if (!baseline) return;
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const updated = await updateBaseline(session, baseline.id, {
        title,
        expected_version: baseline.version,
      });
      setBaseline(updated);
      setMessage(`Saved. Version is now ${updated.version}.`);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Update failed");
    } finally {
      setBusy(false);
    }
  }

  async function runTransition(target: string) {
    if (!baseline) return;
    if ((target === "rejected" || target === "withdrawn") && !reason.trim()) {
      setError("Reason is required for reject/withdraw.");
      return;
    }
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const updated = await transitionBaseline(session, baseline.id, {
        target_status: target,
        expected_version: baseline.version,
        reason: reason.trim() || undefined,
      });
      setBaseline(updated);
      setMessage(`Transitioned to ${updated.approval_status}.`);
      setReason("");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Transition failed");
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <LoadingBlock label="Loading baseline" />;
  if (error && !baseline) return <StatusBanner kind="error">{error}</StatusBanner>;
  if (!baseline) return null;

  const mutable = MUTABLE.has(baseline.approval_status);
  const showEdit = can(session.variant, "edit_draft") && mutable;
  const nextActions: Array<{ label: string; target: string; action: "submit" | "approve" | "reject" }> =
    [];
  if (baseline.approval_status === "draft" && can(session.variant, "submit")) {
    nextActions.push({ label: "Submit", target: "submitted", action: "submit" });
  }
  if (baseline.approval_status === "submitted" && can(session.variant, "submit")) {
    nextActions.push({ label: "Start review", target: "under_review", action: "submit" });
  }
  if (baseline.approval_status === "under_review") {
    if (can(session.variant, "approve")) {
      nextActions.push({ label: "Approve", target: "approved", action: "approve" });
    } else if (isDisabled(session.variant, "approve") && !isHidden(session.variant, "approve")) {
      nextActions.push({ label: "Approve (disabled)", target: "approved", action: "approve" });
    }
    if (can(session.variant, "reject")) {
      nextActions.push({ label: "Reject", target: "rejected", action: "reject" });
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <Link href="/governance/baselines" className="text-sm text-[var(--accent)] underline">
          Back to list
        </Link>
        <h2 className="mt-2 font-display text-3xl tracking-tight">{baseline.title}</h2>
        <p className="text-sm text-[var(--muted)]">
          {baseline.baseline_key} · v{baseline.version} · {baseline.approval_status}
        </p>
      </div>

      {message ? <StatusBanner kind="success">{message}</StatusBanner> : null}
      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}

      <div role="tablist" aria-label="Baseline sections" className="flex gap-2">
        {(["summary", "history"] as const).map((name) => (
          <button
            key={name}
            type="button"
            role="tab"
            aria-selected={tab === name}
            className={`rounded px-3 py-1.5 text-sm ${
              tab === name
                ? "bg-[var(--accent)] text-white"
                : "border border-[var(--line)] bg-white"
            }`}
            onClick={() => setTab(name)}
          >
            {name === "summary" ? "Summary" : "Audit history"}
          </button>
        ))}
      </div>

      {tab === "summary" ? (
        <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <section className="space-y-4 rounded border border-[var(--line)] bg-white p-5">
            <h3 className="font-display text-xl">Summary</h3>
            <dl className="grid gap-3 text-sm sm:grid-cols-2">
              <Item label="Artifact" value={baseline.artifact_path} />
              <Item label="Document version" value={baseline.document_version} />
              <Item label="Classification" value={baseline.classification} />
              <Item label="Updated" value={formatUtc(baseline.updated_at)} />
              <Item label="Created" value={formatUtc(baseline.created_at)} />
              <Item label="Organization" value={baseline.organization_id} />
            </dl>

            {showEdit ? (
              <form onSubmit={saveTitle} className="space-y-3 border-t border-[var(--line)] pt-4">
                <label className="flex flex-col gap-1 text-sm" htmlFor="title">
                  <span>Title (mutable draft)</span>
                  <input
                    id="title"
                    className="rounded border border-[var(--line)] px-3 py-2"
                    value={title}
                    onChange={(event) => setTitle(event.target.value)}
                    required
                  />
                </label>
                <p className="text-xs text-[var(--muted)]">
                  Uses optimistic concurrency with expected version {baseline.version}.
                </p>
                <button
                  type="submit"
                  disabled={busy}
                  className="rounded border border-[var(--line)] px-3 py-2 text-sm disabled:opacity-50"
                >
                  Save title
                </button>
              </form>
            ) : (
              <p className="text-sm text-[var(--muted)]">
                {mutable
                  ? "Edit controls are hidden for this UI role."
                  : "Approved/terminal baselines are immutable here. Use a change request for material edits."}
              </p>
            )}
          </section>

          <section className="space-y-3 rounded border border-[var(--line)] bg-white p-5">
            <h3 className="font-display text-xl">Actions</h3>
            <label className="flex flex-col gap-1 text-sm" htmlFor="reason">
              <span>Reason (required for reject)</span>
              <textarea
                id="reason"
                className="min-h-20 rounded border border-[var(--line)] px-3 py-2"
                value={reason}
                onChange={(event) => setReason(event.target.value)}
              />
            </label>
            <div className="flex flex-col gap-2">
              {nextActions.length === 0 ? (
                <p className="text-sm text-[var(--muted)]">No transitions available for this state/role.</p>
              ) : (
                nextActions.map((action) => {
                  const disabled =
                    busy ||
                    isDisabled(session.variant, action.action) ||
                    !can(session.variant, action.action);
                  return (
                    <button
                      key={action.target}
                      type="button"
                      disabled={disabled}
                      title={
                        disabled
                          ? "Not permitted for this UI role, or server will reject"
                          : undefined
                      }
                      className="rounded bg-[var(--accent)] px-3 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
                      onClick={() => void runTransition(action.target)}
                    >
                      {action.label}
                    </button>
                  );
                })
              )}
            </div>
          </section>
        </div>
      ) : (
        <section className="rounded border border-[var(--line)] bg-white p-5">
          <h3 className="font-display text-xl">Audit history</h3>
          {history.length === 0 ? (
            <p className="mt-3 text-sm text-[var(--muted)]">No audit events.</p>
          ) : (
            <ol className="mt-4 space-y-3">
              {history.map((event) => (
                <li key={event.id} className="border-b border-[var(--line)] pb-3 text-sm last:border-0">
                  <p className="font-medium">
                    {event.action} · v{event.entity_version ?? "—"}
                  </p>
                  <p className="text-[var(--muted)]">
                    {event.actor_kind} · {formatUtc(event.created_at)}
                  </p>
                  {event.reason ? <p>Reason: {event.reason}</p> : null}
                </li>
              ))}
            </ol>
          )}
        </section>
      )}
    </div>
  );
}

function Item({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-[var(--muted)]">{label}</dt>
      <dd className="break-all font-medium">{value}</dd>
    </div>
  );
}
