"""empty message

Revision ID: d9fccc19d12e
Revises: 89fdc9bbd801
Create Date: 2022-07-08 18:07:59.884833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd9fccc19d12e'
down_revision = '89fdc9bbd801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Planets_ibfk_1', 'Planets', type_='foreignkey')
    op.drop_column('Planets', 'user_id')
    op.drop_constraint('characters_ibfk_1', 'characters', type_='foreignkey')
    op.drop_column('characters', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('characters_ibfk_1', 'characters', 'user', ['user_id'], ['id'])
    op.add_column('Planets', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Planets_ibfk_1', 'Planets', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
