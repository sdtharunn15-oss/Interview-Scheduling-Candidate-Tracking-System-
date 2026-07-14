from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Candidate
from app.schemas import CandidateCreate, CandidateUpdate, CandidateResponse
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)

@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    existing = db.query(Candidate).filter(
        Candidate.email == candidate.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Candidate email already exists"
        )

    new_candidate = Candidate(**candidate.model_dump())

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get("/", response_model=list[CandidateResponse])
def get_candidates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Candidate).all()


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: int,
    updated: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    for key, value in updated.model_dump().items():
        setattr(candidate, key, value)

    db.commit()
    db.refresh(candidate)

    return candidate

@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    db.delete(candidate)
    db.commit()

    return {
        "message": "Candidate deleted successfully"
    }