"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";

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
  createAllocation,
  createSkill,
  listAllocations,
  listSkills,
  type CapacityAllocation,
  type CapacitySkill,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function CapacityDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [skills, setSkills] = useState<CapacitySkill[]>([]);
  const [allocations, setAllocations] = useState<CapacityAllocation[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [showCreate, setShowCreate] = useState(false);
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("general");
  const [actorId, setActorId] = useState(session.actorId);
  const [pct, setPct] = useState("40");
  const [fromDate, setFromDate] = useState("2026-08-01");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [skillPage, allocPage] = await Promise.all([
        listSkills(session, { limit, offset }),
        listAllocations(session, { limit: 50, offset: 0 }),
      ]);
      setSkills(skillPage.items);
      setPageMeta(skillPage.page);
      setAllocations(allocPage.items);
    } catch (err) {
      notifyApiError("Unable to load skills and capacity", err);
      setSkills([]);
      setAllocations([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    setActorId(session.actorId);
  }, [session.actorId]);

  async function onCreateSkill(event: FormEvent) {
    event.preventDefault();
    try {
      await createSkill(session, {
        code: code.trim(),
        title: title.trim(),
        category: category.trim() || "general",
      });
      notifySuccess("Skill created");
      setCode("");
      setTitle("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create skill", err);
    }
  }

  async function onCreateAllocation(event: FormEvent) {
    event.preventDefault();
    try {
      await createAllocation(session, {
        actor_id: actorId.trim(),
        allocation_pct: pct.trim(),
        effective_from: fromDate,
      });
      notifySuccess("Allocation created");
      await load();
    } catch (err) {
      notifyApiError("Could not create allocation", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Skills & Capacity"
          description="Org skills and actor allocation percentages (MOD-130)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New skill or allocation
            </Button>
          }
        />

        {showCreate ? (
          <div className="grid shrink-0 gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create skill</h2>
              </CardHeader>
              <CardBody>
                <form onSubmit={onCreateSkill} className="grid gap-4" aria-label="Create skill">
                  <Field label="Code">
                    <Input
                      required
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      placeholder="python"
                    />
                  </Field>
                  <Field label="Title">
                    <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                  </Field>
                  <Field label="Category">
                    <Input value={category} onChange={(e) => setCategory(e.target.value)} />
                  </Field>
                  <Button type="submit">Create skill</Button>
                </form>
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create allocation</h2>
              </CardHeader>
              <CardBody>
                <form
                  onSubmit={onCreateAllocation}
                  className="grid gap-4"
                  aria-label="Create allocation"
                >
                  <Field label="Actor id">
                    <Input required value={actorId} onChange={(e) => setActorId(e.target.value)} />
                  </Field>
                  <Field label="Allocation %">
                    <Input required value={pct} onChange={(e) => setPct(e.target.value)} />
                  </Field>
                  <Field label="Effective from">
                    <Input
                      required
                      type="date"
                      value={fromDate}
                      onChange={(e) => setFromDate(e.target.value)}
                    />
                  </Field>
                  <Button type="submit">Create allocation</Button>
                </form>
              </CardBody>
            </Card>
          </div>
        ) : null}

        <ScrollRegion>
          <div className="grid gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Skills</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : skills.length === 0 ? (
                  <EmptyState title="No skills" body="Create a skill catalog entry." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {skills.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.title}</p>
                          <p className="text-sm text-[var(--muted)]">
                            {row.code} · {row.category}
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
                  label="skills"
                />
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Allocations</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : allocations.length === 0 ? (
                  <EmptyState title="No allocations" body="Record actor capacity." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {allocations.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.allocation_pct}%</p>
                          <p className="text-sm text-[var(--muted)]">
                            Actor {row.actor_id.slice(0, 8)} · from {row.effective_from}
                          </p>
                        </div>
                        <StatusBadge status={row.status} />
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
          </div>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
