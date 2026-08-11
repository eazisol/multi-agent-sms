"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Rocket } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ListPagination } from "@/components/list-pagination";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  EMPTY_PAGE_META,
  approveRelease,
  createRelease,
  formatUtc,
  listReleases,
  submitRelease,
  type PageMeta,
  type Release,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function ReleasesDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<Release[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [versionLabel, setVersionLabel] = useState("1.0.0");
  const [reqId, setReqId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listReleases(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load releases", err);
      setItems([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      const linked = reqId.trim() || crypto.randomUUID();
      const created = await createRelease(session, {
        code: code.trim(),
        title: title.trim(),
        version_label: versionLabel.trim() || "1.0.0",
        items: [
          { link_type: "requirement", linked_entity_id: linked },
          { link_type: "ticket", linked_entity_id: crypto.randomUUID() },
          { link_type: "test_case", linked_entity_id: crypto.randomUUID() },
          { link_type: "bug", linked_entity_id: crypto.randomUUID() },
          { link_type: "change_request", linked_entity_id: crypto.randomUUID() },
          { link_type: "document", linked_entity_id: crypto.randomUUID() },
        ],
      });
      await submitRelease(session, created.id, created.version);
      notifySuccess("Release submitted for production approval");
      setShowCreate(false);
      setCode("");
      setTitle("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create release", err);
    }
  }

  async function onApprove(item: Release) {
    try {
      await approveRelease(session, item.id, {
        evidence: "Desk production approval",
        expected_version: item.version,
      });
      notifySuccess("Release approved for production");
      await load();
    } catch (err) {
      notifyApiError("Could not approve release", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Releases"
          description="Package, approve, deploy, and close releases with full traceability (MOD-430)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New release
            </Button>
          }
        />

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create release package</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create release">
                <Field label="Code">
                  <Input required value={code} onChange={(e) => setCode(e.target.value)} placeholder="REL-1.0.0" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Version label">
                  <Input value={versionLabel} onChange={(e) => setVersionLabel(e.target.value)} />
                </Field>
                <Field label="Requirement id (optional)">
                  <Input value={reqId} onChange={(e) => setReqId(e.target.value)} placeholder="UUID" />
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
            <h2 className="font-display text-lg">Releases</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/releases`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No releases"
                body="Create a traced package before production can be approved."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    New release
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
                        {item.code} · {item.version_label} · {formatUtc(item.updated_at)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={item.status} />
                      {item.status === "ready_for_approval" ? (
                        <Button type="button" variant="ghost" onClick={() => void onApprove(item)}>
                          <Rocket className="h-4 w-4" />
                          Approve prod
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
              <ListPagination page={pageMeta} onOffsetChange={setOffset} onLimitChange={setLimit} label="releases" />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
