"""add sharelink tank

Revision ID: b7d41e9c2a10
Revises: 9336044ae156
Create Date: 2026-11-01 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d41e9c2a10'
down_revision = '9336044ae156'
branch_labels = None
depends_on = None


def upgrade():
    # server_default fills existing rows with D12, the tank they were shown until now
    with op.batch_alter_table('sharelink', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tank', sa.Integer(), server_default='24', nullable=False))


def downgrade():
    with op.batch_alter_table('sharelink', schema=None) as batch_op:
        batch_op.drop_column('tank')
