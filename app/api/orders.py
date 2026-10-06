from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import session
from app.models.item import Item
from app.models.order import Order
from app.core.dependencies import current_user
from fastapi import HTTPException

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/order_item")
async def order_item(item_id: int, user_id: int = Depends(current_user)):
    try:
        async with session.begin() as ssn:
            result = await ssn.execute(select(Item).where(Item.item_id == item_id))
            item = result.scalars().first()
            if not item:
                raise HTTPException(status_code=404, detail="item not found")
            order = Order(user_id=user_id, item_id=item_id)
            ssn.add(order)
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error")
    return {"message":"order placed successfully","order_id":order.order_id}

@router.get("/get_order")
async def get_order(user_id: int = Depends(current_user)):
    try:
        async with session() as ssn:
            result = await ssn.execute(select(Order).where(Order.user_id == user_id))
            return result.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error")
