import { StubPage } from "@/components/layout/stub-page";

export default async function CompanyPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return (
    <StubPage
      title={`Company · ${slug}`}
      description="Timeline of launches, research, GitHub activity, partnerships, and ecosystem mentions."
      prdSection="§6.7 / §12.6"
    />
  );
}
