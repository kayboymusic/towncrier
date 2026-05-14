# Town Crier — Complete Product & System Blueprint

# Product Name
Town Crier

# Product Type
Web-based real-time AI & robotics intelligence platform

---

# 1. Executive Summary

Town Crier is a real-time intelligence platform for the AI and robotics ecosystem.

The platform continuously aggregates, processes, structures, summarizes, ranks, and distributes updates from:
- AI companies
- robotics companies
- research labs
- GitHub repositories
- research papers
- social platforms
- product launches
- changelogs
- conferences
- developer ecosystems

Town Crier transforms fragmented AI information into:
- structured feeds
- AI-generated summaries
- trend intelligence
- personalized discovery
- searchable knowledge
- company intelligence

The product is designed to become the operational intelligence layer for AI builders, founders, researchers, operators, investors, and enthusiasts.

---

# 2. Problem Statement

The AI ecosystem is fragmented across:
- blogs
- X/Twitter
- GitHub
- Reddit
- YouTube
- research portals
- newsletters
- press releases
- changelogs
- conference announcements

Users struggle to:
- stay current in real time
- identify important updates
- separate signal from noise
- track companies efficiently
- discover emerging trends early
- follow research breakthroughs
- monitor robotics developments

Existing platforms are:
- generic
- manually curated
- incomplete
- not AI-native
- weak on robotics coverage
- poor at personalization
- poor at intelligence extraction

---

# 3. Vision

Build the definitive real-time intelligence infrastructure for the global AI and robotics ecosystem.

---

# 4. Product Goals

## Primary Goals
- Aggregate AI and robotics updates in real time
- Deliver high-signal AI-generated summaries
- Enable personalized intelligence feeds
- Detect emerging trends automatically
- Create a searchable AI ecosystem database

## Secondary Goals
- Become daily workflow infrastructure for AI professionals
- Provide enterprise intelligence tooling
- Expose APIs for external developers
- Support market and research intelligence workflows

---

# 5. Target Users

## Primary Users
- AI engineers
- ML researchers
- startup founders
- product teams
- AI enthusiasts
- robotics enthusiasts

## Secondary Users
- investors
- VCs
- journalists
- analysts
- enterprise innovation teams
- students

---

# 6. Core Product Features

# 6.1 Real-Time Intelligence Feed

## Description
Continuously updating stream of AI and robotics updates.

## Feed Content
- model launches
- robotics demos
- research breakthroughs
- product launches
- funding announcements
- acquisitions
- benchmark updates
- open-source releases
- AI regulation updates
- API updates

## Functional Requirements
- Infinite scroll
- Real-time refresh
- Filtering
- Sorting
- Bookmarking
- Search
- Personalized ranking

---

# 6.2 AI Summarization Engine

## Description
Automatically summarizes ecosystem updates into structured intelligence.

## Outputs
- short summaries
- detailed summaries
- bullet takeaways
- impact analysis
- technical breakdowns

---

# 6.3 Categorization System

## Categories
- LLMs
- robotics
- humanoids
- multimodal AI
- AI agents
- infrastructure
- AI chips
- open source
- AI video
- AI audio
- healthcare AI
- defense AI
- regulation
- research

## Features
- Multi-tag support
- AI classification
- Manual admin overrides

---

# 6.4 Personalized Feed

## Users Can Follow
- companies
- categories
- technologies
- researchers
- repositories
- keywords

## Features
- Personalized recommendations
- Adaptive ranking
- Interest onboarding

---

# 6.5 Trend Detection Engine

## Description
Automatically detects ecosystem momentum shifts.

## Trend Signals
- mention velocity
- GitHub star growth
- publication frequency
- social spikes
- funding frequency
- cross-platform mentions

## Outputs
- daily trends
- emerging technologies
- trending companies
- fast-growing repositories
- research momentum

---

# 6.6 Search Engine

## Features
- Full-text search
- Semantic search
- Hybrid search
- Search filters
- Topic discovery

## Filters
- company
- category
- timeframe
- source
- popularity
- relevance

---

# 6.7 Company Intelligence Pages

## Data Displayed
- launches
- research releases
- GitHub activity
- acquisitions
- partnerships
- ecosystem mentions
- trending activity

---

# 6.8 Notifications & Alerts

