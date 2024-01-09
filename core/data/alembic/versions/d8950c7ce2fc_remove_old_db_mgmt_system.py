"""Remove old db mgmt system

Revision ID: d8950c7ce2fc
Revises: 835b862f9bf0
Create Date: 2024-01-09 13:43:51.381175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8950c7ce2fc'
down_revision = '835b862f9bf0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("schema_versions")


def downgrade():
    op.create_table(
        "schema_versions",
        sa.Column("game", sa.String(4), primary_key=True, nullable=False),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        mysql_charset="utf8mb4",
    )
