"""Public portal router — citizen-facing endpoints (no auth required)."""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.complaint import Complaint
from app.models.ward import Ward
from app.models.verification import Verification
from app.models.trust_score import TrustScore
from app.models.citizen import Citizen
from app.models.audit_log import AuditLog
from app.schemas.dashboard import WardScorecard, PublicAction, TrustScoreOut
from app.schemas.complaint import ComplaintCreate, ComplaintOut

router = APIRouter()


@router.get("/ward/{ward_id}/scorecard", response_model=WardScorecard)
async def ward_scorecard(ward_id: int, db: AsyncSession = Depends(get_db)):
    ward = (await db.execute(select(Ward).where(Ward.id == ward_id))).scalar_one_or_none()
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")

    thirty = datetime.utcnow() - timedelta(days=30)

    total = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.ward_id == ward_id, Complaint.created_at >= thirty
        )
    )).scalar() or 0

    resolved = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.ward_id == ward_id,
            Complaint.status.in_(["VERIFIED", "CLOSED"]),
            Complaint.created_at >= thirty,
        )
    )).scalar() or 0

    avg_hours = (await db.execute(
        select(func.avg(
            func.extract("epoch", Complaint.resolved_at - Complaint.created_at) / 3600
        )).where(
            Complaint.ward_id == ward_id,
            Complaint.resolved_at.isnot(None),
        )
    )).scalar() or 0

    # Latest trust score
    trust = (await db.execute(
        select(TrustScore)
        .where(TrustScore.ward_id == ward_id)
        .order_by(TrustScore.date.desc())
        .limit(1)
    )).scalar_one_or_none()

    return WardScorecard(
        ward_id=ward_id,
        ward_name=ward.ward_name,
        ward_number=ward.ward_number,
        total_complaints=total,
        total_resolved=resolved,
        resolution_rate=round(resolved / total * 100, 1) if total > 0 else 0,
        avg_response_hours=round(float(avg_hours), 1),
        trust_score=float(trust.final_trust_score) if trust else 0,
    )


@router.get("/ward/{ward_id}/actions", response_model=list[PublicAction])
async def recent_actions(ward_id: int, db: AsyncSession = Depends(get_db)):
    """Recently resolved complaints in a ward — public facing."""
    stmt = (
        select(Complaint)
        .where(
            Complaint.ward_id == ward_id,
            Complaint.status.in_(["VERIFIED", "CLOSED"]),
        )
        .order_by(Complaint.resolved_at.desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    complaints = result.scalars().all()

    actions = []
    for c in complaints:
        # Check if it has a verification
        ver = (await db.execute(
            select(Verification).where(Verification.complaint_id == c.id)
        )).scalar_one_or_none()

        actions.append(PublicAction(
            complaint_id=c.id,
            summary=c.ai_summary or c.raw_text or "Issue resolved",
            category=c.category.name if c.category else "General",
            status=c.status,
            resolved_at=c.resolved_at,
            has_verification=ver is not None,
        ))
    return actions


@router.get("/ward/{ward_id}/trust", response_model=Optional[TrustScoreOut])
async def ward_trust(ward_id: int, db: AsyncSession = Depends(get_db)):
    trust = (await db.execute(
        select(TrustScore)
        .where(TrustScore.ward_id == ward_id)
        .order_by(TrustScore.date.desc())
        .limit(1)
    )).scalar_one_or_none()

    if not trust:
        return None
    return TrustScoreOut.model_validate(trust)


@router.post("/complaint", response_model=ComplaintOut, status_code=201)
async def public_submit_complaint(
    body: ComplaintCreate,
    db: AsyncSession = Depends(get_db),
):
    """Citizen submits a complaint through the public portal (no auth)."""
    from app.routers.complaints import create_complaint
    return await create_complaint(body, db)
