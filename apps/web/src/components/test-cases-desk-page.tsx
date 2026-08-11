"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Play } from "lucide-react";

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
  approveTestCase,
  completeTestRun,
  createTestCase,
  formatUtc,
  linkTestCoverage,
  listTestCases,
  startTestRun,
  summarizeTestCoverage,
  type CoverageSummary,
  type PageMeta,
  type TestCase,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function TestCasesDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<TestCase[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [summary, setSummary] = useState<CoverageSummary | null>(null);

  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [caseType, setCaseType] = useState("functional");
  const [priority, setPriority] = useState("P2");
  const [stepAction, setStepAction] = useState("");
  const [requirementId, setRequirementId] = useState("");
  const [projectId, setProjectId] = useState("");
  const [buildRef, setBuildRef] = useState("local-dev");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listTestCases(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
      const cov = await summarizeTestCoverage(session, {
        must_have_requirement_ids: requirementId.trim() ? [requirementId.trim()] : [],
      });
      setSummary(cov);
    } catch (err) {
      notifyApiError("Unable to load test cases", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset, requirementId]);

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
      const created = await createTestCase(session, {
        code: code.trim(),
        title: title.trim(),
        case_type: caseType,
        priority,
        project_id: projectId.trim() || undefined,
        steps: stepAction.trim()
          ? [{ step_number: 1, action_text: stepAction.trim(), expected_text: "As specified" }]
          : [],
      });
      if (requirementId.trim()) {
        await linkTestCoverage(session, created.id, {
          requirement_id: requirementId.trim(),
          requirement_priority: "Must-Have",
        });
      }
      await approveTestCase(session, created.id, created.version);
      notifySuccess("Test case created and approved");
      setShowCreate(false);
      setCode("");
      setTitle("");
      setStepAction("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create test case", err);
    }
  }

  async function onRun(item: TestCase) {
    try {
      const run = await startTestRun(session, {
        case_id: item.id,
        project_id: item.project_id || projectId.trim() || undefined,
        environment_code: "local",
        build_ref: buildRef.trim() || "local-dev",
      });
      await completeTestRun(session, run.id, {
        status: "passed",
        result_summary: "Desk M1 manual pass",
        expected_version: run.version,
        evidence_title: "Desk evidence",
        evidence_body: `Passed on ${run.environment_code} @ ${run.build_ref ?? "n/a"}`,
      });
      notifySuccess("Run completed with evidence");
      await load();
    } catch (err) {
      notifyApiError("Could not execute run", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Test Cases"
          description="Requirement-linked cases, runs, and environment/build evidence (MOD-400)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New case
            </Button>
          }
        />

        {summary ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Coverage snapshot</h2>
              <p className="text-sm text-[var(--muted)]">
                Must-Have {summary.must_have_covered}/{summary.must_have_total} · permission/negative{" "}
                {summary.permission_negative_cases}
              </p>
            </CardHeader>
          </Card>
        ) : null}

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create and approve case</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create test case">
                <Field label="Code">
                  <Input required value={code} onChange={(e) => setCode(e.target.value)} placeholder="TC-001" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Type">
                  <Input value={caseType} onChange={(e) => setCaseType(e.target.value)} placeholder="functional | permission | negative" />
                </Field>
                <Field label="Priority">
                  <Input value={priority} onChange={(e) => setPriority(e.target.value)} placeholder="P0–P3" />
                </Field>
                <Field label="Must-Have requirement id (optional)">
                  <Input value={requirementId} onChange={(e) => setRequirementId(e.target.value)} placeholder="UUID" />
                </Field>
                <Field label="Project id (optional)">
                  <Input value={projectId} onChange={(e) => setProjectId(e.target.value)} />
                </Field>
                <Field label="First step action">
                  <Textarea rows={3} value={stepAction} onChange={(e) => setStepAction(e.target.value)} />
                </Field>
                <Field label="Build ref for desk runs">
                  <Input value={buildRef} onChange={(e) => setBuildRef(e.target.value)} />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create &amp; approve</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Cases</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/test-cases/cases`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No test cases"
                body="Create an approved case to start recording runs and coverage."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    New case
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
                        {item.code} · {item.case_type} · {item.priority} · {formatUtc(item.updated_at)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={item.status} />
                      {item.status === "approved" ? (
                        <Button type="button" variant="ghost" onClick={() => void onRun(item)}>
                          <Play className="h-4 w-4" />
                          Run
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
              <ListPagination page={pageMeta} onOffsetChange={setOffset} onLimitChange={setLimit} label="cases" />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
