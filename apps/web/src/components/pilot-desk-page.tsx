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
  addPilotUser,
  approvePilotUser,
  createAcceptanceTest,
  createPilotPlan,
  getAcceptanceGate,
  getPilotApprovalGate,
  getReadinessGate,
  listAcceptanceTests,
  listFinalSignoffs,
  listPilotPlans,
  listPilotUsers,
  signFinalSignoff,
  type AcceptanceGate,
  type AcceptanceTest,
  type FinalSignoff,
  type PilotApprovalGate,
  type PilotPlan,
  type PilotUser,
  type ReadinessGate,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function PilotDeskPage() {
  const { session } = useSession();
  const [plans, setPlans] = useState<PilotPlan[]>([]);
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null);
  const [acceptanceGate, setAcceptanceGate] = useState<AcceptanceGate | null>(null);
  const [approvalGate, setApprovalGate] = useState<PilotApprovalGate | null>(null);
  const [readinessGate, setReadinessGate] = useState<ReadinessGate | null>(null);
  const [users, setUsers] = useState<PilotUser[]>([]);
  const [tests, setTests] = useState<AcceptanceTest[]>([]);
  const [signoffs, setSignoffs] = useState<FinalSignoff[]>([]);
  const [loading, setLoading] = useState(true);

  const [planCode, setPlanCode] = useState("PILOT-630");
  const [planTitle, setPlanTitle] = useState("Controlled production pilot");
  const [userActorId, setUserActorId] = useState(session.actorId);
  const [userRole, setUserRole] = useState("pilot-user");
  const [testCode, setTestCode] = useState("AT-630");
  const [testTitle, setTestTitle] = useState("Critical production path");
  const [testSeverity, setTestSeverity] = useState("critical");
  const [testResult, setTestResult] = useState("passed");
  const [signEvidence, setSignEvidence] = useState("Human production-readiness evidence");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const planPage = await listPilotPlans(session);
      setPlans(planPage.items);
      const planId = selectedPlanId ?? planPage.items[0]?.id ?? null;
      if (planId && planId !== selectedPlanId) {
        setSelectedPlanId(planId);
      }
      if (!planId) {
        setAcceptanceGate(null);
        setApprovalGate(null);
        setReadinessGate(null);
        setUsers([]);
        setTests([]);
        setSignoffs([]);
        return;
      }
      const [acceptRes, approvalRes, readyRes, userPage, testPage, signoffPage] =
        await Promise.all([
          getAcceptanceGate(session, planId),
          getPilotApprovalGate(session, planId),
          getReadinessGate(session, planId),
          listPilotUsers(session, planId),
          listAcceptanceTests(session, planId),
          listFinalSignoffs(session, planId),
        ]);
      setAcceptanceGate(acceptRes);
      setApprovalGate(approvalRes);
      setReadinessGate(readyRes);
      setUsers(userPage.items);
      setTests(testPage.items);
      setSignoffs(signoffPage.items);
    } catch (err) {
      notifyApiError("Unable to load Pilot desk", err);
    } finally {
      setLoading(false);
    }
  }, [session, selectedPlanId]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreatePlan(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createPilotPlan(session, {
        code: planCode.trim(),
        title: planTitle.trim(),
      });
      setSelectedPlanId(created.id);
      notifySuccess("Pilot plan created");
      await load();
    } catch (err) {
      notifyApiError("Create pilot plan failed", err);
    }
  }

  async function onAddUser(event: FormEvent) {
    event.preventDefault();
    if (!selectedPlanId) {
      notifyApiError("Create a plan first", new Error("No pilot plan selected"));
      return;
    }
    try {
      await addPilotUser(session, selectedPlanId, {
        actor_id: userActorId.trim(),
        role_label: userRole.trim(),
      });
      notifySuccess("Pilot user registered");
      await load();
    } catch (err) {
      notifyApiError("Add pilot user failed", err);
    }
  }

  async function onApproveUser(userId: string) {
    if (!selectedPlanId) {
      return;
    }
    try {
      await approvePilotUser(session, selectedPlanId, userId);
      notifySuccess("Pilot user approved production use");
      await load();
    } catch (err) {
      notifyApiError("Approve pilot user failed", err);
    }
  }

  async function onRecordTest(event: FormEvent) {
    event.preventDefault();
    if (!selectedPlanId) {
      notifyApiError("Create a plan first", new Error("No pilot plan selected"));
      return;
    }
    try {
      await createAcceptanceTest(session, selectedPlanId, {
        code: testCode.trim(),
        title: testTitle.trim(),
        severity: testSeverity.trim(),
        result: testResult.trim(),
      });
      notifySuccess("Acceptance test recorded");
      await load();
    } catch (err) {
      notifyApiError("Record acceptance test failed", err);
    }
  }

  async function onSign(signoffId: string) {
    try {
      await signFinalSignoff(session, signoffId, signEvidence.trim());
      notifySuccess("Function signed");
      await load();
    } catch (err) {
      notifyApiError("Sign-off failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Pilot"
        description="Controlled pilot gates, production sign-off records, and human-only readiness (M1)."
        actions={
          <Button variant="secondary" onClick={() => void load()}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        }
      />
      <ScrollRegion className="space-y-6 p-6">
        <div className="grid gap-6 lg:grid-cols-3">
          <Card>
            <CardHeader title="Acceptance gate" />
            <CardBody className="space-y-2 text-sm">
              {acceptanceGate ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>
                      Critical/High failed or blocked: {acceptanceGate.critical_high_failed_count}
                    </span>
                    <StatusBadge status={acceptanceGate.gate_passed ? "passed" : "failed"} />
                  </div>
                </>
              ) : (
                <EmptyState
                  title="Acceptance gate unavailable"
                  body={loading ? "Loading…" : "Create a plan to evaluate the gate."}
                />
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Pilot approval gate" />
            <CardBody className="space-y-2 text-sm">
              {approvalGate ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>
                      {approvalGate.approved_count} approved / {approvalGate.pending_count} pending
                    </span>
                    <StatusBadge status={approvalGate.gate_passed ? "passed" : "failed"} />
                  </div>
                </>
              ) : (
                <EmptyState
                  title="Pilot approval unavailable"
                  body={loading ? "Loading…" : "Create a plan to evaluate the gate."}
                />
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Readiness gate" />
            <CardBody className="space-y-2 text-sm">
              {readinessGate ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>
                      {readinessGate.signed_functions.length} /{" "}
                      {readinessGate.required_functions.length} functions signed
                    </span>
                    <StatusBadge status={readinessGate.gate_passed ? "passed" : "failed"} />
                  </div>
                </>
              ) : (
                <EmptyState
                  title="Readiness gate unavailable"
                  body={loading ? "Loading…" : "Create a plan to evaluate the gate."}
                />
              )}
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Pilot plans" />
            <CardBody className="space-y-4">
              <form onSubmit={onCreatePlan} className="grid gap-3">
                <Field label="Code">
                  <Input value={planCode} onChange={(e) => setPlanCode(e.target.value)} required />
                </Field>
                <Field label="Title">
                  <Input
                    value={planTitle}
                    onChange={(e) => setPlanTitle(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit">Create plan</Button>
              </form>
              {!loading && plans.length === 0 ? (
                <EmptyState
                  title="No pilot plans"
                  body="Create a plan to register users, tests, and sign-offs."
                />
              ) : (
                <ul className="space-y-2 text-sm">
                  {plans.map((plan) => (
                    <li key={plan.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">
                          {plan.code} — {plan.title}
                        </span>
                        <StatusBadge status={plan.status} />
                      </div>
                      <div className="mt-2">
                        <Button
                          type="button"
                          variant="secondary"
                          disabled={selectedPlanId === plan.id}
                          onClick={() => setSelectedPlanId(plan.id)}
                        >
                          {selectedPlanId === plan.id ? "Selected" : "Select"}
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Pilot users" />
            <CardBody className="space-y-4">
              <form onSubmit={onAddUser} className="grid gap-3">
                <Field label="Actor ID">
                  <Input
                    value={userActorId}
                    onChange={(e) => setUserActorId(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Role">
                  <Input value={userRole} onChange={(e) => setUserRole(e.target.value)} required />
                </Field>
                <Button type="submit">Add user</Button>
              </form>
              {!loading && users.length === 0 ? (
                <EmptyState
                  title="No pilot users"
                  body="Register users, then approve each for controlled production use."
                />
              ) : (
                <ul className="space-y-2 text-sm">
                  {users.map((user) => (
                    <li key={user.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">{user.role_label}</span>
                        <StatusBadge
                          status={user.approved_production_use ? "approved" : "pending"}
                        />
                      </div>
                      <div className="text-muted-foreground">{user.actor_id}</div>
                      <div className="mt-2">
                        <Button
                          type="button"
                          variant="secondary"
                          disabled={user.approved_production_use}
                          onClick={() => void onApproveUser(user.id)}
                        >
                          Approve production use
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Acceptance tests" />
            <CardBody className="space-y-4">
              <form onSubmit={onRecordTest} className="grid gap-3">
                <Field label="Code">
                  <Input value={testCode} onChange={(e) => setTestCode(e.target.value)} required />
                </Field>
                <Field label="Title">
                  <Input
                    value={testTitle}
                    onChange={(e) => setTestTitle(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Severity">
                  <Input
                    value={testSeverity}
                    onChange={(e) => setTestSeverity(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Result">
                  <Input
                    value={testResult}
                    onChange={(e) => setTestResult(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit">Record test</Button>
              </form>
              {!loading && tests.length === 0 ? (
                <EmptyState
                  title="No acceptance tests"
                  body="Record Critical/High results. Failed or blocked tests keep the gate closed."
                />
              ) : (
                <ul className="space-y-2 text-sm">
                  {tests.map((item) => (
                    <li key={item.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">
                          {item.code} — {item.title}
                        </span>
                        <StatusBadge status={item.result} />
                      </div>
                      <div className="text-muted-foreground">Severity: {item.severity}</div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Cross-functional sign-off" />
            <CardBody className="space-y-4">
              <Field label="Evidence">
                <Input
                  value={signEvidence}
                  onChange={(e) => setSignEvidence(e.target.value)}
                  required
                />
              </Field>
              {!loading && signoffs.length === 0 ? (
                <EmptyState
                  title="No sign-offs"
                  body="Create a plan to seed product, security, operations, and QA sign-offs. Agents cannot sign."
                />
              ) : (
                <ul className="space-y-2 text-sm">
                  {signoffs.map((item) => (
                    <li key={item.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">{item.function_code}</span>
                        <StatusBadge status={item.status} />
                      </div>
                      <div className="mt-2">
                        <Button
                          type="button"
                          variant="secondary"
                          disabled={item.status === "signed"}
                          onClick={() => void onSign(item.id)}
                        >
                          Sign as human
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>
      </ScrollRegion>
    </AppShell>
  );
}
