"""GekiChu rating tables

Revision ID: 6a7e8277763b
Revises: d8950c7ce2fc
Create Date: 2024-03-13 12:18:53.210018

"""
from alembic import op
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision = '6a7e8277763b'
down_revision = 'd8950c7ce2fc'
branch_labels = None
depends_on = None

GEKICHU_RATING_TABLE_NAMES = [
    "chuni_profile_rating",
    "ongeki_profile_rating",
]

def upgrade():
    for table_name in GEKICHU_RATING_TABLE_NAMES:
        op.create_table(
            table_name,
            Column("id", Integer, primary_key=True, nullable=False),
            Column("user", Integer, nullable=False),
            Column("version", Integer, nullable=False),
            Column("type", String(255), nullable=False),
            Column("index", Integer, nullable=False),
            Column("musicId", Integer),
            Column("difficultId", Integer),
            Column("romVersionCode", Integer),
            Column("score", Integer),
            mysql_charset="utf8mb4",
        )
        op.create_foreign_key(
            None,
            table_name,
            "aime_user",
            ["user"],
            ["id"],
            ondelete="cascade",
            onupdate="cascade",
        )
        op.create_unique_constraint(
            f"{table_name}_uk",
            table_name,
            ["user", "version", "type", "index"],
        )


def downgrade():
    for table_name in GEKICHU_RATING_TABLE_NAMES:
        op.drop_table(table_name)
