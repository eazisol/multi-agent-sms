"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  addFollowUpClosureEvidence,
  closeFollowUp,
  createFollowUp,
  formatUtc,
  listFollowUpEscalations,
  listFollowUpReminders,
  listOpenFollowUps,
  listQueries,
  processFollowUpOverdue,
  type ClientQuery,
  type FollowUp,
  type FollowUpEscalation,
  type FollowUpReminder,
} from "@/lib/api";
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceQueryId,
  setWorkspaceQueryId,
} from "@/lib/workspace";

export function FollowUpsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<FollowUp[]>([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [reminders, setReminders] = useState<FollowUpReminder[]>([]);
  const [escalations, setEscalations] = useState<FollowUpEscalation[]>([]);

  const [title, setTitle] = useState("");
  const [requiredResponse, setRequiredResponse] = useState("Reply with the requested details");
  const [closureCondition, setClosureCondition] = useState("Answer received and recorded");
  const [sourceQueryId, setSourceQueryId] = useState("");
  const [dueOffset, setDueOffset] = useState("24");
  const [evidenceRef, setEvidenceRef] = useState("");
  const [evidenceNote, setEvidenceNote] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const rows = await listOpenFollowUps(session);
      setItems(rows);
      setCurrentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load follow-ups");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    void (async () => {
      try {
        const rows = await listQueries(session, { limit: 100 });
        setQueries(rows);
        const workspace = getWorkspaceQueryId();
        setSourceQueryId((prev) => {
          if (prev && rows.some((r) => r.id === prev)) return prev;
          if (workspace && rows.some((r) => r.id === workspace)) return workspace;
          return rows[0]?.id ?? "";
        });
      } catch {
        setQueries([]);
      }
    })();
  }, [session]);

  const current = useMemo(
    () => items.find((item) => item.id === currentId) ?? null,
    [items, currentId],
  );

  const refreshDetail = useCallback(async () => {
    if (!currentId) {
      setReminders([]);
      setEscalations([]);
      return;
    }
    try {
      const [rem, esc] = await Promise.all([
        listFollowUpReminders(session, currentId),
        listFollowUpEscalations(session, currentId),
      ]);
      setReminders(rem);
      setEscalations(esc);
    } catch {
      setReminders([]);
      setEscalations([]);
    }
  }, [currentId, session]);

  useEffect(() => {
    void refreshDetail();
  }, [refreshDetail]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const queryId = sourceQueryId || getWorkspaceQueryId();
      const projectId = getWorkspaceProjectId();
      const sourceEntityId = queryId || projectId;
      if (!sourceEntityId) {
        setError("Select a linked inquiry, or set a workspace project on Projects");
        return;
      }
      if (queryId) setWorkspaceQueryId(queryId);
      const created = await createFollowUp(session, {
        title: title.trim(),
        source_entity_type: queryId ? "crm_query" : "project",
        source_entity_id: sourceEntityId,
        recipient_actor_id: session.actorId,
        owner_actor_id: session.actorId,
        required_response: requiredResponse.trim(),
        closure_condition: closureCondition.trim(),
        due_offset_hours: Number(dueOffset) || 24,
        project_id: projectId || undefined,
        rule_version_id: crypto.randomUUID(),
      });
      setCurrentId(created.id);
      setOk("Follow-up opened");
      setShowCreate(false);
      setTitle("");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create follow-up");
    }
  }

  async function onAddEvidence() {
    if (!current || !evidenceRef.trim()) return;
    setError(null);
    setOk(null);
    try {
      await addFollowUpClosureEvidence(session, current.id, {
        evidence_ref: evidenceRef.trim(),
        evidence_type: "response",
        note: evidenceNote.trim() || undefined,
      });
      setOk("Closure evidence recorded");
      setEvidenceRef("");
      setEvidenceNote("");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not add evidence");
    }
  }

  async function onClose() {
    if (!current) return;
    setError(null);
    setOk(null);
    try {
      await closeFollowUp(session, current.id);
      setOk("Follow-up closed");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not close follow-up");
    }
  }

  async function onProcessOverdue() {
    if (!current) return;
    setError(null);
    setOk(null);
    try {
      const result = await processFollowUpOverdue(session, current.id);
      setOk(
        `Overdue processed — reminders ${result.reminders_created}, escalations ${result.escalations_created}`,
      );
      await refreshDetail();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not process overdue");
    }
  }

  return (
    <AppShell title="Follow-ups" breadcrumbs={["Coordination", "Follow-ups"]}>
      <PageHeader
        title="Follow-ups"
        description="SLA-aware follow-ups with owners, due dates, reminders, escalations, and closure evidence."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New follow-up
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      {showCreate && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Open follow-up</h2>
            <p className="text-sm text-[var(--muted)]">
              Links to an inquiry from Queries when available. Owner and recipient default to your
              session actor.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create follow-up">
              <Field label="Title" className="md:col-span-2">
                <Input
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Client clarification on scope"
                />
              </Field>
              <Field label="Linked inquiry" className="md:col-span-2">
                <Select
                  value={sourceQueryId}
                  onChange={(e) => setSourceQueryId(e.target.value)}
                  aria-label="Linked inquiry"
                >
                  <option value="">Use workspace project if no inquiry</option>
                  {queries.map((q) => (
                    <option key={q.id} value={q.id}>
                      {q.subject}
                    </option>
                  ))}
                </Select>
              </Field>
              <Field label="Required response">
                <Input
                  required
                  value={requiredResponse}
                  onChange={(e) => setRequiredResponse(e.target.value)}
                />
              </Field>
              <Field label="Closure condition">
                <Input
                  required
                  value={closureCondition}
                  onChange={(e) => setClosureCondition(e.target.value)}
                />
              </Field>
              <Field label="Due offset (hours)">
                <Input
                  type="number"
                  min={1}
                  value={dueOffset}
                  onChange={(e) => setDueOffset(e.target.value)}
                />
              </Field>
              <div className="flex items-end justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Open follow-up</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[minmax(280px,360px)_1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Open follow-ups</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/follow-ups` (open only).</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No open follow-ups"
                body="Create a follow-up with an owner, due date, required response, and closure condition."
                action={
                  can(session.variant, "create") ? (
                    <Button onClick={() => setShowCreate(true)}>New follow-up</Button>
                  ) : null
                }
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {items.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => setCurrentId(item.id)}
                    className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                      item.id === currentId ? "bg-[var(--accent-soft)]" : ""
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">{item.title}</span>
                      <StatusBadge status={item.sla_paused ? "paused" : item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">Due {formatUtc(item.due_at)}</p>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        {current ? (
          <div className="space-y-4">
            <Card>
              <CardHeader className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="font-display text-xl">{current.title}</h2>
                  <p className="mt-1 text-sm text-[var(--muted)]">
                    {current.source_entity_type} · required: {current.required_response}
                  </p>
                </div>
                <StatusBadge status={current.status} />
              </CardHeader>
              <CardBody className="space-y-4 text-sm">
                <p>
                  <span className="text-[var(--muted)]">Due:</span> {formatUtc(current.due_at)}
                </p>
                <p>
                  <span className="text-[var(--muted)]">Closure:</span> {current.closure_condition}
                </p>
                <p>
                  <span className="text-[var(--muted)]">Direction:</span> {current.direction}
                </p>
                <Field label="Closure evidence">
                  <Input
                    value={evidenceRef}
                    onChange={(e) => setEvidenceRef(e.target.value)}
                    placeholder="message://reply-42 or ticket note"
                  />
                </Field>
                <Field label="Evidence note">
                  <Textarea
                    rows={2}
                    value={evidenceNote}
                    onChange={(e) => setEvidenceNote(e.target.value)}
                    placeholder="Optional context"
                  />
                </Field>
                <div className="flex flex-wrap gap-2">
                  <Button variant="outline" onClick={() => void onAddEvidence()}>
                    Add evidence
                  </Button>
                  <Button
                    disabled={!can(session.variant, "submit") && !can(session.variant, "approve")}
                    onClick={() => void onClose()}
                  >
                    Close follow-up
                  </Button>
                  <Button variant="ghost" onClick={() => void onProcessOverdue()}>
                    Process overdue
                  </Button>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <h3 className="font-display text-lg">Reminders</h3>
              </CardHeader>
              {reminders.length === 0 ? (
                <CardBody>
                  <p className="text-sm text-[var(--muted)]">No reminder events yet.</p>
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {reminders.map((r) => (
                    <li key={r.id} className="flex items-center justify-between gap-2 px-5 py-3 text-sm">
                      <span>{formatUtc(r.scheduled_for)}</span>
                      <StatusBadge status={r.status} />
                    </li>
                  ))}
                </ul>
              )}
            </Card>

            <Card>
              <CardHeader>
                <h3 className="font-display text-lg">Escalations</h3>
              </CardHeader>
              {escalations.length === 0 ? (
                <CardBody>
                  <p className="text-sm text-[var(--muted)]">No escalations yet.</p>
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {escalations.map((e) => (
                    <li key={e.id} className="px-5 py-3 text-sm">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span>{e.escalate_to_role_code}</span>
                        <StatusBadge status={e.status} />
                      </div>
                      <p className="mt-1 text-[var(--muted)]">{e.reason}</p>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        ) : !loading ? (
          <EmptyState title="Select a follow-up" body="Choose an open item from the list." />
        ) : null}
      </div>
    </AppShell>
  );
}
