"""initial schema

Revision ID: 7c67fc371bc8
Revises: 
Create Date: 2024-02-22 13:58:45.387684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c67fc371bc8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('displayname', sa.String(), nullable=False),
    sa.Column('groups', sa.JSON(), nullable=False),
    sa.Column('roles', sa.JSON(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subject')
    )
    op.create_table('jobqueue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.Enum('NEW', 'PENDING', 'COMPLETE', 'FAILED', name='jobstate'), nullable=False),
    sa.Column('worker', sa.String(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('function_call', sa.String(), nullable=False),
    sa.Column('parameters', sa.JSON(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('short_code', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('groups', sa.JSON(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_code')
    )
    op.create_table('sysconfig',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key', 'user_id')
    )
    op.create_table('specifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('minimum', sa.Float(), nullable=False),
    sa.Column('typical', sa.Float(), nullable=False),
    sa.Column('maximum', sa.Float(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testruns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('short_code', sa.String(), nullable=True),
    sa.Column('dut_id', sa.String(), nullable=False),
    sa.Column('machine_hostname', sa.String(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('test_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Enum('NEW', 'SETUP_COMPLETE', 'RUNNING', 'INTERRUPTED', 'COMPLETE', 'FAILED', name='testrunstate'), nullable=False),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_code')
    )
    op.create_table('measurement_columns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('data_source', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_note', sa.String(), nullable=True),
    sa.Column('measurement_unit', sa.String(), nullable=True),
    sa.Column('flags', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('specification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['specification_id'], ['specifications.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testrun_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('content', sa.LargeBinary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('testrun_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['testrun_id'], ['testruns.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('forcing_conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sequence_number', sa.Integer(), nullable=False),
    sa.Column('numeric_value', sa.Float(), nullable=True),
    sa.Column('string_value', sa.String(), nullable=True),
    sa.Column('column_id', sa.Integer(), nullable=False),
    sa.Column('testrun_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['column_id'], ['measurement_columns.id'], ),
    sa.ForeignKeyConstraint(['testrun_id'], ['testruns.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measurement_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sequence_number', sa.Integer(), nullable=False),
    sa.Column('numeric_value', sa.Float(), nullable=True),
    sa.Column('string_value', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('flags', sa.Integer(), nullable=True),
    sa.Column('testrun_id', sa.Integer(), nullable=False),
    sa.Column('column_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['column_id'], ['measurement_columns.id'], ),
    sa.ForeignKeyConstraint(['testrun_id'], ['testruns.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # don't do anything when trying to downgrade the initial table creation
    # it's *very* unexpected that a user would want to clear a database that way
    pass
