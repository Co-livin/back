"""fix_delete

Revision ID: 7b8e4428aad3
Revises: 63384434de41
Create Date: 2026-04-08 10:14:04.130314

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '7b8e4428aad3'
down_revision: Union[str, Sequence[str], None] = '63384434de41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_constraint('events_related_task_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_related_task_id_fkey', 
        'events', 'tasks', 
        ['related_task_id'], ['id'], 
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint('events_related_task_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(
        'events_related_task_id_fkey', 
        'events', 'tasks', 
        ['related_task_id'], ['id']
    )
