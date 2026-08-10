"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { useSession } from "@/components/session-provider";
import { StatusBanner } from "@/components/ui-states";
import { ApiError, createBaseline } from "@/lib/api";
import { can } from "@/lib/roles";

export function BaselineCreatePage() {
  const { session } = useSession();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!can(session.variant, "create")) {
    return (
      <StatusBanner kind="error">
        Your UI role cannot create baselines. Server will also reject unauthorized creates.
      </StatusBanner>
    );
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
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
      setError(err instanceof ApiError ? err.problem.message : "Create failed");
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <Link href="/governance/baselines" className="text-sm text-[var(--accent)] underline">
          Back to list
        </Link>
        <h2 className="mt-2 font-display text-3xl tracking-tight">Create baseline</h2>
      </div>
      {error ? <StatusBanner kind="error">{error}</StatusBanner> : null}
      <form
        onSubmit={onSubmit}
        className="space-y-4 rounded border border-[var(--line)] bg-white p-5"
        noValidate
      >
        <Field name="baseline_key" label="Baseline key" required placeholder="BL-SRS-001" />
        <Field name="title" label="Title" required placeholder="MVP SRS" />
        <Field
          name="artifact_path"
          label="Artifact path"
          required
          placeholder="Docs/....md"
        />
        <Field name="document_version" label="Document version" required placeholder="v1.0" />
        <label className="flex flex-col gap-1 text-sm">
          <span>Classification</span>
          <select
            name="classification"
            defaultValue="internal"
            className="rounded border border-[var(--line)] px-3 py-2"
          >
            <option value="public">public</option>
            <option value="internal">internal</option>
            <option value="confidential">confidential</option>
            <option value="restricted">restricted</option>
          </select>
        </label>
        <button
          type="submit"
          disabled={submitting}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {submitting ? "Creating…" : "Create draft"}
        </button>
      </form>
    </div>
  );
}

function Field({
  name,
  label,
  required,
  placeholder,
}: {
  name: string;
  label: string;
  required?: boolean;
  placeholder?: string;
}) {
  const id = `field-${name}`;
  return (
    <label className="flex flex-col gap-1 text-sm" htmlFor={id}>
      <span>
        {label}
        {required ? " *" : ""}
      </span>
      <input
        id={id}
        name={name}
        required={required}
        placeholder={placeholder}
        className="rounded border border-[var(--line)] px-3 py-2"
        aria-required={required}
      />
    </label>
  );
}
