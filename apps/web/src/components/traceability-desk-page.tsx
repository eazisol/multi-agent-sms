"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Download, Link2, Plus, RefreshCw, ShieldCheck } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  addManifestItem,
  createEvidenceExport,
  createEvidenceManifest,
  createRequirementTicketLink,
  formatUtc,
  getAuditCoverage,
  getTraceabilityCoverage,
  listEvidenceExports,
  listEvidenceManifests,
  listMustHaves,
  registerMustHave,
  sealEvidenceManifest,
  type AuditCoverageReport,
  type EvidenceExport,
  type EvidenceManifest,
  type MustHaveRequirement,
  type TraceabilityCoverage,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

function newUuid() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return "00000000-0000-4000-8000-000000000001";
}

export function TraceabilityDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [mustHaves, setMustHaves] = useState<MustHaveRequirement[]>([]);
  const [coverage, setCoverage] = useState<TraceabilityCoverage | null>(null);
  const [audit, setAudit] = useState<AuditCoverageReport | null>(null);
  const [manifests, setManifests] = useState<EvidenceManifest[]>([]);
  const [exports, setExports] = useState<EvidenceExport[]>([]);

  const [reqCode, setReqCode] = useState("MH-001");
  const [reqTitle, setReqTitle] = useState("Must-have requirement");
  const [reqId, setReqId] = useState("");
  const [ticketId, setTicketId] = useState("");
  const [manifestCode, setManifestCode] = useState("EVID-001");
  const [manifestTitle, setManifestTitle] = useState("Release evidence");
  const [selectedManifestId, setSelectedManifestId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [mh, cov, aud, man, exp] = await Promise.allSettled([
        listMustHaves(session, { limit: 20 }),
        getTraceabilityCoverage(session),
        getAuditCoverage(session),
        listEvidenceManifests(session, { limit: 20 }),
        listEvidenceExports(session, { limit: 20 }),
      ]);
      setMustHaves(mh.status === "fulfilled" ? mh.value.items : []);
      setCoverage(cov.status === "fulfilled" ? cov.value : null);
      setAudit(aud.status === "fulfilled" ? aud.value : null);
      setManifests(man.status === "fulfilled" ? man.value.items : []);
      setExports(exp.status === "fulfilled" ? exp.value.items : []);
      if (cov.status === "rejected") {
        notifyApiError("Unable to load coverage", cov.reason);
      }
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onRegisterMustHave(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await registerMustHave(session, {
        requirement_id: reqId.trim() || newUuid(),
        requirement_code: reqCode.trim(),
        title: reqTitle.trim(),
      });
      notifySuccess(`Registered ${created.requirement_code}`);
      setReqId(created.requirement_id);
      setReqCode(`MH-${String(mustHaves.length + 2).padStart(3, "0")}`);
      await load();
    } catch (err) {
      notifyApiError("Could not register must-have", err);
    }
  }

  async function onAddTicketLink(event: FormEvent) {
    event.preventDefault();
    if (!reqId.trim()) {
      notifyApiError("Requirement id required", new Error("missing requirement_id"));
      return;
    }
    try {
      await createRequirementTicketLink(session, {
        requirement_id: reqId.trim(),
        ticket_id: ticketId.trim() || newUuid(),
      });
      notifySuccess("Requirement-ticket link created");
      setTicketId("");
      await load();
    } catch (err) {
      notifyApiError("Could not create link", err);
    }
  }

  async function onCreateManifest(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createEvidenceManifest(session, {
        code: manifestCode.trim(),
        title: manifestTitle.trim(),
      });
      notifySuccess(`Manifest ${created.code} created`);
      setSelectedManifestId(created.id);
      setManifestCode(`EVID-${String(manifests.length + 2).padStart(3, "0")}`);
      await load();
    } catch (err) {
      notifyApiError("Could not create manifest", err);
    }
  }

  async function onAddItemAndSeal() {
    const mid = selectedManifestId || manifests[0]?.id;
    if (!mid) {
      notifyApiError("Create a manifest first", new Error("no manifest"));
      return;
    }
    try {
      await addManifestItem(session, mid, {
        item_type: "requirement",
        item_id: reqId.trim() || mustHaves[0]?.requirement_id || newUuid(),
        label: "requirement",
      });
      const sealed = await sealEvidenceManifest(session, mid, {});
      notifySuccess(`Sealed ${sealed.code}`);
      setSelectedManifestId(mid);
      await load();
    } catch (err) {
      notifyApiError("Could not seal manifest", err);
    }
  }

  async function onExport() {
    const mid = selectedManifestId || manifests.find((m) => m.status === "sealed")?.id;
    if (!mid) {
      notifyApiError("Seal a manifest first", new Error("no sealed manifest"));
      return;
    }
    try {
      await createEvidenceExport(session, { manifest_id: mid, export_format: "json" });
      notifySuccess("Evidence export ready (in-DB preview)");
      await load();
    } catch (err) {
      notifyApiError("Could not create export", err);
    }
  }

  return (
    <AppShell title="Traceability" breadcrumbs={["Governance", "Traceability"]}>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Traceability"
          description="Must-have coverage, link registry, evidence manifests, and reconcilable exports (MOD-460)."
          actions={
            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="outline" onClick={() => void load()}>
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
              <Button type="button" onClick={() => void onExport()}>
                <Download className="h-4 w-4" />
                Export sealed
              </Button>
            </div>
          }
        />

        <div className="grid shrink-0 gap-4 md:grid-cols-2 xl:grid-cols-4">
          {loading && !coverage
            ? Array.from({ length: 4 }).map((_, i) => (
                <Card key={i}>
                  <CardBody>
                    <SkeletonRows rows={2} />
                  </CardBody>
                </Card>
              ))
            : [
                {
                  label: "Must-haves",
                  value: String(coverage?.total_must_haves ?? mustHaves.length ?? "—"),
                },
                {
                  label: "Coverage",
                  value: coverage ? `${coverage.coverage_pct}%` : "—",
                },
                {
                  label: "Release ready",
                  value: coverage?.release_ready ? "Yes (≥95%)" : coverage ? "No" : "—",
                },
                {
                  label: "Audit coverage",
                  value: audit ? `${audit.coverage_pct}%` : "—",
                },
              ].map((card) => (
                <Card key={card.label}>
                  <CardBody>
                    <p className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
                      {card.label}
                    </p>
                    <p className="mt-2 font-display text-2xl tracking-tight">{card.value}</p>
                  </CardBody>
                </Card>
              ))}
        </div>

        <div className="grid min-h-0 flex-1 gap-4 xl:grid-cols-2">
          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Register must-have</h2>
            </CardHeader>
            <CardBody className="shrink-0">
              <form
                onSubmit={onRegisterMustHave}
                className="grid gap-3 md:grid-cols-2"
                aria-label="Register must-have"
              >
                <Field label="Code">
                  <Input required value={reqCode} onChange={(e) => setReqCode(e.target.value)} />
                </Field>
                <Field label="Title">
                  <Input required value={reqTitle} onChange={(e) => setReqTitle(e.target.value)} />
                </Field>
                <Field label="Requirement ID (optional)">
                  <Input
                    value={reqId}
                    onChange={(e) => setReqId(e.target.value)}
                    placeholder="Auto-generate if empty"
                  />
                </Field>
                <div className="flex items-end">
                  <Button type="submit">
                    <Plus className="h-4 w-4" />
                    Register
                  </Button>
                </div>
              </form>
            </CardBody>
            <ScrollRegion className="flex-1">
              {mustHaves.length === 0 ? (
                <CardBody>
                  <EmptyState title="No must-haves" body="Register must-have requirement IDs for coverage." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {mustHaves.map((item) => (
                    <li key={item.id} className="px-5 py-3">
                      <p className="font-medium">
                        {item.requirement_code} · {item.title}
                      </p>
                      <p className="text-xs text-[var(--muted)]">{item.requirement_id}</p>
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Add ticket link</h2>
              <p className="text-sm text-[var(--muted)]">
                Completeness also needs test, release, and document links (API).
              </p>
            </CardHeader>
            <CardBody>
              <form onSubmit={onAddTicketLink} className="grid gap-3" aria-label="Add ticket link">
                <Field label="Requirement ID">
                  <Input
                    required
                    value={reqId}
                    onChange={(e) => setReqId(e.target.value)}
                    placeholder="Use a registered requirement id"
                  />
                </Field>
                <Field label="Ticket ID (optional)">
                  <Input
                    value={ticketId}
                    onChange={(e) => setTicketId(e.target.value)}
                    placeholder="Auto-generate if empty"
                  />
                </Field>
                <Button type="submit">
                  <Link2 className="h-4 w-4" />
                  Link ticket
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Evidence manifests</h2>
            </CardHeader>
            <CardBody className="shrink-0">
              <form
                onSubmit={onCreateManifest}
                className="grid gap-3 md:grid-cols-2"
                aria-label="Create manifest"
              >
                <Field label="Code">
                  <Input
                    required
                    value={manifestCode}
                    onChange={(e) => setManifestCode(e.target.value)}
                  />
                </Field>
                <Field label="Title">
                  <Input
                    required
                    value={manifestTitle}
                    onChange={(e) => setManifestTitle(e.target.value)}
                  />
                </Field>
                <div className="flex flex-wrap gap-2 md:col-span-2">
                  <Button type="submit">
                    <Plus className="h-4 w-4" />
                    Create draft
                  </Button>
                  <Button type="button" variant="outline" onClick={() => void onAddItemAndSeal()}>
                    <ShieldCheck className="h-4 w-4" />
                    Add item + seal
                  </Button>
                </div>
              </form>
            </CardBody>
            <ScrollRegion className="flex-1">
              {manifests.length === 0 ? (
                <CardBody>
                  <EmptyState title="No manifests" body="Create a draft, add items, then seal." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {manifests.map((item) => (
                    <li
                      key={item.id}
                      className="flex cursor-pointer items-center justify-between gap-3 px-5 py-3"
                      onClick={() => setSelectedManifestId(item.id)}
                    >
                      <div>
                        <p className="font-medium">
                          {item.code} · {item.item_count} items
                        </p>
                        <p className="text-xs text-[var(--muted)]">
                          {item.checksum ? `checksum ${item.checksum.slice(0, 12)}…` : "draft"} ·{" "}
                          {formatUtc(item.updated_at)}
                        </p>
                      </div>
                      <StatusBadge status={item.status} />
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>

          <Card className="flex min-h-0 flex-col overflow-hidden">
            <CardHeader className="shrink-0">
              <h2 className="font-display text-lg">Exports</h2>
              <p className="text-sm text-[var(--muted)]">
                In-DB JSON preview with reconciliation_hash matching manifest checksum.
              </p>
            </CardHeader>
            <ScrollRegion className="flex-1">
              {exports.length === 0 ? (
                <CardBody>
                  <EmptyState title="No exports" body="Seal a manifest, then export." />
                </CardBody>
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {exports.map((item) => (
                    <li key={item.id} className="flex items-center justify-between gap-3 px-5 py-3">
                      <div>
                        <p className="font-medium">
                          {item.export_format.toUpperCase()} ·{" "}
                          {item.reconciliation_hash
                            ? item.reconciliation_hash.slice(0, 12) + "…"
                            : "no hash"}
                        </p>
                        <p className="text-xs text-[var(--muted)]">{formatUtc(item.created_at)}</p>
                      </div>
                      <StatusBadge status={item.status} />
                    </li>
                  ))}
                </ul>
              )}
            </ScrollRegion>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
