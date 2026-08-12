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
  listApprovals,
  listFollowUps,
  listNotifications,
  type ApprovalRequest,
  type FollowUp,
  type Notification,
} from "@/lib/api";
import { notifyApiError } from "@/lib/toast";

export function MyWorkDeskPage() {
  const { session } = useSession();
  const [loading, setLoading] = useState(true);
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [fu, appr, ntf] = await Promise.all([
        listFollowUps(session, { status: "open", limit: 20, offset: 0 }),
        listApprovals(session, { status: "pending", limit: 20, offset: 0 }),
        listNotifications(session, {
          recipient_actor_id: session.actorId,
          limit: 20,
          offset: 0,
        }),
      ]);
      const mine = fu.items.filter(
        (row) =>
          row.recipient_actor_id === session.actorId || row.owner_actor_id === session.actorId,
      );
      setFollowUps(mine);
      setApprovals(appr.items);
      setNotifications(ntf.items);
    } catch (err) {
      notifyApiError("Unable to load my work", err);
      setFollowUps([]);
      setApprovals([]);
      setNotifications([]);
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
          title="My Work"
          description="Open follow-ups you own or receive, pending approvals, and your notifications."
        />
        <ScrollRegion>
          <div className="grid gap-4 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <h2 className="font-display text-lg">
                  <Link href="/follow-ups" className="hover:underline">
                    Follow-ups
                  </Link>
                </h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : followUps.length === 0 ? (
                  <EmptyState title="No open follow-ups" body="Nothing assigned to you." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {followUps.map((row) => (
                      <li key={row.id} className="py-2">
                        <p className="font-medium">{row.title}</p>
                        <p className="text-sm text-[var(--muted)]">Due {formatUtc(row.due_at)}</p>
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
                  <Link href="/approvals" className="hover:underline">
                    Pending approvals
                  </Link>
                </h2>
              </CardHeader>
              <CardBody>
                {loading ? (
                  <SkeletonRows />
                ) : approvals.length === 0 ? (
                  <EmptyState title="No pending approvals" body="Queue is clear." />
                ) : (
                  <ul className="divide-y divide-[var(--line)]">
                    {approvals.map((row) => (
                      <li key={row.id} className="py-2">
                        <p className="font-medium">{row.title}</p>
                        <p className="text-sm text-[var(--muted)]">{row.action_code}</p>
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
          </div>
        </ScrollRegion>
      </div>
    </AppShell>
  );
}
