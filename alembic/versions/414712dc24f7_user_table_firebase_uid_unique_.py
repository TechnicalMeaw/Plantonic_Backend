"""user table firebase_uid unique constraint added

Revision ID: 414712dc24f7
Revises: 5a2e3b60c34d
Create Date: 2023-09-17 22:50:30.205658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414712dc24f7'
down_revision = '5a2e3b60c34d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['firebase_uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###