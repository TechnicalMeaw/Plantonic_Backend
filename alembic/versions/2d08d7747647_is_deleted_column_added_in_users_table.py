"""is_deleted column added in users table

Revision ID: 2d08d7747647
Revises: 0c76b41991e4
Create Date: 2024-03-03 20:23:22.111915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d08d7747647'
down_revision = '0c76b41991e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('False'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_deleted')
    # ### end Alembic commands ###