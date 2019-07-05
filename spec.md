# Discord bot

State {
    Map from Channel Id to ChannelState {
        Last Processed Message Id
    }

    Map from User Id to UserState {
        ActiveDeck: Reference to Deck in Decks
        Decks: Set {
            Deck {
                Id
                Archived: bool /// whether this deck has been archived,
                               /// or replaced by a modified version.
                               /// there is no deletion.
                Name: Option<String> /// slug of name is unique among active decks
                Cards: Ordered Map from Reference to Card in Cards to Count (positive integer)
            }
        }
    }

    Set of Cards {
        name: Name,
        slug: Slug,
        types: String,
    }
}

Maybe publish the decks online?


https://scryfall.com/docs/api/cards/search
https://discordapp.com/developers/docs/resources/channel#get-channel-messages
https://discordapp.com/developers/docs/topics/gateway

```
!card Island
```

looks up card info


```
add to deck
add 1 to deck
add 40 to deck island.dec
```

adds/remove to (defaulting to most recent) deck for user, creating new one if none

```
hands with 3 lands
hands with 3 lands by turn 1, 2, 3
hands with 3 lands and counterspell by turn 3
```

simulation and/or calculation of percentages.

do we want to also support custom mulligan rules?

```
sample hand
```

as you'd expect.

```
mana curve
mana curve for island.deck
```

yep.