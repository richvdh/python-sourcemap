# base64 decoder
from typing import List, Tuple, Dict, Mapping, Iterable

B64 = [0] * 127
for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'):
    B64[ord(c)] = i

# src_id, src_line, src_col, name_id
DecodedMapping = Tuple[int, int, int, int]


class Decoder(object):
    def parse_vlq(self, segment: str) -> List[int]:
        """
        Parse a string of VLQ-encoded data.

        Returns:
          a list of integers.
        """

        values = []

        cur, shift = 0, 0
        for c in segment:
            val = B64[ord(c)]
            # Each character is 6 bits:
            # 5 of value and the high bit is the continuation.
            val, cont = val & 0b11111, val >> 5
            cur += val << shift
            shift += 5

            if not cont:
                # The low bit of the unpacked value is the sign.
                cur, sign = cur >> 1, cur & 1
                if sign:
                    cur = -cur
                values.append(cur)
                cur, shift = 0, 0

        if cur or shift:
            raise Exception('leftover cur/shift in vlq decode')

        return values

    def decode_mappings(self, mappings: str) -> Iterable[Mapping[int, DecodedMapping]]:
        """Decode the source mappings

        @returns:
            For each line, a dict from column number to its source location
        """
        src_id, src_line, src_col, name_id = 0, 0, 0, 0

        for line in mappings.split(';'):
            line_index: Dict[int, DecodedMapping] = {}

            # dst_col resets every line
            dst_col = 0
            for segment in line.split(','):
                if not segment:
                    continue
                parse = self.parse_vlq(segment)
                parse += [0] * (5-len(parse))

                dst_col += parse[0]
                src_id += parse[1]
                src_line += parse[2]
                src_col += parse[3]
                name_id += parse[4]

                line_index[dst_col] = (src_id, src_line, src_col, name_id)
            yield line_index
