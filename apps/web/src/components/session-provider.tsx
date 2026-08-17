"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { actorKindForVariant, type GovVariant } from "@/lib/roles";
import { getCurrentIdentity, type SessionState } from "@/lib/api";

type SessionContextValue = {
  session: SessionState;
  setVariant: (variant: GovVariant) => void;
};

const SessionContext = createContext<SessionContextValue | null>(null);

const DEFAULT_ORG =
  process.env.NEXT_PUBLIC_DEFAULT_ORGANIZATION_ID ??
  "00000000-0000-4000-8000-000000000001";
const DEFAULT_ACTOR =
  process.env.NEXT_PUBLIC_DEFAULT_ACTOR_ID ?? "00000000-0000-4000-8000-000000000101";
const AUTH_MODE = process.env.NEXT_PUBLIC_AUTH_MODE ?? "local";

type Auth0Profile = {
  email?: string;
  name?: string;
};

type AccessTokenResponse = {
  token?: string;
};

export function SessionProvider({ children }: { children: ReactNode }) {
  const [variant, setVariant] = useState<GovVariant>("gov.contributor");
  const [authenticatedSession, setAuthenticatedSession] = useState<SessionState | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    if (AUTH_MODE !== "auth0") {
      return;
    }
    let active = true;
    async function loadAuthenticatedSession() {
      try {
        const [profileResponse, tokenResponse] = await Promise.all([
          fetch("/auth/profile", { cache: "no-store" }),
          fetch("/auth/access-token", { cache: "no-store" }),
        ]);
        if (!profileResponse.ok || !tokenResponse.ok) {
          throw new Error("Authentication session is unavailable");
        }
        const profile = (await profileResponse.json()) as Auth0Profile;
        const tokenBody = (await tokenResponse.json()) as AccessTokenResponse;
        if (!tokenBody.token) {
          throw new Error("Auth0 did not return an API access token");
        }
        const identity = await getCurrentIdentity(tokenBody.token);
        if (active) {
          setAuthenticatedSession({
            organizationId: identity.organization_id,
            actorId: identity.actor_id,
            actorKind: identity.actor_kind,
            variant: "gov.contributor",
            accessToken: tokenBody.token,
            displayName: identity.display_name || profile.name,
            email: profile.email,
          });
        }
      } catch (error) {
        if (active) {
          setAuthError(error instanceof Error ? error.message : "Authentication failed");
        }
      }
    }
    void loadAuthenticatedSession();
    return () => {
      active = false;
    };
  }, []);

  const session = useMemo<SessionState>(
    () =>
      authenticatedSession ?? {
        organizationId: DEFAULT_ORG,
        actorId: DEFAULT_ACTOR,
        actorKind: actorKindForVariant(variant),
        variant,
      },
    [authenticatedSession, variant],
  );

  if (AUTH_MODE === "auth0" && authError) {
    return (
      <main className="grid min-h-screen place-items-center p-6">
        <section className="max-w-md rounded-xl border p-6 text-center">
          <h1 className="text-lg font-semibold">Authentication failed</h1>
          <p className="mt-2 text-sm text-[var(--muted)]">{authError}</p>
          <a className="mt-4 inline-block text-sm underline" href="/auth/login">
            Sign in again
          </a>
        </section>
      </main>
    );
  }

  if (AUTH_MODE === "auth0" && !authenticatedSession) {
    return <main className="grid min-h-screen place-items-center">Loading your workspace…</main>;
  }

  return (
    <SessionContext.Provider value={{ session, setVariant }}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession(): SessionContextValue {
  const value = useContext(SessionContext);
  if (!value) {
    throw new Error("useSession must be used within SessionProvider");
  }
  return value;
}
