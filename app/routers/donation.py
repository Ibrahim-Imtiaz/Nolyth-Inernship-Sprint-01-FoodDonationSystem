from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.donation import Donation

from app.schemas.donation import DonationCreate

from fastapi import HTTPException
from app.schemas.donation import DonationUpdate

router = APIRouter()
@router.post("/donations")
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

@router.get("/my-donations")
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
    db.refresh(existing_donation)

    return existing_donation

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


    