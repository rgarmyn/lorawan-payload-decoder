import math
from payload_decoder.decoder_utils import (
    ModulePayloadStandard,
    hex_payload_to_datetime,
    standard_payload,
)
from .unit_mapping import (
    DIF_VIF_MAPPING,
    ModulePayloadExtendedTelegram1,
    ModulePayloadExtendedTelegram2,
    scheduled_extended_plus_telegram1,
    scheduled_extended_plus_telegram2,
)


def decode_cmi4110(
    payload_arr,
) -> ModulePayloadStandard | ModulePayloadExtendedTelegram1 | ModulePayloadExtendedTelegram2:

    if payload_arr[0] not in ["00", "3f", "40"]:
        raise ValueError("payload message type is unknown")
    return decode_cmi4110_standard(payload_arr)
    # elif payload_arr[0] == "3f":
    # print("message type SCHEDULED_EXTENDED_PLUS")
    # print("decoding first telegram")
    # return decode_cmi4110_scheduled_extended_plus_telegram1(payload_arr)
    # elif payload_arr[0] == "40":
    #     print("message type SCHEDULED_EXTENDED_PLUS")
    #     print("decoding second telegram")
    #     return decode_cmi4110_scheduled_extended_plus_telegram2(payload_arr)
    # else:
    #     raise ValueError("payload message type is unknown")


def decode_cmi4110_standard(
    payload_arr: list[str],
) -> ModulePayloadStandard | ModulePayloadExtendedTelegram1 | ModulePayloadExtendedTelegram2:
    decoded_dictionary = {}
    i = 1
    energy_count = 0
    while i < len(payload_arr):
        dif = payload_arr[i].lower()
        dif_int = int(dif, 16)
        vif, i = decode_vif(payload_arr, i)
        bcd_len = dif_int if 2 <= dif_int <= 4 else dif_int - 8
        if len(payload_arr[i:]) <= 3:  # end of payload: error flag
            vif += payload_arr[i]
            i += 1

        if dif not in DIF_VIF_MAPPING or vif not in DIF_VIF_MAPPING[dif]:
            raise ValueError(f"Unknown dif {dif} and vif {vif}")
        reversed_values = "".join(
            reversed(payload_arr[i : i + bcd_len])
        )  # Little-endian (LSB)
        value_int = check_negative_value(reversed_values)
        i += bcd_len

        unit_info = DIF_VIF_MAPPING[dif][vif]
        register = unit_info["measure"]
        match register:
            case "datetime":
                value = hex_payload_to_datetime(reversed_values)
            case "energy":
                if energy_count == 0:
                    pass
                elif energy_count < 4:
                    register = f"energy_tariff_{str(energy_count)}"
                else:
                    raise ValueError("more than 4 energy registers")
                energy_count += 1
                value = int(reversed_values) / math.pow(10, unit_info["decimal"])
            case "flow" | "power":
                value = value_int / math.pow(10, unit_info["decimal"])
            case _:  # default
                value = (
                    int(reversed_values) / math.pow(10, unit_info["decimal"])
                    if unit_info["unit"]
                    else int(reversed_values)
                )
        decoded_dictionary[register] = value

    if "datetime_heat_meter" in decoded_dictionary:
        if "energy_tariff_1" in decoded_dictionary:
            print("message type SCHEDULED_EXTENDED_PLUS - telegram 1")
            return scheduled_extended_plus_telegram1(decoded_dictionary)
        print("message type SCHEDULED_EXTENDED_PLUS - telegram 2")
        return scheduled_extended_plus_telegram2(decoded_dictionary)
    print("message type STANDARD")
    return standard_payload(decoded_dictionary)


def check_negative_value(reversed_values: str) -> int:
    return (
        -int(reversed_values.replace("f0", ""))
        if "f0" in reversed_values
        else int(reversed_values)
    )


def decode_vif(payload_arr, index):
    dif = payload_arr[index].lower()
    dif_value = int(dif, 16)
    if dif_value == 132:
        vif = "".join(payload_arr[index + 1 : index + 3]).lower()
        return vif, index + 3
    else:
        vif = payload_arr[index + 1].lower()
        return vif, index + 2


def get_dib(payload_arr: list[str], i) -> tuple[str, str, str, int, int]:
    """
    Get the data information block (DIB) from the payload array
    """
    dif = payload_arr[i].lower()
    dif_int = int(dif, 16)
    if dif_int not in {2, 3, 4, 9, 10, 11, 12, 132}:
        raise ValueError("dif not valid")

    vif, i = decode_vif(payload_arr, i)
    bcd_len = dif_int if 2 <= dif_int <= 4 else dif_int - 8
    if len(payload_arr[i:]) <= 3:  # end of payload: error flag
        vif += payload_arr[i]
        i += 1
    reversed_values = "".join(
        reversed(payload_arr[i : i + bcd_len])
    )  # Little-endian (LSB)
    value_int = (
        -int(reversed_values.replace("f0", ""))
        if "f0" in reversed_values
        else int(reversed_values)
    )
    i += bcd_len
    return dif, vif, reversed_values, value_int, i


# def decode_cmi4110_scheduled_extended_plus_telegram1(
#     payload_arr: list[str],
# ) -> ModulePayloadExtendedTelegram1:


# def decode_cmi4110_scheduled_extended_plus_telegram2(
#     payload_arr: list[str],
# ) -> ModulePayloadStandard:
#     # TODO
#     decoded_dictionary = init_decoded_dict()
#     return decoded_dictionary
