"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Check, X } from "lucide-react";

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
  addChangeImpact,
  createChangeRequest,
  decideChangeRequest,
  formatUtc,
  getChangeDevelopmentGate,
  listChangeRequests,
  submitChangeRequest,
  type ChangeRequest,
  type DevelopmentGate,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function ChangeRequestsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<ChangeRequest[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [selectedGate, setSelectedGate] = useState<DevelopmentGate | null>(null);

  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [impact, setImpact] = useState("");
  const [projectId, setProjectId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listChangeRequests(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load change requests", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

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
      const created = await createChangeRequest(session, {
        code: code.trim(),
        title: title.trim(),
        project_id: projectId.trim() || undefined,
        change_type: "scope",
      });
      await addChangeImpact(session, created.id, {
        summary: impact.trim() || title.trim(),
        affected_areas: ["scope"],
        expected_version: created.version,
      });
      const refreshed = await listChangeRequests(session, { q: created.code, limit: 1 });
      const current = refreshed.items[0] ?? created;
      await submitChangeRequest(session, current.id, current.version);
      notifySuccess("Change request submitted for approval");
      setShowCreate(false);
      setCode("");
      setTitle("");
      setImpact("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create change request", err);
    }
  }

  async function onDecide(item: ChangeRequest, decision: "approved" | "rejected") {
    try {
      await decideChangeRequest(session, item.id, {
        decision,
        rationale: decision === "approved" ? "Desk approval" : "Desk rejection",
        evidence: decision === "approved" ? "Owner sign-off" : "Out of capacity",
        expected_version: item.version,
      });
      notifySuccess(`Change request ${decision}`);
      await load();
    } catch (err) {
      notifyApiError("Could not record decision", err);
    }
  }

  async function onGate(item: ChangeRequest) {
    try {
      setSelectedGate(await getChangeDevelopmentGate(session, item.id));
    } catch (err) {
      notifyApiError("Could not load development gate", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Change Requests"
          description="Scope-affecting changes with impact analysis, approvals, and development gates (MOD-420)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New CR
            </Button>
          }
        />

        {selectedGate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Development gate</h2>
              <p className="text-sm text-[var(--muted)]">
                {selectedGate.status}: {selectedGate.allowed ? "allowed" : "blocked"} — {selectedGate.reason}
              </p>
            </CardHeader>
          </Card>
        ) : null}

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create and submit CR</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create change request">
                <Field label="Code">
                  <Input required value={code} onChange={(e) => setCode(e.target.value)} placeholder="CR-001" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Project id (optional)">
                  <Input value={projectId} onChange={(e) => setProjectId(e.target.value)} />
                </Field>
                <Field label="Impact summary">
                  <Textarea rows={3} value={impact} onChange={(e) => setImpact(e.target.value)} />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create &amp; submit</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Change requests</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/change-control/change-requests`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No change requests"
                body="Create a CR with impact analysis before it can enter development."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    New CR
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
                        {item.code} · {item.change_type} · {formatUtc(item.updated_at)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={item.status} />
                      <Button type="button" variant="ghost" onClick={() => void onGate(item)}>
                        Gate
                      </Button>
                      {item.status === "pending_approval" ? (
                        <>
                          <Button type="button" variant="ghost" onClick={() => void onDecide(item, "approved")}>
                            <Check className="h-4 w-4" />
                            Approve
                          </Button>
                          <Button type="button" variant="ghost" onClick={() => void onDecide(item, "rejected")}>
                            <X className="h-4 w-4" />
                            Reject
                          </Button>
                        </>
                      ) : null}
                    </div>
                  </li>
                ))}
              </ul>
            </ScrollRegion>
          )}
          {!loading && (items.length > 0 || pageMeta.total > 0) ? (
            <div className="shrink-0">
              <ListPagination page={pageMeta} onOffsetChange={setOffset} onLimitChange={setLimit} label="CRs" />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
