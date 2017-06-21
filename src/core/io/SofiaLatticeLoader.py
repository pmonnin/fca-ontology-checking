import json

from core.fca.Lattice import Lattice

__author__ = "Pierre Monnin"


class SofiaLatticeLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_lattice(lattice_path):
        with open(lattice_path, encoding='utf-8') as lattice_file:
            return Lattice(json.loads(lattice_file.read()))
