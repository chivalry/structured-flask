"""empty message

Revision ID: df36e048c49a
Revises: 9ead62ad44d6
Create Date: 2019-04-22 10:22:19.331553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df36e048c49a'
down_revision = '9ead62ad44d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_hash', sa.String(length=255), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('_hash')

    # ### end Alembic commands ###
