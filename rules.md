https://yawgatog.com/resources/magic-rules/

Magic is complicated, so we'll start with a super-simplified model.

A game has >= 1 players.
Players may not join the game after it's started, but players may be killed and removed from the game.
Players have an integer life count, which starts at 20.
If a player has <= 0 life during a State Check, they die. (Unless a card effect lets them stay alive with negative life.)



A State Check event occurs before each time a player would get priority (have the oppertunity to play a card).
If a State Check produces any effects, they are applied simultaneously, and another State Check is triggered (before the player gets priority).




