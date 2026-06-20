from dataclasses import dataclass

from pygments.formatters.img import PilNotAvailable


@dataclass
class Piazzamento:
    idPilota: int
    posizione: int