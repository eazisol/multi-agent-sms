"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows, StatusBanner } from "@/components/ui-states";
import {
  ApiError,
  addApprovalEvidence,
  createApproval,
  decideApproval,
  formatUtc,
  listApprovalDecisions,
  listApprovalSteps,
  listApprovals,
  type ApprovalDecision,
  type ApprovalRequest,
  type ApprovalStep,
} from "@/lib/api";
import { can } from "@/lib/roles";
import { getWorkspaceProjectId, getWorkspaceQueryId } from "@/lib/workspace";

type FilterTab = { id: string; label: string; status?: string };

const FILTER_TABS: FilterTab[] = [
  { id: "all", label: "All" },
  { id: "pending", label: "Pending", status: "pending" },
  { id: "approved", label: "Approved", status: "approved" },
  { id: "rejected", label: "Rejected", status: "rejected" },
];

export function ApprovalsDeskPage() {
  const { session } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [activeTab, setActiveTab] = useState("pending");
  const [items, setItems] = useState<ApprovalRequest[]>([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [steps, setSteps] = useState<ApprovalStep[]>([]);
  const [decisions, setDecisions] = useState<ApprovalDecision[]>([]);
  const [reason, setReason] = useState("");
  const [evidenceRef, setEvidenceRef] = useState("");

  const [title, setTitle] = useState("");
  const [actionCode, setActionCode] = useState("srs.baseline");
  const [targetType, setTargetType] = useState("srs_baseline");
  const [targetId, setTargetId] = useState("");
  const [targetVersion, setTargetVersion] = useState("1");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const tab = FILTER_TABS.find((t) => t.id === activeTab) ?? FILTER_TABS[0];
      const rows = await listApprovals(session, { status: tab.status });
      setItems(rows);
      setCurrentId((prev) => {
        if (prev && rows.some((r) => r.id === prev)) return prev;
        return rows[0]?.id ?? null;
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load approvals");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [session, activeTab]);

  useEffect(() => {
    void load();
  }, [load]);

  const current = useMemo(
    () => items.find((item) => item.id === currentId) ?? null,
    [items, currentId],
  );

  const refreshDetails = useCallback(async () => {
    if (!currentId) {
      setSteps([]);
      setDecisions([]);
      return;
    }
    try {
      const [stepRows, decisionRows] = await Promise.all([
        listApprovalSteps(session, currentId),
        listApprovalDecisions(session, currentId),
      ]);
      setSteps(stepRows);
      setDecisions(decisionRows);
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Unable to load approval detail");
    }
  }, [currentId, session]);

  useEffect(() => {
    void refreshDetails();
  }, [refreshDetails]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setOk(null);
    try {
      const entityId = targetId.trim() || getWorkspaceQueryId() || getWorkspaceProjectId();
      if (!entityId) {
        setError("Provide a target entity id, or select a query/project on those desks first");
        return;
      }
      const created = await createApproval(session, {
        action_code: actionCode.trim(),
        title: title.trim(),
        target_entity_type: targetType.trim(),
        target_entity_id: entityId,
        target_version: Number(targetVersion) || 1,
        project_id: getWorkspaceProjectId() || undefined,
        steps: [{ role_code: "approver", order: 1, assignee_actor_id: session.actorId }],
      });
      setCurrentId(created.id);
      setOk("Approval request submitted");
      setShowCreate(false);
      setTitle("");
      setTargetId("");
      setActiveTab("pending");
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not create approval");
    }
  }

  async function onDecide(decision: "approve" | "reject" | "withdraw") {
    if (!current) return;
    setError(null);
    setOk(null);
    try {
      await decideApproval(session, current.id, {
        decision,
        reason: reason.trim() || undefined,
        expected_version: current.version,
      });
      setOk(`Decision recorded: ${decision}`);
      setReason("");
      await load();
      await refreshDetails();
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Decision failed");
    }
  }

  async function onEvidence() {
    if (!current || !evidenceRef.trim()) return;
    setError(null);
    setOk(null);
    try {
      await addApprovalEvidence(session, current.id, {
        evidence_ref: evidenceRef.trim(),
        evidence_type: "reference",
      });
      setOk("Evidence attached");
      setEvidenceRef("");
    } catch (err) {
      setError(err instanceof ApiError ? err.problem.message : "Could not attach evidence");
    }
  }

  return (
    <AppShell title="Approvals" breadcrumbs={["Coordination", "Approvals"]}>
      <PageHeader
        title="Approvals"
        description="Human approval gates bound to an exact entity version. Agents may recommend; humans decide."
        actions={
          can(session.variant, "create") || can(session.variant, "submit") ? (
            <Button onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New approval
            </Button>
          ) : null
        }
      />

      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      {ok ? <StatusBanner kind="success">{ok}</StatusBanner> : null}

      {showCreate ? (
        <Card className="mb-6">
          <CardHeader>
            <h2 className="font-display text-lg">Submit approval</h2>
            <p className="text-sm text-[var(--muted)]">
              Locks the request to a target type, id, and version. Defaults target id from the
              workspace query or project when blank.
            </p>
          </CardHeader>
          <CardBody>
            <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create approval">
              <Field label="Title" className="md:col-span-2">
                <Input
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Approve SRS baseline v1"
                />
              </Field>
              <Field label="Action code">
                <Input
                  required
                  value={actionCode}
                  onChange={(e) => setActionCode(e.target.value)}
                  placeholder="srs.baseline"
                />
              </Field>
              <Field label="Target type">
                <Input
                  required
                  value={targetType}
                  onChange={(e) => setTargetType(e.target.value)}
                  placeholder="srs_baseline"
                />
              </Field>
              <Field label="Target entity id" hint="Optional if a Queries or Projects selection exists">
                <Input
                  value={targetId}
                  onChange={(e) => setTargetId(e.target.value)}
                  placeholder="Leave blank to use workspace query/project"
                />
              </Field>
              <Field label="Target version">
                <Input
                  required
                  type="number"
                  min={1}
                  value={targetVersion}
                  onChange={(e) => setTargetVersion(e.target.value)}
                />
              </Field>
              <div className="flex justify-end gap-2 md:col-span-2">
                <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </Button>
                <Button type="submit">Submit request</Button>
              </div>
            </form>
          </CardBody>
        </Card>
      ) : null}

      <div className="mb-4 flex flex-wrap gap-2">
        {FILTER_TABS.map((tab) => (
          <Button
            key={tab.id}
            variant={activeTab === tab.id ? "primary" : "outline"}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </Button>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(280px,360px)_1fr]">
        <Card>
          <CardHeader>
            <h2 className="font-display text-lg">Approval queue</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/approvals`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No approvals"
                body="Submit an approval for an entity version that needs a human gate."
                action={
                  can(session.variant, "create") || can(session.variant, "submit") ? (
                    <Button onClick={() => setShowCreate(true)}>New approval</Button>
                  ) : null
                }
              />
            </CardBody>
          ) : (
            <ul className="divide-y divide-[var(--line)]">
              {items.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => setCurrentId(item.id)}
                    className={`w-full px-5 py-3 text-left transition hover:bg-[var(--surface-muted)]/70 ${
                      item.id === currentId ? "bg-[var(--accent-soft)]" : ""
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">{item.title}</span>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {item.action_code} · v{item.target_version}
                    </p>
                    <p className="mt-1 text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </Card>

        {current ? (
          <div className="space-y-4">
            <Card>
              <CardHeader className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="font-display text-xl">{current.title}</h2>
                  <p className="mt-1 text-sm text-[var(--muted)]">
                    {current.target_entity_type} · {current.target_entity_id.slice(0, 8)}… · version{" "}
                    {current.target_version}
                  </p>
                </div>
                <StatusBadge status={current.status} />
              </CardHeader>
              <CardBody className="space-y-4 text-sm">
                <p>
                  <span className="text-[var(--muted)]">Action:</span> {current.action_code}
                </p>
                <p>
                  <span className="text-[var(--muted)]">Step:</span> {current.current_step_order}
                </p>
                {current.status === "pending" ? (
                  <>
                    <Field label="Decision reason" hint="Required for reject / withdraw">
                      <Textarea
                        rows={2}
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="Why this decision?"
                      />
                    </Field>
                    <div className="flex flex-wrap gap-2">
                      <Button
                        disabled={!can(session.variant, "approve")}
                        onClick={() => void onDecide("approve")}
                      >
                        Approve
                      </Button>
                      <Button
                        variant="outline"
                        disabled={!can(session.variant, "reject")}
                        onClick={() => void onDecide("reject")}
                      >
                        Reject
                      </Button>
                      <Button
                        variant="ghost"
                        disabled={!can(session.variant, "submit")}
                        onClick={() => void onDecide("withdraw")}
                      >
                        Withdraw
                      </Button>
                    </div>
                    {!can(session.variant, "approve") ? (
                      <StatusBanner kind="info">
                        Switch to Baseline Approver or Admin in the role selector to record an
                        approval.
                      </StatusBanner>
                    ) : null}
                  </>
                ) : null}
                <div className="flex flex-wrap items-end gap-2">
                  <Field label="Evidence ref" className="min-w-[240px] flex-1">
                    <Input
                      value={evidenceRef}
                      onChange={(e) => setEvidenceRef(e.target.value)}
                      placeholder="doc://review-notes"
                    />
                  </Field>
                  <Button variant="outline" onClick={() => void onEvidence()}>
                    Attach evidence
                  </Button>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <h3 className="font-display text-lg">Steps</h3>
              </CardHeader>
              {steps.length === 0 ? (
                <CardBody>
                  <p className="text-sm text-[var(--muted)]">No steps loaded.</p>
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {steps.map((s) => (
                    <li key={s.id} className="flex items-center justify-between gap-2 px-5 py-3 text-sm">
                      <span>
                        #{s.step_order} · {s.role_code}
                      </span>
                      <StatusBadge status={s.status} />
                    </li>
                  ))}
                </ul>
              )}
            </Card>

            <Card>
              <CardHeader>
                <h3 className="font-display text-lg">Decision history</h3>
              </CardHeader>
              {decisions.length === 0 ? (
                <CardBody>
                  <p className="text-sm text-[var(--muted)]">No decisions yet.</p>
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {decisions.map((d) => (
                    <li key={d.id} className="px-5 py-3 text-sm">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <StatusBadge status={d.decision} />
                        <span className="text-xs text-[var(--muted)]">{formatUtc(d.decided_at)}</span>
                      </div>
                      {d.reason ? <p className="mt-1 text-[var(--muted)]">{d.reason}</p> : null}
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>
        ) : !loading ? (
          <EmptyState title="Select an approval" body="Choose a request from the queue." />
        ) : null}
      </div>
    </AppShell>
  );
}
