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
  formatUtc,
  listDeployments,
  listReleases,
  startDeployment,
  type Deployment,
  type PageMeta,
  type Release,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function DeploymentsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Deployment[]>([]);
  const [releases, setReleases] = useState<Release[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [status, setStatus] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [releaseId, setReleaseId] = useState("");
  const [environment, setEnvironment] = useState("staging");
  const [buildRef, setBuildRef] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [deploys, releasePage] = await Promise.all([
        listDeployments(session, { status: status || undefined, limit, offset }),
        listReleases(session, { limit: 50, offset: 0 }),
      ]);
      setItems(deploys.items);
      setPageMeta(deploys.page);
      setReleases(releasePage.items);
      setReleaseId((prev) => prev || releasePage.items[0]?.id || "");
    } catch (err) {
      notifyApiError("Unable to load deployments", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, status, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onStart(event: FormEvent) {
    event.preventDefault();
    const release = releases.find((row) => row.id === releaseId);
    try {
      await startDeployment(session, releaseId, {
        environment_code: environment,
        build_ref: buildRef.trim() || undefined,
        expected_version: release?.version,
      });
      notifySuccess("Deployment requested");
      setShowCreate(false);
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not start deployment", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Deployments"
          description="Org-wide release deployments. Production still requires approval and backup (MOD-430)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Start deployment
            </Button>
          }
        />

        <div className="flex shrink-0 gap-2">
          <Select value={status} onChange={(e) => { setStatus(e.target.value); setOffset(0); }}>
            <option value="">All statuses</option>
            <option value="requested">requested</option>
            <option value="succeeded">succeeded</option>
            <option value="failed">failed</option>
          </Select>
        </div>

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Start deployment</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onStart} className="grid gap-4 md:grid-cols-2" aria-label="Start deployment">
                <Field label="Release">
                  <Select required value={releaseId} onChange={(e) => setReleaseId(e.target.value)}>
                    {releases.length === 0 ? (
                      <option value="">No releases</option>
                    ) : (
                      releases.map((row) => (
                        <option key={row.id} value={row.id}>
                          {row.code} · {row.status}
                        </option>
                      ))
                    )}
                  </Select>
                </Field>
                <Field label="Environment">
                  <Select value={environment} onChange={(e) => setEnvironment(e.target.value)}>
                    <option value="staging">staging</option>
                    <option value="production">production</option>
                  </Select>
                </Field>
                <Field label="Build ref">
                  <Input value={buildRef} onChange={(e) => setBuildRef(e.target.value)} />
                </Field>
                <Button type="submit" disabled={!releaseId}>
                  Start
                </Button>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <ScrollRegion>
          <Card>
            <CardBody>
              {loading ? (
                <SkeletonRows />
              ) : items.length === 0 ? (
                <EmptyState
                  title="No deployments"
                  body="Start a deployment against an existing release."
                />
              ) : (
                <ul className="divide-y divide-[var(--line)]">
                  {items.map((row) => (
                    <li key={row.id} className="flex items-center justify-between gap-3 py-3">
                      <div>
                        <p className="font-medium">{row.environment_code}</p>
                        <p className="text-sm text-[var(--muted)]">
                          Release {row.release_id.slice(0, 8)} · {formatUtc(row.created_at)}
                          {row.build_ref ? ` · ${row.build_ref}` : ""}
                        </p>
                      </div>
                      <StatusBadge status={row.status} />
                    </li>
                  ))}
                </ul>
              )}
              <ListPagination
                page={pageMeta}
                onOffsetChange={setOffset}
                onLimitChange={setLimit}
                label="deployments"
              />
            </CardBody>
          </Card>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
