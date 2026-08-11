"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/field";
import type { PageMeta } from "@/lib/api";

const PAGE_SIZE_OPTIONS = [10, 20, 50] as const;

type ListPaginationProps = {
  page: PageMeta;
  onOffsetChange: (offset: number) => void;
  onLimitChange?: (limit: number) => void;
  label?: string;
};

export function ListPagination({
  page,
  onOffsetChange,
  onLimitChange,
  label = "rows",
}: ListPaginationProps) {
  const { limit, offset, total, has_more } = page;
  const from = total === 0 ? 0 : offset + 1;
  const to = Math.min(offset + limit, total);
  const canPrev = offset > 0;
  const canNext = has_more;

  return (
    <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-[var(--line)] px-5 py-3 text-sm text-[var(--muted)]">
      <p className="m-0 leading-8">
        Showing {from}–{to} of {total} {label}
      </p>
      <div className="flex flex-wrap items-center gap-2">
        {onLimitChange ? (
          <label className="flex h-8 items-center gap-2 whitespace-nowrap">
            <span className="text-xs text-[var(--muted)]">Page size</span>
            <Select
              aria-label="Page size"
              className="h-8 w-[4.5rem] py-0"
              value={String(limit)}
              onChange={(event) => {
                onLimitChange(Number(event.target.value));
                onOffsetChange(0);
              }}
            >
              {PAGE_SIZE_OPTIONS.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
              {!PAGE_SIZE_OPTIONS.includes(limit as (typeof PAGE_SIZE_OPTIONS)[number]) ? (
                <option value={limit}>{limit}</option>
              ) : null}
            </Select>
          </label>
        ) : null}
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={!canPrev}
          onClick={() => onOffsetChange(Math.max(0, offset - limit))}
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={!canNext}
          onClick={() => onOffsetChange(offset + limit)}
        >
          Next
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
