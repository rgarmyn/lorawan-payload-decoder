from typing import TypedDict


class ModulePayload(TypedDict):
    energy: float
    volume: float
    power: float
    flow: float
    forward_temperature: float
    return_temperature: float
    serial_from_message: int
    error_flag: float


def reverse_little_endian(list_of_values: list[str]) -> str:
    """
    Most significant byte is last in the list
    """
    list_of_values.reverse()
    return "".join(list_of_values)


def separate_payload(payload: str) -> list[str]:
    return [payload[i : i + 2] for i in range(0, len(payload), 2)]


def init_decoded_dict() -> ModulePayload:
    d: ModulePayload = {
        "energy": 0,
        "volume": 0,
        "power": 0,
        "flow": 0,
        "forward_temperature": 0,
        "return_temperature": 0,
        "serial_from_message": 0,
        "error_flag": 0,
    }
    return d
