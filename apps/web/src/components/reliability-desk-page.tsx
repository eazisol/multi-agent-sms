"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader } from "@/components/ui-states";
import {
  completeWorkflowReplay,
  createDrRunbook,
  createPerformanceTest,
  createWorkflowReplay,
  failWorkflowReplay,
  formatUtc,
  getApiSlo,
  getDashboardSlo,
  listDrRunbooks,
  resumeWorkflowReplay,
  type ApiSlo,
  type DashboardSlo,
  type DrRunbook,
  type WorkflowReplay,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function ReliabilityDeskPage() {
  const { session } = useSession();
  const [apiSlo, setApiSlo] = useState<ApiSlo | null>(null);
  const [dashboardSlo, setDashboardSlo] = useState<DashboardSlo | null>(null);
  const [runbooks, setRunbooks] = useState<DrRunbook[]>([]);
  const [replay, setReplay] = useState<WorkflowReplay | null>(null);
  const [loading, setLoading] = useState(true);

  const [perfCode, setPerfCode] = useState("PERF-610");
  const [suiteName, setSuiteName] = useState("api-normal");
  const [p95Ms, setP95Ms] = useState("1800");
  const [workflowName, setWorkflowName] = useState("query_intake");
  const [idempotencyKey, setIdempotencyKey] = useState("replay-610");
  const [runbookCode, setRunbookCode] = useState("DR-610");
  const [runbookTitle, setRunbookTitle] = useState("Local restore runbook");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [apiRes, dashRes, runbookPage] = await Promise.all([
        getApiSlo(session),
        getDashboardSlo(session),
        listDrRunbooks(session),
      ]);
      setApiSlo(apiRes);
      setDashboardSlo(dashRes);
      setRunbooks(runbookPage.items);
    } catch (err) {
      notifyApiError("Unable to load Reliability desk", err);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onRecordPerformance(event: FormEvent) {
    event.preventDefault();
    try {
      await createPerformanceTest(session, {
        code: perfCode.trim(),
        suite_name: suiteName.trim(),
        p95_ms: Number(p95Ms),
      });
      notifySuccess("Performance test recorded");
      await load();
    } catch (err) {
      notifyApiError("Record performance test failed", err);
    }
  }

  async function onCreateReplay(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createWorkflowReplay(session, {
        workflow_name: workflowName.trim(),
        idempotency_key: idempotencyKey.trim(),
      });
      setReplay(created);
      notifySuccess("Workflow replay created");
    } catch (err) {
      notifyApiError("Create replay failed", err);
    }
  }

  async function onFailReplay(event: FormEvent) {
    event.preventDefault();
    if (!replay) return;
    try {
      const failed = await failWorkflowReplay(session, replay.id, {
        last_error: "Simulated worker failure",
        expected_version: replay.version,
      });
      setReplay(failed);
      notifySuccess("Replay marked failed");
    } catch (err) {
      notifyApiError("Fail replay failed", err);
    }
  }

  async function onResumeReplay(event: FormEvent) {
    event.preventDefault();
    if (!replay) return;
    try {
      const resumed = await resumeWorkflowReplay(session, replay.id, {
        expected_version: replay.version,
      });
      const completed = await completeWorkflowReplay(session, resumed.id, {
        expected_version: resumed.version,
      });
      setReplay(completed);
      notifySuccess("Replay resumed and completed");
    } catch (err) {
      notifyApiError("Resume replay failed", err);
    }
  }

  async function onCreateRunbook(event: FormEvent) {
    event.preventDefault();
    try {
      await createDrRunbook(session, {
        code: runbookCode.trim(),
        title: runbookTitle.trim(),
        rto_minutes: 120,
        rpo_minutes: 60,
        body_preview: "Documented restore steps for local/pilot environments.",
      });
      notifySuccess("DR runbook recorded");
      await load();
    } catch (err) {
      notifyApiError("Create DR runbook failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Reliability"
        description="API and dashboard SLOs, performance test records, workflow replay, and DR runbooks (M1)."
        actions={
          <Button variant="secondary" onClick={() => void load()}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        }
      />
      <ScrollRegion className="space-y-6 p-6">
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="API SLO" />
            <CardBody className="space-y-2 text-sm">
              {apiSlo ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>p95 ≤ {apiSlo.budget_ms} ms</span>
                    <StatusBadge status={apiSlo.slo_met ? "passed" : "failed"} />
                  </div>
                  <div>Recorded p95: {apiSlo.p95_ms ?? "—"} ms</div>
                  <div>Samples: {apiSlo.sample_count}</div>
                </>
              ) : (
                <EmptyState title="API SLO unavailable" body={loading ? "Loading…" : "Refresh to load."} />
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Dashboard SLO" />
            <CardBody className="space-y-2 text-sm">
              {dashboardSlo ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>p95 ≤ {dashboardSlo.budget_ms} ms</span>
                    <StatusBadge status={dashboardSlo.slo_met ? "passed" : "failed"} />
                  </div>
                  <div>Recorded p95: {dashboardSlo.dashboard_p95_ms ?? "—"} ms</div>
                </>
              ) : (
                <EmptyState
                  title="Dashboard SLO unavailable"
                  body={loading ? "Loading…" : "Refresh to load."}
                />
              )}
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Record performance test" />
            <CardBody>
              <form onSubmit={onRecordPerformance} className="grid gap-3">
                <Field label="Code">
                  <Input value={perfCode} onChange={(e) => setPerfCode(e.target.value)} required />
                </Field>
                <Field label="Suite">
                  <Input value={suiteName} onChange={(e) => setSuiteName(e.target.value)} required />
                </Field>
                <Field label="p95 ms">
                  <Input value={p95Ms} onChange={(e) => setP95Ms(e.target.value)} required />
                </Field>
                <Button type="submit">Record run</Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Workflow replay" />
            <CardBody className="space-y-4">
              <form onSubmit={onCreateReplay} className="grid gap-3">
                <Field label="Workflow name">
                  <Input
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Idempotency key">
                  <Input
                    value={idempotencyKey}
                    onChange={(e) => setIdempotencyKey(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit">Create replay</Button>
              </form>
              <div className="text-sm text-muted-foreground">
                Status: {replay ? replay.status : "none"}
              </div>
              <div className="flex flex-wrap gap-2">
                <form onSubmit={onFailReplay}>
                  <Button type="submit" variant="secondary" disabled={!replay}>
                    Simulate fail
                  </Button>
                </form>
                <form onSubmit={onResumeReplay}>
                  <Button type="submit" disabled={!replay}>
                    Resume
                  </Button>
                </form>
              </div>
            </CardBody>
          </Card>
        </div>

        <Card>
          <CardHeader title="DR runbooks" />
          <CardBody className="space-y-4">
            <form onSubmit={onCreateRunbook} className="grid gap-3 md:grid-cols-3">
              <Field label="Code">
                <Input value={runbookCode} onChange={(e) => setRunbookCode(e.target.value)} required />
              </Field>
              <Field label="Title">
                <Input
                  value={runbookTitle}
                  onChange={(e) => setRunbookTitle(e.target.value)}
                  required
                />
              </Field>
              <div className="flex items-end">
                <Button type="submit">Record runbook</Button>
              </div>
            </form>
            {!loading && runbooks.length === 0 ? (
              <EmptyState title="No DR runbooks" body="Record a runbook document for restore procedures." />
            ) : (
              <ul className="space-y-2 text-sm">
                {runbooks.map((runbook) => (
                  <li key={runbook.id} className="rounded border p-2">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">
                        {runbook.code} — {runbook.title}
                      </span>
                      <StatusBadge status={runbook.status} />
                    </div>
                    <div className="text-muted-foreground">
                      RTO {runbook.rto_minutes}m / RPO {runbook.rpo_minutes}m — {formatUtc(runbook.created_at)}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </CardBody>
        </Card>
      </ScrollRegion>
    </AppShell>
  );
}
