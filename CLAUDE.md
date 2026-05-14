# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Town Crier is a real-time intelligence platform for the AI/robotics ecosystem. The product spec is in `town_crier_complete_product_and_system_blueprint.md` — read it for the long-term vision. The current code is the **MVP vertical slice**: a few RSS sources → AI summarization → Postgres → a Next.js `/feed`. Search, trends, personalization, notifications, and auth are intentionally stubbed (folders/routes exist, real logic does not).

## Repo layout (Turborepo monorepo)

```
apps/web/        Next.js 15 (App Router, TS, Tailwind, TanStack Query, Zustand)
apps/api/        FastAPI — read-only API (the only real endpoint is /api/feed)
apps/workers/    Python ingestion + AI pipeline (CLI-driven, not a long-running service)
packages/shared-types/   TS types mirroring FastAPI schemas (hand-written, not codegen)
supabase/migrations/     SQL migrations — pgvector + tables + feed_view
```

Three languages, three package managers: **pnpm** (root + apps/web), **uv** (apps/api, apps/workers). All three apps share a single `.env` at the repo root.

## Common commands

```bash
# Install
pnpm install                              # JS deps (root)
cd apps/api && uv sync                    # API Python deps
cd apps/workers && uv sync                # Workers Python deps

# Run dev
pnpm dev                                  # web (:3000) + api (:8000) in parallel
pnpm --filter @town-crier/web dev         # web only
pnpm dev:api                              # api only

# Ingestion pipeline
pnpm workers:run-once                     # one full cycle (seeds + polls all sources)
pnpm workers:poll                         # continuous loop, every 5 min
pnpm workers:seed-companies               # idempotent company seed only
cd apps/workers && uv run python -m workers.cli --help    # all CLI commands

# DB
supabase db push                          # apply migrations (after `supabase link`)
# Or paste supabase/migrations/0001_init.sql into the SQL editor.

# Checks
pnpm typecheck                            # ts check across workspace
pnpm lint
```

## Data flow (read this before changing anything)

```
RSS source row in `sources` table
  ↓  workers/ingest/rss.py (feedparser, etag-aware)
RawItem
  ↓  workers/pipeline.py  ← the orchestrator. load-bearing.
items row (upsert by url)
  ↓  workers/ai/embed.py  (OpenAI text-embedding-3-small)
item_embeddings row
  ↓  workers/ai/dedupe.py  (pgvector cosine <=>, threshold 0.92, 7-day window)
  ↓  workers/ai/summarize.py  (LLMProvider — Claude | OpenAI | Grok)
item_summaries row
  ↓  workers/ai/classify.py  (rules first, LLM fallback)
item_categories rows
  ↓
feed_view  (SQL view in 0001_init.sql, joins everything)
  ↓
apps/api/app/services/feed_service.py   (cursor-paginated read)
  ↓
apps/web/src/components/feed/feed-list.tsx   (TanStack infinite query)
```

The pipeline is **idempotent** by design: `items.url` is unique, child tables PK on `item_id`, every write is an upsert. Re-running `run-once` never creates duplicates.

## Provider abstraction (`apps/workers/workers/ai/llm.py`)

`LLMProvider` is an ABC with three implementations:
- `AnthropicProvider` — Claude Sonnet (summary), Claude Haiku (classify)
- `OpenAIProvider` — gpt-4o-mini for completions
- `GrokProvider` — xAI via OpenAI-compatible base URL (`https://api.x.ai/v1`)

Routing is config-driven (`SUMMARY_PROVIDER`, `CLASSIFY_PROVIDER` in `.env`). **Embeddings always go through OpenAI** regardless of provider config — only OpenAI ships the embedding endpoint the pipeline expects.

When adding a new LLM call, route through `get_summary_provider()` / `get_classify_provider()`; don't instantiate clients directly.

## Important quirks & gotchas

- **Single `.env` at the repo root.** Both `apps/api/app/core/config.py` and `apps/workers/workers/config.py` resolve it via `Path(__file__).parents[N]`. The depth (`parents[N]`) differs between the two apps because their `__file__` lives at different nesting levels. If you move config files, recount.
- **No auth.** `users`/`follows`/`bookmarks` tables exist but are unused. `/feed` is public. CORS on the API is open to `localhost:3000`. RLS is intentionally OFF in the migration. Re-enable RLS before exposing the API to the anon key in the browser.
- **`DATABASE_URL` is optional** for the pipeline. `dedupe.find_duplicate` short-circuits to `None` when it's missing; the URL-uniqueness constraint still prevents literal dupes, but the semantic similarity check is skipped. The Supabase SDK doesn't expose pgvector ops cleanly, which is why dedupe uses raw `psycopg`.
- **Cursor pagination** in `feed_service.py` is base64-encoded `(published_at, id)`. PostgREST keyset semantics are emulated with `or_(...)` because PostgREST doesn't have first-class compound keyset filters.
- **Stub routes are real Next.js / FastAPI routes**, not 404s. They render "Coming soon" cards (web) or `{"stub": true}` (api) so navigation is complete. Filling them in means replacing the body, not creating the route.
- **Categories are a Postgres enum** (`item_category`). Adding a new category = new migration + `_RULES` entry in `classify.py`. Don't try to insert an off-enum value.
- **Date math in `pipeline._run_for_source`** uses the literal string `"now()"` because the Supabase JS-style client serializes it through PostgREST, which treats `now()` as a function. Don't switch to `datetime.now().isoformat()` unless you've also changed the column default.

## What's intentionally NOT here yet

Auth, search (FTS + semantic), trend detection, real company intelligence pages, notifications, Kafka, Playwright/Firecrawl scraping, GitHub/Reddit/YouTube/X ingestion, observability stack, deployment configs. All have placeholder folders/routes — add behind the existing seams rather than inventing new ones.

See PRD §25 "Product Development Phases" for the intended order.
