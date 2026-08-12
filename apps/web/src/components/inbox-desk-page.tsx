"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

import { AppShell } from "@/components/app-shell";
import { ScrollRegion } from "@/components/page-shell";
import { useSession } from "@/components/session-provider";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { EmptyState, PageHeader, SkeletonRows } from "@/components/ui-states";
import {
  formatUtc,
  listGmailMessages,
  listNotifications,
  listQueries,
  type ClientQuery,
  type GmailMessageMapping,
  type Notification,
} from "@/lib/api";
import { notifyApiError } from "@/lib/toast";

export function InboxDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [messages, setMessages] = useState<GmailMessageMapping[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [queryPage, ntf, gmail] = await Promise.all([
        listQueries(session, { limit: 20, offset: 0 }),
        listNotifications(session, {
          recipient_actor_id: session.actorId,
          limit: 20,
          offset: 0,
        }),
        listGmailMessages(session, { limit: 20, offset: 0 }).catch(() => ({
          items: [] as GmailMessageMapping[],
        })),
      ]);
      setQueries(queryPage.items);
      setNotifications(ntf.items);
      setMessages(gmail.items);
    } catch (err) {
      notifyApiError("Unable to load inbox", err);
      setQueries([]);
      setNotifications([]);
      setMessages([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <AppShell>
      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden p-4 md:p-6">
        <PageHeader
          title="Inbox"
          description="Recent queries, in-app notifications, and mapped Gmail messages."
        />
        <ScrollRegion>
          <div className="grid gap-4 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">
                  <Link href="/queries" className="hover:underline">
                    Queries
                  </Link>
                </h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : queries.length === 0 ? (
                  <EmptyState title="No queries" body="Inbound client queries appear here." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {queries.map((row) => (
                      <li key={row.id} className="py-2">
                        <p className="font-medium">{row.subject}</p>
                        <p className="text-sm text-[var(--muted)]">{formatUtc(row.created_at)}</p>
                        <StatusBadge status={row.status} />
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">
                  <Link href="/notifications" className="hover:underline">
                    Notifications
                  </Link>
                </h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : notifications.length === 0 ? (
                  <EmptyState title="No notifications" body="Nothing for this actor." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {notifications.map((row) => (
                      <li key={row.id} className="py-2">
                        <p className="font-medium">{row.title}</p>
                        <p className="text-sm text-[var(--muted)]">{row.body}</p>
                        <StatusBadge status={row.status} />
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">
                  <Link href="/gmail" className="hover:underline">
                    Gmail
                  </Link>
                </h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : messages.length === 0 ? (
                  <EmptyState
                    title="No mapped messages"
                    body="Connect Gmail to see mapped mail here."
                  />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {messages.map((row) => (
                      <li key={row.id} className="py-2">
                        <p className="font-medium">{row.subject ?? "(no subject)"}</p>
                        <p className="text-sm text-[var(--muted)]">
                          {row.direction} · {formatUtc(row.created_at)}
                        </p>
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
