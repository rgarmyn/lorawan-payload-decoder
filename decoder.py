import pandas as pd
from typing import Optional, Literal
from decoder_utils import (
    ModulePayload,
    separate_payload,
)
from elvaco_modules.cmi4110.cmi4110_decoder import decode_cmi4110
from elvaco_modules.cmi4111.cmi4111_decoder import decode_cmi4111
from elvaco_modules.cmi4130.cmi4130_decoder import decode_cmi4130
from elvaco_modules.cmi4140.cmi4140_decoder import decode_cmi4140
from elvaco_modules.cmi4160.cmi4160_decoder import decode_cmi4160


def decode_payload(
    payload: str, sensor_type: Literal["cmi4110", "cmi4111", "cmi4130", "cmi4140", "cmi4160"]
) -> Optional[ModulePayload]:
    payload_arr = separate_payload(payload)
    try:
        func = globals()[f"decode_{sensor_type}"]
        return func(payload_arr)
    except (ValueError, KeyError):
        print("Error in decode_payload")
        return None


if __name__ == "__main__":
    (payload, model) = (
        "1e0407cc1e040004157a8c0c00022ce01d023c0301025a9003025e8c02077922988461a511400401fd1700",
        "cmi4160",
    )
    decoded_payload = decode_payload(payload, model)
    print(decoded_payload)
