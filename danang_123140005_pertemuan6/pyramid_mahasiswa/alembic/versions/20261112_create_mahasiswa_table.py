"""create mahasiswa table

Revision ID: 4a9f3b8c2d1e
Revises: 
Create Date: 2026-11-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a9f3b8c2d1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mahasiswa',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nim', sa.Text(), nullable=False),
        sa.Column('nama', sa.Text(), nullable=False),
        sa.Column('jurusan', sa.Text(), nullable=False),
        sa.Column('tanggal_lahir', sa.Date(), nullable=True),
        sa.Column('alamat', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_mahasiswa')),
        sa.UniqueConstraint('nim', name=op.f('uq_mahasiswa_nim'))
    )


def downgrade():
    op.drop_table('mahasiswa')
