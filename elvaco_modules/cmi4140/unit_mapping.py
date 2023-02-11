from typing import TypedDict
from datetime import datetime


class ModulePayloadExtendedTelegram1(TypedDict):
    energy: float
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


class ReadingConfig(TypedDict):
    measure: str
    unit: str
    decimal: int


MESSAGE_TYPE: dict[str, str] = {
    "15": "standard",
    "3b": "extended_telegram_1",
    "3c": "extended_telegram_2",
}

DIF_VIF_MAPPING: dict[str, dict[str, ReadingConfig]] = {
    "04": {
        "00": {"measure": "energy", "unit": "kWh", "decimal": 6},
        "01": {"measure": "energy", "unit": "kWh", "decimal": 5},
        "02": {"measure": "energy", "unit": "kWh", "decimal": 4},
        "03": {"measure": "energy", "unit": "kWh", "decimal": 3},
        "04": {"measure": "energy", "unit": "kWh", "decimal": 2},
        "05": {"measure": "energy", "unit": "kWh", "decimal": 1},
        "06": {"measure": "energy", "unit": "kWh", "decimal": 0},
        "07": {"measure": "energy", "unit": "kWh", "decimal": -1},
        "11": {"measure": "volume", "unit": "m3", "decimal": 5},
        "12": {"measure": "volume", "unit": "m3", "decimal": 4},
        "13": {"measure": "volume", "unit": "m3", "decimal": 3},
        "14": {"measure": "volume", "unit": "m3", "decimal": 2},
        "15": {"measure": "volume", "unit": "m3", "decimal": 1},
        "16": {"measure": "volume", "unit": "m3", "decimal": 0},
        "17": {"measure": "volume", "unit": "m3", "decimal": -1},
        "fd17": {"measure": "error_flag", "unit": "", "decimal": 0},
        "6d": {"measure": "datetime_heat_meter", "unit": "", "decimal": 0},
    },
    "02": {
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
        "58": {"measure": "forward_temperature", "unit": "°C", "decimal": 3},
        "59": {"measure": "forward_temperature", "unit": "°C", "decimal": 2},
        "5a": {"measure": "forward_temperature", "unit": "°C", "decimal": 1},
        "5b": {"measure": "forward_temperature", "unit": "°C", "decimal": 0},
        "5c": {"measure": "return_temperature", "unit": "°C", "decimal": 3},
        "5d": {"measure": "return_temperature", "unit": "°C", "decimal": 2},
        "5e": {"measure": "return_temperature", "unit": "°C", "decimal": 1},
        "5f": {"measure": "return_temperature", "unit": "°C", "decimal": 0},
        "fd17": {"measure": "error_flag", "unit": "", "decimal": 0},
    },
    "0c": {"78": {"measure": "serial_from_message", "unit": "", "decimal": 0}},
    "84": {
        "0201": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 5},
        "0202": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 4},
        "0203": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 3},
        "0204": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 2},
        "0205": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 1},
        "0206": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 0},
        "0207": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": -1},
        "2001": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 5},
        "2002": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 4},
        "2003": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 3},
        "2004": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 2},
        "2005": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 1},
        "2006": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": 0},
        "2007": {"measure": "energy_tariff_2", "unit": "kWh", "decimal": -1},
        "0301": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 5},
        "0302": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 4},
        "0303": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 3},
        "0304": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 2},
        "0305": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 1},
        "0306": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 0},
        "0307": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": -1},
        "3001": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 5},
        "3002": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 4},
        "3003": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 3},
        "3004": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 2},
        "3005": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 1},
        "3006": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": 0},
        "3007": {"measure": "energy_tariff_3", "unit": "kWh", "decimal": -1},
    },
}
