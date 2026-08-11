"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Flag, Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
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
  const [showCreate, setShowCreate] = useState(false);
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
      setError(err instanceof ApiError ? err.problem.message : "Unable to load phases");
      setPhases([]);
    } finally {
      setLoading(false);
    }
  }, [projectId, session]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  function applyWorkspaceProject(id: string) {
    setProjectId(id);
    setWorkspaceProjectId(id);
  }

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
      setOk(`${phase.title} phase added`);
      setShowCreate(false);
      await refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create phase");
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
      setOk(`Milestone ${created.title} created`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create milestone");
    }
  }

  async function onApproveMs() {
    if (!milestone) return;
    try {
      const approved = await approveMilestone(session, milestone.id);
      setMilestone(approved);
      setOk("Milestone approved");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Approval failed");
    }
  }

  async function onCompleteMs() {
    if (!milestone) return;
    try {
      const done = await completeMilestone(session, milestone.id);
      setMilestone(done);
      setOk("Milestone completed");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not complete milestone");
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
      setError(err instanceof ApiError ? err.problem.message : "Could not complete phase");
    }
  }

  return (
    <AppShell title="Roadmaps" breadcrumbs={["Project Delivery", "Roadmaps"]}>
      <PageHeader
        title="Roadmaps"
        description="Phases and checkpoints for the workspace project â€” plan discovery, build, and release milestones."
        actions={
          can(session.variant, "create") && projectId ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Add phase
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      <Card className="mb-6">
        <CardBody>
          <Field
            label="Workspace project"
            hint="Use the project created on Projects to load and edit its roadmap."
          >
            <Input
              value={projectId}
              onChange={(e) => applyWorkspaceProject(e.target.value.trim())}
              placeholder="Create a project on Projects first"
            />
          </Field>
        </CardBody>
      </Card>

      {showCreate && projectId && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Add phase</h2>
            <p className="text-sm text-[var(--muted)]">
              Phases sequence the delivery journey â€” Discovery, Build, Launch, and beyond.
            </p>
          </CardHeader>
          <CardBody>
            <form
              onSubmit={onCreatePhase}
              className="grid gap-4 md:grid-cols-3"
              aria-label="Add phase"
            >
              <Field label="Code">
                <Input
                  required
                  value={phaseCode}
                  onChange={(e) => setPhaseCode(e.target.value)}
                  placeholder="DISCOVER"
                />
              </Field>
              <Field label="Title" className="md:col-span-2">
                <Input
                  required
                  value={phaseTitle}
                  onChange={(e) => setPhaseTitle(e.target.value)}
                  placeholder="Discovery"
                />
              </Field>
              <div className="flex justify-end gap-2 md:col-span-3">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Add phase</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <Card>
        <CardHeader>
          <h2 className="font-display text-lg">Phases</h2>
          <p className="text-sm text-[var(--muted)]">
            Track status and attach milestones that need approval.
          </p>
        </CardHeader>
        {!projectId ? (
          <CardBody>
            <EmptyState
              title="No project linked"
              body="Open Projects, create a delivery project, then return here to plan phases."
            />
          </CardBody>
        ) : loading ? (
          <SkeletonRows />
        ) : phases.length === 0 ? (
          <CardBody>
            <EmptyState
              title="No phases yet"
              body="Add a discovery or build phase to start the roadmap."
              action={
                can(session.variant, "create") ? (
                  <Button onClick={() => setShowCreate(true)}>
                    <Plus className="h-4 w-4" />
                    Add phase
                  </Button>
                ) : null
              }
            />
          </CardBody>
        ) : (
          <ul className="divide-y divide-[var(--line)]">
            {phases.map((phase) => (
              <li key={phase.id} className="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="font-medium">{phase.title}</p>
                    <StatusBadge status={phase.status} />
                  </div>
                  <p className="mt-1 text-xs text-[var(--muted)]">{phase.code}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    disabled={!can(session.variant, "create")}
                    onClick={() => void onAddMilestone(phase.id)}
                  >
                    <Flag className="h-3.5 w-3.5" />
                    Add milestone
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    disabled={
                      phase.status === "completed" || !can(session.variant, "approve")
                    }
                    onClick={() => void onCompletePhase(phase.id)}
                  >
                    Complete phase
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      {milestone ? (
        <Card className="mt-6">
          <CardHeader className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 className="font-display text-lg">{milestone.title}</h3>
              <p className="text-sm text-[var(--muted)]">
                {milestone.code} Â· target {milestone.target_date}
              </p>
            </div>
            <StatusBadge status={milestone.status} />
          </CardHeader>
          <CardBody className="flex flex-wrap gap-2">
            <Button
              variant="outline"
              disabled={!can(session.variant, "approve")}
              onClick={() => void onApproveMs()}
            >
              Approve
            </Button>
            <Button
              disabled={!can(session.variant, "approve")}
              onClick={() => void onCompleteMs()}
            >
              Complete
            </Button>
          </CardBody>
        </Card>
      ) : null}
    </AppShell>
  );
}
