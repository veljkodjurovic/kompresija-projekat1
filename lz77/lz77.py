from entropy import *
import struct

def lz77_codes(data : bytes, window_size=4):
    i = 0
    codes = []

    while i < len(data):
        match = (0, 0, data[i])  # (offset, length, next symbol)
        startIndex = max(0, i - window_size)
        searchBuffer = data[startIndex:i]
        lookAheadBuffer = data[i:i + window_size]

        for j in range(len(searchBuffer)):
            length = 0
            while (length < len(lookAheadBuffer)
                   and j + length < len(searchBuffer)
                   and searchBuffer[j + length] == lookAheadBuffer[length]):
                length += 1

            if length > match[1]:
                offset = len(searchBuffer) - j
                next_symbol = lookAheadBuffer[length:length+1] if length < len(lookAheadBuffer) else b'\x00'
                match = (offset, length, next_symbol)

        codes.append(match)
        i += match[1] + 1

    return codes


def lz77_compress(codes):
    with open("lz77compressed.bin", "wb") as f:
        for offset, length, symbol in codes:
            if isinstance(symbol, int):
                symbol = bytes([symbol])
            elif isinstance(symbol, str):
                symbol = symbol.encode('latin1')

            if len(symbol) != 1:
                symbol = b'\x00'

            f.write(struct.pack("BBc", offset, length, symbol))

def load_compressed():
    codes = []
    with open("lz77compressed.bin", "rb") as f:
        while True:
            chunk = f.read(3)
            if not chunk:
                break
            offset, length, symbol = struct.unpack("BBc", chunk)
            codes.append((offset, length, symbol))
    return codes

def lz77_decompress(codes):
    output = bytearray()

    for offset, length, symbol in codes:
        if offset == 0 and length == 0:
            # nema poklapanja — samo dodaj simbol
            output.append(symbol[0] if isinstance(symbol, bytes) else ord(symbol))
        else:
            # pronađi deo koji treba kopirati unazad
            start = len(output) - offset
            for i in range(length):
                output.append(output[start + i])
            # dodaj sledeći simbol
            if symbol:
                output.append(symbol[0] if isinstance(symbol, bytes) else ord(symbol))

    with open("lz77decompressed.bin", "wb") as f:
        f.write(output)

def lz77(data, window_size = 4):
    codes = lz77_codes(data, window_size)
    lz77_compress(codes)

    compressedCodes = load_compressed()
    lz77_decompress(compressedCodes)
