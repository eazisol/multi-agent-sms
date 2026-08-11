"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, RotateCcw, ShieldAlert } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  createBug,
  formatUtc,
  getBugReleaseGate,
  listBugs,
  rejectBug,
  reopenBug,
  type Bug,
  type PageMeta,
  type ReleaseGate,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function BugsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<Bug[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [gate, setGate] = useState<ReleaseGate | null>(null);

  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [severity, setSeverity] = useState("high");
  const [projectId, setProjectId] = useState("");
  const [rejectEvidence, setRejectEvidence] = useState("Desk QA evidence");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listBugs(session, {
        limit,
        offset,
        project_id: projectId.trim() || undefined,
      });
      setItems(result.items);
      setPageMeta(result.page);
      setGate(await getBugReleaseGate(session, projectId.trim() || undefined));
    } catch (err) {
      notifyApiError("Unable to load bugs", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset, projectId]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    const workspaceProject = getWorkspaceProjectId();
    if (workspaceProject) setProjectId(workspaceProject);
  }, []);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      await createBug(session, {
        code: code.trim(),
        title: title.trim(),
        severity,
        project_id: projectId.trim() || undefined,
      });
      notifySuccess("Bug created");
      setShowCreate(false);
      setCode("");
      setTitle("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create bug", err);
    }
  }

  async function onReject(item: Bug) {
    try {
      await rejectBug(session, item.id, {
        reason: "QA rejection from desk",
        evidence: rejectEvidence.trim() || "Desk evidence",
        expected_version: item.version,
      });
      notifySuccess("Bug rejected with evidence");
      await load();
    } catch (err) {
      notifyApiError("Could not reject bug", err);
    }
  }

  async function onReopen(item: Bug) {
    try {
      await reopenBug(session, item.id, {
        reason: "Development reopen from desk",
        expected_version: item.version,
      });
      notifySuccess("Bug reopened");
      await load();
    } catch (err) {
      notifyApiError("Could not reopen bug", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Bugs"
          description="QA reject/reopen, fix/retest history, and release blockers (MOD-410)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New bug
            </Button>
          }
        />

        {gate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg flex items-center gap-2">
                <ShieldAlert className="h-4 w-4" />
                Release gate
              </h2>
              <p className="text-sm text-[var(--muted)]">
                {gate.release_allowed
                  ? "No active blocking defects for this scope."
                  : `Blocked by: ${gate.blocking_codes.join(", ") || "unknown"}`}
              </p>
            </CardHeader>
          </Card>
        ) : null}

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create bug</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create bug">
                <Field label="Code">
                  <Input required value={code} onChange={(e) => setCode(e.target.value)} placeholder="BUG-001" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Severity">
                  <Input value={severity} onChange={(e) => setSeverity(e.target.value)} placeholder="critical|high|medium|low" />
                </Field>
                <Field label="Project id (optional)">
                  <Input value={projectId} onChange={(e) => setProjectId(e.target.value)} />
                </Field>
                <Field label="Reject evidence default">
                  <Textarea rows={2} value={rejectEvidence} onChange={(e) => setRejectEvidence(e.target.value)} />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Defects</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/bugs`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No bugs"
                body="Create a defect to exercise reject/reopen and the release gate."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    New bug
                  </Button>
                }
              />
            </CardBody>
          ) : (
            <ScrollRegion className="flex-1">
              <ul className="divide-y divide-[var(--line)]">
                {items.map((item) => (
                  <li key={item.id} className="flex flex-wrap items-center justify-between gap-3 px-5 py-3">
                    <div>
                      <span className="font-medium">{item.title}</span>
                      <p className="text-xs text-[var(--muted)]">
                        {item.code} · {item.severity}
                        {item.blocks_release ? " · blocks release" : ""} · {formatUtc(item.updated_at)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={item.status} />
                      {item.status !== "rejected" && item.status !== "closed" && item.status !== "verified" ? (
                        <Button type="button" variant="ghost" onClick={() => void onReject(item)}>
                          Reject
                        </Button>
                      ) : null}
                      {item.status === "rejected" ? (
                        <Button type="button" variant="ghost" onClick={() => void onReopen(item)}>
                          <RotateCcw className="h-4 w-4" />
                          Reopen
                        </Button>
                      ) : null}
                    </div>
                  </li>
                ))}
              </ul>
            </ScrollRegion>
          )}
          {!loading && (items.length > 0 || pageMeta.total > 0) ? (
            <div className="shrink-0">
              <ListPagination page={pageMeta} onOffsetChange={setOffset} onLimitChange={setLimit} label="bugs" />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
