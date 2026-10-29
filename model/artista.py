from dataclasses import dataclass, field


@dataclass
class Artista:
    id: int
    name: str
    numeroBrani: int
    ricavo: float
    genere: int = None                            # genere principale (GenreId), lo riempi dopo
    clienti: set = field(default_factory=set)     # clienti del paese che l'hanno comprato

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name
