import type { ActorKind, GovVariant } from "@/lib/roles";

export type SessionState = {
  organizationId: string;
  actorId: string;
  actorKind: ActorKind;
  variant: GovVariant;
};

export type ProblemDetails = {
  code: string;
  message: string;
  correlation_id?: string | null;
  details?: Array<Record<string, unknown>> | null;
};

export type PageMeta = {
  limit: number;
  offset: number;
  total: number;
  has_more: boolean;
};

export type Baseline = {
  id: string;
  organization_id: string;
  baseline_key: string;
  title: string;
  artifact_path: string;
  document_version: string;
  classification: string;
  approval_status: string;
  version: number;
  created_at: string;
  updated_at: string;
};

export type BaselinePage = {
  items: Baseline[];
  page: PageMeta;
};

export type AuditEvent = {
  id: string;
  organization_id: string;
  actor_id: string;
  actor_kind: string;
  action: string;
  entity_type: string;
  entity_id: string;
  entity_version: number | null;
  reason: string | null;
  source: string;
  correlation_id: string;
  created_at: string;
};

export type AuditEventPage = {
  items: AuditEvent[];
  page: PageMeta;
};

export class ApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails;

  constructor(status: number, problem: ProblemDetails) {
    super(problem.message);
    this.status = status;
    this.problem = problem;
  }
}

function apiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
}

function headers(session: SessionState): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Organization-Id": session.organizationId,
    "X-Actor-Id": session.actorId,
    "X-Actor-Kind": session.actorKind,
    "X-Correlation-Id": crypto.randomUUID(),
    "X-Actor-Name": `web:${session.variant}`,
  };
}

async function parse<T>(response: Response): Promise<T> {
  if (response.ok) {
    if (response.status === 204) {
      return undefined as T;
    }
    return (await response.json()) as T;
  }
  let problem: ProblemDetails = {
    code: "http_error",
    message: `Request failed (${response.status})`,
  };
  try {
    problem = (await response.json()) as ProblemDetails;
  } catch {
    // keep fallback
  }
  throw new ApiError(response.status, problem);
}

export async function listBaselines(
  session: SessionState,
  params: { limit?: number; offset?: number; q?: string; status?: string; sort?: string } = {},
): Promise<BaselinePage> {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));
  if (params.q) query.set("q", params.q);
  if (params.status) query.set("status", params.status);
  if (params.sort) query.set("sort", params.sort);
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines?${query}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<BaselinePage>(response);
}

export async function getBaseline(session: SessionState, id: string): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<Baseline>(response);
}

export async function createBaseline(
  session: SessionState,
  body: {
    baseline_key: string;
    title: string;
    artifact_path: string;
    document_version: string;
    classification?: string;
  },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function updateBaseline(
  session: SessionState,
  id: string,
  body: { title: string; expected_version: number },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}`, {
    method: "PATCH",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function transitionBaseline(
  session: SessionState,
  id: string,
  body: { target_status: string; expected_version: number; reason?: string },
): Promise<Baseline> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}/transitions`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  return parse<Baseline>(response);
}

export async function listBaselineHistory(
  session: SessionState,
  id: string,
): Promise<AuditEventPage> {
  const response = await fetch(`${apiBase()}/api/v1/governance/baselines/${id}/history`, {
    headers: headers(session),
    cache: "no-store",
  });
  return parse<AuditEventPage>(response);
}

export function formatUtc(iso: string): string {
  const date = new Date(iso);
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(date) + " UTC";
}
