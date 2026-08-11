"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  ORCHESTRATOR_WORKFLOW_CODES,
  formatUtc,
  listWorkflowInstances,
  startWorkflowInstance,
  type PageMeta,
  type WorkflowInstance,
} from "@/lib/api";
import { newId } from "@/lib/id";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function WorkflowsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showStart, setShowStart] = useState(false);
  const [items, setItems] = useState<WorkflowInstance[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [status, setStatus] = useState("all");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  const [workflowCode, setWorkflowCode] = useState<string>(ORCHESTRATOR_WORKFLOW_CODES[0]);
  const [relatedType, setRelatedType] = useState("crm_query");
  const [relatedId, setRelatedId] = useState("");
  const [projectId, setProjectId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listWorkflowInstances(session, {
        status: status === "all" ? undefined : status,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load workflow instances", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, status, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    const workspaceProject = getWorkspaceProjectId();
    if (workspaceProject) setProjectId(workspaceProject);
  }, []);

  async function onStart(event: FormEvent) {
    event.preventDefault();
    try {
      const entityId = relatedId.trim() || newId();
      await startWorkflowInstance(session, {
        workflow_code: workflowCode,
        related_entity_type: relatedType.trim() || "crm_query",
        related_entity_id: entityId,
        project_id: projectId.trim() || undefined,
      });
      notifySuccess("Workflow instance started");
      setShowStart(false);
      setRelatedId("");
      setStatus("running");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not start workflow instance", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Workflows"
          description="Orchestrator registry (MOD-350). Postgres is the source of truth; Temporal uses a stub adapter in M1."
          actions={
            <Button type="button" onClick={() => setShowStart((v) => !v)}>
              <Plus className="h-4 w-4" />
              Start instance
            </Button>
          }
        />

        {showStart ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Start workflow instance</h2>
              <p className="text-sm text-[var(--muted)]">
                Requires an active version for the selected catalog code. Stub Temporal run ids are
                stored on the instance.
              </p>
            </CardHeader>
            <CardBody>
              <form onSubmit={onStart} className="grid gap-4 md:grid-cols-2" aria-label="Start workflow">
                <Field label="Workflow code">
                  <Select
                    value={workflowCode}
                    onChange={(e) => setWorkflowCode(e.target.value)}
                    required
                  >
                    {ORCHESTRATOR_WORKFLOW_CODES.map((code) => (
                      <option key={code} value={code}>
                        {code}
                      </option>
                    ))}
                  </Select>
                </Field>
                <Field label="Related entity type">
                  <Input
                    required
                    value={relatedType}
                    onChange={(e) => setRelatedType(e.target.value)}
                    placeholder="crm_query"
                  />
                </Field>
                <Field
                  label="Related entity id"
                  hint="Leave blank to generate a UUID for local testing"
                >
                  <Input
                    value={relatedId}
                    onChange={(e) => setRelatedId(e.target.value)}
                    placeholder="UUID"
                  />
                </Field>
                <Field label="Project id (optional)">
                  <Input
                    value={projectId}
                    onChange={(e) => setProjectId(e.target.value)}
                    placeholder="Optional project UUID"
                  />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowStart(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Start</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <div className="flex shrink-0 flex-wrap items-center gap-2">
          {(
            [
              ["all", "All"],
              ["running", "Running"],
              ["waiting", "Waiting"],
              ["failed", "Failed"],
              ["completed", "Completed"],
              ["cancelled", "Cancelled"],
            ] as const
          ).map(([id, label]) => (
            <Button
              key={id}
              variant={status === id ? "primary" : "outline"}
              onClick={() => {
                setStatus(id);
                setOffset(0);
              }}
            >
              {label}
            </Button>
          ))}
        </div>

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Workflow instances</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/orchestrator/instances`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No workflow instances"
                body="Create and activate a workflow version, then start an instance from the catalog."
                action={
                  <Button type="button" onClick={() => setShowStart(true)}>
                    Start instance
                  </Button>
                }
              />
            </CardBody>
          ) : (
            <ScrollRegion className="flex-1">
              <ul className="divide-y divide-[var(--line)]">
                {items.map((item) => (
                  <li key={item.id} className="px-5 py-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-medium">{item.workflow_code}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {item.related_entity_type} · {item.related_entity_id.slice(0, 8)}…
                      {item.temporal_run_id ? ` · ${item.temporal_run_id}` : ""}
                    </p>
                    <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
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
                label="instances"
              />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
