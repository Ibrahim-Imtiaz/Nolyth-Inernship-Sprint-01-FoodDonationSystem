from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.donation import Donation

from app.schemas.donation import DonationCreate, DonationUpdate, DonationResponse

from fastapi import HTTPException

from typing import List

router = APIRouter()
@router.post("/donations",response_model=DonationResponse,status_code=201)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_donation = Donation(
    food_name=donation.food_name,
    quantity=donation.quantity,
    expiry_time=donation.expiry_time,
    pickup_address=donation.pickup_address,
    owner_id=current_user.id
)
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation

@router.get("/my-donations", response_model=List[DonationResponse])
def get_my_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    donations = db.query(Donation).filter(
    Donation.owner_id == current_user.id
    ).all()

    return donations
    
@router.put("/donations/{donation_id}")
def update_donation(
    donation_id: int,
    donation: DonationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_donation = db.query(Donation).filter(
        Donation.id == donation_id
    ).first()

    if not existing_donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )

    if existing_donation.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own donations"
        )

    existing_donation.food_name = donation.food_name
    existing_donation.quantity = donation.quantity
    existing_donation.expiry_time = donation.expiry_time
    existing_donation.pickup_address = donation.pickup_address

    db.commit()

    return {
        "message": "Donation updated successfully"
    }

@router.delete("/donations/{donation_id}")
def delete_donation(
    donation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_donation = db.query(Donation).filter(
    Donation.id == donation_id
    ).first()

    if not existing_donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )
    
    if existing_donation.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own donations"
        )
    
    db.delete(existing_donation)
    db.commit()

    return {
    "message": "Donation deleted successfully"
    }

@router.get("/available-donations",response_model=List[DonationResponse])
def get_available_donations(
    db: Session = Depends(get_db)
):
    donations = db.query(Donation).filter(
        Donation.status == "Available"
    ).all()

    return donations
    
@router.post("/claim/{donation_id}")
def claim_donation(
    donation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "NGO":
        raise HTTPException(
            status_code=403,
            detail="Only NGOs can claim donations"
        )

    donation = db.query(Donation).filter(
        Donation.id == donation_id
    ).first()

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )

    if donation.status == "Claimed":
        raise HTTPException(
            status_code=400,
            detail="Donation has already been claimed"
        )
    
    if donation.owner_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot claim your own donation"
        )

    donation.status = "Claimed"
    donation.claimed_by = current_user.id

    db.commit()

    return {
        "message": "Donation claimed successfully"
    }

@router.get("/my-claims",response_model=List[DonationResponse])
def get_my_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "NGO":
        raise HTTPException(
            status_code=403,
            detail="Only NGOs can view their claims"
        )

    claims = db.query(Donation).filter(
        Donation.claimed_by == current_user.id
    ).all()

    return claims