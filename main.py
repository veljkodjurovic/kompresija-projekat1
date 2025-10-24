import collections
import math
from typing import Dict, Tuple, List, Callable
import pickle


def calculate_entrophy(data : bytes) -> Tuple[float, Dict[int, int], Dict[int, float]]:
    N = len(data) #ukupna duzina podataka
    if N == 0:
        return 0.0, {}, {}
    
    probs = {}
    counts = collections.Counter(data) #broj pojavljivanja svakog bajta
    for byte, count in counts.items():
        probs[byte] = count / N #pretvaranje u verovatnoce

    H = 0.0
    for p in probs.values():
        if(p > 0):
            H += p*math.log2(p) #formula za entropiju

    H = -H #entropija je negativan zbir
    return H, dict(counts), probs


def sort_probs_desc(probs : Dict[int, float]) -> List[Tuple[int, float]]:
    sortedProbs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    codes = {symbol: "" for symbol, _ in sortedProbs}

    return sortedProbs, codes

def shannon_fano_code(probs: List[Tuple[int, float]], codes: Dict[int, str], prefix = "") -> Dict[int, str]:
    if len(probs) == 1:
        symbol, _ = probs[0]
        codes[symbol] = prefix
        return

    total = sum(p for _, p in probs) #racunam ukupnu verovatnocu trenutnog niza, pa je posle delim na pola da bih podelio bajtove u posebne grupe
    acc = 0
    split_index = 0
    for i, (_, p) in enumerate(probs):
        acc += p
        if acc >= total / 2:
            split_index = i + 1
            break

    left = probs[:split_index]
    right = probs[split_index:]

    shannon_fano_code(left, codes, prefix + "0")
    shannon_fano_code(right, codes, prefix + "1")

def shannon_fano_compress(data : bytes, codes : Dict[int, str]):
    codes_serialized = pickle.dumps(codes)
    codes_size = len(codes_serialized)      

    bit_string = ''#pravim string koji ce da sadrzi sve kodove
    for b in data: 
        bit_string += codes[b] 

    bitsLeftForByte = (8 - len(bit_string) % 8) % 8 #dodajem nule na kraj da dobijem ceo bajt
    bit_string += '0' * bitsLeftForByte

    compressed_data = bytearray()
    for i in range(0, len(bit_string), 8):#uzimam po 8 bitova da dobijem bajt
        byte = bit_string[i:i+8]
        compressed_data.append(int(byte, 2))

    with open("compressed.bin", "wb") as f:
        f.write(codes_size.to_bytes(4, byteorder='big'))
        f.write(codes_serialized)
        f.write(compressed_data)


if __name__ == "__main__":

    with open("test.bin", "wb") as f:
        f.write(bytes(range(256)))


    with open("test.bin", "rb") as f:
        data = f.read()

    H, counts, probs = calculate_entrophy(data)

    sortedProbs, codes = sort_probs_desc(probs)
    shannon_fano_code(sortedProbs, codes)
    shannon_fano_compress(data, codes)
