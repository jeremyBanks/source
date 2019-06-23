#!/usr/bin/env python
from random import shuffle

import magic
import cards


def main():
    board = magic.Board()
    board.deck.extend([cards.chimney_imp] * 50)
    board.deck.extend([cards.island] * 35)
    board.deck.extend([cards.sol_ring] * 8)
    shuffle(board.deck)

    for n in range(7):
        board.draw()

    print("initial hand: {}".format(board.hand))


if __name__ == "__main__":
    main()
