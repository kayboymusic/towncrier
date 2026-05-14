from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db.supabase import supabase

router = APIRouter(prefix="/api/company", tags=["company"])


@router.get("/{slug}")
def company(slug: str) -> dict:
    sb = supabase()
    rows = sb.table("companies").select("*").eq("slug", slug).limit(1).execute().data
    if not rows:
        raise HTTPException(status_code=404, detail="company not found")
    # Timeline/launches/ecosystem mapping deferred — see PRD §6.7 / §12.6.
    return {"company": rows[0], "items": [], "stub": True}
