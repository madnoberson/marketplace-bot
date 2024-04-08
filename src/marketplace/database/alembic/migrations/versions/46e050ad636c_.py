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
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.execute(
        """
        INSERT INTO categories (id, name) VALUES
            (1, 'Apparel'),
            (2, 'Family'),
            (3, 'Home and Garden'),
            (4, 'Housing'),
            (5, 'Electronic'),
            (6, 'Hobbies'),
            (7, 'Vehicles'),
            (8, 'Entertainment')
        """,
    )
    op.create_table(
        "subcategories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
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
            (1, 1, 'Hats'),
            (2, 2, 'Toys'),
            (3, 3, 'Shovels'),
            (4, 4, 'Soap'),
            (5, 5, 'Laptops'),
            (6, 6, 'Books'),
            (7, 7, 'Wheels'),
            (8, 8, 'Puzzles')
        """
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subcategory_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["subcategory_id"],
            ["subcategories.id"],
            ondelete="CASCADE",
        )
    )
    op.execute(
        """
        INSERT INTO products (id, subcategory_id, name, description, quantity) VALUES
            (1, 1, 'Big hat', 'Nice hat', 10),
            (2, 2, 'Godzilla toy', 'He is terrifying', 5),
            (3, 3, 'Wide shovel', 'It is so wide', 200),
            (4, 4, 'Most soapest soap', 'So soapy', 1000),
            (5, 5, 'Thinkpad T470', 'Great laptop', 3),
            (6, 6, 'DDD', 'Dive into DDD', 19),
            (7, 7, 'Big wheel', 'Big enough for tractors', 888),
            (8, 8, 'Colorful puzzles', 'Red, yellow, blue and more...', 444)
        """
    )


def downgrade() -> None:
    op.drop_table("categories")
    op.drop_table("subcategories")
    op.drop_table("products")
