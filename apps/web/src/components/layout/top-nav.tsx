import Link from "next/link";

import { cn } from "@/lib/utils";

const NAV = [
  { href: "/feed", label: "Feed" },
  { href: "/trending", label: "Trending" },
  { href: "/companies", label: "Companies" },
  { href: "/research", label: "Research" },
  { href: "/robotics", label: "Robotics" },
  { href: "/search", label: "Search" },
  { href: "/saved", label: "Saved" },
] as const;

export function TopNav() {
  return (
    <header className="border-b bg-background/80 backdrop-blur sticky top-0 z-50">
      <div className="container flex h-14 items-center gap-6">
        <Link
          href="/"
          className="font-mono text-sm font-semibold tracking-tight"
        >
          <span className="text-accent">▲</span> town crier
        </Link>
        <nav className="flex items-center gap-4 text-sm text-muted-foreground">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "hover:text-foreground transition-colors",
              )}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
