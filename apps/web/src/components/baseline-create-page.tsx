"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { useSession } from "@/components/session-provider";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, Input, Select } from "@/components/ui/field";
import { PageHeader, StatusBanner } from "@/components/ui-states";
import { createBaseline } from "@/lib/api";
import { notifyApiError } from "@/lib/toast";
import { can } from "@/lib/roles";

export function BaselineCreatePage() {
  const { session } = useSession();
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);

  if (!can(session.variant, "create")) {
    return (
      <StatusBanner kind="error">
        Your role cannot create source baselines.
      </StatusBanner>
    );
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    const form = new FormData(event.currentTarget);
    try {
      const created = await createBaseline(session, {
        baseline_key: String(form.get("baseline_key") ?? ""),
        title: String(form.get("title") ?? ""),
        artifact_path: String(form.get("artifact_path") ?? ""),
        document_version: String(form.get("document_version") ?? ""),
        classification: String(form.get("classification") ?? "internal"),
      });
      router.push(`/governance/baselines/${created.id}`);
    } catch (err) {
      notifyApiError("Create failed", err);
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <Link
          href="/governance/baselines"
          className="text-sm font-medium text-[var(--accent)] hover:underline"
        >
          Back to source baselines
        </Link>
        <PageHeader
          title="Create baseline"
          description="Register a draft source of truth. Submit it for review when the artifact is ready."
        />
      </div>

      <Card>
        <CardHeader>
          <h2 className="font-display text-lg">Baseline details</h2>
          <p className="text-sm text-[var(--muted)]">
            Keys and paths identify the document; classification controls who may work with it.
          </p>
        </CardHeader>
        <CardBody>
          <form onSubmit={onSubmit} className="grid gap-4" noValidate>
            <Field label="Baseline key">
              <Input name="baseline_key" required placeholder="BL-SRS-001" />
            </Field>
            <Field label="Title">
              <Input name="title" required placeholder="MVP SRS" />
            </Field>
            <Field label="Artifact path" hint="Repository or document path for the baseline artifact">
              <Input name="artifact_path" required placeholder="docs/srs/mvp.md" />
            </Field>
            <Field label="Document version">
              <Input name="document_version" required placeholder="v1.0" />
            </Field>
            <Field label="Classification">
              <Select name="classification" defaultValue="internal">
                <option value="public">Public</option>
                <option value="internal">Internal</option>
                <option value="confidential">Confidential</option>
                <option value="restricted">Restricted</option>
              </Select>
            </Field>
            <div className="flex justify-end gap-2">
              <Link href="/governance/baselines">
                <Button type="button" variant="ghost">
                  Cancel
                </Button>
              </Link>
              <Button type="submit" disabled={submitting}>
                {submitting ? "Creating…" : "Create draft"}
              </Button>
            </div>
          </form>
        </CardBody>
      </Card>
    </div>
  );
}
