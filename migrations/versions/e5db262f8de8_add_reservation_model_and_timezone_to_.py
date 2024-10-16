"""Add Reservation model and timezone to User

Revision ID: e5db262f8de8
Revises: 50af48b86c7a
Create Date: 2024-10-14 17:15:59.852235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5db262f8de8'
down_revision = '50af48b86c7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reminder_sent', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timezone', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('timezone')

    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('confirmed')
        batch_op.drop_column('reminder_sent')

    # ### end Alembic commands ###
