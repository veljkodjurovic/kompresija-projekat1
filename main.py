import collections
import math
from typing import Dict

def calculate_entrophy(data : bytes):
    N = len(data) #ukupna duzina podataka
    if N == 0:
        return 0.0, {}, {}
    
    counts = collections.Counter(data) #broj pojavljivanja svakog bajta
    for byte, count in counts.items():
        probs = {byte : count / N} #pretvaranje u verovatnoce

    H = 0.0
    for p in probs.values():
        if(p > 0):
            H += p*math.log2(p)

    H = -H
    return H, dict(counts), probs


if __name__ == "__main__":

    with open("test.bin", "wb") as f:
        f.write(bytes(range(10)))
        f.write(bytes(range(5)))


    with open("test.bin", "rb") as f:
        data = f.read()

    H, counts, probs = calculate_entrophy(data)
    print(f"Entropija: {H}")
    print(f"Broj pojavljivanja bajtova: {counts}")
    print(f"Verovatnoce pojavljivanja bajtova: {probs}") 