import { FeedList } from "@/components/feed/feed-list";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function FeedPage() {
  let initial;
  try {
    initial = await api.feed({ limit: 25 });
  } catch (err) {
    return (
      <div className="rounded-lg border border-destructive/40 bg-destructive/5 p-6">
        <h2 className="text-lg font-semibold">API unreachable</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Could not load the feed. Is the FastAPI server running on{" "}
          <code className="font-mono">localhost:8000</code>?
        </p>
        <pre className="mt-3 overflow-x-auto rounded bg-muted p-2 text-xs">
          {(err as Error).message}
        </pre>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">Feed</h1>
        <p className="text-sm text-muted-foreground">
          Latest updates across AI &amp; robotics, summarized.
        </p>
      </header>
      <FeedList initialPage={initial} />
    </div>
  );
}
