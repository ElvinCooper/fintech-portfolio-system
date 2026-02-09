"""eliminar el campo cartera_id

Revision ID: 819586e43166
Revises: 5c39e1eb977f
Create Date: 2026-02-09 20:25:26.999951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '819586e43166'
down_revision: Union[str, Sequence[str], None] = '5c39e1eb977f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Eliminar columna cartera_id de productos."""
    # DROP COLUMN CASCADE CONSTRAINTS
    op.execute('ALTER TABLE productos DROP COLUMN cartera_id CASCADE CONSTRAINTS')


def downgrade() -> None:
    """Revertir: agregar cartera_id de nuevo."""
    op.add_column('productos',
        sa.Column('cartera_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key('fk_productos_cartera',
        'productos', 'cartera', ['cartera_id'], ['id'])