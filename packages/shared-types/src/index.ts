// Hand-written types mirroring the FastAPI schemas in apps/api/app/schemas/.
// Replace with codegen (e.g. supabase-codegen or fastapi-codegen) once the
// schema stabilizes.

export type ItemCategory =
  | "llms"
  | "robotics"
  | "humanoids"
  | "multimodal"
  | "agents"
  | "infrastructure"
  | "ai_chips"
  | "open_source"
  | "ai_video"
  | "ai_audio"
  | "healthcare_ai"
  | "defense_ai"
  | "regulation"
  | "research"
  | "funding"
  | "product_launch"
  | "other";

export interface CompanyRef {
  slug: string;
  name: string;
}

export interface FeedItem {
  id: string;
  url: string;
  title: string;
  author: string | null;
  published_at: string; // ISO-8601
  fetched_at: string;
  source_name: string | null;
  source_homepage: string | null;
  short_summary: string | null;
  bullets: string[];
  impact: string | null;
  categories: string[];
  companies: CompanyRef[];
}

export interface FeedPage {
  items: FeedItem[];
  next_cursor: string | null;
}
