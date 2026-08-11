"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";

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
  activateKnowledgeVersion,
  createKnowledgeItem,
  createKnowledgeVersion,
  formatUtc,
  listKnowledgeItems,
  searchKnowledge,
  type KnowledgeCitation,
  type KnowledgeItem,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";
import { getWorkspaceProjectId } from "@/lib/workspace";

export function KnowledgeDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [projectId, setProjectId] = useState("");

  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<KnowledgeCitation[]>([]);
  const [searching, setSearching] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listKnowledgeItems(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load knowledge items", err);
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
      const item = await createKnowledgeItem(session, {
        code: code.trim(),
        title: title.trim(),
        project_id: projectId.trim() || undefined,
      });
      const version = await createKnowledgeVersion(session, item.id, {
        body_text: body.trim() || title.trim(),
      });
      await activateKnowledgeVersion(session, version.id);
      notifySuccess("Knowledge item published");
      setShowCreate(false);
      setCode("");
      setTitle("");
      setBody("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not publish knowledge item", err);
    }
  }

  async function onSearch(event: FormEvent) {
    event.preventDefault();
    setSearching(true);
    try {
      const result = await searchKnowledge(session, {
        query: query.trim(),
        project_id: projectId.trim() || undefined,
        limit: 10,
      });
      setHits(result.items);
      if (result.items.length === 0) {
        notifySuccess("No cited hits for that query");
      }
    } catch (err) {
      notifyApiError("Knowledge search failed", err);
      setHits([]);
    } finally {
      setSearching(false);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Knowledge"
          description="Approved, versioned knowledge with stub retrieval and source citations (MOD-370). No live embedding model in M1."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Publish item
            </Button>
          }
        />

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Publish knowledge item</h2>
              <p className="text-sm text-[var(--muted)]">
                Creates item + version and activates it (chunks + stub embeddings).
              </p>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Publish knowledge">
                <Field label="Code">
                  <Input required value={code} onChange={(e) => setCode(e.target.value)} placeholder="policy_change" />
                </Field>
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Project id (optional — project knowledge outranks org-generic)">
                  <Input value={projectId} onChange={(e) => setProjectId(e.target.value)} placeholder="Optional project UUID" />
                </Field>
                <Field label="Body">
                  <Textarea required rows={4} value={body} onChange={(e) => setBody(e.target.value)} />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Publish</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <Card className="shrink-0">
          <CardHeader>
            <h2 className="font-display text-lg">Stub search</h2>
          </CardHeader>
          <CardBody>
            <form onSubmit={onSearch} className="flex flex-wrap items-end gap-3" aria-label="Search knowledge">
              <Field label="Query">
                <Input required value={query} onChange={(e) => setQuery(e.target.value)} placeholder="scope changes approval" className="min-w-[16rem]" />
              </Field>
              <Button type="submit" disabled={searching}>
                <Search className="h-4 w-4" />
                Search
              </Button>
            </form>
            {hits.length > 0 ? (
              <ul className="mt-4 divide-y divide-[var(--line)]">
                {hits.map((hit) => (
                  <li key={hit.chunk_id} className="py-2">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-medium">{hit.item_title}</span>
                      <span className="text-xs text-[var(--muted)]">score {hit.score.toFixed(2)}</span>
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">{hit.source_citation}</p>
                    <p className="mt-1 text-sm">{hit.content_text.slice(0, 180)}{hit.content_text.length > 180 ? "…" : ""}</p>
                  </li>
                ))}
              </ul>
            ) : null}
          </CardBody>
        </Card>

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Knowledge items</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/knowledge/items`.</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No knowledge items"
                body="Publish an approved version to make content retrievable."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    Publish item
                  </Button>
                }
              />
            </CardBody>
          ) : (
            <ScrollRegion className="flex-1">
              <ul className="divide-y divide-[var(--line)]">
                {items.map((item) => (
                  <li key={item.id} className="px-5 py-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <span className="font-medium">{item.title}</span>
                        <p className="text-xs text-[var(--muted)]">{item.code}</p>
                      </div>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {item.project_id ? `project ${item.project_id.slice(0, 8)}…` : "org-generic"} ·{" "}
                      {formatUtc(item.updated_at)}
                    </p>
                  </li>
                ))}
              </ul>
            </ScrollRegion>
          )}
          {!loading && (items.length > 0 || pageMeta.total > 0) ? (
            <div className="shrink-0">
              <ListPagination page={pageMeta} onOffsetChange={setOffset} onLimitChange={setLimit} label="items" />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