## Notification Types
- breaking AI news
- followed company updates
- trend alerts
- keyword alerts

## Delivery Channels
- in-app
- email
- push notifications

---

# 7. MVP Scope

## Included
- real-time feed
- AI summaries
- categories
- search
- authentication
- bookmarking
- source ingestion
- company pages
- basic personalization

## Excluded
- enterprise analytics
- mobile apps
- predictive analytics
- advanced recommendation systems
- API marketplace

---

# 8. Technical Product Requirements

# 8.1 System Objectives

The platform must support:
- high-frequency ingestion
- real-time updates
- AI processing pipelines
- scalable search
- semantic discovery
- personalization
- trend intelligence
- future enterprise APIs

---

# 8.2 Core Technical Requirements

| Requirement | Target |
|---|---|
| Feed freshness | < 5 minutes |
| Feed load time | < 2 seconds |
| Search latency | < 500ms |
| Uptime | 99.9% |
| Deduplication accuracy | > 90% |
| Summary quality | > 90% |

---

# 9. High-Level Architecture

```text
                    ┌────────────────────┐
                    │ External Sources   │
                    └─────────┬──────────┘
                              │
                ┌─────────────▼─────────────┐
                │ Ingestion Layer           │
                │ RSS/API/Scrapers/Webhooks │
                └─────────────┬─────────────┘
                              │
                     Queue/Event Bus
                              │
                ┌─────────────▼─────────────┐
                │ Processing Pipeline       │
                │ AI + NLP + Classification │
                └─────────────┬─────────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
     ┌────────▼───────┐ ┌────▼───────┐ ┌──────▼────────┐
     │ PostgreSQL     │ │ OpenSearch │ │ Redis Cache   │
     └────────┬───────┘ └────┬───────┘ └──────┬────────┘
              │               │                │
              └───────────────┼────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │ Backend API Layer   │
                   │ FastAPI/GraphQL     │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │ Next.js Frontend    │
                   └─────────────────────┘
```

---

# 10. Frontend Architecture

# Stack

| Technology | Purpose |
|---|---|
| Next.js | Frontend framework |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| shadcn/ui | Component system |
| TanStack Query | Data fetching |
| Zustand | Client state |
| Framer Motion | UI animations |

---

# Frontend Responsibilities

- render feeds
- render search
- authentication
- trend dashboards
- notifications
- personalization
- bookmarks
- company pages
- user preferences

---

# Frontend Routes

| Route | Purpose |
|---|---|
| / | Landing page |
| /feed | Main feed |
| /trending | Trend explorer |
| /companies | Company directory |
| /company/[slug] | Company intelligence page |
| /robotics | Robotics feed |
| /research | Research feed |
| /search | Search results |
| /saved | Bookmarks |
| /settings | User settings |

---

# 11. Backend Architecture

# Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend APIs |
| Python | AI ecosystem tooling |
| GraphQL | Aggregated querying |
| REST | Public endpoints |
| WebSockets | Real-time updates |

---

# Backend Responsibilities

- feed orchestration
- ranking
- personalization
- search APIs
- notifications
- AI orchestration
- authentication
- source management
- analytics

---

# 12. Core Service Architecture

Town Crier should use modular services.

NOT a giant monolith.

---

# 12.1 Feed Service

## Responsibilities
- aggregate feed items
- rank feed content
- apply personalization
- manage pagination
- freshness ordering

## Internal Components
- Feed Aggregator
- Feed Ranker
- Personalization Adapter
- Feed Serializer
- Cache Manager

---

# 12.2 Search Service

## Responsibilities
- full-text search
- semantic search
- hybrid ranking
- search indexing
- query parsing

## Search Types
- keyword search
- semantic search
- hybrid search
- trending search

---

# 12.3 Personalization Service

## Responsibilities
- user profiling
- recommendation ranking
- behavioral analysis
- preference learning

## User Signals
- follows
- bookmarks
- clicks
- dwell time
- search history

---

# 12.4 Trend Intelligence Service

## Responsibilities
- detect momentum shifts
- trend scoring
- velocity detection
- emerging topic detection

## Trend Inputs
- article mentions
- GitHub growth
- publication spikes
- engagement spikes
- social mentions

---

# 12.5 Notification Service

## Responsibilities
- in-app notifications
- email alerts
- trend alerts
- company alerts

