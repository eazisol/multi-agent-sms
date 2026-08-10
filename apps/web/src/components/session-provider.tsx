"use client";

import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { actorKindForVariant, type GovVariant } from "@/lib/roles";
import type { SessionState } from "@/lib/api";

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

export function SessionProvider({ children }: { children: ReactNode }) {
  const [variant, setVariant] = useState<GovVariant>("gov.contributor");
  const session = useMemo<SessionState>(
    () => ({
      organizationId: DEFAULT_ORG,
      actorId: DEFAULT_ACTOR,
      actorKind: actorKindForVariant(variant),
      variant,
    }),
    [variant],
  );

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
