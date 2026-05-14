"""Town Crier workers CLI.

Examples:
    uv run python -m workers.cli seed-companies
    uv run python -m workers.cli seed-sources
    uv run python -m workers.cli run-once
    uv run python -m workers.cli poll --interval 300
"""

from __future__ import annotations

import time

import typer
from rich import print

from workers.logging import configure, get_logger
from workers.pipeline import PipelineStats, _enrich_pending, run_once
from workers.seed import seed_companies as _seed_companies
from workers.seed import seed_sources as _seed_sources

app = typer.Typer(help="Town Crier ingestion + AI workers", no_args_is_help=True)
log = get_logger(__name__)


@app.callback()
def _root() -> None:
    configure()


@app.command("seed-companies")
def seed_companies_cmd() -> None:
    """Upsert the known companies list."""
    n = _seed_companies()
    print(f"[green]Seeded {n} companies[/green]")


@app.command("seed-sources")
def seed_sources_cmd() -> None:
    """Upsert the known RSS/API sources list."""
    n = _seed_sources()
    print(f"[green]Seeded {n} sources[/green]")


@app.command("run-once")
def run_once_cmd(
    seed: bool = typer.Option(True, help="Seed sources + companies before running"),
) -> None:
    """Run one full pipeline cycle across all enabled sources."""
    if seed:
        _seed_sources()
        _seed_companies()
    stats = run_once()
    print(stats)


@app.command("enrich-pending")
def enrich_pending_cmd(
    limit: int = typer.Option(500, help="Max items to enrich in one run"),
) -> None:
    """Back-fill summaries/embeddings/categories for items missing them.

    Useful after a partial failure (rate limit, key error, network blip)
    when items are already in the DB but the AI step never finished.
    """
    stats = PipelineStats()
    _enrich_pending(stats, batch_limit=limit)
    print(stats)


@app.command("poll")
def poll_cmd(
    interval: int = typer.Option(300, help="Seconds between cycles"),
) -> None:
    """Continuously poll on a fixed interval."""
    _seed_sources()
    _seed_companies()
    while True:
        try:
            run_once()
        except Exception as exc:  # noqa: BLE001
            log.error("poll.cycle_failed", error=str(exc))
        time.sleep(interval)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
