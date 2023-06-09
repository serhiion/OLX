"""empty message

Revision ID: 6d72b935b134
Revises: 56535eaae860
Create Date: 2023-05-02 14:32:28.427283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d72b935b134'
down_revision = '56535eaae860'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
