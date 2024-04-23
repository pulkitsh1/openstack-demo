"""empty message

Revision ID: 84d0adef0613
Revises: aa7c2a54b43f
Create Date: 2024-04-18 11:48:27.955678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d0adef0613'
down_revision = 'aa7c2a54b43f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subnet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ip_version', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('gateway_ip', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subnet', schema=None) as batch_op:
        batch_op.drop_column('gateway_ip')
        batch_op.drop_column('ip_version')

    # ### end Alembic commands ###
