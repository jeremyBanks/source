from magic import *

island = Card(name="Island", types=frozenset({land}))
sol_ring = Card(name="Sol Ring", types=frozenset({artifact}))
divination = Card(name="Divination", types=frozenset({sorcery}))
naga_eternal = Card(name="Naga Eternal", types=frozenset({creature}))
unsummon = Card(name="Unsummon", types=frozenset({instant}))


class Sets:
    μu = [island, sol_ring, divination, naga_eternal, unsummon]
