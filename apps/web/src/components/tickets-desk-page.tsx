"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  addTicketEvidence,
  createTicket,
  formatUtc,
  linkTicketRequirement,
  listDoneChecks,
  listPhases,
  listReadinessChecks,
  listRequirements,
  listTickets,
  reopenTicket,
  satisfyDoneCheck,
  satisfyReadinessCheck,
  transitionTicket,
  updateTicket,
  type Ticket,
  type TicketCheck,
} from "@/lib/api";
import { notifyApiError, notifyError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceTicketId,
  setWorkspaceProjectId,
  setWorkspaceTicketId,
} from "@/lib/workspace";

const FLOW_TRANSITIONS = [
  "assigned",
  "in_progress",
  "code_review",
  "ready_for_qa",
  "qa_in_progress",
  "passed_qa",
  "done",
] as const;

export function TicketsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [projectId, setProjectId] = useState("");
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [active, setActive] = useState<Ticket | null>(null);
  const [readiness, setReadiness] = useState<TicketCheck[]>([]);
  const [doneChecks, setDoneChecks] = useState<TicketCheck[]>([]);
  const [code, setCode] = useState("T-1");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [acceptance, setAcceptance] = useState("");
  const [dod, setDod] = useState("");
  const [estimate, setEstimate] = useState("3");
  const [phaseId, setPhaseId] = useState("");
  const [requirementId, setRequirementId] = useState("");
  const [reopenReason, setReopenReason] = useState("");

  useEffect(() => {
    setProjectId(getWorkspaceProjectId());
  }, []);

  const refresh = useCallback(async () => {
    if (!projectId) {
      setTickets([]);
      return;
    }
    setLoading(true);
    try {
      const rows = await listTickets(session, projectId);
      setTickets(rows);
      const preferred = getWorkspaceTicketId();
      const selected =
        rows.find((t) => t.id === (active?.id ?? preferred)) ?? rows[0] ?? null;
      setActive(selected);
      if (selected) {
        setWorkspaceTicketId(selected.id);
        setReadiness(await listReadinessChecks(session, selected.id));
        setDoneChecks(await listDoneChecks(session, selected.id));
      } else {
        setReadiness([]);
        setDoneChecks([]);
      }
    } catch (err) {
      notifyApiError("Unable to load tickets", err);
      setTickets([]);
    } finally {
      setLoading(false);
    }
  }, [active?.id, projectId, session]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  function applyWorkspaceProject(id: string) {
    setProjectId(id);
    setWorkspaceProjectId(id);
  }

  async function selectTicket(ticket: Ticket) {
    setActive(ticket);
    setWorkspaceTicketId(ticket.id);
    try {
      setReadiness(await listReadinessChecks(session, ticket.id));
      setDoneChecks(await listDoneChecks(session, ticket.id));
    } catch {
      setReadiness([]);
      setDoneChecks([]);
    }
  }

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    if (!projectId) {
      notifyError("Select a workspace project first (create one on Projects)");
      return;
    }
    try {
      const ticket = await createTicket(session, {
        project_id: projectId,
        code: code.trim(),
        title: title.trim(),
        description: description.trim() || undefined,
        priority: "high",
        owner_actor_id: session.actorId,
        estimate_points: estimate || undefined,
        acceptance_criteria: acceptance.trim() || undefined,
        definition_of_done: dod.trim() || undefined,
        phase_id: phaseId || undefined,
        requirement_id: requirementId || undefined,
      });
      setWorkspaceProjectId(projectId);
      setWorkspaceTicketId(ticket.id);
      setActive(ticket);
      notifySuccess(`${ticket.code} created`);
      setTitle("");
      setDescription("");
      setShowCreate(false);
      await refresh();
    } catch (err) {
      notifyApiError("Could not create ticket", err);
    }
  }

  async function onPrepareReady() {
    if (!active || !projectId) return;
    try {
      let ticket = active;
      if (!phaseId) {
        const phases = await listPhases(session, projectId);
        if (phases[0]) setPhaseId(phases[0].id);
      }
      const reqs = requirementId
        ? [{ id: requirementId }]
        : await listRequirements(session, projectId);
      const req = reqs[0];
      if (req && !requirementId) setRequirementId(req.id);

      ticket = await updateTicket(session, ticket.id, {
        description: description.trim() || ticket.description || "Implementation work item",
        acceptance_criteria:
          acceptance.trim() || ticket.acceptance_criteria || "Meets stated acceptance criteria",
        definition_of_done: dod.trim() || ticket.definition_of_done || "Tests pass and reviewed",
        estimate_points: estimate || String(ticket.estimate_points ?? "3"),
        priority: "high",
        phase_id: phaseId || (await listPhases(session, projectId))[0]?.id,
        owner_actor_id: session.actorId,
        expected_version: ticket.version,
      });
      if (req) {
        try {
          await linkTicketRequirement(session, {
            ticket_id: ticket.id,
            requirement_id: req.id,
          });
        } catch {
          // already linked is fine
        }
      }
      const checks = await listReadinessChecks(session, ticket.id);
      for (const check of checks) {
        if (!check.is_satisfied) {
          await satisfyReadinessCheck(session, check.id, "desk");
        }
      }
      ticket = await transitionTicket(session, ticket.id, {
        next_status: "ready",
        expected_version: ticket.version,
      });
      setActive(ticket);
      notifySuccess("Ticket prepared and marked Ready");
      await refresh();
    } catch (err) {
      notifyApiError("Could not prepare Ready", err);
    }
  }

  async function onTransition(next: string) {
    if (!active) return;
    try {
      if (next === "done") {
        const checks = await listDoneChecks(session, active.id);
        for (const check of checks) {
          if (!check.is_satisfied) {
            await satisfyDoneCheck(session, check.id, "desk");
          }
        }
      }
      const updated = await transitionTicket(session, active.id, {
        next_status: next,
        expected_version: active.version,
        blocked_reason: next === "blocked" ? "Blocked from tickets desk" : undefined,
      });
      setActive(updated);
      notifySuccess(`Moved to ${updated.status.replace(/_/g, " ")}`);
      await refresh();
    } catch (err) {
      notifyApiError("Transition failed", err);
    }
  }

  async function onReopen() {
    if (!active || !reopenReason.trim()) return;
    try {
      const evidence = await addTicketEvidence(session, {
        ticket_id: active.id,
        evidence_type: "reopen_justification",
        title: "Reopen justification",
        summary: reopenReason.trim(),
      });
      const updated = await reopenTicket(session, active.id, {
        reason: reopenReason.trim(),
        evidence_id: evidence.id,
        next_status: "in_progress",
        expected_version: active.version,
      });
      setActive(updated);
      notifySuccess("Ticket reopened");
      setReopenReason("");
      await refresh();
    } catch (err) {
      notifyApiError("Reopen failed", err);
    }
  }

  return (
    <AppShell title="Tickets" breadcrumbs={["Project Delivery", "Tickets"]}>
      <PageHeader
        title="Tickets"
        description="Work items with readiness and done gates â€” prepare Ready, move through delivery, and reopen with evidence when needed."
        actions={
          can(session.variant, "create") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New ticket
            </Button>
          ) : null
        }
      />

      <Card className="mb-6">
        <CardBody>
          <Field
            label="Workspace project"
            hint="Use the project created on Projects to load its tickets."
          >
            <Input
              value={projectId}
              onChange={(e) => applyWorkspaceProject(e.target.value.trim())}
              placeholder="Create a project on Projects first"
            />
          </Field>
        </CardBody>
      </Card>

      {showCreate && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Create ticket</h2>
            <p className="text-sm text-[var(--muted)]">
              Capture enough detail for Definition of Ready before pulling into active work.
            </p>
          </CardHeader>
          <CardBody>
            <form
              onSubmit={onCreate}
              className="grid gap-4 md:grid-cols-2"
              aria-label="Create ticket"
            >
              <Field label="Code">
                <Input
                  required
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="T-12"
                />
              </Field>
              <Field label="Estimate">
                <Input
                  value={estimate}
                  onChange={(e) => setEstimate(e.target.value)}
                  placeholder="3"
                />
              </Field>
              <Field label="Title" className="md:col-span-2">
                <Input
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Implement secure sign-in"
                />
              </Field>
              <Field label="Description" className="md:col-span-2">
                <Textarea
                  rows={2}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="What needs to be built and any constraints"
                />
              </Field>
              <Field label="Acceptance criteria">
                <Input
                  value={acceptance}
                  onChange={(e) => setAcceptance(e.target.value)}
                  placeholder="Users can authenticate with MFA"
                />
              </Field>
              <Field label="Definition of Done">
                <Input
                  value={dod}
                  onChange={(e) => setDod(e.target.value)}
                  placeholder="Tests pass and peer review complete"
                />
              </Field>
              <div className="flex justify-end gap-2 md:col-span-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Create ticket</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[1fr_1.1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Ticket list</h2>
            <p className="text-sm text-[var(--muted)]">
              Select a ticket to prepare Ready, transition, or reopen.
            </p>
          </CardHeader>
          {!projectId ? (
            <CardBody>
              <EmptyState
                title="No project linked"
                body="Create a project on Projects, then open tickets for that workspace."
              />
            </CardBody>
          ) : loading ? (
            <SkeletonRows />
          ) : tickets.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No tickets yet"
                body="Create the first work item for this project."
                action={
                  can(session.variant, "create") ? (
                    <Button onClick={() => setShowCreate(true)}>New ticket</Button>
                  ) : null
                }
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {tickets.map((t) => (
                <li key={t.id}>
                  <button
                    type="button"
                    className={`flex w-full items-center justify-between gap-3 px-5 py-3 text-left text-sm hover:bg-[var(--surface-muted)]/70 ${
                      active?.id === t.id ? "bg-[var(--accent-soft)]/40" : ""
                    }`}
                    onClick={() => void selectTicket(t)}
                  >
                    <span>
                      <span className="font-medium">{t.code}</span>
                      <span className="ml-2 text-[var(--muted)]">{t.title}</span>
                    </span>
                    <span className="flex shrink-0 flex-col items-end gap-1">
                      <StatusBadge status={t.status} />
                      <span className="text-xs text-[var(--muted)]">{formatUtc(t.created_at)}</span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Actions</h2>
            <p className="text-sm text-[var(--muted)]">
              Readiness gates, status moves, and reopen with evidence.
            </p>
          </CardHeader>
          {!active ? (
            <CardBody>
              <EmptyState
                title="No ticket selected"
                body="Choose a ticket from the list to manage its delivery flow."
              />
            </CardBody>
          ) : (
            <CardBody className="space-y-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3 className="font-display text-xl">
                    {active.code} â€” {active.title}
                  </h3>
                  <p className="mt-1 text-xs text-[var(--muted)]">Revision {active.version}</p>
                </div>
                <StatusBadge status={active.status} />
              </div>

              <div className="flex flex-wrap gap-2">
                {active.status === "backlog" ? (
                  <Button onClick={() => void onPrepareReady()}>Prepare &amp; mark Ready</Button>
                ) : null}
                {FLOW_TRANSITIONS.map((next) => (
                  <Button
                    key={next}
                    size="sm"
                    variant="outline"
                    onClick={() => void onTransition(next)}
                  >
                    {next.replace(/_/g, " ")}
                  </Button>
                ))}
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <p className="mb-2 text-sm font-medium">Ready checks</p>
                  <ul className="space-y-1.5 text-sm">
                    {readiness.length === 0 ? (
                      <li className="text-[var(--muted)]">No checks yet</li>
                    ) : (
                      readiness.map((c) => (
                        <li key={c.id} className="flex items-start gap-2">
                          <span className={c.is_satisfied ? "text-[var(--success)]" : "text-[var(--muted)]"}>
                            {c.is_satisfied ? "âœ“" : "â—‹"}
                          </span>
                          <span>{c.label}</span>
                        </li>
                      ))
                    )}
                  </ul>
                </div>
                <div>
                  <p className="mb-2 text-sm font-medium">Done checks</p>
                  <ul className="space-y-1.5 text-sm">
                    {doneChecks.length === 0 ? (
                      <li className="text-[var(--muted)]">No checks yet</li>
                    ) : (
                      doneChecks.map((c) => (
                        <li key={c.id} className="flex items-start gap-2">
                          <span className={c.is_satisfied ? "text-[var(--success)]" : "text-[var(--muted)]"}>
                            {c.is_satisfied ? "âœ“" : "â—‹"}
                          </span>
                          <span>{c.label}</span>
                        </li>
                      ))
                    )}
                  </ul>
                </div>
              </div>

              {active.status === "done" ? (
                <div className="space-y-3 border-t border-[var(--line)] pt-4">
                  <Field label="Reopen reason" hint="Required evidence when returning a done ticket to active work.">
                    <Input
                      value={reopenReason}
                      onChange={(e) => setReopenReason(e.target.value)}
                      placeholder="Why this work must reopen"
                    />
                  </Field>
                  <Button
                    variant="outline"
                    disabled={!reopenReason.trim()}
                    onClick={() => void onReopen()}
                  >
                    Reopen with evidence
                  </Button>
                </div>
              ) : null}
            </CardBody>
          )}
        </Card>
      </div>
    </AppShell>
  );
}
