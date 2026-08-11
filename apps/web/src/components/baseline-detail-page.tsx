"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";

import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
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
        setError("You don’t have permission to view this baseline.");
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
      setMessage(`Title saved (revision ${updated.version}).`);
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
      setError("A reason is required to reject or withdraw.");
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
      setMessage(`Moved to ${updated.approval_status.replace(/_/g, " ")}.`);
      setReason("");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Transition failed");
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <Card>
        <SkeletonRows rows={6} />
      </Card>
    );
  }
  if (error && !baseline) return <StatusBanner kind="error">{error}</StatusBanner>;
  if (!baseline) return null;

  const mutable = MUTABLE.has(baseline.approval_status);
  const showEdit = can(session.variant, "edit_draft") && mutable;
  const nextActions: Array<{
    label: string;
    target: string;
    action: "submit" | "approve" | "reject";
  }> = [];
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
      nextActions.push({ label: "Approve (unavailable)", target: "approved", action: "approve" });
    }
    if (can(session.variant, "reject")) {
      nextActions.push({ label: "Reject", target: "rejected", action: "reject" });
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/governance/baselines"
          className="text-sm font-medium text-[var(--accent)] hover:underline"
        >
          Back to source baselines
        </Link>
        <PageHeader
          title={baseline.title}
          description={`${baseline.baseline_key} · revision ${baseline.version}`}
          actions={<StatusBadge status={baseline.approval_status} />}
        />
      </div>

      {message ? <StatusBanner kind="success">{message}</StatusBanner> : null}
      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}

      <div role="tablist" aria-label="Baseline sections" className="flex gap-2">
        {(["summary", "history"] as const).map((name) => (
          <Button
            key={name}
            type="button"
            role="tab"
            aria-selected={tab === name}
            size="sm"
            variant={tab === name ? "primary" : "outline"}
            onClick={() => setTab(name)}
          >
            {name === "summary" ? "Summary" : "Audit history"}
          </Button>
        ))}
      </div>

      {tab === "summary" ? (
        <div className="grid gap-4 lg:grid-cols-[2fr_1fr]">
          <Card>
            <CardHeader>
              <h3 className="font-display text-lg">Summary</h3>
            </CardHeader>
            <CardBody className="space-y-4">
              <dl className="grid gap-3 text-sm sm:grid-cols-2">
                <Item label="Artifact" value={baseline.artifact_path} />
                <Item label="Document version" value={baseline.document_version} />
                <Item label="Classification" value={baseline.classification} />
                <Item label="Updated" value={formatUtc(baseline.updated_at)} />
                <Item label="Created" value={formatUtc(baseline.created_at)} />
              </dl>

              {showEdit ? (
                <form
                  onSubmit={saveTitle}
                  className="space-y-3 border-t border-[var(--line)] pt-4"
                >
                  <Field label="Title">
                    <Input
                      value={title}
                      onChange={(event) => setTitle(event.target.value)}
                      required
                    />
                  </Field>
                  <Button type="submit" variant="outline" disabled={busy}>
                    Save title
                  </Button>
                </form>
              ) : (
                <p className="text-sm text-[var(--muted)]">
                  {mutable
                    ? "Edit controls are hidden for your role."
                    : "Approved baselines are immutable here. Use a change request for material edits."}
                </p>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="font-display text-lg">Actions</h3>
            </CardHeader>
            <CardBody className="space-y-3">
              <Field label="Reason" hint="Required when rejecting or withdrawing.">
                <Textarea
                  rows={4}
                  value={reason}
                  onChange={(event) => setReason(event.target.value)}
                />
              </Field>
              <div className="flex flex-col gap-2">
                {nextActions.length === 0 ? (
                  <p className="text-sm text-[var(--muted)]">
                    No transitions available for this state or role.
                  </p>
                ) : (
                  nextActions.map((action) => {
                    const disabled =
                      busy ||
                      isDisabled(session.variant, action.action) ||
                      !can(session.variant, action.action);
                    return (
                      <Button
                        key={action.target}
                        type="button"
                        disabled={disabled}
                        variant={action.action === "reject" ? "destructive" : "primary"}
                        onClick={() => void runTransition(action.target)}
                      >
                        {action.label}
                      </Button>
                    );
                  })
                )}
              </div>
            </CardBody>
          </Card>
        </div>
      ) : (
        <Card>
          <CardHeader>
            <h3 className="font-display text-lg">Audit history</h3>
          </CardHeader>
          <CardBody>
            {history.length === 0 ? (
              <p className="text-sm text-[var(--muted)]">No audit events yet.</p>
            ) : (
              <ol className="space-y-3">
                {history.map((event) => (
                  <li
                    key={event.id}
                    className="border-b border-[var(--line)] pb-3 text-sm last:border-0"
                  >
                    <p className="font-medium">
                      {event.action.replace(/_/g, " ")}
                      {event.entity_version != null ? ` · revision ${event.entity_version}` : ""}
                    </p>
                    <p className="text-[var(--muted)]">
                      {event.actor_kind} · {formatUtc(event.created_at)}
                    </p>
                    {event.reason ? <p className="mt-1">Reason: {event.reason}</p> : null}
                  </li>
                ))}
              </ol>
            )}
          </CardBody>
        </Card>
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
