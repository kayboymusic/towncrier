-- =========================================================
-- Town Crier — initial schema
-- =========================================================
-- Conventions:
--   * snake_case
--   * UUID primary keys (default gen_random_uuid())
--   * timestamptz for all timestamps
--   * Everything text by default; constrain later
-- =========================================================

create extension if not exists "pgcrypto";
create extension if not exists "vector";

-- ---------- Reference data ----------

create type source_kind as enum ('rss', 'api', 'scrape', 'webhook');

create type item_category as enum (
  'llms',
  'robotics',
  'humanoids',
  'multimodal',
  'agents',
  'infrastructure',
  'ai_chips',
  'open_source',
  'ai_video',
  'ai_audio',
  'healthcare_ai',
  'defense_ai',
  'regulation',
  'research',
  'funding',
  'product_launch',
  'other'
);

create table sources (
  id              uuid primary key default gen_random_uuid(),
  name            text not null,
  kind            source_kind not null,
  url             text not null unique,
  homepage        text,
  enabled         boolean not null default true,
  last_polled_at  timestamptz,
  etag            text,
  last_modified   text,
  created_at      timestamptz not null default now()
);

create table companies (
  id           uuid primary key default gen_random_uuid(),
  slug         text not null unique,
  name         text not null,
  website      text,
  twitter      text,
  github_org   text,
  description  text,
  logo_url     text,
  created_at   timestamptz not null default now()
);

-- ---------- Core content ----------

create table items (
  id            uuid primary key default gen_random_uuid(),
  source_id     uuid references sources(id) on delete set null,
  external_id   text,                       -- guid/id reported by the source
  url           text not null unique,
  title         text not null,
  author        text,
  raw_content   text,                       -- cleaned plaintext
  raw_html      text,                       -- original html (optional)
  published_at  timestamptz not null,
  fetched_at    timestamptz not null default now(),
  language      text default 'en',
  unique (source_id, external_id)
);

create index items_published_at_idx on items (published_at desc);
create index items_title_trgm_idx on items using gin (to_tsvector('english', title));

create table item_summaries (
  item_id      uuid primary key references items(id) on delete cascade,
  model        text not null,
  short        text not null,
  bullets      jsonb not null default '[]'::jsonb,
  impact       text,
  generated_at timestamptz not null default now()
);

create table item_categories (
  item_id     uuid references items(id) on delete cascade,
  category    item_category not null,
  confidence  real not null default 1.0,
  primary key (item_id, category)
);

create index item_categories_category_idx on item_categories (category);

create table item_companies (
  item_id     uuid references items(id) on delete cascade,
  company_id  uuid references companies(id) on delete cascade,
  confidence  real not null default 1.0,
  primary key (item_id, company_id)
);

create index item_companies_company_idx on item_companies (company_id);

create table item_embeddings (
  item_id    uuid primary key references items(id) on delete cascade,
  model      text not null,
  embedding  vector(1536) not null,
  created_at timestamptz not null default now()
);

-- IVFFLAT requires data before it can be tuned; small lists is fine to start.
create index item_embeddings_ivfflat_idx
  on item_embeddings using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- ---------- User-facing tables (auth deferred — created but unused) ----------

create table users (
  id           uuid primary key default gen_random_uuid(),
  email        text unique,
  display_name text,
  created_at   timestamptz not null default now()
);

create table follows (
  user_id     uuid references users(id) on delete cascade,
  company_id  uuid references companies(id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (user_id, company_id)
);

create table bookmarks (
  user_id     uuid references users(id) on delete cascade,
  item_id     uuid references items(id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (user_id, item_id)
);

-- ---------- Feed view (read path) ----------

create view feed_view as
select
  i.id,
  i.url,
  i.title,
  i.author,
  i.published_at,
  i.fetched_at,
  s.name      as source_name,
  s.homepage  as source_homepage,
  sm.short    as short_summary,
  sm.bullets  as bullets,
  sm.impact   as impact,
  coalesce(
    (select array_agg(ic.category::text) from item_categories ic where ic.item_id = i.id),
    array[]::text[]
  ) as categories,
  coalesce(
    (select jsonb_agg(jsonb_build_object('slug', c.slug, 'name', c.name))
       from item_companies icx
       join companies c on c.id = icx.company_id
      where icx.item_id = i.id),
    '[]'::jsonb
  ) as companies
from items i
left join sources s on s.id = i.source_id
left join item_summaries sm on sm.item_id = i.id;

-- =========================================================
-- Notes:
--   * Run `analyze item_embeddings;` after first big insert to
--     let IVFFLAT pick reasonable centroids.
--   * RLS is intentionally off for MVP (no auth). Re-enable
--     before exposing /api directly to the browser with anon key.
-- =========================================================
