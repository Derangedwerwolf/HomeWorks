"""Add confirmed column

Revision ID: 2ddaf378bb45
Revises: 783ce77982ef
Create Date: 2023-08-28 18:51:34.948910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ddaf378bb45'
down_revision: Union[str, None] = '783ce77982ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('access_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'access_token')
    # ### end Alembic commands ###
