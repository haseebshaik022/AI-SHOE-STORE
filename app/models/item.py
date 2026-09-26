from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"
    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_name: Mapped[str]
    item_price: Mapped[int]
