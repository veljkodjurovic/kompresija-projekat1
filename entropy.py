from typing import Tuple, Dict, List
import math, collections

def calculate_entropy(data : bytes) -> Tuple[float, Dict[int, int], Dict[int, float]]:
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