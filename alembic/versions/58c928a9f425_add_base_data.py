"""add base data

Revision ID: 58c928a9f425
Revises: 11607058d1ca
Create Date: 2023-03-30 11:14:11.873368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58c928a9f425'
down_revision = '11607058d1ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_data = [
        {'username': 'Pond1', 'password': '$2a$12$6dhdabhOcPo2MjX3uNjPeeYzDfnvNLIdmeqYPaUK0/ICo.e/Doyc6', 'email': 'Pond1@example.com', 'role': 'USER', 'createBy': 'ADMIN', 'updateBy': 'ADMIN', 'verified': True},
        {'username': 'Pond2', 'password': '$2a$12$6dhdabhOcPo2MjX3uNjPeeYzDfnvNLIdmeqYPaUK0/ICo.e/Doyc6', 'email': 'Pond2@example.com', 'role': 'USER', 'createBy': 'ADMIN', 'updateBy': 'ADMIN', 'verified': True}
    ]
    table = sa.Table('user', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, user_data)

    farm_data = [
        {'name': 'Pond1\'s Farm',
         'maxHumidity': 3,
         'minCO2': 1000,
         'lightStatus': False,
         'ACTemp': 25,
         'farmKey': 'e16b124c457888545f978862c45d69ec',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'}
    ]
    table = sa.Table('farm', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, farm_data)

    ac_data = [
        {'farmId': 1,
         'name': 'AC1',
         'status': False,
         'temperature': 25,
         'fanLevel': 4,
         'automation': True,
         'isAvailable': True,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'name': 'AC2',
         'status': False,
         'temperature': 25,
         'fanLevel': 4,
         'automation': True,
         'isAvailable': True,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('AC', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, ac_data)

    co2_controller_data = [
        {'farmId': 1,
         'status': False,
         'isAvailable': True,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('CO2Controller', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, co2_controller_data)

    co2_sensor_data = [
        {'farmId': 1,
         'CO2': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'CO2': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'CO2': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'CO2': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('CO2Sensor', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, co2_sensor_data)

    dehumidifier_data = [
        {'farmId': 1,
         'status': False,
         'isAvailable': True,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('dehumidifier', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, dehumidifier_data)

    humidity_sensor_data = [
        {'farmId': 1,
         'humidity': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('humiditySensor', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, humidity_sensor_data)

    light_data = [
        {'farmId': 1,
         'name': 'Light1',
         'status': False,
         'isAvailable': True,
         'automation': True,
         'UVLightDensity': 50,
         'IRLightDensity': 50,
         'naturalLightDensity': 50,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'name': 'Light2',
         'status': False,
         'isAvailable': True,
         'automation': True,
         'UVLightDensity': 50,
         'IRLightDensity': 50,
         'naturalLightDensity': 50,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'name': 'Light3',
         'status': False,
         'isAvailable': True,
         'automation': True,
         'UVLightDensity': 50,
         'IRLightDensity': 50,
         'naturalLightDensity': 50,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'farmId': 1,
         'name': 'Light4',
         'status': False,
         'isAvailable': True,
         'automation': True,
         'UVLightDensity': 50,
         'IRLightDensity': 50,
         'naturalLightDensity': 50,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('light', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, light_data)

    temperature_sensor_data = [
        {'farmId': 1,
         'temperature': 0,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('temperatureSensor', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, temperature_sensor_data)

    water_controller_data = [
        {'farmId': 1,
         'automation': True,
         'isAvailable': True,
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('waterController', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, water_controller_data)

    MQTT_map_data = [
        {'hardwareType': 'HUMIDITY_SENSOR',
         'hardwareId': 1,
         'ESPId': 1,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'HUMIDITY_SENSOR',
         'hardwareId': 2,
         'ESPId': 2,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'HUMIDITY_SENSOR',
         'hardwareId': 3,
         'ESPId': 3,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'HUMIDITY_SENSOR',
         'hardwareId': 4,
         'ESPId': 4,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'TEMPERATURE_SENSOR',
         'hardwareId': 1,
         'ESPId': 1,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'TEMPERATURE_SENSOR',
         'hardwareId': 2,
         'ESPId': 2,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'TEMPERATURE_SENSOR',
         'hardwareId': 3,
         'ESPId': 3,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'TEMPERATURE_SENSOR',
         'hardwareId': 4,
         'ESPId': 4,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'CO2_SENSOR',
         'hardwareId': 1,
         'ESPId': 1,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'CO2_SENSOR',
         'hardwareId': 2,
         'ESPId': 2,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'CO2_SENSOR',
         'hardwareId': 3,
         'ESPId': 3,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'CO2_SENSOR',
         'hardwareId': 4,
         'ESPId': 4,
         'ESPType': 'SENSOR',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'AC',
         'hardwareId': 1,
         'ESPId': 5,
         'ESPType': 'AC_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'AC',
         'hardwareId': 2,
         'ESPId': 6,
         'ESPType': 'AC_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'LIGHT',
         'hardwareId': 1,
         'ESPId': 7,
         'ESPType': 'LIGHT_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'LIGHT',
         'hardwareId': 1,
         'ESPId': 8,
         'ESPType': 'LIGHT_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'LIGHT',
         'hardwareId': 1,
         'ESPId': 9,
         'ESPType': 'LIGHT_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'LIGHT',
         'hardwareId': 1,
         'ESPId': 10,
         'ESPType': 'LIGHT_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'DEHUMIDIFIER',
         'hardwareId': 1,
         'ESPId': 11,
         'ESPType': 'DEHUMIDIFIER_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'CO2_CONTROLLER',
         'hardwareId': 1,
         'ESPId': 12,
         'ESPType': 'CO2_CONTROLLER',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
        {'hardwareType': 'WATERING',
         'hardwareId': 1,
         'ESPId': 13,
         'ESPType': 'WATERING_SYSTEM',
         'createBy': 'ADMIN',
         'updateBy': 'ADMIN'},
    ]
    table = sa.Table('MQTTMap', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(table, MQTT_map_data)


def downgrade() -> None:
    op.execute("DELETE FROM MQTTMap")
    op.execute("DELETE FROM AC")
    op.execute("DELETE FROM CO2Controller")
    op.execute("DELETE FROM CO2Sensor")
    op.execute("DELETE FROM dehumidifier")
    op.execute("DELETE FROM humiditySensor")
    op.execute("DELETE FROM light")
    op.execute("DELETE FROM temperatureSensor")
    op.execute("DELETE FROM waterController")
    op.execute("DELETE FROM user")
    op.execute("DELETE FROM farm")


