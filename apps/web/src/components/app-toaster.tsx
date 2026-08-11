"use client";

import { Toaster } from "sonner";

import { useTheme } from "@/components/theme-provider";

/** Single global toast host — mount once in the root layout. */
export function AppToaster() {
  const { theme } = useTheme();
  return (
    <Toaster
      theme={theme}
      position="bottom-right"
      closeButton
      richColors={false}
      expand={false}
      visibleToasts={4}
      gap={10}
      offset={24}
      toastOptions={{
        classNames: {
          toast:
            "group toast !bg-[var(--surface)] !text-[var(--ink)] !border !border-[var(--line-strong)] !shadow-[var(--shadow-float)] !rounded-[var(--radius-md)]",
          title: "!text-sm !font-semibold !text-[var(--ink)]",
          description: "!text-xs !text-[var(--muted)]",
          closeButton:
            "!bg-[var(--surface-muted)] !border-[var(--line)] !text-[var(--muted)]",
          success: "!border-l-4 !border-l-[var(--success)]",
          error: "!border-l-4 !border-l-[var(--danger)]",
          warning: "!border-l-4 !border-l-[var(--warning)]",
          info: "!border-l-4 !border-l-[var(--info)]",
        },
      }}
    />
  );
}
