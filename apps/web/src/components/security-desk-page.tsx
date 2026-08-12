"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader } from "@/components/ui-states";
import {
  closeSecurityIncident,
  createSecurityBackup,
  createSecurityIncident,
  createSecurityRestoreTest,
  formatUtc,
  getSecurityGate,
  getSecurityTrainingPolicy,
  listSecurityLegalHolds,
  updateSecurityTrainingPolicy,
  type SecurityBackupRecord,
  type SecurityGate,
  type SecurityIncident,
  type SecurityLegalHold,
  type SecurityTrainingPolicy,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function SecurityDeskPage() {
  const { session } = useSession();
  const [gate, setGate] = useState<SecurityGate | null>(null);
  const [policy, setPolicy] = useState<SecurityTrainingPolicy | null>(null);
  const [holds, setHolds] = useState<SecurityLegalHold[]>([]);
  const [lastBackup, setLastBackup] = useState<SecurityBackupRecord | null>(null);
  const [loading, setLoading] = useState(true);

  const [incidentCode, setIncidentCode] = useState("INC-600");
  const [incidentTitle, setIncidentTitle] = useState("Critical sample defect");
  const [evidence, setEvidence] = useState("");
  const [allowTraining, setAllowTraining] = useState(false);
  const [backupRef, setBackupRef] = useState("bk-local-600");
  const [rpo, setRpo] = useState("60");
  const [rto, setRto] = useState("120");
  const [measuredRpo, setMeasuredRpo] = useState("30");
  const [measuredRto, setMeasuredRto] = useState("90");
  const [openIncident, setOpenIncident] = useState<SecurityIncident | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [gateRes, policyRes, holdsPage] = await Promise.all([
        getSecurityGate(session),
        getSecurityTrainingPolicy(session),
        listSecurityLegalHolds(session),
      ]);
      setGate(gateRes);
      setPolicy(policyRes);
      setAllowTraining(policyRes.allow_model_training);
      setHolds(holdsPage.items);
    } catch (err) {
      notifyApiError("Unable to load Security desk", err);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateIncident(event: FormEvent) {
    event.preventDefault();
    try {
      const incident = await createSecurityIncident(session, {
        code: incidentCode.trim(),
        title: incidentTitle.trim(),
        severity: "critical",
        summary: "Opened from Security desk for gate validation",
      });
      setOpenIncident(incident);
      notifySuccess("Critical incident opened — gate should fail");
      await load();
    } catch (err) {
      notifyApiError("Create incident failed", err);
    }
  }

  async function onCloseIncident(event: FormEvent) {
    event.preventDefault();
    if (!openIncident) return;
    try {
      await closeSecurityIncident(session, openIncident.id, {
        expected_version: openIncident.version,
      });
      setOpenIncident(null);
      notifySuccess("Incident closed — gate should pass");
      await load();
    } catch (err) {
      notifyApiError("Close incident failed", err);
    }
  }

  async function onUpdateTraining(event: FormEvent) {
    event.preventDefault();
    try {
      const updated = await updateSecurityTrainingPolicy(session, {
        allow_model_training: allowTraining,
        human_approval_evidence: evidence.trim() || undefined,
      });
      setPolicy(updated);
      notifySuccess("Training policy updated");
      await load();
    } catch (err) {
      notifyApiError("Training policy update failed", err);
    }
  }

  async function onRecordBackup(event: FormEvent) {
    event.preventDefault();
    try {
      const backup = await createSecurityBackup(session, {
        backup_ref: backupRef.trim(),
        environment: "local",
        rpo_minutes: Number(rpo),
        rto_minutes: Number(rto),
      });
      setLastBackup(backup);
      notifySuccess("Backup record created");
    } catch (err) {
      notifyApiError("Backup record failed", err);
    }
  }

  async function onRestoreTest(event: FormEvent) {
    event.preventDefault();
    if (!lastBackup) return;
    try {
      await createSecurityRestoreTest(session, {
        backup_record_id: lastBackup.id,
        measured_rpo_minutes: Number(measuredRpo),
        measured_rto_minutes: Number(measuredRto),
        notes: "Desk restore measurement",
      });
      notifySuccess("Restore test recorded");
    } catch (err) {
      notifyApiError("Restore test failed", err);
    }
  }

  return (
    <AppShell>
      <PageHeader
        title="Security"
        description="Gate status, training opt-in, incidents, backups, restore tests, and legal holds (M1)."
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
            <CardHeader title="Security gate" />
            <CardBody className="space-y-2 text-sm">
              {gate ? (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span>Gate</span>
                    <StatusBadge status={gate.gate_passed ? "passed" : "failed"} />
                  </div>
                  <div>Critical open: {gate.critical_open_count}</div>
                </>
              ) : (
                <EmptyState title="Gate unavailable" body={loading ? "Loading…" : "Refresh to load."} />
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Training policy" />
            <CardBody>
              <form onSubmit={onUpdateTraining} className="grid gap-3">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={allowTraining}
                    onChange={(e) => setAllowTraining(e.target.checked)}
                  />
                  Allow model training
                </label>
                <Field label="Human approval evidence">
                  <Textarea
                    value={evidence}
                    onChange={(e) => setEvidence(e.target.value)}
                    placeholder="Required when enabling training"
                  />
                </Field>
                <div className="text-xs text-muted-foreground">
                  Current: {policy?.allow_model_training ? "enabled" : "disabled (default)"}
                </div>
                <Button type="submit">Save training policy</Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Critical incident" />
            <CardBody className="space-y-4">
              <form onSubmit={onCreateIncident} className="grid gap-3">
                <Field label="Code">
                  <Input value={incidentCode} onChange={(e) => setIncidentCode(e.target.value)} required />
                </Field>
                <Field label="Title">
                  <Input value={incidentTitle} onChange={(e) => setIncidentTitle(e.target.value)} required />
                </Field>
                <Button type="submit">Open critical incident</Button>
              </form>
              <form onSubmit={onCloseIncident}>
                <Button type="submit" variant="secondary" disabled={!openIncident}>
                  Close last opened incident
                </Button>
              </form>
            </CardBody>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Backup + restore test" />
            <CardBody className="space-y-4">
              <form onSubmit={onRecordBackup} className="grid gap-3">
                <Field label="Backup ref">
                  <Input value={backupRef} onChange={(e) => setBackupRef(e.target.value)} required />
                </Field>
                <div className="grid grid-cols-2 gap-3">
                  <Field label="RPO minutes">
                    <Input value={rpo} onChange={(e) => setRpo(e.target.value)} required />
                  </Field>
                  <Field label="RTO minutes">
                    <Input value={rto} onChange={(e) => setRto(e.target.value)} required />
                  </Field>
                </div>
                <Button type="submit">Record backup</Button>
              </form>
              <form onSubmit={onRestoreTest} className="grid gap-3">
                <div className="grid grid-cols-2 gap-3">
                  <Field label="Measured RPO">
                    <Input value={measuredRpo} onChange={(e) => setMeasuredRpo(e.target.value)} required />
                  </Field>
                  <Field label="Measured RTO">
                    <Input value={measuredRto} onChange={(e) => setMeasuredRto(e.target.value)} required />
                  </Field>
                </div>
                <Button type="submit" disabled={!lastBackup}>
                  Run restore test
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Legal holds" />
            <CardBody>
              {!loading && holds.length === 0 ? (
                <EmptyState title="No legal holds" body="Create holds via API to block deletion jobs." />
              ) : (
                <ul className="space-y-2 text-sm">
                  {holds.map((hold) => (
                    <li key={hold.id} className="rounded border p-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium">{hold.code}</span>
                        <StatusBadge status={hold.status} />
                      </div>
                      <div className="text-muted-foreground">
                        {hold.reason} — {formatUtc(hold.created_at)}
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
