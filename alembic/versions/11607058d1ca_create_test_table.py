"""create test_table

Revision ID: 11607058d1ca
Revises: 
Create Date: 2023-03-03 09:17:05.809754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11607058d1ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('username', sa.VARCHAR(45), nullable=False, unique=True),
        sa.Column('password', sa.VARCHAR(255), nullable=False),
        sa.Column('email', sa.VARCHAR(45), nullable=False, unique=True),
        sa.Column('role', sa.Enum('ADMIN', 'USER', 'VIEWER'), nullable=False)
    )
    op.create_table(
        'farm',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('name', sa.VARCHAR(45), nullable=False),
        sa.Column('maxHumidity', sa.Integer, nullable=False),
        sa.Column('minCO2', sa.Integer, nullable=False),
        sa.Column('lightStatus', sa.Boolean, nullable=False),
        sa.Column('ACTemp', sa.Integer, nullable=False),
        sa.Column('farmKey', sa.VARCHAR(45), nullable=False, unique=True)
    )
    op.create_table(
        'farmOwner',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('userId', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    )
    op.create_table(
        'temperatureSensor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('temperature', sa.Integer, nullable=False)
    )
    op.create_table(
        'AC',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.Column('status', sa.Boolean, nullable=False),
        sa.Column('temperature', sa.Integer, nullable=False),
        sa.Column('fanLevel', sa.Integer, nullable=False),
        sa.Column('automation', sa.Boolean, nullable=False),
        sa.Column('isAvailable', sa.Boolean, nullable=False)
    )
    op.create_table(
        'ACAutomation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('temperature', sa.Integer, nullable=False),
        sa.Column('startTime', sa.Time, nullable=False),
        sa.Column('endTime', sa.Time, nullable=False)
    )
    op.create_table(
        'humiditySensor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('humidity', sa.Integer, nullable=False)
    )
    op.create_table(
        'dehumidifier',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('status', sa.Boolean, nullable=False),
        sa.Column('isAvailable', sa.Boolean, nullable=False)

    )
    op.create_table(
        'CO2Sensor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('CO2', sa.Integer, nullable=False)

    )
    op.create_table(
        'CO2Controller',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('status', sa.Boolean, nullable=False),
        sa.Column('isAvailable', sa.Boolean, nullable=False)
    )
    op.create_table(
        'wateringAutomation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('startTime', sa.Time, nullable=False),
        sa.Column('endTime', sa.Time, nullable=False)
    )
    op.create_table(
        'light',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('name', sa.VARCHAR(45), nullable=False),
        sa.Column('status', sa.Boolean, nullable=False),
        sa.Column('isAvailable', sa.Boolean, nullable=False),
        sa.Column('automation', sa.Boolean, nullable=False),
        sa.Column('UVLightDensity', sa.Integer, nullable=False),
        sa.Column('IRLightDensity', sa.Integer, nullable=False),
        sa.Column('naturalLightDensity', sa.Integer, nullable=False)
    )
    op.create_table(
        'farmLightPreset',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('name', sa.VARCHAR(255), nullable=False)

    )
    op.create_table(
        'lightPresetAutomation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('startTime', sa.Time, nullable=False),
        sa.Column('endTime', sa.Time, nullable=False),
        sa.Column('farmLightPresetId', sa.Integer, nullable=False)

    )
    op.create_table(
        'lightCombination',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('lightId', sa.Integer, sa.ForeignKey('light.id'), nullable=False),
        sa.Column('farmLightPresetId', sa.Integer, sa.ForeignKey('farmLightPreset.id'), nullable=False),
        sa.Column('automation', sa.Boolean, nullable=False),
        sa.Column('UVLightDensity', sa.Integer, nullable=False),
        sa.Column('IRLightDensity', sa.Integer, nullable=False),
        sa.Column('naturalLightDensity', sa.Integer, nullable=False)

    )
    op.create_table(
        'MQTTMap',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('hardwareType', sa.Enum('LIGHT','AC','CO2_SENSOR','CO2_CONTROLLER','DEHUMIDIFIER','HUMIDITY_SENSOR',
                                          'TEMPERATURE_SENSOR','WATERING'), nullable=False),
        sa.Column('hardwareId', sa.Integer, nullable=False),
        sa.Column('ESPId', sa.Integer, nullable=False),
        sa.Column('ESPType', sa.Enum('SENSOR','CO2_CONTROLLER','LIGHT_CONTROLLER','AC_CONTROLLER',
                                     'DEHUMIDIFIER_CONTROLLER','WATERING_SYSTEM'), nullable=False)

    )
    op.create_table(
        'waterController',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customData', sa.JSON, nullable=True),
        sa.Column('createAt', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updateAt', sa.DateTime, nullable=False, server_default=sa.func.now(),
                  onupdate=sa.func.now()),
        sa.Column('deleteAt', sa.DateTime, nullable=True),
        sa.Column('createBy', sa.VARCHAR(45), nullable=False),
        sa.Column('updateBy', sa.VARCHAR(45), nullable=False),
        sa.Column('deleteBy', sa.VARCHAR(45), nullable=True),

        sa.Column('farmId', sa.Integer, sa.ForeignKey('farm.id'), nullable=False),
        sa.Column('automation', sa.Boolean, nullable=False),
        sa.Column('isAvailable', sa.Boolean, nullable=False)
    )


def downgrade():
    op.drop_table('waterController')
    op.drop_table('MQTTMap')
    op.drop_table('lightPresetAutomation')
    op.drop_table('lightCombination')
    op.drop_table('farmLightPreset')
    op.drop_table('light')
    op.drop_table('wateringAutomation')
    op.drop_table('CO2Controller')
    op.drop_table('CO2Sensor')
    op.drop_table('dehumidifier')
    op.drop_table('humiditySensor')
    op.drop_table('ACAutomation')
    op.drop_table('AC')
    op.drop_table('temperatureSensor')
    op.drop_table('farmOwner')
    op.drop_table('user')
    op.drop_table('farm')
