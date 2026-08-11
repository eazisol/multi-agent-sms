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
  AGENT_RUNTIME_CODES,
  EMPTY_PAGE_META,
  formatUtc,
  listAgentRuns,
  startAgentRun,
  type AgentRun,
  type PageMeta,
} from "@/lib/api";
import { newId } from "@/lib/id";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function AgentRunsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showStart, setShowStart] = useState(false);
  const [items, setItems] = useState<AgentRun[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [status, setStatus] = useState("all");
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  const [agentCode, setAgentCode] = useState<string>(AGENT_RUNTIME_CODES[0]);
  const [relatedType, setRelatedType] = useState("crm_query");
  const [relatedId, setRelatedId] = useState("");
  const [projectId, setProjectId] = useState("");
  const [forceReview, setForceReview] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listAgentRuns(session, {
        status: status === "all" ? undefined : status,
        limit,
        offset,
      });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load agent runs", err);
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
      await startAgentRun(session, {
        agent_code: agentCode,
        related_entity_type: relatedType.trim() || "crm_query",
        related_entity_id: entityId,
        project_id: projectId.trim() || undefined,
        input_json: forceReview ? { force_low_confidence: true } : {},
      });
      notifySuccess("Agent run started");
      setShowStart(false);
      setRelatedId("");
      setForceReview(false);
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not start agent run", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Agent Runs"
          description="LangGraph stub runs (MOD-360). Postgres stores model, prompt, sources, tools, output, and review state."
          actions={
            <Button type="button" onClick={() => setShowStart((v) => !v)}>
              <Plus className="h-4 w-4" />
              Start run
            </Button>
          }
        />

        {showStart ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Start agent run</h2>
              <p className="text-sm text-[var(--muted)]">
                Bootstraps an active stub prompt when needed. Low confidence routes to human review.
              </p>
            </CardHeader>
            <CardBody>
              <form onSubmit={onStart} className="grid gap-4 md:grid-cols-2" aria-label="Start agent run">
                <Field label="Agent code">
                  <Select value={agentCode} onChange={(e) => setAgentCode(e.target.value)} required>
                    {AGENT_RUNTIME_CODES.map((code) => (
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
                <Field label="Related entity id" hint="Leave blank to generate a UUID for local testing">
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
                <Field label="Force low confidence review">
                  <Select
                    value={forceReview ? "yes" : "no"}
                    onChange={(e) => setForceReview(e.target.value === "yes")}
                  >
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </Select>
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
              ["completed", "Completed"],
              ["review_required", "Review"],
              ["failed", "Failed"],
              ["running", "Running"],
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
            <h2 className="font-display text-lg">Runs</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/agent-runtime/runs`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No agent runs"
                body="Start a run from an approved catalog agent code."
                action={
                  <Button type="button" onClick={() => setShowStart(true)}>
                    Start run
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
                      <span className="font-medium">{item.agent_code}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {item.related_entity_type} · {item.related_entity_id.slice(0, 8)}…
                      {item.langgraph_run_id ? ` · ${item.langgraph_run_id}` : ""}
                      {item.confidence != null ? ` · conf ${item.confidence.toFixed(2)}` : ""}
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
                label="runs"
              />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
