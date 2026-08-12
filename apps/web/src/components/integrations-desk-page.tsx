"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Activity, Inbox, Plus, RefreshCw, Webhook } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  activateIntegrationConnection,
  createIntegrationConnection,
  formatUtc,
  getConnectionHealth,
  listIntegrationConnections,
  processInboxEvent,
  receiveInboxEvent,
  receiveIntegrationWebhook,
  type ConnectionHealth,
  type InboxEvent,
  type IntegrationConnection,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function IntegrationsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [connections, setConnections] = useState<IntegrationConnection[]>([]);
  const [healthByConn, setHealthByConn] = useState<Record<string, ConnectionHealth>>({});

  const [code, setCode] = useState("gh-main");
  const [provider, setProvider] = useState("github");
  const [authType, setAuthType] = useState("oauth2");

  const [selectedConnId, setSelectedConnId] = useState("");
  const [webhookEventId, setWebhookEventId] = useState("wh-sim-1");
  const [inboxEventId, setInboxEventId] = useState("inbox-sim-1");
  const [externalEntityId, setExternalEntityId] = useState("EXT-001");
  const [recentInbox, setRecentInbox] = useState<InboxEvent[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const listed = await listIntegrationConnections(session, { limit: 20 });
      setConnections(listed.items);
      if (listed.items.length > 0 && !selectedConnId) {
        setSelectedConnId(listed.items[0].id);
      }
      const healthEntries = await Promise.allSettled(
        listed.items.map(async (conn) => {
          try {
            const health = await getConnectionHealth(session, conn.id);
            return [conn.id, health] as const;
          } catch {
            return [conn.id, null] as const;
          }
        }),
      );
      const map: Record<string, ConnectionHealth> = {};
      for (const entry of healthEntries) {
        if (entry.status === "fulfilled" && entry.value[1]) {
          map[entry.value[0]] = entry.value[1];
        }
      }
      setHealthByConn(map);
    } catch (err) {
      notifyApiError("Unable to load integrations", err);
    } finally {
      setLoading(false);
    }
  }, [session, selectedConnId]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateConnection(event: FormEvent) {
    event.preventDefault();
    try {
      const created = await createIntegrationConnection(session, {
        code: code.trim(),
        provider,
        auth_type: authType,
      });
      if (created.status === "draft") {
        await activateIntegrationConnection(session, created.id);
      }
      notifySuccess(`Connection ${created.code} created`);
      setCode(`${provider}-${connections.length + 2}`);
      await load();
    } catch (err) {
      notifyApiError("Could not create connection", err);
    }
  }

  async function onSimulateWebhook(event: FormEvent) {
    event.preventDefault();
    if (!selectedConnId) {
      notifyApiError("Select a connection", new Error("missing connection"));
      return;
    }
    try {
      await receiveIntegrationWebhook(session, {
        connection_id: selectedConnId,
        external_event_id: webhookEventId.trim(),
        event_type: "push",
        payload: { simulated: true },
      });
      notifySuccess("Webhook received");
      setWebhookEventId(`wh-sim-${Date.now()}`);
      await load();
    } catch (err) {
      notifyApiError("Webhook receive failed", err);
    }
  }

  async function onSimulateInbox(event: FormEvent) {
    event.preventDefault();
    if (!selectedConnId) {
      notifyApiError("Select a connection", new Error("missing connection"));
      return;
    }
    try {
      const received = await receiveInboxEvent(session, {
        connection_id: selectedConnId,
        external_event_id: inboxEventId.trim(),
        event_type: "entity.sync",
        payload: {
          internal_entity_type: "ticket",
          internal_entity_id: crypto.randomUUID(),
          external_entity_type: "issue",
          external_entity_id: externalEntityId.trim(),
        },
      });
      setRecentInbox((prev) => [received, ...prev].slice(0, 5));
      notifySuccess("Inbox event queued");
      setInboxEventId(`inbox-sim-${Date.now()}`);
    } catch (err) {
      notifyApiError("Inbox receive failed", err);
    }
  }

  async function onProcessInbox(inboxId: string, forceFail: boolean) {
    try {
      const processed = await processInboxEvent(session, inboxId, { force_fail: forceFail });
      notifySuccess(`Inbox ${processed.status}`);
      await load();
    } catch (err) {
      notifyApiError("Inbox process failed", err);
    }
  }

  return (
    <AppShell>
      <ScrollRegion>
        <PageHeader
          title="Integrations"
          description="OAuth connections, webhooks, inbox processing, and connection health (M1 simulated relay)."
          actions={
            <Button variant="secondary" size="sm" onClick={() => void load()}>
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
          }
        />

        <div className="grid gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader title="Create connection" />
            <CardBody>
              <form className="space-y-3" onSubmit={onCreateConnection}>
                <Field label="Code">
                  <Input value={code} onChange={(e) => setCode(e.target.value)} required />
                </Field>
                <Field label="Provider">
                  <Select value={provider} onChange={(e) => setProvider(e.target.value)}>
                    <option value="github">GitHub</option>
                    <option value="jira">Jira</option>
                    <option value="slack">Slack</option>
                    <option value="custom">Custom</option>
                  </Select>
                </Field>
                <Field label="Auth type">
                  <Select value={authType} onChange={(e) => setAuthType(e.target.value)}>
                    <option value="oauth2">OAuth2</option>
                    <option value="api_key">API key</option>
                    <option value="none">None</option>
                  </Select>
                </Field>
                <p className="text-xs text-muted-foreground">
                  credential_ref is generated automatically (secrets/oauth/…); raw secrets are rejected.
                </p>
                <Button type="submit">
                  <Plus className="h-4 w-4" />
                  Create &amp; activate
                </Button>
              </form>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Simulate webhook &amp; inbox" />
            <CardBody className="space-y-4">
              <Field label="Connection">
                <Select
                  value={selectedConnId}
                  onChange={(e) => setSelectedConnId(e.target.value)}
                >
                  <option value="">Select…</option>
                  {connections.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.code} ({c.provider})
                    </option>
                  ))}
                </Select>
              </Field>
              <form className="space-y-2" onSubmit={onSimulateWebhook}>
                <Field label="Webhook external event id">
                  <Input
                    value={webhookEventId}
                    onChange={(e) => setWebhookEventId(e.target.value)}
                  />
                </Field>
                <Button type="submit" variant="secondary" size="sm">
                  <Webhook className="h-4 w-4" />
                  Receive webhook
                </Button>
              </form>
              <form className="space-y-2 border-t pt-3" onSubmit={onSimulateInbox}>
                <Field label="Inbox external event id">
                  <Input value={inboxEventId} onChange={(e) => setInboxEventId(e.target.value)} />
                </Field>
                <Field label="External entity id">
                  <Input
                    value={externalEntityId}
                    onChange={(e) => setExternalEntityId(e.target.value)}
                  />
                </Field>
                <Button type="submit" variant="secondary" size="sm">
                  <Inbox className="h-4 w-4" />
                  Receive inbox
                </Button>
              </form>
            </CardBody>
          </Card>
        </div>

        <Card className="mt-4">
          <CardHeader title="Connections &amp; health" />
          <CardBody>
            {loading ? (
              <SkeletonRows rows={4} />
            ) : connections.length === 0 ? (
              <EmptyState
                title="No connections"
                body="Create a connection to start simulating webhooks and inbox processing."
              />
            ) : (
              <ul className="divide-y">
                {connections.map((conn) => {
                  const health = healthByConn[conn.id];
                  return (
                    <li key={conn.id} className="flex flex-wrap items-center gap-3 py-3">
                      <div className="min-w-0 flex-1">
                        <p className="font-medium">{conn.code}</p>
                        <p className="text-xs text-muted-foreground">
                          {conn.provider} · {conn.auth_type} · ref {conn.credential_ref}
                        </p>
                      </div>
                      <StatusBadge status={conn.status} />
                      {health ? (
                        <span className="flex items-center gap-1 text-xs">
                          <Activity className="h-3 w-3" />
                          {health.health_status}
                          {health.last_failure_at ? (
                            <span className="text-muted-foreground">
                              fail {formatUtc(health.last_failure_at)}
                            </span>
                          ) : null}
                        </span>
                      ) : (
                        <span className="text-xs text-muted-foreground">No health record</span>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </CardBody>
        </Card>

        {recentInbox.length > 0 ? (
          <Card className="mt-4">
            <CardHeader title="Recent inbox (process)" />
            <CardBody>
              <ul className="space-y-2">
                {recentInbox.map((item) => (
                  <li
                    key={item.id}
                    className="flex flex-wrap items-center gap-2 rounded border p-2 text-sm"
                  >
                    <span className="font-mono text-xs">{item.external_event_id}</span>
                    <StatusBadge status={item.status} />
                    {item.status === "pending" ? (
                      <>
                        <Button
                          size="sm"
                          variant="secondary"
                          onClick={() => void onProcessInbox(item.id, false)}
                        >
                          Process OK
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => void onProcessInbox(item.id, true)}
                        >
                          Force fail
                        </Button>
                      </>
                    ) : null}
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>
        ) : null}
      </ScrollRegion>
    </AppShell>
  );
}
