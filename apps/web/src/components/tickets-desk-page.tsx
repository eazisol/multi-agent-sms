"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, LoadingBlock, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
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
import { can } from "@/lib/roles";
import {
  getWorkspaceProjectId,
  getWorkspaceTicketId,
  setWorkspaceProjectId,
  setWorkspaceTicketId,
} from "@/lib/workspace";

export function TicketsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
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
    const tid = getWorkspaceTicketId();
    if (tid) {
      // loaded after list refresh
    }
  }, []);

  const refresh = useCallback(async () => {
    if (!projectId) {
      setTickets([]);
      return;
    }
    setLoading(true);
    setError(null);
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
      setError(err instanceof ApiError ? err.problem.message : "Load tickets failed");
      setTickets([]);
    } finally {
      setLoading(false);
    }
  }, [active?.id, projectId, session]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    if (!projectId) {
      setError("Set a workspace project id (create one on Projects desk first)");
      return;
    }
    setError(null);
    setOk(null);
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
      setOk(`Ticket ${ticket.code} created in ${ticket.status}`);
      setTitle("");
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create ticket failed");
    }
  }

  async function onPrepareReady() {
    if (!active || !projectId) return;
    setError(null);
    setOk(null);
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
        description: description.trim() || ticket.description || "Desk description",
        acceptance_criteria:
          acceptance.trim() || ticket.acceptance_criteria || "Desk acceptance criteria",
        definition_of_done: dod.trim() || ticket.definition_of_done || "Tests pass",
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
          // already linked is fine for desk UX
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
      setOk("Ticket marked Ready");
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Ready prepare failed");
    }
  }

  async function onTransition(next: string) {
    if (!active) return;
    setError(null);
    setOk(null);
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
      setOk(`Status → ${updated.status}`);
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Transition failed");
    }
  }

  async function onReopen() {
    if (!active || !reopenReason.trim()) return;
    setError(null);
    setOk(null);
    try {
      const evidence = await addTicketEvidence(session, {
        ticket_id: active.id,
        evidence_type: "reopen_justification",
        title: "Reopen from tickets desk",
        summary: reopenReason.trim(),
      });
      const updated = await reopenTicket(session, active.id, {
        reason: reopenReason.trim(),
        evidence_id: evidence.id,
        next_status: "in_progress",
        expected_version: active.version,
      });
      setActive(updated);
      setOk("Ticket reopened");
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Reopen failed");
    }
  }

  return (
    <AppShell title="Tickets">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Tickets desk</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-300 work items with Definition of Ready / Done gates and authorized reopen.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        <label className="flex max-w-xl flex-col gap-1 text-sm">
          <span>Workspace project id</span>
          <input
            className="rounded border border-[var(--line)] px-3 py-2 font-mono text-xs"
            value={projectId}
            onChange={(e) => {
              setProjectId(e.target.value);
              setWorkspaceProjectId(e.target.value);
            }}
            placeholder="From Projects desk"
          />
        </label>

        {can(session.variant, "create") ? (
          <form
            onSubmit={onCreate}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-2"
            aria-label="Create ticket"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Code</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Title</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm md:col-span-2">
              <span>Description</span>
              <textarea
                rows={2}
                className="rounded border border-[var(--line)] px-3 py-2"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Acceptance criteria</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2"
                value={acceptance}
                onChange={(e) => setAcceptance(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Definition of Done</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2"
                value={dod}
                onChange={(e) => setDod(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Estimate</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2"
                value={estimate}
                onChange={(e) => setEstimate(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span>Phase id (optional)</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2 font-mono text-xs"
                value={phaseId}
                onChange={(e) => setPhaseId(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm md:col-span-2">
              <span>Requirement id (optional)</span>
              <input
                className="rounded border border-[var(--line)] px-3 py-2 font-mono text-xs"
                value={requirementId}
                onChange={(e) => setRequirementId(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:col-span-2 md:w-fit"
            >
              Create ticket
            </button>
          </form>
        ) : null}

        <section aria-label="Ticket list">
          <h3 className="font-display text-xl">Project tickets</h3>
          {loading ? <LoadingBlock label="Loading tickets" /> : null}
          {!loading && tickets.length === 0 ? (
            <EmptyState
              title="No tickets"
              body="Create a ticket for the workspace project."
            />
          ) : (
            <ul className="mt-3 divide-y divide-[var(--line)] rounded border border-[var(--line)] bg-white">
              {tickets.map((t) => (
                <li key={t.id}>
                  <button
                    type="button"
                    className={`flex w-full items-center justify-between px-4 py-3 text-left text-sm ${
                      active?.id === t.id ? "bg-[var(--accent-soft)]" : ""
                    }`}
                    onClick={() => {
                      setActive(t);
                      setWorkspaceTicketId(t.id);
                      void listReadinessChecks(session, t.id).then(setReadiness);
                      void listDoneChecks(session, t.id).then(setDoneChecks);
                    }}
                  >
                    <span>
                      <span className="font-medium">{t.code}</span> — {t.title}
                    </span>
                    <span className="text-[var(--muted)]">
                      {t.status} · {formatUtc(t.created_at)}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>

        {active ? (
          <section className="space-y-3 rounded border border-[var(--line)] bg-white p-4">
            <h3 className="font-display text-xl">
              {active.code} · {active.status}
            </h3>
            <p className="text-sm text-[var(--muted)]">version {active.version}</p>
            <div className="flex flex-wrap gap-2">
              {active.status === "backlog" ? (
                <button
                  type="button"
                  className="rounded border border-[var(--line)] px-3 py-2 text-sm"
                  onClick={() => void onPrepareReady()}
                >
                  Prepare &amp; mark Ready
                </button>
              ) : null}
              {[
                "assigned",
                "in_progress",
                "code_review",
                "ready_for_qa",
                "qa_in_progress",
                "passed_qa",
                "done",
              ].map((next) => (
                <button
                  key={next}
                  type="button"
                  className="rounded border border-[var(--line)] px-3 py-2 text-sm"
                  onClick={() => void onTransition(next)}
                >
                  → {next}
                </button>
              ))}
            </div>
            <div className="grid gap-2 text-sm md:grid-cols-2">
              <div>
                <p className="font-medium">Readiness checks</p>
                <ul className="mt-1 space-y-1">
                  {readiness.map((c) => (
                    <li key={c.id}>
                      {c.is_satisfied ? "[x]" : "[ ]"} {c.label}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="font-medium">Done checks</p>
                <ul className="mt-1 space-y-1">
                  {doneChecks.map((c) => (
                    <li key={c.id}>
                      {c.is_satisfied ? "[x]" : "[ ]"} {c.label}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            {active.status === "done" ? (
              <div className="flex flex-wrap items-end gap-2">
                <label className="flex min-w-[16rem] flex-1 flex-col gap-1 text-sm">
                  <span>Reopen reason</span>
                  <input
                    className="rounded border border-[var(--line)] px-3 py-2"
                    value={reopenReason}
                    onChange={(e) => setReopenReason(e.target.value)}
                  />
                </label>
                <button
                  type="button"
                  className="rounded border border-[var(--line)] px-3 py-2 text-sm"
                  onClick={() => void onReopen()}
                >
                  Reopen with evidence
                </button>
              </div>
            ) : null}
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}
