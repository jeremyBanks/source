import magic


class ChimneyImp(magic.Card):
    name = "Chimney Imp"
    types = {magic.Type.creature}


class SolRing(magic.Card):
    name = "Sol Ring"
    types = {magic.Type.artifact}


class Island(magic.Card):
    name = "Island"
    types = {magic.Type.basic, magic.Type.land}
