"""editing the database

Revision ID: 04fcaa523131
Revises: 
Create Date: 2024-06-03 12:52:04.040184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04fcaa523131'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('middle_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('instagram_account')
        batch_op.drop_column('twitter_account')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('twitter_account', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('instagram_account', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.alter_column('middle_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
