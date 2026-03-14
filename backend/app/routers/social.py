"""Social media router — feed, sentiment, alerts, scan."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.social_post import SocialPost
from app.schemas.dashboard import SocialPostOut, SocialAlert

router = APIRouter()


@router.get("/feed", response_model=list[SocialPostOut])
async def social_feed(
    limit: int = Query(30, ge=1, le=100),
    platform: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Latest monitored social media posts."""
    stmt = select(SocialPost).order_by(desc(SocialPost.created_at)).limit(limit)
    if platform:
        stmt = stmt.where(SocialPost.platform == platform)
    result = await db.execute(stmt)
    return [SocialPostOut.model_validate(p) for p in result.scalars().all()]


@router.get("/sentiment")
async def sentiment_overview(db: AsyncSession = Depends(get_db)):
    """Aggregate sentiment breakdown."""
    stmt = (
        select(SocialPost.sentiment, func.count().label("count"))
        .group_by(SocialPost.sentiment)
    )
    result = await db.execute(stmt)
    breakdown = {row.sentiment: row.count for row in result.all()}

    total = sum(breakdown.values()) or 1
    return {
        "total_posts": total,
        "positive": breakdown.get("POSITIVE", 0),
        "negative": breakdown.get("NEGATIVE", 0),
        "angry": breakdown.get("ANGRY", 0),
        "neutral": breakdown.get("NEUTRAL", 0),
        "positive_pct": round(breakdown.get("POSITIVE", 0) / total * 100, 1),
        "negative_pct": round(breakdown.get("NEGATIVE", 0) / total * 100, 1),
        "angry_pct": round(breakdown.get("ANGRY", 0) / total * 100, 1),
        "neutral_pct": round(breakdown.get("NEUTRAL", 0) / total * 100, 1),
    }


@router.get("/alerts", response_model=list[SocialAlert])
async def social_alerts(db: AsyncSession = Depends(get_db)):
    """Viral posts and misinformation alerts."""
    stmt = (
        select(SocialPost)
        .where(
            (SocialPost.is_misinformation == True)
            | (SocialPost.virality_score >= 70)
        )
        .order_by(desc(SocialPost.virality_score))
        .limit(20)
    )
    result = await db.execute(stmt)
    posts = result.scalars().all()
    return [
        SocialAlert(
            id=p.id,
            post_text=p.post_text or "",
            platform=p.platform,
            sentiment=p.sentiment or "NEUTRAL",
            virality_score=p.virality_score or 0,
            is_misinformation=p.is_misinformation or False,
            misinfo_explanation=p.misinfo_explanation,
        )
        for p in posts
    ]


@router.post("/scan")
async def trigger_scan(db: AsyncSession = Depends(get_db)):
    """Trigger a manual social media scan."""
    from app.services.social_service import scan_social_media

    posts = await scan_social_media("Delhi", ["Shanti Nagar", "Rajendra Nagar"])

    saved = 0
    for p in posts:
        sp = SocialPost(
            platform=p.get("platform", "twitter"),
            post_url=p.get("post_url"),
            post_text=p.get("post_text"),
            author_handle=p.get("author_handle"),
            sentiment=p.get("sentiment"),
            sentiment_score=p.get("sentiment_score"),
            extracted_category=p.get("category"),
            extracted_ward=p.get("extracted_ward"),
            is_complaint=p.get("is_complaint", False),
            is_misinformation=p.get("is_misinformation", False),
            misinfo_confidence=p.get("misinfo_confidence"),
            misinfo_explanation=p.get("misinfo_explanation"),
            likes=p.get("likes", 0),
            shares=p.get("shares", 0),
            replies=p.get("replies", 0),
            virality_score=p.get("virality_score", 0),
        )
        db.add(sp)
        saved += 1

    await db.flush()
    return {"message": f"Scanned and saved {saved} posts"}
