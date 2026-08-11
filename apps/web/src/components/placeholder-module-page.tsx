"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card, CardBody } from "@/components/ui/card";
import { PageHeader, EmptyState } from "@/components/ui-states";

export function PlaceholderModulePage({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <AppShell title={title}>
      <PageHeader
        title={title}
        description={description}
      />
      <EmptyState
        icon="✦"
        title={`${title} is coming next`}
        body="This workspace is on the product roadmap. Core delivery modules are live today — Clients, Queries, Projects, Requirements, Roadmaps, Tickets, Documents, and Messages."
        action={
          <Link href="/">
            <Button>Back to Dashboard</Button>
          </Link>
        }
        secondaryAction={
          <Button variant="ai">
            <Sparkles className="h-4 w-4" />
            Ask AI what to open
          </Button>
        }
      />
      <Card className="mt-6">
        <CardBody className="text-sm text-[var(--muted)]">
          When this module ships it will follow the same Design System: sidebar navigation,
          searchable tables, status badges, and contextual AI actions — without raw IDs or
          developer tooling in the main experience.
        </CardBody>
      </Card>
    </AppShell>
  );
}
