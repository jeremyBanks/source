#!/usr/bin/env python
from pprint import pprint

from magic import *
from cards import *


def main():
    island_card = Card(name="Island", types=frozenset({basic, land}))
    island_token = island_card.as_token()

    print(island_card)
    print(island_token)
    pprint(Sets.μu)


if __name__ == "__main__":
    main()
