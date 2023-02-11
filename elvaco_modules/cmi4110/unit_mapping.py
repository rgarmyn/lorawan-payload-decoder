from typing import TypedDict
from datetime import datetime


class ModulePayloadExtendedTelegram1(TypedDict):
    energy: float
    energy_tariff_1: float
    energy_tariff_2: float
    energy_tariff_3: float
    serial_from_message: int
    datetime_heat_meter: datetime


class ModulePayloadExtendedTelegram2(TypedDict):
    volume: float
    power: float
    flow: float
    forward_temperature: float
    return_temperature: float
    serial_from_message: int
    error_flag: float
    datetime_heat_meter: datetime


def scheduled_extended_plus_telegram1(
    decoded_dictionary: dict,
) -> ModulePayloadExtendedTelegram1:
    return ModulePayloadExtendedTelegram1(
        energy=decoded_dictionary["energy"],
        energy_tariff_1=decoded_dictionary["energy_tariff_1"],
        energy_tariff_2=decoded_dictionary["energy_tariff_2"],
        energy_tariff_3=decoded_dictionary["energy_tariff_3"],
        serial_from_message=decoded_dictionary["serial_from_message"],
        datetime_heat_meter=decoded_dictionary["datetime_heat_meter"],
    )


def scheduled_extended_plus_telegram2(
    decoded_dictionary: dict,
) -> ModulePayloadExtendedTelegram2:
    return ModulePayloadExtendedTelegram2(
        volume=decoded_dictionary["volume"],
        power=decoded_dictionary["power"],
        flow=decoded_dictionary["flow"],
        forward_temperature=decoded_dictionary["forward_temperature"],
        return_temperature=decoded_dictionary["return_temperature"],
        serial_from_message=decoded_dictionary["serial_from_message"],
        error_flag=decoded_dictionary["error_flag"],
        datetime_heat_meter=decoded_dictionary["datetime_heat_meter"],
    )


class ReadingConfig(TypedDict):
    measure: str
    unit: str
    decimal: int


DIF_VIF_MAPPING: dict[str, dict[str, ReadingConfig]] = {
    "0c": {
        "06": {"measure": "energy", "unit": "kWh", "decimal": 0},
        "07": {"measure": "energy", "unit": "kWh", "decimal": -1},
        # "FB00": {"measure": "energy", "unit": "kWh", "decimal": -3},
        # "FB01": {"measure": "energy", "unit": "kWh", "decimal": -3},
        "14": {"measure": "volume", "unit": "m3", "decimal": 2},
        "15": {"measure": "volume", "unit": "m3", "decimal": 1},
        "16": {"measure": "volume", "unit": "m3", "decimal": 0},
        "78": {"measure": "serial_from_message", "unit": "", "decimal": 0},
    },
    "0b": {
        "2a": {"measure": "power", "unit": "kW", "decimal": 4},
        "2b": {"measure": "power", "unit": "kW", "decimal": 3},
        "2c": {"measure": "power", "unit": "kW", "decimal": 2},
        "2d": {"measure": "power", "unit": "kW", "decimal": 1},
        "2e": {"measure": "power", "unit": "kW", "decimal": 0},
        "2f": {"measure": "power", "unit": "kW", "decimal": -1},
        "3b": {"measure": "flow", "unit": "m3/h", "decimal": 3},
        "3c": {"measure": "flow", "unit": "m3/h", "decimal": 2},
        "3d": {"measure": "flow", "unit": "m3/h", "decimal": 1},
        "3e": {"measure": "flow", "unit": "m3/h", "decimal": 0},
        "3f": {"measure": "flow", "unit": "m3/h", "decimal": -1},
    },
    "0a": {
        "5a": {"measure": "forward_temperature", "unit": "°C", "decimal": 1},
        "5b": {"measure": "forward_temperature", "unit": "°C", "decimal": 0},
        "5e": {"measure": "return_temperature", "unit": "°C", "decimal": 1},
        "5f": {"measure": "return_temperature", "unit": "°C", "decimal": 0},
    },
    "02": {"fd17": {"measure": "error_flag", "unit": "", "decimal": 0}},
    "04": {"fd17": {"measure": "error_flag", "unit": "", "decimal": 0}},
}
