"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, LoadingBlock, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  approveMilestone,
  completeMilestone,
  completePhase,
  createMilestone,
  createPhase,
  listPhases,
  type Milestone,
  type Phase,
} from "@/lib/api";
import { can } from "@/lib/roles";
import { getWorkspaceProjectId, setWorkspaceProjectId } from "@/lib/workspace";

export function RoadmapDeskPage() {
  const { session } = useSession();
  const [projectId, setProjectId] = useState("");
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [phaseCode, setPhaseCode] = useState("DISCOVER");
  const [phaseTitle, setPhaseTitle] = useState("Discovery");
  const [milestone, setMilestone] = useState<Milestone | null>(null);

  useEffect(() => {
    setProjectId(getWorkspaceProjectId());
  }, []);

  const refresh = useCallback(async () => {
    if (!projectId) {
      setPhases([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setPhases(await listPhases(session, projectId));
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Load phases failed");
      setPhases([]);
    } finally {
      setLoading(false);
    }
  }, [projectId, session]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function onCreatePhase(event: FormEvent) {
    event.preventDefault();
    if (!projectId) return;
    setError(null);
    setOk(null);
    try {
      const phase = await createPhase(session, {
        project_id: projectId,
        code: phaseCode.trim().toUpperCase(),
        title: phaseTitle.trim(),
        sequence: phases.length + 1,
      });
      setOk(`Phase ${phase.code} created`);
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create phase failed");
    }
  }

  async function onAddMilestone(phaseId: string) {
    setError(null);
    setOk(null);
    try {
      const created = await createMilestone(session, {
        phase_id: phaseId,
        code: `MS-${Date.now().toString().slice(-4)}`,
        title: "Kickoff milestone",
        owner_actor_id: session.actorId,
        target_date: new Date().toISOString().slice(0, 10),
        requires_approval: true,
      });
      setMilestone(created);
      setOk(`Milestone ${created.code} created`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Milestone create failed");
    }
  }

  async function onApproveMs() {
    if (!milestone) return;
    try {
      const approved = await approveMilestone(session, milestone.id);
      setMilestone(approved);
      setOk("Milestone approved");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Approve failed");
    }
  }

  async function onCompleteMs() {
    if (!milestone) return;
    try {
      const done = await completeMilestone(session, milestone.id);
      setMilestone(done);
      setOk("Milestone completed");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Complete failed");
    }
  }

  async function onCompletePhase(phaseId: string) {
    setError(null);
    setOk(null);
    try {
      await completePhase(session, phaseId);
      setOk("Phase completed");
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Phase complete failed");
    }
  }

  return (
    <AppShell title="Roadmap">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Roadmap desk</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-260 phases and milestones for a workspace project.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        <label className="flex flex-col gap-1 text-sm">
          <span>Project id</span>
          <input
            className="rounded border border-[var(--line)] bg-white px-3 py-2 font-mono text-xs"
            value={projectId}
            onChange={(e) => {
              setProjectId(e.target.value);
              setWorkspaceProjectId(e.target.value);
            }}
            placeholder="Create a project on the Projects desk first"
          />
        </label>

        {can(session.variant, "create") && projectId ? (
          <form
            onSubmit={onCreatePhase}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-3"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Phase code</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={phaseCode}
                onChange={(e) => setPhaseCode(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm md:col-span-2">
              <span>Title</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={phaseTitle}
                onChange={(e) => setPhaseTitle(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:w-fit"
            >
              Add phase
            </button>
          </form>
        ) : null}

        {loading ? <LoadingBlock label="Loading phases" /> : null}
        {!loading && projectId && phases.length === 0 ? (
          <EmptyState title="No phases" body="Add a discovery/build phase for this project." />
        ) : null}

        <ul className="space-y-3">
          {phases.map((phase) => (
            <li
              key={phase.id}
              className="rounded border border-[var(--line)] bg-white p-4 text-sm"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <strong>{phase.code}</strong> — {phase.title}{" "}
                  <span className="text-[var(--muted)]">({phase.status})</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    className="rounded border border-[var(--line)] px-3 py-1.5"
                    onClick={() => void onAddMilestone(phase.id)}
                    disabled={!can(session.variant, "create")}
                  >
                    Add milestone
                  </button>
                  <button
                    type="button"
                    className="rounded border border-[var(--line)] px-3 py-1.5"
                    onClick={() => void onCompletePhase(phase.id)}
                    disabled={
                      phase.status === "completed" || !can(session.variant, "approve")
                    }
                  >
                    Complete phase
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>

        {milestone ? (
          <section className="rounded border border-[var(--line)] bg-white p-4 text-sm">
            <p>
              Latest milestone <strong>{milestone.code}</strong> · {milestone.status} ·{" "}
              {milestone.target_date}
            </p>
            <div className="mt-2 flex gap-2">
              <button
                type="button"
                className="rounded border border-[var(--line)] px-3 py-1.5"
                onClick={() => void onApproveMs()}
                disabled={!can(session.variant, "approve")}
              >
                Approve
              </button>
              <button
                type="button"
                className="rounded border border-[var(--line)] px-3 py-1.5"
                onClick={() => void onCompleteMs()}
                disabled={!can(session.variant, "approve")}
              >
                Complete
              </button>
            </div>
          </section>
        ) : null}
      </div>
    </AppShell>
  );
}
