from alembic import op
import sqlalchemy as sa

revision = 'new_migration_add_completed'
down_revision = 'new_migration_add_db'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('completed', sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('completed')
