import math
from payload_decoder.decoder_utils import (
    ModulePayloadStandard,
    hex_payload_to_datetime,
    standard_payload,
)
from .unit_mapping import (
    DIF_VIF_MAPPING,
    MESSAGE_TYPE,
    ModulePayloadExtendedTelegram1,
    ModulePayloadExtendedTelegram2,
)


def decode_cmi4140(
    payload_arr,
) -> ModulePayloadStandard | ModulePayloadExtendedTelegram1 | ModulePayloadExtendedTelegram2:
    if payload_arr[0] not in ["15", "3b", "3c"]:
        raise ValueError("payload type is unknown")
    print(f"message type {MESSAGE_TYPE[payload_arr[0]]}")
    return decode_cmi4140_standard(payload_arr)


def decode_cmi4140_standard(
    payload_arr: list[str],
) -> ModulePayloadStandard | ModulePayloadExtendedTelegram1 | ModulePayloadExtendedTelegram2:
    decoded_dictionary = {}
    i = 1
    while i < len(payload_arr):
        dif = payload_arr[i].lower()
        dif_int = int(dif, 16)
        vif, i = decode_vif(payload_arr, i)
        bcd_len = dif_int if 2 <= dif_int <= 4 else 4
        if len(payload_arr[i:]) <= 5 and vif == "fd":  # end of payload: error flag
            vif = vif + payload_arr[i]
            i += 1
        if dif not in DIF_VIF_MAPPING or vif not in DIF_VIF_MAPPING[dif]:
            raise ValueError(f"Unknown dif {dif} and vif {vif}")
        reversed_values = "".join(
            reversed(payload_arr[i : i + bcd_len])
        )  # Little-endian (LSB)
        i += bcd_len

        unit_info = DIF_VIF_MAPPING[dif][vif]
        if unit_info["measure"] == "datetime_heat_meter":
            value = hex_payload_to_datetime(reversed_values)
        else:
            value = (
                int(reversed_values, 16) / math.pow(10, unit_info["decimal"])
                if unit_info["unit"]
                else int(reversed_values)
            )
        decoded_dictionary[unit_info["measure"]] = value
    if "datetime_heat_meter" in decoded_dictionary:
        if "energy_tariff_2" in decoded_dictionary:
            return scheduled_extended_plus_telegram1(decoded_dictionary)
        return scheduled_extended_plus_telegram2(decoded_dictionary)
    return standard_payload(decoded_dictionary)


def decode_vif(payload_arr, index):
    dif = payload_arr[index].lower()
    dif_value = int(dif, 16)
    if dif_value == 132:
        vif = "".join(payload_arr[index + 1 : index + 3]).lower()
        return vif, index + 3
    else:
        vif = payload_arr[index + 1].lower()
        return vif, index + 2


def scheduled_extended_plus_telegram1(
    decoded_dictionary: dict,
) -> ModulePayloadExtendedTelegram1:
    return ModulePayloadExtendedTelegram1(
        energy=decoded_dictionary["energy"],
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
