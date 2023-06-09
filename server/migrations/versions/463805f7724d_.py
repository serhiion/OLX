"""empty message

Revision ID: 463805f7724d
Revises: 6d72b935b134
Create Date: 2023-05-02 16:44:50.314248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '463805f7724d'
down_revision = '6d72b935b134'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.drop_index('ix_advertisements_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.create_index('ix_advertisements_name', ['name'], unique=False)

    # ### end Alembic commands ###
