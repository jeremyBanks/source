#!/usr/bin/env python
from random import shuffle

import magic
import cards


def main():
    board = magic.Board()
    board.shuffle_into_deck([cards.chimney_imp] * 50)
    board.shuffle_into_deck([cards.island] * 35)
    board.shuffle_into_deck([cards.sol_ring] * 8)
    board.reset()

    print("initial hand: {}".format(board.hand))


if __name__ == "__main__":
    main()
