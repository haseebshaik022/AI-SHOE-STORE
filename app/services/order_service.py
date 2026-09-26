from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.models.order import Order

async def create_order(ssn: AsyncSession, user_id: int, item_id: int):
    result = await ssn.execute(select(Item).where(Item.item_id == item_id))
    item = result.scalars().first()
    if not item:
        return None
    order = Order(user_id=user_id, item_id=item_id)
    ssn.add(order)
    await ssn.commit()
    return order

async def get_user_orders(ssn: AsyncSession, user_id: int):
    result = await ssn.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()
