"""add_sentiment_model_version_column

Revision ID: 38fbae3e45e2
Revises: a7b4ae11ab7b
Create Date: 2025-11-11 00:16:29.191054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38fbae3e45e2'
down_revision = 'a7b4ae11ab7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Agregar columna sentiment_model_version a la tabla reviews
    op.add_column('reviews', sa.Column('sentiment_model_version', sa.Text(), nullable=True, comment='Versión del modelo que realizó la predicción: v1, v2, etc.'))


def downgrade() -> None:
    # Eliminar columna sentiment_model_version
    op.drop_column('reviews', 'sentiment_model_version')
