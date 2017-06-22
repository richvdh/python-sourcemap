import python_sourcemap.decoder

def decode_mappings(mappings):
    dec = decoder.Decoder()
    return dec.decode_mappings(mappings)
