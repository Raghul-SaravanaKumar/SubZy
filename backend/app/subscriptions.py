from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database import db
from app.models import Subscription, UpdateSubscription
from app.auth_dependency import get_current_user

router = APIRouter()


# ==========================================
# Add Subscription
# ==========================================
@router.post("")
def add_subscription(
    subscription: Subscription,
    current_user=Depends(get_current_user)
):

    data = subscription.model_dump()

    data["user_id"] = current_user["id"]

    result = db.subscriptions.insert_one(data)

    return {
        "message": "Subscription added successfully",
        "subscription_id": str(result.inserted_id)
    }


# ==========================================
# Get All Subscriptions
# ==========================================
@router.get("")
def get_subscriptions(
    current_user=Depends(get_current_user)
):

    subscriptions = list(
        db.subscriptions.find(
            {
                "user_id": current_user["id"]
            }
        )
    )

    for sub in subscriptions:
        sub["_id"] = str(sub["_id"])

    return subscriptions


# ==========================================
# Get Single Subscription
# ==========================================
@router.get("/{subscription_id}")
def get_subscription(
    subscription_id: str,
    current_user=Depends(get_current_user)
):

    subscription = db.subscriptions.find_one(
        {
            "_id": ObjectId(subscription_id),
            "user_id": current_user["id"]
        }
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    subscription["_id"] = str(subscription["_id"])

    return subscription


# ==========================================
# Update Subscription
# ==========================================
@router.put("/{subscription_id}")
def update_subscription(
    subscription_id: str,
    subscription: UpdateSubscription,
    current_user=Depends(get_current_user)
):

    update_data = subscription.model_dump(
        exclude_none=True
    )

    result = db.subscriptions.update_one(
        {
            "_id": ObjectId(subscription_id),
            "user_id": current_user["id"]
        },
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return {
        "message": "Subscription updated successfully"
    }


# ==========================================
# Delete Subscription
# ==========================================
@router.delete("/{subscription_id}")
def delete_subscription(
    subscription_id: str,
    current_user=Depends(get_current_user)
):

    result = db.subscriptions.delete_one(
        {
            "_id": ObjectId(subscription_id),
            "user_id": current_user["id"]
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return {
        "message": "Subscription deleted successfully"
    }