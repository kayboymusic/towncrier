import Link from "next/link";

export default function Home() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 py-16">
      <p className="font-mono text-xs uppercase tracking-widest text-accent">
        Town Crier
      </p>
      <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
        Real-time intelligence for the AI and robotics ecosystem.
      </h1>
      <p className="text-muted-foreground text-lg">
        Every launch, paper, repo, and demo across AI &amp; robotics —
        summarized, categorized, and ranked.
      </p>
      <div className="flex gap-3 pt-2">
        <Link
          href="/feed"
          className="inline-flex items-center rounded-md bg-accent px-4 py-2 text-sm font-medium text-accent-foreground hover:opacity-90"
        >
          Open the feed →
        </Link>
        <Link
          href="/trending"
          className="inline-flex items-center rounded-md border px-4 py-2 text-sm font-medium hover:bg-muted"
        >
          What's trending
        </Link>
      </div>
    </div>
  );
}
