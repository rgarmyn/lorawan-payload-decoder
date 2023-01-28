import math
from payload_decoder.decoder_utils import (
    ModulePayload,
    reverse_little_endian,
    init_decoded_dict,
)


def decode_cmi4110(payload_arr) -> ModulePayload:
    decoded_dictionary = init_decoded_dict()
    if payload_arr[0] != "00":  # message_type = "Standard"
        raise ValueError("payload message type is unknown")
    i = 1
    while i < len(payload_arr):
        is_valid_dif = False
        dif = payload_arr[i]
        vif = payload_arr[i + 1]
        dif_int = int(dif, 16)
        i += 2
        if 9 <= dif_int <= 12 or dif_int:
            is_valid_dif = True
        if not is_valid_dif:
            raise ValueError("dif is not valid")

        bcd_len = dif_int if 2 <= dif_int <= 4 else dif_int - 8
        if len(payload_arr[i:]) <= 3:  # end of payload: error flag
            vif = vif + payload_arr[i]
            i += 1
        reversed_values = reverse_little_endian(payload_arr[i : i + bcd_len])
        if "f0" in reversed_values:  # value_int can be negative
            value_int = -int(reversed_values.replace("f0", ""))
        else:
            value_int = int(reversed_values)

        i += bcd_len
        match dif.lower() + vif.lower():
            case "0c06" | "0c07":  # Convert all to kWh (0406)
                decoded_dictionary["energy"] = int(reversed_values) / math.pow(
                    10, int("06", 16) - int(vif, 16)
                )
            case "0c14" | "0c15" | "0c16":  # Convert all to m3 (0416)
                decoded_dictionary["volume"] = int(reversed_values) / math.pow(
                    10, int("16", 16) - int(vif, 16)
                )
            case "0b2a" | "0b2b" | "0b2c" | "0b2d" | "0b2e" | "0b2f":  # Convert all to kW (022e)
                decoded_dictionary["power"] = value_int / math.pow(
                    10, int("2e", 16) - int(vif, 16)
                )
            case "0b3b" | "0b2c" | "0b3d" | "0b3e":  # Convert all to m3/h (023e)
                decoded_dictionary["flow"] = value_int / math.pow(
                    10, int("3e", 16) - int(vif, 16)
                )
            case "0a5a" | "0a5b":  # Convert all to °C (025b)
                decoded_dictionary["forward_temperature"] = int(
                    reversed_values
                ) / math.pow(10, int("5b", 16) - int(vif, 16))

            case "0a5e" | "0a5f":  # Convert all to °C (025f)
                decoded_dictionary["return_temperature"] = int(
                    reversed_values
                ) / math.pow(10, int("5f", 16) - int(vif, 16))

            case "0c78":
                decoded_dictionary["serial_from_message"] = int(reversed_values)
            case "04fd17":
                decoded_dictionary["error_flag"] = int(reversed_values)
    return decoded_dictionary
