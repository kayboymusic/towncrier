from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("")
def trends() -> dict:
    # Stub — see PRD §6.5 / §12.4. Will compute mention velocity,
    # GitHub star growth, publication frequency, social spikes.
    return {"trends": [], "stub": True}