## Delivery Channels
- email
- push notifications
- in-app sockets

---

# 12.6 Company Intelligence Service

## Responsibilities
- company timelines
- launch tracking
- ecosystem mapping
- relationship tracking

---

# 13. AI Processing Architecture

# 13.1 AI Processing Pipeline

```text
Raw Content
   ↓
Cleaning
   ↓
Deduplication
   ↓
Classification
   ↓
Summarization
   ↓
Embedding Generation
   ↓
Trend Processing
   ↓
Search Indexing
```

---

# 13.2 Summarization Engine

## Responsibilities
- short summaries
- long summaries
- bullet takeaways
- technical breakdowns

## Models
| Task | Model |
|---|---|
| premium summaries | GPT/Claude |
| cheap summaries | local LLMs |
| validation | rule systems |

---

# 13.3 Classification Engine

## Responsibilities
- category tagging
- company detection
- technology extraction
- topic labeling

---

# 13.4 Deduplication Engine

## Responsibilities
Prevent duplicate stories.

## Techniques
- embedding similarity
- clustering
- cosine similarity
- fingerprint hashing

---

# 13.5 Embedding Engine

## Responsibilities
Generate embeddings for:
- semantic search
- recommendations
- clustering
- personalization

---

# 13.6 Signal Ranking Engine

## Ranking Inputs
| Signal | Weight |
|---|---|
| source credibility | High |
| recency | High |
| trend acceleration | High |
| engagement | Medium |
| relevance | High |

---

# 14. Data Ingestion Architecture

# Purpose
Continuously collect AI ecosystem updates.

---

# Ingestion Sources

## Official Sources
- blogs
- newsroom pages
- changelogs
- documentation updates

## APIs
- GitHub API
- Reddit API
- YouTube API
- X/Twitter API
- Hugging Face API

## Research Sources
- arXiv
- conference feeds
- Papers With Code

## Scraped Sources
- Product Hunt
- robotics sites
- AI launch sites
- startup launch platforms

---

# Ingestion Systems

| System | Purpose |
|---|---|
| RSS Collector | blogs/news |
| API Collectors | structured APIs |
| Scraper Cluster | websites |
| GitHub Listener | repositories |
| Research Indexer | papers |
| Social Stream Listener | social updates |

---

# Ingestion Pipeline

```text
Source Discovery
   ↓
Content Fetching
   ↓
Normalization
   ↓
Parsing
   ↓
Queue Publishing
```

---

# Scraping Infrastructure

## Components
- scheduler
- headless browsers
- parser workers
- anti-bot layer
- retry workers

## Technologies
| Tool | Purpose |
|---|---|
| Playwright | browser automation |
| Firecrawl | structured extraction |
| Crawl4AI | AI extraction |
| BrightData | proxies |

---

# 15. Queue & Event Architecture

# Purpose
Support asynchronous distributed processing.

---

# Queue Stack

| Tool | Purpose |
|---|---|
| Kafka | event streaming |
| BullMQ | background jobs |
| Redis Streams | lightweight streams |

---

# Kafka Topics

```text
raw-content
processed-content
summaries
embeddings
search-indexing
notifications
trends
```

---

# Queue Consumers

| Consumer | Responsibility |
|---|---|
| summarizer-worker | summaries |
| classifier-worker | tagging |
| embedding-worker | embeddings |
| trend-worker | trends |
| search-worker | indexing |

---

# 16. Storage Architecture

# 16.1 PostgreSQL

## Stores
- users
- follows
- bookmarks
- metadata
- subscriptions
- relationships

---

# 16.2 OpenSearch

## Stores
- indexed articles
- summaries
- trends
- search metadata

---

# 16.3 Redis

## Uses
- caching
- session storage
- queues
- feed snapshots
- rate limiting

---

# 16.4 Vector Database

## Stores
- embeddings
- semantic vectors
- similarity indexes

## Recommended
- pgvector (MVP)
- Pinecone (future scale)
- Weaviate (advanced systems)

---

# 16.5 Object Storage

## Stores
- scraped HTML
- screenshots
- media
- archived documents

---

# 17. Real-Time Systems

# Real-Time Features
- live feed updates
- live notifications
- trend refreshes
- collaborative alerts

---

# Real-Time Stack

