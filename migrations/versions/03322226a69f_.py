"""empty message

Revision ID: 03322226a69f
Revises: 9403c9872083
Create Date: 2022-06-08 19:31:29.020579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03322226a69f'
down_revision = '9403c9872083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('height', sa.String(), nullable=True),
    sa.Column('hair_color', sa.String(), nullable=True),
    sa.Column('eye_color', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('characters')
    # ### end Alembic commands ###
