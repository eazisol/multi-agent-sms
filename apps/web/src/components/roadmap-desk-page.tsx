"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Flag, Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  approveMilestone,
  completeMilestone,
  completePhase,
  createMilestone,
  createPhase,
  listMilestones,
  listPhases,
  listProjects,
  type Milestone,
  type Phase,
  type Project,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";
import { getWorkspaceProjectId, setWorkspaceProjectId } from "@/lib/workspace";

export function RoadmapDeskPage() {
  const { session } = useSession();
  const [projects, setProjects] = useState<Project[]>([]);
  const [projectId, setProjectId] = useState("");
  const [phases, setPhases] = useState<Phase[]>([]);
  const [milestones, setMilestones] = useState<Milestone[]>([]);
  const [selectedMilestoneId, setSelectedMilestoneId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [phaseCode, setPhaseCode] = useState("DISCOVER");
  const [phaseTitle, setPhaseTitle] = useState("Discovery");

  useEffect(() => {
    void (async () => {
      try {
        const result = await listProjects(session, { limit: 100 });
        const rows = result.items;
        setProjects(rows);
        const workspace = getWorkspaceProjectId();
        setProjectId((prev) => {
          if (prev && rows.some((r) => r.id === prev)) return prev;
          if (workspace && rows.some((r) => r.id === workspace)) return workspace;
          return rows[0]?.id ?? workspace ?? "";
        });
      } catch {
        setProjects([]);
        setProjectId(getWorkspaceProjectId());
      }
    })();
  }, [session]);

  const refresh = useCallback(async () => {
    if (!projectId) {
      setPhases([]);
      setMilestones([]);
      return;
    }
    setLoading(true);
    try {
      const [phaseRows, milestoneRows] = await Promise.all([
        listPhases(session, projectId),
        listMilestones(session, projectId),
      ]);
      setPhases(phaseRows);
      setMilestones(milestoneRows);
      setSelectedMilestoneId((prev) => {
        if (prev && milestoneRows.some((m) => m.id === prev)) return prev;
        return milestoneRows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load roadmap", err);
      setPhases([]);
      setMilestones([]);
    } finally {
      setLoading(false);
    }
  }, [projectId, session]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const selectedMilestone = useMemo(
    () => milestones.find((m) => m.id === selectedMilestoneId) ?? null,
    [milestones, selectedMilestoneId],
  );

  function applyWorkspaceProject(id: string) {
    setProjectId(id);
    setWorkspaceProjectId(id);
    setSelectedMilestoneId(null);
  }

  async function onCreatePhase(event: FormEvent) {
    event.preventDefault();
    if (!projectId) return;
    try {
      const phase = await createPhase(session, {
        project_id: projectId,
        code: phaseCode.trim().toUpperCase(),
        title: phaseTitle.trim(),
        sequence: phases.length + 1,
      });
      notifySuccess(`${phase.title} phase added`);
      setShowCreate(false);
      await refresh();
    } catch (err) {
      notifyApiError("Could not create phase", err);
    }
  }

  async function onAddMilestone(phaseId: string) {
    try {
      const created = await createMilestone(session, {
        phase_id: phaseId,
        code: `MS-${Date.now().toString().slice(-4)}`,
        title: "Kickoff milestone",
        owner_actor_id: session.actorId,
        target_date: new Date().toISOString().slice(0, 10),
        requires_approval: true,
      });
      setSelectedMilestoneId(created.id);
      notifySuccess(`Milestone ${created.title} created`);
      await refresh();
    } catch (err) {
      notifyApiError("Could not create milestone", err);
    }
  }

  async function onApproveMs() {
    if (!selectedMilestone) return;
    try {
      const approved = await approveMilestone(session, selectedMilestone.id);
      setSelectedMilestoneId(approved.id);
      notifySuccess("Milestone approved");
      await refresh();
    } catch (err) {
      notifyApiError("Approval failed", err);
    }
  }

  async function onCompleteMs() {
    if (!selectedMilestone) return;
    try {
      const done = await completeMilestone(session, selectedMilestone.id);
      setSelectedMilestoneId(done.id);
      notifySuccess("Milestone completed");
      await refresh();
    } catch (err) {
      notifyApiError("Could not complete milestone", err);
    }
  }

  async function onCompletePhase(phaseId: string) {
    try {
      await completePhase(session, phaseId);
      notifySuccess("Phase completed");
      await refresh();
    } catch (err) {
      notifyApiError("Could not complete phase", err);
    }
  }

  return (
    <AppShell title="Roadmaps" breadcrumbs={["Project Delivery", "Roadmaps"]}>
      <PageHeader
        title="Roadmaps"
        description="Phases and checkpoints for the workspace project — plan discovery, build, and release milestones."
        actions={
          can(session.variant, "create") && projectId ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Add phase
            </Button>
          ) : null
        }
      />

      <Card className="mb-6">
        <CardBody>
          <Field
            label="Workspace project"
            hint="Roadmap phases and milestones load from the selected project."
          >
            <Select
              value={projectId}
              onChange={(e) => applyWorkspaceProject(e.target.value)}
              aria-label="Workspace project"
            >
              <option value="">Select a project…</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.code} — {p.title}
                </option>
              ))}
            </Select>
          </Field>
        </CardBody>
      </Card>

      {showCreate && projectId && can(session.variant, "create") ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Add phase</h2>
            <p className="text-sm text-[var(--muted)]">
              Phases sequence the delivery journey — Discovery, Build, Launch, and beyond.
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

      <div className="grid gap-4 lg:grid-cols-2">
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
                <li
                  key={phase.id}
                  className="flex flex-wrap items-center justify-between gap-3 px-5 py-4"
                >
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

        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Milestones</h2>
            <p className="text-sm text-[var(--muted)]">
              Loaded from the database for this project — survives reload.
            </p>
          </CardHeader>
          {!projectId ? (
            <CardBody>
              <EmptyState title="Select a project" body="Milestones appear after a project is chosen." />
            </CardBody>
          ) : loading ? (
            <SkeletonRows />
          ) : milestones.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No milestones yet"
                body="Add a milestone on a phase to track approval checkpoints."
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {milestones.map((item) => {
                const phase = phases.find((p) => p.id === item.phase_id);
                return (
                  <li key={item.id}>
                    <button
                      type="button"
                      onClick={() => setSelectedMilestoneId(item.id)}
                      className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                        item.id === selectedMilestoneId ? "bg-[var(--accent-soft)]" : ""
                      }`}
                    >
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="font-medium">{item.title}</span>
                        <StatusBadge status={item.status} />
                      </div>
                      <p className="mt-1 text-xs text-[var(--muted)]">
                        {item.code}
                        {phase ? ` · ${phase.title}` : ""} · target {item.target_date}
                      </p>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </Card>
      </div>

      {selectedMilestone ? (
        <Card className="mt-6">
          <CardHeader className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 className="font-display text-lg">{selectedMilestone.title}</h3>
              <p className="text-sm text-[var(--muted)]">
                {selectedMilestone.code} · target {selectedMilestone.target_date}
              </p>
            </div>
            <StatusBadge status={selectedMilestone.status} />
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
