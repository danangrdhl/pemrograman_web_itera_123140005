"""create matakuliah table

Revision ID: 7b8c9d0e1f2a
Revises: 4a9f3b8c2d1e
Create Date: 2026-11-12 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b8c9d0e1f2a'
down_revision = '4a9f3b8c2d1e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'matakuliah',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('kode_mk', sa.Text(), nullable=False),
        sa.Column('nama_mk', sa.Text(), nullable=False),
        sa.Column('sks', sa.Integer(), nullable=False),
        sa.Column('semester', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_matakuliah')),
        sa.UniqueConstraint('kode_mk', name=op.f('uq_matakuliah_kode_mk'))
    )


def downgrade():
    op.drop_table('matakuliah')
