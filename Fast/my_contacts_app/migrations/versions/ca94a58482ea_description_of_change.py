"""description_of_change

Revision ID: ca94a58482ea
Revises: 
Create Date: 2023-08-23 13:56:18.125314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca94a58482ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_email'), 'contacts', ['email'], unique=True)
    op.create_index(op.f('ix_contacts_first_name'), 'contacts', ['first_name'], unique=False)
    op.create_index(op.f('ix_contacts_id'), 'contacts', ['id'], unique=False)
    op.create_index(op.f('ix_contacts_last_name'), 'contacts', ['last_name'], unique=False)
    op.create_index(op.f('ix_contacts_phone_number'), 'contacts', ['phone_number'], unique=False)
    op.drop_index('ix_notes_id', table_name='notes')
    op.drop_table('notes')
    op.drop_index('ix_cats_id', table_name='cats')
    op.drop_index('ix_cats_nick', table_name='cats')
    op.drop_table('cats')
    op.drop_index('ix_owners_email', table_name='owners')
    op.drop_index('ix_owners_id', table_name='owners')
    op.drop_table('owners')
    op.drop_index('ix_todos_description', table_name='todos')
    op.drop_index('ix_todos_title', table_name='todos')
    op.drop_table('todos')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('login', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('login', name='users_login_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='todos_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_index('ix_todos_title', 'todos', ['title'], unique=False)
    op.create_index('ix_todos_description', 'todos', ['description'], unique=False)
    op.create_table('owners',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('owners_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='owners_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_owners_id', 'owners', ['id'], unique=False)
    op.create_index('ix_owners_email', 'owners', ['email'], unique=False)
    op.create_table('cats',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nick', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vaccinated', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], name='cats_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='cats_pkey')
    )
    op.create_index('ix_cats_nick', 'cats', ['nick'], unique=False)
    op.create_index('ix_cats_id', 'cats', ['id'], unique=False)
    op.create_table('notes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='notes_pkey')
    )
    op.create_index('ix_notes_id', 'notes', ['id'], unique=False)
    op.drop_index(op.f('ix_contacts_phone_number'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_last_name'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_first_name'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_email'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###
