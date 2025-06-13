#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Décompresse un fichier .hpy (format HuAPyZip basé sur Huffman).
Usage :
    python decompressor.py fichier.hpy [-o sortie]
"""
import argparse
import struct
from pathlib import Path
from collections import Counter
from typing import Optional, List


MAGIC = b"HuAP"
VERSION = 1
UINT64 = struct.Struct(">Q")  # big-endian, 8 octets


# ---------- Structures de données Huffman ----------
class Node:
    __slots__ = ("freq", "byte", "left", "right")
    def __init__(self, freq: int, byte: Optional[int] = None,
                 left: Optional["Node"] = None, right: Optional["Node"] = None):
        self.freq, self.byte, self.left, self.right = freq, byte, left, right
    # Pour la file de priorité
    def __lt__(self, other): return self.freq < other.freq


def build_huffman_tree(freq_table: List[int]) -> Node:
    """classic O(256 log 256) = négligeable"""
    import heapq
    heap = [Node(f, b) for b, f in enumerate(freq_table) if f]
    if len(heap) == 1:                   # cas pathologique : un seul symbole
        only = heap[0]
        return Node(only.freq, None, only, None)  # racine factice
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        heapq.heappush(heap, Node(n1.freq + n2.freq, None, n1, n2))
    return heap[0]


# ---------- Lecture bit à bit ----------
class BitReader:
    def __init__(self, fileobj):
        self.f = fileobj
        self.buffer = 0
        self.nbits = 0

    def read_bit(self) -> Optional[int]:
        if self.nbits == 0:
            chunk = self.f.read(1)
            if not chunk:
                return None         # EOF
            self.buffer = chunk[0]
            self.nbits = 8
        self.nbits -= 1
        return (self.buffer >> self.nbits) & 1

    def close(self):
        self.f.close()


# ---------- Décompression principale ----------
def decompress(src: Path, dst: Optional[Path] = None):
    if dst is None:
        dst = src.with_suffix(".out")

    with src.open("rb") as f:
        if f.read(4) != MAGIC:
            raise ValueError("Pas un fichier HuAPyZip")
        version = f.read(1)[0]
        if version != VERSION:
            raise ValueError(f"Version {version} non gérée")

        orig_size = UINT64.unpack(f.read(8))[0]
        freq_table = [UINT64.unpack(f.read(8))[0] for _ in range(256)]

        root = build_huffman_tree(freq_table)

        bit_reader = BitReader(f)
        with dst.open("wb") as out:
            for _ in range(orig_size):
                node = root
                # descente jusqu'à une feuille
                while node.byte is None:
                    bit = bit_reader.read_bit()
                    if bit is None:
                        raise EOFError("Flux compressé tronqué")
                    node = node.left if bit == 0 else node.right
                out.write(bytes((node.byte,)))
        bit_reader.close()

    # Affichage taux de compression
    ratio = dst.stat().st_size / src.stat().st_size
    print(f"Décompression OK -> {dst}  (ratio compressé/orig ≃ {ratio:.3f})")


# ---------- CLI ----------
def main():
    p = argparse.ArgumentParser(description="Décompresse les fichiers HuAPyZip (.hpy)")
    p.add_argument("fichier", type=Path, help="fichier .hpy à décompresser")
    p.add_argument("-o", "--output", type=Path, help="chemin du fichier résultat")
    args = p.parse_args()
    decompress(args.fichier, args.output)


if __name__ == "__main__":
    main()
