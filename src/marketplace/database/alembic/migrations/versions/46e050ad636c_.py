"""empty message

Revision ID: 46e050ad636c
Revises:
Create Date: 2024-04-07 10:41:02.945390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46e050ad636c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.execute(
        """
        INSERT INTO categories (id, name) VALUES
            (gen_random_uuid(), 'Apparel'),
            (gen_random_uuid(), 'Family'),
            (gen_random_uuid(), 'Home and Garden'),
            (gen_random_uuid(), 'Housing'),
            (gen_random_uuid(), 'Electronic'),
            (gen_random_uuid(), 'Hobbies'),
            (gen_random_uuid(), 'Vehicles'),
            (gen_random_uuid(), 'Entertainment')
        """,
    )


def downgrade() -> None:
    op.drop_table("categories")
