"""Add imagem_produto table

Revision ID: 656ff02770c5
Revises: 744fd54da892
Create Date: 2025-07-07 18:43:07.099372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '656ff02770c5'
down_revision = '744fd54da892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.String(length=100), nullable=False),
    sa.Column('senha', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('usuario')
    )
    op.create_table('imagem_produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_arquivo', sa.String(length=200), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.drop_column('imagem')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagem', sa.VARCHAR(length=120), nullable=True))

    op.drop_table('imagem_produto')
    op.drop_table('admin')
    # ### end Alembic commands ###
