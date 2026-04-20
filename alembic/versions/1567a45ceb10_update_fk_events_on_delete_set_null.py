"""update fk events on delete set null

Revision ID: 1567a45ceb10
Revises: 7b8e4428aad3
Create Date: 2026-04-20 13:35:45.659663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1567a45ceb10'
down_revision: Union[str, Sequence[str], None] = '7b8e4428aad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint('events_related_task_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_related_task_id_fkey', 
        source_table='events', 
        referent_table='tasks', 
        local_cols=['related_task_id'], 
        remote_cols=['id'], 
        ondelete='SET NULL'
    )

def downgrade():
    op.drop_constraint('events_related_task_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_related_task_id_fkey', 
        source_table='events', 
        referent_table='tasks', 
        local_cols=['related_task_id'], 
        remote_cols=['id']
    )
