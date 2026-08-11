"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { EmptyState, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  addAcceptanceCriterion,
  approveRequirementVersion,
  approveSrsBaseline,
  createProject,
  createRequirement,
  createRequirementVersion,
  createSrsBaseline,
  listRequirements,
  type ProjectRequirement,
  type RequirementVersion,
} from "@/lib/api";
import { can } from "@/lib/roles";
import { getWorkspaceProjectId, setWorkspaceProjectId } from "@/lib/workspace";

export function ProjectsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [projectId, setProjectId] = useState("");
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [reqCode, setReqCode] = useState("REQ-001");
  const [reqTitle, setReqTitle] = useState("");
  const [statement, setStatement] = useState("");
  const [requirements, setRequirements] = useState<ProjectRequirement[]>([]);
  const [lastVersion, setLastVersion] = useState<RequirementVersion | null>(null);

  useEffect(() => {
    setProjectId(getWorkspaceProjectId());
  }, []);

  const refreshRequirements = useCallback(async () => {
    if (!projectId) {
      setRequirements([]);
      return;
    }
    try {
      setRequirements(await listRequirements(session, projectId));
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Load requirements failed");
    }
  }, [projectId, session]);

  useEffect(() => {
    void refreshRequirements();
  }, [refreshRequirements]);

  async function onCreateProject(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const project = await createProject(session, {
        code: code.trim().toUpperCase(),
        title: title.trim(),
      });
      setProjectId(project.id);
      setWorkspaceProjectId(project.id);
      setOk(`Project ${project.code} created`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Create project failed");
    }
  }

  async function onCreateRequirement(event: FormEvent) {
    event.preventDefault();
    if (!projectId) return;
    setError(null);
    setOk(null);
    try {
      const requirement = await createRequirement(session, {
        project_id: projectId,
        requirement_code: reqCode.trim(),
        title: reqTitle.trim(),
      });
      const version = await createRequirementVersion(session, {
        requirement_id: requirement.id,
        statement: statement.trim(),
        priority: "must_have",
      });
      await addAcceptanceCriterion(session, {
        requirement_version_id: version.id,
        criterion_code: "AC-1",
        text: "Acceptance criterion for first version",
      });
      setLastVersion(version);
      setOk(`Requirement ${requirement.requirement_code} v${version.version_number} drafted`);
      await refreshRequirements();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Requirement draft failed");
    }
  }

  async function onApproveVersion() {
    if (!lastVersion) return;
    setError(null);
    setOk(null);
    try {
      const approved = await approveRequirementVersion(session, lastVersion.id);
      setLastVersion(approved);
      setOk("Requirement version approved");
      await refreshRequirements();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Approve failed");
    }
  }

  async function onApproveSrs() {
    if (!projectId || !lastVersion || lastVersion.status !== "approved") {
      setError("Need an approved requirement version first");
      return;
    }
    setError(null);
    setOk(null);
    try {
      const baseline = await createSrsBaseline(session, {
        project_id: projectId,
        title: "SRS from desk",
        summary: "Created from Projects desk",
        requirement_version_ids: [lastVersion.id],
      });
      const approved = await approveSrsBaseline(session, baseline.id);
      setOk(`SRS v${approved.version_number} approved`);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "SRS approve failed");
    }
  }

  return (
    <AppShell title="Projects">
      <div className="space-y-6">
        <div>
          <h2 className="font-display text-3xl tracking-tight">Projects &amp; SRS</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            MOD-240 project records, requirement versions, and human-approved SRS baselines.
          </p>
        </div>
        {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
        {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

        {can(session.variant, "create") ? (
          <form
            onSubmit={onCreateProject}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4 md:grid-cols-3"
          >
            <label className="flex flex-col gap-1 text-sm">
              <span>Project code</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm md:col-span-2">
              <span>Title</span>
              <input
                required
                className="rounded border border-[var(--line)] px-3 py-2"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:w-fit"
            >
              Create project
            </button>
          </form>
        ) : null}

        <label className="flex flex-col gap-1 text-sm">
          <span>Active project id</span>
          <input
            className="rounded border border-[var(--line)] bg-white px-3 py-2 font-mono text-xs"
            value={projectId}
            onChange={(e) => {
              setProjectId(e.target.value);
              setWorkspaceProjectId(e.target.value);
            }}
          />
        </label>

        {projectId && can(session.variant, "create") ? (
          <form
            onSubmit={onCreateRequirement}
            className="grid gap-3 rounded border border-[var(--line)] bg-white p-4"
          >
            <h3 className="font-medium">Draft requirement + AC</h3>
            <div className="grid gap-3 md:grid-cols-2">
              <label className="flex flex-col gap-1 text-sm">
                <span>Requirement code</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={reqCode}
                  onChange={(e) => setReqCode(e.target.value)}
                />
              </label>
              <label className="flex flex-col gap-1 text-sm">
                <span>Title</span>
                <input
                  required
                  className="rounded border border-[var(--line)] px-3 py-2"
                  value={reqTitle}
                  onChange={(e) => setReqTitle(e.target.value)}
                />
              </label>
            </div>
            <label className="flex flex-col gap-1 text-sm">
              <span>Statement</span>
              <textarea
                required
                className="min-h-20 rounded border border-[var(--line)] px-3 py-2"
                value={statement}
                onChange={(e) => setStatement(e.target.value)}
              />
            </label>
            <button
              type="submit"
              className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white md:w-fit"
            >
              Create draft version
            </button>
          </form>
        ) : null}

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded border border-[var(--line)] bg-white px-3 py-1.5 text-sm"
            onClick={() => void onApproveVersion()}
            disabled={!lastVersion || !can(session.variant, "approve")}
          >
            Approve last requirement version
          </button>
          <button
            type="button"
            className="rounded border border-[var(--line)] bg-white px-3 py-1.5 text-sm"
            onClick={() => void onApproveSrs()}
            disabled={!lastVersion || !can(session.variant, "approve")}
          >
            Create &amp; approve SRS
          </button>
        </div>

        {requirements.length === 0 ? (
          <EmptyState title="No requirements" body="Create a project requirement draft above." />
        ) : (
          <ul className="space-y-2 rounded border border-[var(--line)] bg-white p-4 text-sm">
            {requirements.map((item) => (
              <li key={item.id}>
                <strong>{item.requirement_code}</strong> — {item.title}{" "}
                <span className="text-[var(--muted)]">({item.status})</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </AppShell>
  );
}
