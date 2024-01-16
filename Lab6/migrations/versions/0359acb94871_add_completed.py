from alembic import op
import sqlalchemy as sa


revision = '0359acb94871'
down_revision = '4d3c2bef1b82'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('completed', sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('completed')
