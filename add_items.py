import asyncio
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import session
from app.models.item import Item

items = [
    Item(item_name="Urban Runner Sneakers", item_price=1299),
    Item(item_name="Classic Street Kicks", item_price=1599),
    Item(item_name="Aero Flex Sports Shoes", item_price=1899),
    Item(item_name="Royal Walk Sneakers", item_price=1499),
    Item(item_name="Velocity Casual Shoes", item_price=1199),
    Item(item_name="Urban Edge Trainers", item_price=1799),
    Item(item_name="FlexStep Running Shoes", item_price=1399),
    Item(item_name="Pro Glide Sneakers", item_price=2199),
    Item(item_name="StreetMax Casual Kicks", item_price=1699),
    Item(item_name="Velocity Pro Shoes", item_price=1999),
]

async def add_items():
    try:
        async with session.begin() as ssn:
            ssn.add_all(items)
        print("items added")
    except SQLAlchemyError as e:
        print("database error:", e)

if __name__ == "__main__":
    asyncio.run(add_items())
