"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion, TableScroll } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  addAcceptanceCriterion,
  approveRequirementVersion,
  approveSrsBaseline,
  createProject,
  createRequirement,
  createRequirementVersion,
  createSrsBaseline,
  formatUtc,
  listProjects,
  listRequirements,
  type PageMeta,
  type Project,
  type ProjectRequirement,
  type RequirementVersion,
} from "@/lib/api";
import { notifyApiError, notifyError, notifySuccess } from "@/lib/toast";
import { can } from "@/lib/roles";
import { getWorkspaceProjectId, setWorkspaceProjectId } from "@/lib/workspace";

export function ProjectsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [loadingReqs, setLoadingReqs] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [showReq, setShowReq] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [reqCode, setReqCode] = useState("REQ-001");
  const [reqTitle, setReqTitle] = useState("");
  const [statement, setStatement] = useState("");
  const [requirements, setRequirements] = useState<ProjectRequirement[]>([]);
  const [lastVersion, setLastVersion] = useState<RequirementVersion | null>(null);

  const loadProjects = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listProjects(session, {
        q: search.trim() || undefined,
        status: status || undefined,
        limit,
        offset,
      });
      setProjects(result.items);
      setPageMeta(result.page);
      const rows = result.items;
      const workspaceId = getWorkspaceProjectId();
      setProjectId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        if (workspaceId && rows.some((r) => r.id === workspaceId)) return workspaceId;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      notifyApiError("Unable to load projects", err);
      setProjects([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, search, status, limit, offset]);

  useEffect(() => {
    void loadProjects();
  }, [loadProjects]);

  const current = useMemo(
    () => projects.find((item) => item.id === projectId) ?? null,
    [projects, projectId],
  );

  const refreshRequirements = useCallback(async () => {
    if (!projectId) {
      setRequirements([]);
      return;
    }
    setLoadingReqs(true);
    try {
      setRequirements(await listRequirements(session, projectId));
    } catch (err) {
      notifyApiError("Unable to load requirements", err);
    } finally {
      setLoadingReqs(false);
    }
  }, [projectId, session]);

  useEffect(() => {
    void refreshRequirements();
  }, [refreshRequirements]);

  function selectProject(id: string) {
    setProjectId(id);
    setWorkspaceProjectId(id);
    setLastVersion(null);
  }

  async function onCreateProject(event: FormEvent) {
    event.preventDefault();
    try {
      const project = await createProject(session, {
        code: code.trim().toUpperCase(),
        title: title.trim(),
      });
      setWorkspaceProjectId(project.id);
      setProjectId(project.id);
      notifySuccess(`${project.code} created and selected as the workspace project`);
      setCode("");
      setTitle("");
      setShowCreate(false);
      await loadProjects();
    } catch (err) {
      notifyApiError("Could not create project", err);
    }
  }

  async function onCreateRequirement(event: FormEvent) {
    event.preventDefault();
    if (!projectId) return;
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
      notifySuccess(`${requirement.requirement_code} draft ready for review`);
      setReqTitle("");
      setStatement("");
      setShowReq(false);
      await refreshRequirements();
    } catch (err) {
      notifyApiError("Could not draft requirement", err);
    }
  }

  async function onApproveVersion() {
    if (!lastVersion) return;
    try {
      const approved = await approveRequirementVersion(session, lastVersion.id);
      setLastVersion(approved);
      notifySuccess("Requirement version approved");
      await refreshRequirements();
    } catch (err) {
      notifyApiError("Approval failed", err);
    }
  }

  async function onApproveSrs() {
    if (!projectId || !lastVersion || lastVersion.status !== "approved") {
      notifyError("Approve a requirement version before creating an SRS baseline");
      return;
    }
    try {
      const baseline = await createSrsBaseline(session, {
        project_id: projectId,
        title: "Project SRS",
        summary: "SRS baseline from approved requirements",
        requirement_version_ids: [lastVersion.id],
      });
      const approved = await approveSrsBaseline(session, baseline.id);
      notifySuccess(`SRS version ${approved.version_number} approved`);
    } catch (err) {
      notifyApiError("SRS approval failed", err);
    }
  }

  return (
    <AppShell title="Projects" breadcrumbs={["Project Delivery", "Projects"]} fill>
      <div className="flex min-h-0 flex-1 flex-col gap-4">
        <PageHeader
          title="Projects"
          description="Delivery homes for clients — create a project, draft must-have requirements, and approve an SRS baseline."
          actions={
            can(session.variant, "create") ? (
              <Button onClick={() => setShowCreate((v) => !v)}>
                <Plus className="h-4 w-4" />
                New project
              </Button>
            ) : null
          }
        />

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create project</h2>
              <p className="text-sm text-[var(--muted)]">
                A short code and title are enough to open delivery work for a client engagement.
              </p>
            </CardHeader>
            <CardBody>
              <form
                onSubmit={onCreateProject}
                className="grid gap-4 md:grid-cols-3"
                aria-label="Create project"
              >
                <Field label="Project code">
                  <Input
                    required
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="EARTH"
                  />
                </Field>
                <Field label="Title" className="md:col-span-2">
                  <Input
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="EarthCo client portal"
                  />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-3">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create project</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <div className="grid min-h-0 flex-1 gap-4 overflow-hidden lg:grid-cols-[minmax(280px,340px)_1fr]">
          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Project inventory</h2>
              <p className="text-sm text-[var(--muted)]">Loaded from the organization database.</p>
              <div className="relative mt-3">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted)]" />
                <Input
                  className="pl-9"
                  value={search}
                  onChange={(e) => {
                    setSearch(e.target.value);
                    setOffset(0);
                  }}
                  placeholder="Search code or title"
                  aria-label="Search projects"
                />
              </div>
              <Field label="Status" className="mt-3 mb-0">
                <Select
                  value={status}
                  onChange={(e) => {
                    setStatus(e.target.value);
                    setOffset(0);
                  }}
                  aria-label="Filter projects by status"
                >
                  <option value="">Any status</option>
                  <option value="active">Active</option>
                  <option value="draft">Draft</option>
                  <option value="on_hold">On hold</option>
                  <option value="at_risk">At risk</option>
                  <option value="blocked">Blocked</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </Select>
              </Field>
            </CardHeader>
            {loading ? (
              <SkeletonRows />
            ) : projects.length === 0 ? (
              <CardBody>
                <EmptyState
                  title={search.trim() || status ? "No matching projects" : "No projects yet"}
                  body={
                    search.trim() || status
                      ? "Try a different search or status filter."
                      : "Create a project to start drafting requirements and building an approved SRS."
                  }
                  action={
                    !search.trim() && !status && can(session.variant, "create") ? (
                      <Button onClick={() => setShowCreate(true)}>
                        <Plus className="h-4 w-4" />
                        New project
                      </Button>
                    ) : null
                  }
                />
              </CardBody>
            ) : (
              <ScrollRegion className="flex-1">
                <ul className="divide-y divide-[var(--line)]">
                  {projects.map((item) => (
                    <li key={item.id}>
                      <button
                        type="button"
                        onClick={() => selectProject(item.id)}
                        className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                          item.id === projectId ? "bg-[var(--accent-soft)]" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="font-medium">{item.code}</span>
                          <StatusBadge status={item.status} />
                        </div>
                        <p className="mt-1 text-sm text-[var(--muted)]">{item.title}</p>
                        <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                      </button>
                    </li>
                  ))}
                </ul>
              </ScrollRegion>
            )}
            {!loading && (projects.length > 0 || pageMeta.total > 0) ? (
              <div className="shrink-0">
                <ListPagination
                  page={pageMeta}
                  onOffsetChange={setOffset}
                  onLimitChange={setLimit}
                  label="projects"
                />
              </div>
            ) : null}
          </Card>

          <ScrollRegion className="min-h-0">
            <div className="grid gap-4 pb-2">
              {current ? (
                <Card>
                  <CardHeader className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <h2 className="font-display text-xl">{current.title}</h2>
                      <p className="mt-1 text-sm text-[var(--muted)]">
                        Workspace project for Roadmap, Tickets, and Documents.
                      </p>
                    </div>
                    <StatusBadge status={current.status} />
                  </CardHeader>
                  <CardBody className="space-y-3 text-sm">
                    <p>
                      <span className="text-[var(--muted)]">Code:</span> {current.code}
                    </p>
                    {can(session.variant, "create") ? (
                      <div className="flex flex-wrap gap-2">
                        <Button variant="outline" onClick={() => setShowReq((v) => !v)}>
                          <Plus className="h-4 w-4" />
                          Draft requirement
                        </Button>
                        {lastVersion ? (
                          <>
                            <Button
                              variant="outline"
                              disabled={!can(session.variant, "approve")}
                              onClick={() => void onApproveVersion()}
                            >
                              Approve last version
                            </Button>
                            <Button
                              variant="outline"
                              disabled={!can(session.variant, "approve")}
                              onClick={() => void onApproveSrs()}
                            >
                              Create &amp; approve SRS
                            </Button>
                          </>
                        ) : null}
                      </div>
                    ) : null}
                  </CardBody>
                </Card>
              ) : null}

              {showReq && projectId && can(session.variant, "create") ? (
                <Card>
                  <CardHeader>
                    <h2 className="font-display text-lg">Draft requirement</h2>
                    <p className="text-sm text-[var(--muted)]">
                      Capture a must-have statement and a first acceptance criterion.
                    </p>
                  </CardHeader>
                  <CardBody>
                    <form
                      onSubmit={onCreateRequirement}
                      className="grid gap-4 md:grid-cols-2"
                      aria-label="Draft requirement"
                    >
                      <Field label="Requirement code">
                        <Input
                          required
                          value={reqCode}
                          onChange={(e) => setReqCode(e.target.value)}
                          placeholder="REQ-001"
                        />
                      </Field>
                      <Field label="Title">
                        <Input
                          required
                          value={reqTitle}
                          onChange={(e) => setReqTitle(e.target.value)}
                          placeholder="User can sign in securely"
                        />
                      </Field>
                      <Field label="Statement" className="md:col-span-2">
                        <Textarea
                          required
                          rows={3}
                          value={statement}
                          onChange={(e) => setStatement(e.target.value)}
                          placeholder="The system shall…"
                        />
                      </Field>
                      <div className="flex justify-end gap-2 md:col-span-2">
                        <Button type="button" variant="ghost" onClick={() => setShowReq(false)}>
                          Cancel
                        </Button>
                        <Button type="submit">Create draft</Button>
                      </div>
                    </form>
                  </CardBody>
                </Card>
              ) : null}

              <Card>
                <CardHeader className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <h2 className="font-display text-lg">Requirements</h2>
                    <p className="text-sm text-[var(--muted)]">
                      Must-have items tracked toward the project SRS.
                    </p>
                  </div>
                  {lastVersion ? <StatusBadge status={lastVersion.status} /> : null}
                </CardHeader>
                {!projectId ? (
                  <CardBody>
                    <EmptyState
                      title="No project selected"
                      body="Create or select a project from the inventory."
                    />
                  </CardBody>
                ) : loadingReqs ? (
                  <SkeletonRows />
                ) : requirements.length === 0 ? (
                  <CardBody>
                    <EmptyState
                      title="No requirements yet"
                      body="Draft the first must-have so the team can review and approve an SRS baseline."
                      action={
                        can(session.variant, "create") ? (
                          <Button onClick={() => setShowReq(true)}>Draft requirement</Button>
                        ) : null
                      }
                    />
                  </CardBody>
                ) : (
                  <TableScroll className="rounded-none border-0 border-t border-[var(--line)]">
                    <table className="w-full min-w-full table-fixed text-left text-sm">
                      <thead className="sticky top-0 z-10 bg-[var(--surface-muted)] text-xs uppercase tracking-wide text-[var(--muted)]">
                        <tr>
                          <th className="w-[25%] px-5 py-3 font-medium">Code</th>
                          <th className="w-[55%] px-5 py-3 font-medium">Title</th>
                          <th className="w-[20%] px-5 py-3 font-medium">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {requirements.map((item) => (
                          <tr
                            key={item.id}
                            className="border-t border-[var(--line)] hover:bg-[var(--surface-muted)]/70"
                          >
                            <td className="truncate px-5 py-3 font-medium">{item.requirement_code}</td>
                            <td className="px-5 py-3">
                              <span className="line-clamp-2">{item.title}</span>
                            </td>
                            <td className="px-5 py-3">
                              <StatusBadge status={item.status} />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </TableScroll>
                )}
              </Card>
            </div>
          </ScrollRegion>
        </div>
      </div>
    </AppShell>
  );
}
