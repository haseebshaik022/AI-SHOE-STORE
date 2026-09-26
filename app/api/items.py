from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import session
from app.models.item import Item
from app.core.dependencies import current_user
from app.services.redis_client import rd

import json


router = APIRouter(prefix="/items")


@router.get("/get_all_items")
async def get_items():

    try:

        key = "items:all"

        # 1. Check Redis first
        cached = await rd.get(key)

        if cached:
            return json.loads(cached)

        # 2. Redis doesn't have it → get from database
        async with session() as ssn:

            result = await ssn.execute(select(Item))

            items = result.scalars().all()

            data = [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "item_price": item.item_price
                }
                for item in items
            ]

        # 3. Store in Redis for 60 seconds
        await rd.set(
            key,
            json.dumps(data),
            ex=60
        )

        return data

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="database error"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="server error"
        )


@router.get("/search_item")
async def search_item(item_name: str):

    try:

        key = f"items:search:{item_name.lower()}"

        # 1. Check Redis
        cached = await rd.get(key)

        if cached:
            return json.loads(cached)

        # 2. Redis miss → database
        async with session() as ssn:

            result = await ssn.execute(
                select(Item).where(
                    Item.item_name.ilike(f"%{item_name}%")
                )
            )

            items = result.scalars().all()

            data = [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "item_price": item.item_price
                }
                for item in items
            ]

        # 3. Cache search result for 60 seconds
        await rd.set(
            key,
            json.dumps(data),
            ex=60
        )

        return data

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="database error"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="server error"
        )