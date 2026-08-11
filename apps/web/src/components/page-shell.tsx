import { cn } from "@/lib/cn";

/** Standard primary content padding inside the app scroll main. */
export function PageShell({
  children,
  className,
  fill = false,
}: {
  children: React.ReactNode;
  className?: string;
  /** Stretch to the viewport main pane (split layouts, boards). */
  fill?: boolean;
}) {
  return (
    <div
      className={cn(
        "mx-auto w-full max-w-7xl px-4 py-6 md:px-6",
        fill && "flex h-full min-h-0 flex-col",
        className,
      )}
    >
      {children}
    </div>
  );
}

/** Nested independent scroll region (drawer body, split pane, table viewport). */
export function ScrollRegion({
  children,
  className,
  orientation = "vertical",
}: {
  children: React.ReactNode;
  className?: string;
  orientation?: "vertical" | "horizontal" | "both";
}) {
  const overflow =
    orientation === "horizontal"
      ? "overflow-x-auto overflow-y-hidden"
      : orientation === "both"
        ? "overflow-auto"
        : "overflow-y-auto overflow-x-hidden";

  return (
    <div className={cn("min-h-0 min-w-0", overflow, className)}>{children}</div>
  );
}

/**
 * Two independently scrolling panes that fill remaining shell height.
 * Use under AppShell `fill` pages (Queries, Requirements, approvals review, etc.).
 */
export function SplitScroll({
  left,
  right,
  className,
  leftClassName,
  rightClassName,
}: {
  left: React.ReactNode;
  right: React.ReactNode;
  className?: string;
  leftClassName?: string;
  rightClassName?: string;
}) {
  return (
    <div
      className={cn(
        "grid min-h-0 flex-1 gap-4 overflow-hidden lg:grid-cols-[minmax(18rem,0.95fr)_minmax(0,1.25fr)]",
        className,
      )}
    >
      <ScrollRegion className={cn("rounded-[var(--radius-lg)]", leftClassName)}>
        {left}
      </ScrollRegion>
      <ScrollRegion className={cn("rounded-[var(--radius-lg)]", rightClassName)}>
        {right}
      </ScrollRegion>
    </div>
  );
}

/** Wide table viewport: vertical + horizontal scroll with optional max height. */
export function TableScroll({
  children,
  className,
  maxHeightClassName = "max-h-[min(36rem,calc(100dvh-16rem))]",
}: {
  children: React.ReactNode;
  className?: string;
  maxHeightClassName?: string;
}) {
  return (
    <div
      className={cn(
        "min-h-0 overflow-auto rounded-[var(--radius-lg)] border border-[var(--line)]",
        maxHeightClassName,
        className,
      )}
    >
      {children}
    </div>
  );
}
