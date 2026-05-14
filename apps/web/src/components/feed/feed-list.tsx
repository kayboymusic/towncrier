"use client";

import { useInfiniteQuery } from "@tanstack/react-query";
import { Loader2 } from "lucide-react";
import { useEffect, useRef } from "react";

import type { FeedPage } from "@town-crier/shared-types";
import { FeedItem } from "@/components/feed/feed-item";
import { api } from "@/lib/api";

export function FeedList({ initialPage }: { initialPage: FeedPage }) {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery({
      queryKey: ["feed"],
      initialPageParam: undefined as string | undefined,
      queryFn: ({ pageParam }) => api.feed({ cursor: pageParam, limit: 25 }),
      getNextPageParam: (last) => last.next_cursor ?? undefined,
      initialData: {
        pages: [initialPage],
        pageParams: [undefined],
      },
    });

  const sentinelRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const node = sentinelRef.current;
    if (!node || !hasNextPage) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { rootMargin: "400px" },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);

  const items = data?.pages.flatMap((p) => p.items) ?? [];

  if (!items.length) {
    return (
      <div className="rounded-lg border border-dashed p-12 text-center">
        <p className="text-sm text-muted-foreground">
          No items yet. Run{" "}
          <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-xs">
            pnpm workers:run-once
          </code>{" "}
          to ingest the first batch.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <FeedItem key={item.id} item={item} />
      ))}
      <div ref={sentinelRef} />
      {isFetchingNextPage && (
        <div className="flex justify-center py-6 text-sm text-muted-foreground">
          <Loader2 className="mr-2 size-4 animate-spin" />
          Loading more…
        </div>
      )}
      {!hasNextPage && items.length > 0 && (
        <p className="py-6 text-center text-xs text-muted-foreground">
          End of feed.
        </p>
      )}
    </div>
  );
}
