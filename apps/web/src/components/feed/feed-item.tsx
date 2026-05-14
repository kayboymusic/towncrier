"use client";

import { formatDistanceToNow } from "date-fns";
import { ExternalLink } from "lucide-react";
import { useState } from "react";

import type { FeedItem as FeedItemType } from "@town-crier/shared-types";
import { cn } from "@/lib/utils";

export function FeedItem({ item }: { item: FeedItemType }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <article className="group rounded-lg border bg-card p-5 transition-colors hover:border-foreground/20">
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        {item.source_name && (
          <span className="font-mono">{item.source_name}</span>
        )}
        <span>·</span>
        <time dateTime={item.published_at}>
          {formatDistanceToNow(new Date(item.published_at), { addSuffix: true })}
        </time>
        {item.companies?.length ? (
          <>
            <span>·</span>
            <div className="flex flex-wrap gap-1">
              {item.companies.map((c) => (
                <span
                  key={c.slug}
                  className="rounded-sm bg-muted px-1.5 py-0.5 text-[10px] font-medium"
                >
                  {c.name}
                </span>
              ))}
            </div>
          </>
        ) : null}
      </div>

      <h2 className="mt-2 text-lg font-semibold leading-snug tracking-tight">
        <a
          href={item.url}
          target="_blank"
          rel="noreferrer"
          className="hover:text-accent inline-flex items-start gap-1"
        >
          {item.title}
          <ExternalLink className="mt-1 size-3.5 shrink-0 opacity-50 group-hover:opacity-100" />
        </a>
      </h2>

      {item.short_summary && (
        <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
          {item.short_summary}
        </p>
      )}

      {(item.bullets?.length || item.impact) && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mt-3 text-xs font-medium text-muted-foreground hover:text-foreground"
        >
          {expanded ? "Hide takeaways" : "Show takeaways"}
        </button>
      )}

      <div
        className={cn(
          "grid transition-[grid-template-rows] duration-200",
          expanded ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
        )}
      >
        <div className="overflow-hidden">
          {item.bullets?.length ? (
            <ul className="mt-3 space-y-1 text-sm">
              {item.bullets.map((b, i) => (
                <li key={i} className="flex gap-2">
                  <span className="text-accent">›</span>
                  <span>{b}</span>
                </li>
              ))}
            </ul>
          ) : null}
          {item.impact && (
            <p className="mt-3 rounded-md bg-muted px-3 py-2 text-xs italic text-muted-foreground">
              <span className="font-semibold not-italic">Why it matters: </span>
              {item.impact}
            </p>
          )}
        </div>
      </div>

      {item.categories?.length ? (
        <div className="mt-3 flex flex-wrap gap-1">
          {item.categories.map((c) => (
            <span
              key={c}
              className="rounded-full border px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider text-muted-foreground"
            >
              {c.replaceAll("_", " ")}
            </span>
          ))}
        </div>
      ) : null}
    </article>
  );
}
