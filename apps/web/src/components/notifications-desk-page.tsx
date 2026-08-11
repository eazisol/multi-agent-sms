"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { Bell, Check, Plus, RotateCcw, XCircle } from "lucide-react";

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
  createNotification,
  deliverNotification,
  formatUtc,
  listNotifications,
  markNotificationRead,
  retryNotification,
  upsertNotificationPreference,
  type Notification,
  type PageMeta,
} from "@/lib/api";
import { notifyApiError, notifySuccess } from "@/lib/toast";

export function NotificationsDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [items, setItems] = useState<Notification[]>([]);
  const [pageMeta, setPageMeta] = useState<PageMeta>(EMPTY_PAGE_META);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [channel, setChannel] = useState("in_app");
  const [notificationType, setNotificationType] = useState("assignment");
  const [priority, setPriority] = useState("normal");
  const [recipient, setRecipient] = useState(session.actorId);
  const [muteReminderEmail, setMuteReminderEmail] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await listNotifications(session, { limit, offset });
      setItems(result.items);
      setPageMeta(result.page);
    } catch (err) {
      notifyApiError("Unable to load notifications", err);
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
    setRecipient(session.actorId);
  }, [session.actorId]);

  async function onCreate(event: FormEvent) {
    event.preventDefault();
    try {
      await createNotification(session, {
        title: title.trim(),
        body: body.trim(),
        channel,
        notification_type: notificationType,
        priority,
        recipient_actor_id: recipient.trim() || session.actorId,
      });
      notifySuccess("Notification created");
      setShowCreate(false);
      setTitle("");
      setBody("");
      setOffset(0);
      await load();
    } catch (err) {
      notifyApiError("Could not create notification", err);
    }
  }

  async function onMutePref() {
    try {
      await upsertNotificationPreference(session, {
        actor_id: session.actorId,
        channel: "email",
        notification_type: "reminder",
        enabled: !muteReminderEmail,
      });
      setMuteReminderEmail(!muteReminderEmail);
      notifySuccess(
        muteReminderEmail ? "Reminder email unmuted" : "Reminder email muted (critical/system_alert cannot mute)",
      );
    } catch (err) {
      notifyApiError("Could not update preference", err);
    }
  }

  async function onMarkRead(item: Notification) {
    try {
      await markNotificationRead(session, item.id, item.version);
      notifySuccess("Marked read");
      await load();
    } catch (err) {
      notifyApiError("Could not mark read", err);
    }
  }

  async function onDeliver(item: Notification, succeed: boolean) {
    try {
      await deliverNotification(session, item.id, {
        succeed,
        error_message: succeed ? undefined : "Simulated delivery failure",
      });
      notifySuccess(succeed ? "Delivered (simulated)" : "Delivery failed (simulated)");
      await load();
    } catch (err) {
      notifyApiError("Could not simulate delivery", err);
    }
  }

  async function onRetry(item: Notification) {
    try {
      await retryNotification(session, item.id);
      notifySuccess("Retry scheduled");
      await load();
    } catch (err) {
      notifyApiError("Could not retry", err);
    }
  }

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Notifications"
          description="Org-scoped notifications with preferences, simulated delivery, DLQ recovery (MOD-440)."
          actions={
            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="ghost" onClick={() => void onMutePref()}>
                {muteReminderEmail ? "Unmute reminder email" : "Mute reminder email"}
              </Button>
              <Button type="button" onClick={() => setShowCreate((v) => !v)}>
                <Plus className="h-4 w-4" />
                New notification
              </Button>
            </div>
          }
        />

        <p className="shrink-0 text-sm text-[var(--muted)]">
          Preferences can mute non-critical types; critical priority and system_alert cannot be disabled.
        </p>

        {showCreate ? (
          <Card className="shrink-0">
            <CardHeader>
              <h2 className="font-display text-lg">Create notification</h2>
            </CardHeader>
            <CardBody>
              <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2" aria-label="Create notification">
                <Field label="Title">
                  <Input required value={title} onChange={(e) => setTitle(e.target.value)} />
                </Field>
                <Field label="Recipient actor id">
                  <Input required value={recipient} onChange={(e) => setRecipient(e.target.value)} />
                </Field>
                <Field label="Body" className="md:col-span-2">
                  <Input required value={body} onChange={(e) => setBody(e.target.value)} />
                </Field>
                <Field label="Channel">
                  <Input value={channel} onChange={(e) => setChannel(e.target.value)} placeholder="in_app | email" />
                </Field>
                <Field label="Type">
                  <Input
                    value={notificationType}
                    onChange={(e) => setNotificationType(e.target.value)}
                    placeholder="assignment"
                  />
                </Field>
                <Field label="Priority">
                  <Input value={priority} onChange={(e) => setPriority(e.target.value)} placeholder="normal" />
                </Field>
                <div className="flex justify-end gap-2 md:col-span-2">
                  <Button type="button" variant="ghost" onClick={() => setShowCreate(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create</Button>
                </div>
              </form>
            </CardBody>
          </Card>
        ) : null}

        <Card className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0">
            <h2 className="font-display text-lg">Inbox</h2>
            <p className="text-sm text-[var(--muted)]">From `/api/v1/notifications` (local-sim delivery only).</p>
          </CardHeader>
          {loading ? (
            <SkeletonRows />
          ) : items.length === 0 ? (
            <CardBody>
              <EmptyState
                title="No notifications"
                body="Create a notification to exercise delivery and recovery."
                action={
                  <Button type="button" onClick={() => setShowCreate(true)}>
                    New notification
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
                        {item.notification_type} · {item.channel} · {item.priority} · retries{" "}
                        {item.retry_count} · {formatUtc(item.updated_at)}
                      </p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                      <StatusBadge status={item.status} />
                      {item.status === "delivered" || item.status === "sent" ? (
                        <Button type="button" variant="ghost" onClick={() => void onMarkRead(item)}>
                          <Check className="h-4 w-4" />
                          Mark read
                        </Button>
                      ) : null}
                      {item.status === "pending" || item.status === "queued" || item.status === "failed" ? (
                        <>
                          <Button type="button" variant="ghost" onClick={() => void onDeliver(item, true)}>
                            <Bell className="h-4 w-4" />
                            Deliver OK
                          </Button>
                          <Button type="button" variant="ghost" onClick={() => void onDeliver(item, false)}>
                            <XCircle className="h-4 w-4" />
                            Deliver fail
                          </Button>
                        </>
                      ) : null}
                      {item.status === "failed" ? (
                        <Button type="button" variant="ghost" onClick={() => void onRetry(item)}>
                          <RotateCcw className="h-4 w-4" />
                          Retry
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
              <ListPagination
                page={pageMeta}
                onOffsetChange={setOffset}
                onLimitChange={setLimit}
                label="notifications"
              />
            </div>
          ) : null}
        </Card>
      </div>
    </AppShell>
  );
}
