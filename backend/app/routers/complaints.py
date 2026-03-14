"""Complaints router — full CRUD + AI pipeline."""

import uuid
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.complaint import Complaint
from app.models.citizen import Citizen
from app.models.category import Category
from app.models.audit_log import AuditLog
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintAssign,
    ComplaintStatusUpdate,
    ComplaintOut,
    ComplaintListOut,
    ComplaintStats,
)
from app.utils.helpers import get_current_user, get_current_user_optional

logger = logging.getLogger(__name__)
router = APIRouter()


# ── Helpers ──────────────────────────────────────────────

def _complaint_query():
    """Base query with eager-loaded relationships."""
    return (
        select(Complaint)
        .options(
            selectinload(Complaint.category),
            selectinload(Complaint.ward),
            selectinload(Complaint.assignee),
        )
    )


async def _process_complaint(complaint: Complaint, db: AsyncSession):
    """Run AI pipeline on a new complaint (NLP + priority scoring)."""
    from app.services.ai_service import extract_complaint_details
    from app.services.priority_service import calculate_priority_score

    if not complaint.raw_text:
        return

    try:
        # Step 1: NLP extraction
        ai_data = await extract_complaint_details(
            complaint.raw_text,
            complaint.source_language or "auto",
        )

        complaint.ai_summary = ai_data.get("summary_english", "")
        complaint.ai_location = ai_data.get("location_text")
        complaint.ai_duration_days = ai_data.get("duration_days")
        complaint.ai_category_confidence = ai_data.get("category_confidence", 0)

        # Map category name → id
        cat_name = ai_data.get("category", "Other")
        cat_result = await db.execute(
            select(Category).where(Category.name == cat_name)
        )
        cat = cat_result.scalar_one_or_none()
        if cat:
            complaint.category_id = cat.id

        # Step 2: Priority scoring
        priority = await calculate_priority_score(
            {
                "category": cat_name,
                "is_emergency": ai_data.get("is_emergency", False),
                "duration_days": ai_data.get("duration_days"),
                "affected_estimate": ai_data.get("affected_estimate", "individual"),
                "ward_id": complaint.ward_id,
                "category_id": complaint.category_id,
                "area_sentiment": 0,
            },
            db,
        )

        complaint.urgency_score = priority["urgency_score"]
        complaint.impact_score = priority["impact_score"]
        complaint.recurrence_score = priority["recurrence_score"]
        complaint.sentiment_score = priority["sentiment_score"]
        complaint.vulnerability_score = priority["vulnerability_score"]
        complaint.final_priority_score = priority["final_priority_score"]
        complaint.priority_level = priority["priority_level"]

    except Exception as e:
        logger.error(f"AI pipeline failed for complaint {complaint.id}: {e}")


# ── Endpoints ────────────────────────────────────────────

