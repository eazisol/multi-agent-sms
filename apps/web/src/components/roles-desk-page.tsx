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
  createPermission,
  createRole,
  grantRolePermission,
  listPermissions,
  listRoles,
  type AccessPermission,
  type IdentityRole,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function RolesDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [roles, setRoles] = useState<IdentityRole[]>([]);
  const [permissions, setPermissions] = useState<AccessPermission[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [showCreate, setShowCreate] = useState(false);
  const [code, setCode] = useState("");
  const [title, setTitle] = useState("");
  const [permCode, setPermCode] = useState("");
  const [moduleKey, setModuleKey] = useState("identity");
  const [actionKey, setActionKey] = useState("read");
  const [permTitle, setPermTitle] = useState("");
  const [grantRoleId, setGrantRoleId] = useState("");
  const [grantPermId, setGrantPermId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [rolePage, perms] = await Promise.all([
        listRoles(session, { limit, offset }),
        listPermissions(session),
      ]);
      setRoles(rolePage.items);
      setPageMeta(rolePage.page);
      setPermissions(perms);
      setGrantRoleId((prev) => prev || rolePage.items[0]?.id || "");
      setGrantPermId((prev) => prev || perms[0]?.id || "");
    } catch (err) {
      notifyApiError("Unable to load roles and permissions", err);
      setRoles([]);
      setPermissions([]);
      setPageMeta(EMPTY_PAGE_META);
    } finally {
      setLoading(false);
    }
  }, [session, limit, offset]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateRole(event: FormEvent) {
    event.preventDefault();
    try {
      await createRole(session, { code: code.trim(), title: title.trim() });
      notifySuccess("Role created");
      setCode("");
      setTitle("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create role", err);
    }
  }

  async function onCreatePermission(event: FormEvent) {
    event.preventDefault();
    try {
      await createPermission(session, {
        code: permCode.trim(),
        module_key: moduleKey.trim(),
        action_key: actionKey.trim(),
        title: permTitle.trim(),
      });
      notifySuccess("Permission created");
      setPermCode("");
      setPermTitle("");
      await load();
    } catch (err) {
      notifyApiError("Could not create permission", err);
    }
  }

  async function onGrant(event: FormEvent) {
    event.preventDefault();
    try {
      await grantRolePermission(session, {
        role_id: grantRoleId,
        permission_id: grantPermId,
      });
      notifySuccess("Permission granted to role");
    } catch (err) {
      notifyApiError("Could not grant permission", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Roles & Permissions"
          description="Identity roles and access-control permissions (MOD-100 / MOD-120)."
          actions={
            <Button type="button" onClick={() => setShowCreate((v) => !v)}>
              <Plus className="h-4 w-4" />
              Manage
            </Button>
          }
        />

        {showCreate ? (
          <div className="grid shrink-0 gap-4 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create role</h2>
              </CardHeader>
              <CardBody>
                <form onSubmit={onCreateRole} className="grid gap-4" aria-label="Create role">
                  <Field label="Code">
                    <Input required value={code} onChange={(e) => setCode(e.target.value)} />
                  </Field>
                  <Field label="Title">
                    <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                  </Field>
                  <Button type="submit">Create role</Button>
                </form>
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Create permission</h2>
              </CardHeader>
              <CardBody>
                <form
                  onSubmit={onCreatePermission}
                  className="grid gap-4"
                  aria-label="Create permission"
                >
                  <Field label="Code">
                    <Input
                      required
                      value={permCode}
                      onChange={(e) => setPermCode(e.target.value)}
                      placeholder="identity.read"
                    />
                  </Field>
                  <Field label="Module key">
                    <Input required value={moduleKey} onChange={(e) => setModuleKey(e.target.value)} />
                  </Field>
                  <Field label="Action key">
                    <Input required value={actionKey} onChange={(e) => setActionKey(e.target.value)} />
                  </Field>
                  <Field label="Title">
                    <Input required value={permTitle} onChange={(e) => setPermTitle(e.target.value)} />
                  </Field>
                  <Button type="submit">Create permission</Button>
                </form>
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Grant permission</h2>
              </CardHeader>
              <CardBody>
                <form onSubmit={onGrant} className="grid gap-4" aria-label="Grant permission">
                  <Field label="Role">
                    <Select value={grantRoleId} onChange={(e) => setGrantRoleId(e.target.value)}>
                      {roles.map((row) => (
                        <option key={row.id} value={row.id}>
                          {row.code}
                        </option>
                      ))}
                    </Select>
                  </Field>
                  <Field label="Permission">
                    <Select value={grantPermId} onChange={(e) => setGrantPermId(e.target.value)}>
                      {permissions.map((row) => (
                        <option key={row.id} value={row.id}>
                          {row.code}
                        </option>
                      ))}
                    </Select>
                  </Field>
                  <Button type="submit" disabled={!grantRoleId || !grantPermId}>
                    Grant
                  </Button>
                </form>
              </CardBody>
            </Card>
          </div>
        ) : null}

        <ScrollRegion>
          <div className="grid gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Roles</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : roles.length === 0 ? (
                  <EmptyState title="No roles" body="Create a role definition." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {roles.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.title}</p>
                          <p className="text-sm text-[var(--muted)]">{row.code}</p>
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
                  label="roles"
                />
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">Permissions</h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : permissions.length === 0 ? (
                  <EmptyState title="No permissions" body="Create a permission code." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {permissions.map((row) => (
                      <li key={row.id} className="flex items-center justify-between gap-3 py-2">
                        <div>
                          <p className="font-medium">{row.title}</p>
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
