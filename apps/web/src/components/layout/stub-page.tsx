export function StubPage({
  title,
  description,
  prdSection,
}: {
  title: string;
  description: string;
  prdSection: string;
}) {
  return (
    <div className="mx-auto max-w-2xl space-y-4 py-12">
      <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
        Coming soon
      </p>
      <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
      <p className="text-muted-foreground">{description}</p>
      <div className="rounded-lg border border-dashed p-6 text-sm text-muted-foreground">
        This view is scaffolded but not yet wired. See{" "}
        <span className="font-mono">{prdSection}</span> in the PRD for the full
        specification.
      </div>
    </div>
  );
}
