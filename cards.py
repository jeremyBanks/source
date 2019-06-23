import magic


class ChimneyImp(magic.Card):
    name = "Chimney Imp"
    types = {magic.Type.creature}

chimney_imp = ChimneyImp()


class SolRing(magic.Card):
    name = "Sol Ring"
    types = {magic.Type.artifact}

sol_ring = SolRing()


class Island(magic.Card):
    name = "Island"
    types = {magic.Type.basic, magic.Type.land}

island = Island()