@router.post("", response_model=ComplaintOut, status_code=201)
async def create_complaint(
    body: ComplaintCreate,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new complaint (text, voice, or image)."""
    # Create or find citizen
    citizen = None
    if body.citizen_phone:
        result = await db.execute(
            select(Citizen).where(Citizen.phone == body.citizen_phone)
        )
        citizen = result.scalar_one_or_none()
        if not citizen:
            citizen = Citizen(
                name=body.citizen_name,
                phone=body.citizen_phone,
                ward_id=body.ward_id,
                is_anonymous=body.is_anonymous,
            )
            db.add(citizen)
            await db.flush()

    complaint = Complaint(
        citizen_id=citizen.id if citizen else None,
        raw_text=body.raw_text,
        input_type=body.input_type,
        source_language=body.source_language,
        ward_id=body.ward_id,
        status="OPEN",
    )
    db.add(complaint)
    await db.flush()

    # Run AI pipeline
    await _process_complaint(complaint, db)
    await db.flush()

    # Audit log
    db.add(AuditLog(
        entity_type="complaint",
        entity_id=complaint.id,
        action="CREATED",
        new_value=complaint.status,
    ))

    await db.refresh(complaint)
    # Re-fetch with relationships
    result = await db.execute(
        _complaint_query().where(Complaint.id == complaint.id)
    )
    return ComplaintOut.model_validate(result.scalar_one())


@router.get("", response_model=ComplaintListOut)
async def list_complaints(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    ward_id: Optional[int] = None,
    category_id: Optional[int] = None,
    priority_level: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = _complaint_query()

    if status:
        stmt = stmt.where(Complaint.status == status)
    if ward_id:
        stmt = stmt.where(Complaint.ward_id == ward_id)
    if category_id:
        stmt = stmt.where(Complaint.category_id == category_id)
    if priority_level:
        stmt = stmt.where(Complaint.priority_level == priority_level)
    if search:
        stmt = stmt.where(
            Complaint.raw_text.ilike(f"%{search}%")
            | Complaint.ai_summary.ilike(f"%{search}%")
        )

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    # Paginate
    stmt = (
        stmt.order_by(desc(Complaint.created_at))
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(stmt)
    items = [ComplaintOut.model_validate(c) for c in result.scalars().all()]

    return ComplaintListOut(items=items, total=total, page=page, per_page=per_page)


@router.get("/priority-queue", response_model=ComplaintListOut)
async def priority_queue(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    ward_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Return complaints sorted by priority score descending."""
    stmt = _complaint_query().where(
        Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"])
    )
    if ward_id:
        stmt = stmt.where(Complaint.ward_id == ward_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        stmt.order_by(desc(Complaint.final_priority_score))
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(stmt)
    items = [ComplaintOut.model_validate(c) for c in result.scalars().all()]

    return ComplaintListOut(items=items, total=total, page=page, per_page=per_page)


@router.get("/stats", response_model=ComplaintStats)
async def complaint_stats(db: AsyncSession = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    total = (await db.execute(select(func.count()).select_from(Complaint))).scalar() or 0
    total_open = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"])
        )
    )).scalar() or 0
    total_critical = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.priority_level == "CRITICAL",
            Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
        )
    )).scalar() or 0
    resolved_today = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["VERIFIED", "CLOSED"]),
            Complaint.resolved_at >= today_start,
        )
    )).scalar() or 0
    total_resolved = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["VERIFIED", "CLOSED"])
        )
    )).scalar() or 0

    return ComplaintStats(
        total_open=total_open,
        total_critical=total_critical,
        resolved_today=resolved_today,
        avg_trust_score=72.5,  # Will be computed from trust_scores table
        total_complaints=total,
        total_resolved=total_resolved,
    )


@router.get("/ward/{ward_id}", response_model=ComplaintListOut)
async def complaints_by_ward(
    ward_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = _complaint_query().where(Complaint.ward_id == ward_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = stmt.order_by(desc(Complaint.created_at)).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    items = [ComplaintOut.model_validate(c) for c in result.scalars().all()]
    return ComplaintListOut(items=items, total=total, page=page, per_page=per_page)


@router.get("/{complaint_id}", response_model=ComplaintOut)
async def get_complaint(complaint_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        _complaint_query().where(Complaint.id == complaint_id)
    )
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return ComplaintOut.model_validate(complaint)


@router.put("/{complaint_id}/assign", response_model=ComplaintOut)
async def assign_complaint(
    complaint_id: uuid.UUID,
    body: ComplaintAssign,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        _complaint_query().where(Complaint.id == complaint_id)
    )
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    old_status = complaint.status
    complaint.assigned_to = body.assigned_to
    complaint.assigned_at = datetime.utcnow()
    complaint.status = "ASSIGNED"

    db.add(AuditLog(
        entity_type="complaint",
        entity_id=complaint.id,
        action="ASSIGNED",
        old_value=old_status,
        new_value="ASSIGNED",
        performed_by=user.id,
    ))

    await db.flush()
    await db.refresh(complaint)
    return ComplaintOut.model_validate(complaint)


@router.put("/{complaint_id}/status", response_model=ComplaintOut)
async def update_status(
    complaint_id: uuid.UUID,
    body: ComplaintStatusUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        _complaint_query().where(Complaint.id == complaint_id)
    )
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    old_status = complaint.status
    complaint.status = body.status
    complaint.updated_at = datetime.utcnow()

    if body.status in ("VERIFIED", "CLOSED"):
        complaint.resolved_at = datetime.utcnow()
    if body.status == "VERIFIED":
        complaint.verified_at = datetime.utcnow()

    db.add(AuditLog(
        entity_type="complaint",
        entity_id=complaint.id,
        action="STATUS_CHANGED",
        old_value=old_status,
        new_value=body.status,
        performed_by=user.id,
    ))

    await db.flush()
    await db.refresh(complaint)
    return ComplaintOut.model_validate(complaint)
