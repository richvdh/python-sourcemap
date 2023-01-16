from typing import Tuple, Mapping, Iterable

import python_sourcemap.decoder
from python_sourcemap.decoder import DecodedMapping


def decode_mappings(mappings: str) -> Iterable[Mapping[int, DecodedMapping]]:
    """Decode the source mappings

    @returns:
        For each line, a dict from column number to its source location
    """
    dec = python_sourcemap.decoder.Decoder()
    return dec.decode_mappings(mappings)


__all__ = ["DecodedMapping", "decode_mappings"]
