import collections
import math
from typing import Dict, Tuple, List, Callable
import pickle


class Node:
    def __init__(self, symbol=None, prob=0.0, left=None, right=None):
        self.symbol = symbol
        self.prob = prob
        self.left = left
        self.right = right

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


def sort_probs_desc(probs : Dict[int, float], desc = True) -> List[Tuple[int, float]]:
    sortedProbs = sorted(probs.items(), key=lambda x: x[1], reverse=desc)
    codes = {symbol: "" for symbol, _ in sortedProbs}

    return sortedProbs, codes

def generate_shannon_fano_codes(probs: List[Tuple[int, float]], codes: Dict[int, str], prefix = "") -> Dict[int, str]:
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

    generate_shannon_fano_codes(left, codes, prefix + "0")
    generate_shannon_fano_codes(right, codes, prefix + "1")

def shannon_fano_compress(data : bytes, codes : Dict[int, str]):
    codes_serialized = pickle.dumps(codes)
    codes_size = len(codes_serialized)      

    bitString = ''#pravim string koji ce da sadrzi sve kodove
    for b in data: 
        bitString += codes[b] 

    bitsLeftForByte = (8 - len(bitString) % 8) % 8 #dodajem nule na kraj da dobijem ceo bajt
    bitString += '0' * bitsLeftForByte

    compressed_data = bytearray()
    for i in range(0, len(bitString), 8):#uzimam po 8 bitova da dobijem bajt
        byte = bitString[i:i+8]
        compressed_data.append(int(byte, 2))

    with open("shannonfanocompressed.bin", "wb") as f:
        f.write(codes_size.to_bytes(4, byteorder='big'))
        f.write(codes_serialized)
        f.write(compressed_data)

def shannon_fano_decompress(codes : Dict[int, str], compressed_data : bytes):
    reverseCodes = {v: k for k, v  in codes.items()}#key je string kod, a value je sam bajt

    bitString = ''
    for byte in compressed_data:
        bitString += bin(byte)[2:].rjust(8, '0')

    decodedBytes = bytearray()
    currentCode = ''

    for bit in bitString:
        currentCode += bit
        if currentCode in reverseCodes:
            decodedBytes.append(reverseCodes[currentCode])
            currentCode = ''

    with open("shannonfanodecompressed.bin", "wb") as f:
        f.write(decodedBytes)



def shannon_fano(data : bytes):
    H, counts, probs = calculate_entrophy(data)

    sortedProbs, codes = sort_probs_desc(probs)
    generate_shannon_fano_codes(sortedProbs, codes)
    shannon_fano_compress(data, codes)
    shannon_fano_decompress(codes, data)






def generate_huffman_tree(probs: List[Tuple[int, float]]):
    
    nodes = []
    for symbol, prob in probs:
        node = Node(symbol=symbol, prob=prob)
        nodes.append(node)

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.prob)

        left = nodes.pop(0)
        right = nodes.pop(0)

        parent = Node(prob=left.prob + right.prob, left=left, right=right)
        nodes.append(parent)

    root = nodes[0]
    return root

def generate_huffman_codes(root : Node, prefix = "", codes = None):
    if codes is None:
        codes = {}
    
    if root is None:
        return

    if root.symbol is not None:
        codes[root.symbol] = prefix
        return


    if root.left:
        generate_huffman_codes(root.left, prefix + "0", codes)

    if root.right:
        generate_huffman_codes(root.right, prefix + "1", codes)

    return codes


def huffman_compress(data : bytes, codes : Dict[int, str]):
    codes_serialized = pickle.dumps(codes)
    codes_size = len(codes_serialized)      

    bitString = ''#pravim string koji ce da sadrzi sve kodove
    for b in data: 
        bitString += codes[b] 

    bitsLeftForByte = (8 - len(bitString) % 8) % 8 #dodajem nule na kraj da dobijem ceo bajt
    bitString += '0' * bitsLeftForByte

    compressed_data = bytearray()
    for i in range(0, len(bitString), 8):#uzimam po 8 bitova da dobijem bajt
        byte = bitString[i:i+8]
        compressed_data.append(int(byte, 2))

    with open("huffmancompressed.bin", "wb") as f:
        f.write(codes_size.to_bytes(4, byteorder='big'))
        f.write(codes_serialized)
        f.write(compressed_data)

def huffman_decompress(codes : Dict[int, str], compressed_data : bytes):
    reverseCodes = {v: k for k, v  in codes.items()}#key je string kod, a value je sam bajt

    bitString = ''
    for byte in compressed_data:
        bitString += bin(byte)[2:].rjust(8, '0')

    decodedBytes = bytearray()
    currentCode = ''

    for bit in bitString:
        currentCode += bit
        if currentCode in reverseCodes:
            decodedBytes.append(reverseCodes[currentCode])
            currentCode = ''

    with open("huffmandecompressed.bin", "wb") as f:
        f.write(decodedBytes)



def huffman(data : bytes):
    H, counts, probs = calculate_entrophy(data)

    sortedProbs, _ = sort_probs_desc(probs)
    root = generate_huffman_tree(sortedProbs)
    codes = generate_huffman_codes(root)
    huffman_compress(data, codes)
    huffman_decompress(codes, data)


if __name__ == "__main__":

    with open("original.bin", "wb") as f:
        f.write(bytes(range(5)))
        f.write(bytes(range(5,7)))
        f.write(bytes(range(5,7)))
        f.write(bytes(range(7,10)))


    with open("original.bin", "rb") as f:
        data = f.read()

    shannon_fano(data)
    huffman(data)

    print(lz77_compress(data,4))

    

    