| Tool | Purpose |
|---|---|
| WebSockets | persistent connections |
| Redis Pub/Sub | event propagation |
| SSE | lightweight streaming |

---

# 18. Search Architecture

# Search Pipeline

```text
User Query
   ↓
Query Parser
   ↓
Keyword Search
   ↓
Vector Search
   ↓
Result Fusion
   ↓
Ranking Layer
   ↓
Results
```

---

# Search Features
- semantic search
- full-text search
- hybrid ranking
- topic exploration
- contextual discovery

---

# Search Infrastructure

| Tool | Purpose |
|---|---|
| OpenSearch | full-text search |
| pgvector | semantic search |
| Pinecone | scalable vectors |

---

# 19. Security Architecture

# Security Layers

```text
Cloudflare
   ↓
API Gateway
   ↓
Auth Middleware
   ↓
Rate Limiting
   ↓
Service Authorization
```

---

# Security Features

| Feature | Purpose |
|---|---|
| OAuth | secure login |
| JWT | sessions |
| RBAC | admin permissions |
| Rate limiting | abuse prevention |
| CAPTCHA | bot protection |

---

# 20. Authentication System

# Supported Methods
- Google OAuth
- GitHub OAuth
- email/password

---

# Recommended Auth Providers

| Tool | Purpose |
|---|---|
| Clerk | fast MVP |
| Auth.js | open alternative |
| Supabase Auth | integrated stack |

---

# 21. Observability & Monitoring

# Monitoring Stack

| Tool | Purpose |
|---|---|
| Grafana | dashboards |
| Prometheus | metrics |
| Sentry | error monitoring |
| OpenTelemetry | tracing |
| PostHog | product analytics |

---

# Metrics To Track

## Infrastructure
- queue lag
- ingestion latency
- scraper success rate
- API latency

## Product
- retention
- feed engagement
- search usage
- trend interaction

---

# 22. Scalability Architecture

# Scaling Strategy

## Horizontal Scaling
Scale independently:
- API nodes
- ingestion workers
- AI workers
- search clusters
- queue consumers

---

# Distributed Processing

```text
Load Balancer
    ↓
Stateless API Nodes
    ↓
Worker Clusters
    ↓
Distributed Databases
```

---

# 23. Deployment Architecture

# MVP Infrastructure

| Layer | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Railway |
| PostgreSQL | Supabase |
| Redis | Upstash |
| Search | Elastic Cloud |

---

# Production Infrastructure

| Layer | Platform |
|---|---|
| Compute | AWS EKS |
| CDN | Cloudflare |
| Queue | Kafka |
| Search | OpenSearch |
| Object Storage | S3 |

---

# 24. API Design

# Public Endpoints

## Feed API
```http
GET /api/feed
```

## Company API
```http
GET /api/company/{slug}
```

## Trend API
```http
GET /api/trends
```

## Search API
```http
GET /api/search?q=humanoid+robots
```

---

# 25. Product Development Phases

# Phase 1 — MVP

## Deliverables
- ingestion system
- feed
- AI summaries
- search
- authentication
- bookmarking
- company pages

## Timeline
4–8 weeks

---

# Phase 2 — Intelligence Layer

## Deliverables
- trend intelligence
- personalization
- semantic discovery
- recommendation systems

## Timeline
6–10 weeks

---

# Phase 3 — Scale & Enterprise

## Deliverables
- enterprise APIs
- advanced analytics
- distributed infrastructure
- predictive intelligence

---

# 26. Engineering Priorities

## Highest Priority
1. ingestion reliability
2. deduplication
3. feed quality
4. summary quality
5. search performance

---

## Medium Priority
1. personalization
2. trend intelligence
3. notifications

---

## Lower Priority
1. enterprise tooling
2. predictive systems
3. AI agents

---

# 27. Future Systems

# Future AI Systems
- predictive trend forecasting
- AI research agents
- AI market intelligence
- startup intelligence scoring
- automated ecosystem mapping

---

# Future Product Systems
- browser extension
- mobile app
- desktop terminal
- enterprise dashboards
- API marketplace

---

# 28. Product Principles

- Real-time first
- Signal over noise
- AI-native workflows
- Fast information access
- Deep robotics coverage
- Source transparency
- Personalized intelligence
- Scalable infrastructure
- Search-centric discovery
- Intelligence over aggregation

