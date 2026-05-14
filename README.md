# Town Crier

Real-time intelligence platform for the AI & robotics ecosystem. See `town_crier_complete_product_and_system_blueprint.md` for the full product spec.

This repo is the **MVP vertical slice**: real RSS sources → AI summarization (Claude/OpenAI/Grok) → Postgres (Supabase + pgvector) → Next.js `/feed`. Search, trends, personalization, notifications, and auth are scaffolded but not yet wired.

---

## Stack

| Layer    | Tech                                                  |
| -------- | ----------------------------------------------------- |
| Web      | Next.js 15, TypeScript, Tailwind, shadcn/ui, TanStack Query |
| API      | FastAPI (Python 3.11+)                                |
| Workers  | Python (feedparser, httpx, anthropic, openai)         |
| Data     | Supabase (Postgres + pgvector + Storage)              |
| Cache    | Upstash Redis                                         |
| Build    | Turborepo + pnpm + uv                                 |

## Layout

```
apps/
  web/        Next.js frontend
  api/        FastAPI service (read APIs)
  workers/    Ingestion + AI processing
packages/
  shared-types/   TS types shared across web
  eslint-config/  shared lint config
supabase/
  migrations/     SQL migrations (apply with `supabase db push`)
infra/
  docker-compose.yml   local Redis (optional, used if you skip Upstash)
```

## Prerequisites

- Node 20+, pnpm 9+
- Python 3.11+ and [uv](https://docs.astral.sh/uv/) (`brew install uv`)
- A Supabase project (free tier is fine)
- An Upstash Redis (free tier is fine)
- API keys: Anthropic + OpenAI (required), xAI Grok (optional)

## First-time setup

```bash
# 1. Node deps
pnpm install

# 2. Python deps (api + workers)
cd apps/api && uv sync && cd ../..
cd apps/workers && uv sync && cd ../..

# 3. Env
cp .env.example .env
# Fill SUPABASE_*, DATABASE_URL, ANTHROPIC_API_KEY, OPENAI_API_KEY, UPSTASH_*

# 4. Apply the schema
#    Option A — Supabase CLI:
supabase db push
#    Option B — paste supabase/migrations/0001_init.sql into the SQL editor.

# 5. Seed companies
pnpm workers:seed-companies

# 6. Run one ingestion cycle (RSS → summarize → embed → upsert)
pnpm workers:run-once
```

## Run dev

```bash
pnpm dev          # web (:3000) + api (:8000) in parallel
```

Visit http://localhost:3000/feed.

## CLI

```bash
pnpm workers:run-once        # one-shot poll of all enabled sources
pnpm workers:poll            # continuous loop (every 5 min)
pnpm workers:seed-companies  # idempotent company seed
```

## What's runnable today vs stubbed

**Runnable:** RSS ingestion (4 sources), dedupe via embeddings, summaries (short + bullets + impact), category tagging, `/feed` page with infinite scroll.

**Stubbed:** `/trending`, `/companies`, `/company/[slug]`, `/search`, `/saved`, `/settings` — they render placeholder cards. Auth deferred entirely.

## Roadmap

See PRD §25 (Product Development Phases). Next up: search (FTS + semantic), trend detection, company intelligence pages, auth.
