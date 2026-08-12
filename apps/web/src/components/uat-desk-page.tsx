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
  createAgentEvaluation,
  createAcceptanceEvidence,
  formatUtc,
  getAgentQuality,
  getSampleGate,
  listAcceptanceEvidence,
  listSampleProjects,
  markSampleProjectPassed,
  seedSampleProjects,
  type AcceptanceEvidence,
  type AgentQuality,
  type SampleGate,
  type SampleProject,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function UatDeskPage() {
  const { session } = useSession();
  const [gate, setGate] = useState<SampleGate | null>(null);
  const [quality, setQuality] = useState<AgentQuality | null>(null);
  const [samples, setSamples] = useState<SampleProject[]>([]);
  const [evidence, setEvidence] = useState<AcceptanceEvidence[]>([]);
  const [loading, setLoading] = useState(true);

  const [evalCode, setEvalCode] = useState("EVAL-620");
  const [agentCode, setAgentCode] = useState("intake-agent");
  const [accuracyPct, setAccuracyPct] = useState("85");
  const [evidenceCode, setEvidenceCode] = useState("EV-620");
  const [evidenceTitle, setEvidenceTitle] = useState("UAT acceptance pack");
  const [evidenceRef, setEvidenceRef] = useState("docs/uat/ev-620");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [gateRes, qualityRes, samplePage, evidencePage] = await Promise.all([
        getSampleGate(session),
        getAgentQuality(session),
        listSampleProjects(session),
        listAcceptanceEvidence(session),
      ]);
      setGate(gateRes);
      setQuality(qualityRes);
      setSamples(samplePage.items);
      setEvidence(evidencePage.items);
    } catch (err) {
      notifyApiError("Unable to load UAT desk", err);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onSeedSamples(event: FormEvent) {
    event.preventDefault();
    try {
      await seedSampleProjects(session);
      notifySuccess("Sample projects seeded");
      await load();
    } catch (err) {
      notifyApiError("Seed sample projects failed", err);
    }
  }

  async function onPassSample(code: string) {
    try {
      await markSampleProjectPassed(session, code);
      notifySuccess(`${code} marked passed`);
      await load();
    } catch (err) {
      notifyApiError(`Pass ${code} failed`, err);
    }
  }

  async function onRecordEval(event: FormEvent) {
    event.preventDefault();
    try {
      await createAgentEvaluation(session, {
        code: evalCode.trim(),
        agent_code: agentCode.trim(),
        accuracy_pct: Number(accuracyPct),
        sample_count: 20,
      });
      notifySuccess("Agent evaluation recorded");
      await load();
    } catch (err) {
      notifyApiError("Record agent evaluation failed", err);
    }
  }

  async function onCreateEvidence(event: FormEvent) {
    event.preventDefault();
    try {
      await createAcceptanceEvidence(session, {
        code: evidenceCode.trim(),
        title: evidenceTitle.trim(),
        evidence_ref: evidenceRef.trim(),
        status: "submitted",
      });
      notifySuccess("Acceptance evidence recorded");
      await load();
    } catch (err) {
      notifyApiError("Record evidence failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="UAT"
        description="Synthetic sample projects, agent quality, and acceptance evidence (M1)."
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
            <CardHeader title="Sample-project gate" />
            <CardBody className="space-y-2 text-sm">
              {gate ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>
                      {gate.passed_count} / {gate.required_count} workflows passed
                    </span>
                    <StatusBadge status={gate.gate_passed ? "passed" : "failed"} />
                  </div>
                  <div>Required sample projects: {gate.required_count}</div>
                </>
              ) : (
                <EmptyState
                  title="Sample gate unavailable"
                  body={loading ? "Loading…" : "Refresh to load."}
                />
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Agent quality" />
            <CardBody className="space-y-2 text-sm">
              {quality ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>Target ≥ {quality.target_pct}%</span>
                    <StatusBadge status={quality.meets_target ? "passed" : "failed"} />
                  </div>
                  <div>Latest score: {quality.latest_score ?? "—"}%</div>
                </>
              ) : (
                <EmptyState
                  title="Agent quality unavailable"
                  body={loading ? "Loading…" : "Refresh to load."}
                />
              )}
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Synthetic sample projects" />
            <CardBody className="space-y-4">
              <form onSubmit={onSeedSamples}>
                <Button type="submit">Seed SAMPLE-A / B / C</Button>
              </form>
              {!loading && samples.length === 0 ? (
                <EmptyState
                  title="No sample projects"
                  body="Seed the three synthetic project codes to start the workflow gate."
                />
              ) : (
                <ul className="space-y-2 text-sm">
                  {samples.map((sample) => (
                    <li key={sample.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">
                          {sample.code} — {sample.title}
                        </span>
                        <StatusBadge status={sample.workflow_status} />
                      </div>
                      <div className="mt-2">
                        <Button
                          type="button"
                          variant="secondary"
                          disabled={sample.workflow_status === "passed"}
                          onClick={() => void onPassSample(sample.code)}
                        >
                          Mark passed
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Record agent evaluation" />
            <CardBody>
              <form onSubmit={onRecordEval} className="grid gap-3">
                <Field label="Code">
                  <Input value={evalCode} onChange={(e) => setEvalCode(e.target.value)} required />
                </Field>
                <Field label="Agent code">
                  <Input
                    value={agentCode}
                    onChange={(e) => setAgentCode(e.target.value)}
                    required
                  />
                </Field>
                <Field label="Accuracy %">
                  <Input
                    value={accuracyPct}
                    onChange={(e) => setAccuracyPct(e.target.value)}
                    required
                  />
                </Field>
                <Button type="submit">Record evaluation</Button>
              </form>
            </CardBody>
          </Card>
        </div>

        <Card>
          <CardHeader title="Acceptance evidence" />
          <CardBody className="space-y-4">
            <form onSubmit={onCreateEvidence} className="grid gap-3 md:grid-cols-3">
              <Field label="Code">
                <Input
                  value={evidenceCode}
                  onChange={(e) => setEvidenceCode(e.target.value)}
                  required
                />
              </Field>
              <Field label="Title">
                <Input
                  value={evidenceTitle}
                  onChange={(e) => setEvidenceTitle(e.target.value)}
                  required
                />
              </Field>
              <Field label="Evidence ref">
                <Input
                  value={evidenceRef}
                  onChange={(e) => setEvidenceRef(e.target.value)}
                  required
                />
              </Field>
              <div className="flex items-end md:col-span-3">
                <Button type="submit">Record evidence</Button>
              </div>
            </form>
            {!loading && evidence.length === 0 ? (
              <EmptyState
                title="No acceptance evidence"
                body="Record a reference to UAT evidence. Agents cannot accept these records."
              />
            ) : (
              <ul className="space-y-2 text-sm">
                {evidence.map((item) => (
                  <li key={item.id} className="rounded border p-2">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">
                        {item.code} — {item.title}
                      </span>
                      <StatusBadge status={item.status} />
                    </div>
                    <div className="text-muted-foreground">
                      {item.evidence_ref} — {formatUtc(item.created_at)}
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
