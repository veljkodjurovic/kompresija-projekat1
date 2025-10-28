import sys, os

from shannonfano.shannonfano import shannon_fano
from huffman.huffman import huffman
from lz77.lz77 import lz77


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Upotreba: python main.py [ime_fajla]")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Greška: fajl '{filename}' ne postoji.")
        sys.exit(1)

    with open(filename, "rb") as f:
        data = f.read()

    shannon_fano(data)
    huffman(data)
    lz77(data)

    

    