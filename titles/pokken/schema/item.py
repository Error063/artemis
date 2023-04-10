from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

item = Table(
    'pokken_item',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user', ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False, unique=True),
    Column('category', Integer),
    Column('content', Integer),
    Column('type', Integer),
    UniqueConstraint('user', 'category', 'content', 'type', name='pokken_item_uk'),
    mysql_charset="utf8mb4",
)

class PokkenItemData(BaseData):
    """
    Items obtained as rewards
    """
    pass
