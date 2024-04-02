"""mai2_buddies_support

Revision ID: 81e44dd6047a
Revises: d8950c7ce2fc
Create Date: 2024-03-12 19:10:37.063907

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "81e44dd6047a"
down_revision = "6a7e8277763b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mai2_playlog_2p",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=False),
        sa.Column("userId1", sa.Integer(), nullable=True),
        sa.Column("userId2", sa.Integer(), nullable=True),
        sa.Column("userName1", sa.String(length=25), nullable=True),
        sa.Column("userName2", sa.String(length=25), nullable=True),
        sa.Column("regionId", sa.Integer(), nullable=True),
        sa.Column("placeId", sa.Integer(), nullable=True),
        sa.Column("user2pPlaylogDetailList", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user"], ["aime_user.id"], onupdate="cascade", ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
    )

    op.add_column(
        "mai2_playlog",
        sa.Column(
            "extBool1", sa.Boolean(), nullable=True, server_default=sa.text("NULL")
        ),
    )

    op.add_column(
        "mai2_profile_detail",
        sa.Column(
            "renameCredit", sa.Integer(), nullable=True, server_default=sa.text("NULL")
        ),
    )
    op.add_column(
        "mai2_profile_detail",
        sa.Column(
            "currentPlayCount",
            sa.Integer(),
            nullable=True,
            server_default=sa.text("NULL"),
        ),
    )


def downgrade():
    op.drop_table("mai2_playlog_2p")

    op.drop_column("mai2_playlog", "extBool1")
    op.drop_column("mai2_profile_detail", "renameCredit")
    op.drop_column("mai2_profile_detail", "currentPlayCount")
