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
            ('87a77985-ff82-4b32-a981-981aecd9c2bb', 'Apparel'),
            ('87a77985-ff82-4b32-a981-981aecd9c3bb', 'Family'),
            ('87a77985-ff82-4b32-a981-981aecd9c4bb', 'Home and Garden'),
            ('87a77985-ff82-4b32-a981-981aecd9c5bb', 'Housing'),
            ('87a77985-ff82-4b32-a981-981aecd9c6bb', 'Electronic'),
            ('87a77985-ff82-4b32-a981-981aecd9c7bb', 'Hobbies'),
            ('87a77985-ff82-4b32-a981-981aecd9c8bb', 'Vehicles'),
            ('87a77985-ff82-4b32-a981-981aecd9c9bb', 'Entertainment')
        """,
    )
    op.create_table(
        "subcategories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("category_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("name"),
    )
    op.execute(
        """
        INSERT INTO subcategories (id, category_id, name) VALUES
            (
                'ab415d24-f504-4563-8944-39f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c2bb',
                'Hats'
            ),
            (
                'ab415d24-f504-4563-8944-49f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c3bb',
                'Toys'
            ),
            (
                'ab415d24-f504-4563-8944-59f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c4bb',
                'Shovels'
            ),
            (
                'ab415d24-f504-4563-8944-69f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c5bb',
                'Soap'
            ),
            (
                'ab415d24-f504-4563-8944-89f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c6bb',
                'Laptops'
            ),
            (
                'ab415d24-f504-4563-8944-99f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c7bb',
                'Books'
            ),
            (
                'ab415d24-f504-4563-8944-19f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c8bb',
                'Wheels'
            ),
            (
                'ab415d24-f504-4563-8944-29f784b786b6',
                '87a77985-ff82-4b32-a981-981aecd9c9bb',
                'Puzzles'
            )
        """
    )


def downgrade() -> None:
    op.drop_table("categories")
    op.drop_table("subcategories")
