"""empty message

Revision ID: 5a9322e77fc2
Revises: 4d4d27ce1907
Create Date: 2019-05-15 11:30:28.975634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5a9322e77fc2'
down_revision = '4d4d27ce1907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decks', sa.Column('comment', sa.Text(), nullable=False, server_default=sa.text("''")))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decks', 'comment')
    # ### end Alembic commands ###
