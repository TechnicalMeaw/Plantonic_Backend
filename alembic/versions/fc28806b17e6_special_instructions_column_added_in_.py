"""special_instructions column added in ordwes table

Revision ID: fc28806b17e6
Revises: bf0c0dd9f16b
Create Date: 2024-01-13 01:31:48.766999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc28806b17e6'
down_revision = 'bf0c0dd9f16b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('special_instructions', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'special_instructions')
    # ### end Alembic commands ###
