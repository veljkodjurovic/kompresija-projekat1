from entropy import *
import pickle

class Node:
    def __init__(self, symbol=None, prob=0.0, left=None, right=None):
        self.symbol = symbol
        self.prob = prob
        self.left = left
        self.right = right

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
    H, counts, probs = calculate_entropy(data)
    sortedProbs, _ = sort_probs_desc(probs)
    root = generate_huffman_tree(sortedProbs)
    codes = generate_huffman_codes(root)
    huffman_compress(data, codes)
    huffman_decompress(codes, data)