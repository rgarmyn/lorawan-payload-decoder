import math
from payload_decoder.decoder_utils import (
    ModulePayloadStandard,
    init_decoded_dict,
    reverse_little_endian,
)


def decode_cmi4160(payload_arr) -> ModulePayloadStandard:
    decoded_dictionary = init_decoded_dict()

    if payload_arr[0] != "1e":  # message_type = "Standard"
        raise ValueError("payload type is unknown")
    i = 1
    while i < len(payload_arr):
        is_valid_dif = False
        dif = payload_arr[i]
        vif = payload_arr[i + 1]
        dif_int = int(dif, 16)
        i += 2
        if 1 <= dif_int <= 4 or dif_int == 12 or dif_int == 7:
            is_valid_dif = True
        if not is_valid_dif:
            raise ValueError("No BCD value")
        bcd_len = dif_int if 2 <= dif_int <= 4 or dif_int == 7 else 4
        if len(payload_arr[i:]) <= 3:  # end of payload: error flag
            vif = vif + payload_arr[i]
            i += 1
        reversed_values = reverse_little_endian(payload_arr[i : i + bcd_len])
        i += bcd_len
        match dif.lower() + vif.lower():
            case "0402" | "0403" | "0404" | "0405" | "0406" | "0407":  # Convert all to kWh (0406)
                decoded_dictionary["energy"] = int(reversed_values, 16) / math.pow(
                    10, int("06", 16) - int(vif, 16)
                )
            case "0412" | "0413" | "0414" | "0415" | "0416" | "0417":  # Convert all to m3 (0416)
                decoded_dictionary["volume"] = int(reversed_values, 16) / math.pow(
                    10, int("16", 16) - int(vif, 16)
                )

            case "022a" | "022b" | "022c" | "022d" | "022e" | "022f":  # Convert all to kW (022e)
                decoded_dictionary["power"] = int(reversed_values, 16) / math.pow(
                    10, int("2e", 16) - int(vif, 16)
                )

            case "023b" | "023c" | "023d" | "023e" | "023f":  # Convert all to m3/h (023e)
                decoded_dictionary["flow"] = int(reversed_values, 16) / math.pow(
                    10, int("3e", 16) - int(vif, 16)
                )
            case "0258" | "0259" | "025a" | "025b":  # Convert all to °C (025b)
                decoded_dictionary["forward_temperature"] = int(
                    reversed_values, 16
                ) / math.pow(10, int("5b", 16) - int(vif, 16))

            case "025c" | "025d" | "025e" | "025f":  # Convert all to °C (025f)
                decoded_dictionary["return_temperature"] = int(
                    reversed_values, 16
                ) / math.pow(10, int("5f", 16) - int(vif, 16))

            case "0779":
                decoded_dictionary["serial_from_message"] = int(reversed_values[-8:])
                i += 1

            case "01fd17":
                decoded_dictionary["error_flag"] = int(reversed_values, 16)

    return decoded_dictionary
