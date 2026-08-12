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
  createHuman,
  createTeam,
  listHumans,
  listTeams,
  type HumanUser,
  type IdentityTeam,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function UsersDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [humans, setHumans] = useState<HumanUser[]>([]);
  const [teams, setTeams] = useState<IdentityTeam[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [showCreate, setShowCreate] = useState(false);
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [roleCode, setRoleCode] = useState("");
  const [teamCode, setTeamCode] = useState("");
  const [teamName, setTeamName] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [people, teamPage] = await Promise.all([
        listHumans(session, { limit, offset }),
        listTeams(session, { limit: 50, offset: 0 }),
      ]);
      setHumans(people.items);
      setPageMeta(people.page);
      setTeams(teamPage.items);
    } catch (err) {
      notifyApiError("Unable to load users and teams", err);
      setHumans([]);
      setTeams([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateHuman(event: FormEvent) {
    event.preventDefault();
    try {
      await createHuman(session, {
        email: email.trim(),
        full_name: fullName.trim(),
        primary_role_code: roleCode.trim() || undefined,
      });
      notifySuccess("User created");
      setEmail("");
      setFullName("");
      setRoleCode("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create user", err);
    }
  }

  async function onCreateTeam(event: FormEvent) {
    event.preventDefault();
    try {
      await createTeam(session, { code: teamCode.trim(), name: teamName.trim() });
      notifySuccess("Team created");
      setTeamCode("");
      setTeamName("");
      await load();
    } catch (err) {
      notifyApiError("Could not create team", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Users & Teams"
          description="Human users and teams in the current organization (MOD-100)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              New user or team
            </Button>
          }
        />

        {showCreate ? (
          <div className="grid shrink-0 gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create user</h2>
              </CardHeader>
              <CardBody>
                <form onSubmit={onCreateHuman} className="grid gap-4" aria-label="Create user">
                  <Field label="Full name">
                    <Input required value={fullName} onChange={(e) => setFullName(e.target.value)} />
                  </Field>
                  <Field label="Email">
                    <Input
                      required
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </Field>
                  <Field label="Primary role code">
                    <Input value={roleCode} onChange={(e) => setRoleCode(e.target.value)} />
                  </Field>
                  <Button type="submit">Create user</Button>
                </form>
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create team</h2>
              </CardHeader>
              <CardBody>
                <form onSubmit={onCreateTeam} className="grid gap-4" aria-label="Create team">
                  <Field label="Code">
                    <Input required value={teamCode} onChange={(e) => setTeamCode(e.target.value)} />
                  </Field>
                  <Field label="Name">
                    <Input required value={teamName} onChange={(e) => setTeamName(e.target.value)} />
                  </Field>
                  <Button type="submit">Create team</Button>
                </form>
              </CardBody>
            </Card>
          </div>
        ) : null}

        <ScrollRegion>
          <div className="grid gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Users</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : humans.length === 0 ? (
                  <EmptyState title="No users" body="Create a human user to start." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {humans.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.full_name}</p>
                          <p className="text-sm text-[var(--muted)]">{row.email}</p>
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
                  label="users"
                />
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Teams</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : teams.length === 0 ? (
                  <EmptyState title="No teams" body="Create a team to group actors." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {teams.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.name}</p>
                          <p className="text-sm text-[var(--muted)]">{row.code}</p>
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
