"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  addFollowUpClosureEvidence,
  closeFollowUp,
  createFollowUp,
  formatUtc,
  listFollowUpEscalations,
  listFollowUpReminders,
  listFollowUps,
  listQueries,
  processFollowUpOverdue,
  type ClientQuery,
  type FollowUp,
  type FollowUpEscalation,
  type FollowUpReminder,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifyError, notifySuccess } from "@/lib/toast";
import { newId } from "@/lib/id";
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceQueryId,
  setWorkspaceQueryId,
} from "@/lib/workspace";

export function FollowUpsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<FollowUp[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [status, setStatus] = useState("open");
  const [search, setSearch] = useState("");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
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
    try {
      const result = await listFollowUps(session, {
        status,
        q: search.trim() || undefined,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
      const rows = result.items;
      setCurrentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load follow-ups", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, status, search, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    void (async () => {
      try {
        const result = await listQueries(session, { limit: 100 });
        const rows = result.items;
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
    try {
      const queryId = sourceQueryId || getWorkspaceQueryId();
      const projectId = getWorkspaceProjectId();
      const sourceEntityId = queryId || projectId;
      if (!sourceEntityId) {
        notifyError("Select a linked inquiry, or set a workspace project on Projects");
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
        rule_version_id: newId(),
      });
      setCurrentId(created.id);
      notifySuccess("Follow-up opened");
      setShowCreate(false);
      setTitle("");
      setStatus("open");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create follow-up", err);
    }
  }

  async function onAddEvidence() {
    if (!current || !evidenceRef.trim()) return;
    try {
      await addFollowUpClosureEvidence(session, current.id, {
        evidence_ref: evidenceRef.trim(),
        evidence_type: "response",
        note: evidenceNote.trim() || undefined,
      });
      notifySuccess("Closure evidence recorded");
      setEvidenceRef("");
      setEvidenceNote("");
    } catch (err) {
      notifyApiError("Could not add evidence", err);
    }
  }

  async function onClose() {
    if (!current) return;
    try {
      await closeFollowUp(session, current.id);
      notifySuccess("Follow-up closed");
      await load();
    } catch (err) {
      notifyApiError("Could not close follow-up", err);
    }
  }

  async function onProcessOverdue() {
    if (!current) return;
    try {
      const result = await processFollowUpOverdue(session, current.id);
      notifySuccess(
        `Overdue processed — reminders ${result.reminders_created}, escalations ${result.escalations_created}`,
      );
      await refreshDetail();
    } catch (err) {
      notifyApiError("Could not process overdue", err);
    }
  }

  const listTitle =
    status === "open" ? "Open follow-ups" : status === "closed" ? "Closed follow-ups" : "Follow-ups";

  return (
    <AppShell title="Follow-ups" breadcrumbs={["Coordination", "Follow-ups"]} fill>
      <div className="flex min-h-0 flex-1 flex-col gap-4">
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

        {showCreate && can(session.variant, "create") ? (
          <Card className="shrink-0">
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

        <div className="flex shrink-0 flex-wrap items-end gap-3">
          <Field label="Status" className="mb-0 min-w-[10rem]">
            <Select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setOffset(0);
              }}
              aria-label="Filter follow-ups by status"
            >
              <option value="open">Open</option>
              <option value="closed">Closed</option>
              <option value="all">All</option>
            </Select>
          </Field>
          <div className="relative max-w-xs min-w-[12rem] flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
            <Input
              className="pl-9"
              placeholder="Search title"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setOffset(0);
              }}
              aria-label="Search follow-ups"
            />
          </div>
        </div>

        <div className="grid min-h-0 flex-1 gap-4 overflow-hidden lg:grid-cols-[minmax(280px,360px)_1fr]">
          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">{listTitle}</h2>
              <p className="text-sm text-[var(--muted)]">From `/api/v1/follow-ups`.</p>
            </CardHeader>
            {loading ? (
              <SkeletonRows />
            ) : items.length === 0 ? (
              <CardBody>
                <EmptyState
                  title={search.trim() || status !== "open" ? "No matching follow-ups" : "No open follow-ups"}
                  body={
                    search.trim() || status !== "open"
                      ? "Try a different search or status filter."
                      : "Create a follow-up with an owner, due date, required response, and closure condition."
                  }
                  action={
                    status === "open" && !search.trim() && can(session.variant, "create") ? (
                      <Button onClick={() => setShowCreate(true)}>New follow-up</Button>
                    ) : null
                  }
                />
              </CardBody>
            ) : (
              <ScrollRegion className="flex-1">
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
              </ScrollRegion>
            )}
            {!loading && (items.length > 0 || pageMeta.total > 0) ? (
              <div className="shrink-0">
                <ListPagination
                  page={pageMeta}
                  onOffsetChange={setOffset}
                  onLimitChange={setLimit}
                  label="follow-ups"
                />
              </div>
            ) : null}
          </Card>

          {current ? (
            <ScrollRegion className="min-h-0">
              <div className="grid gap-4 pb-2">
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
            </ScrollRegion>
          ) : !loading ? (
            <EmptyState title="Select a follow-up" body="Choose an item from the list." />
          ) : null}
        </div>
      </div>
    </AppShell>
  );
}
