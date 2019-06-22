use rand::{seq::SliceRandom, thread_rng};
use rayon::prelude::*;


impl Board {
    fn reset(mut self) -> Self {
        self.hand.clear();
        self.deck.clear();

        self.deck.extend(vec![Land; 35]);
        self.deck.extend(vec![ManaRock; 8]);
        self.deck.extend(vec![OtherShit; 56]);

        assert_eq!(self.deck.len(), 99);

        self.deck.shuffle(&mut thread_rng());

        self
    }

    fn new() -> Self {
        Board::default().reset()
    }

    fn draw(&mut self) -> &Card {
        let card = self.deck.pop().expect("deck not empty");
        self.hand.push(card);
        self.hand.last().unwrap()
    }
}

fn condition_in_n_turns(n: usize) -> bool {
    let mut board = Board::new();

    if board.hand.iter().filter(|card| card == &&Land).count() > 3 && board.hand.contains(&ManaRock) {
        return true;
    }

    // initial hand
    for _ in 0..7 {
        board.draw();
        if board.hand.iter().filter(|card| card == &&Land).count() > 3 && board.hand.contains(&ManaRock) {
            return true;
        }
    }

    if !(board.hand.iter().filter(|card| card == &&Land).count() > 2 && board.hand.contains(&ManaRock)) {
        // mulligan
        board = board.reset();

        for _ in 0..7 {
            board.draw();
            if board.hand.iter().filter(|card| card == &&Land).count() > 3 && board.hand.contains(&ManaRock) {
                return true;
            }
        }
    }

    // draw for first N turns
    for _ in 0..n {
        board.draw();
        if board.hand.iter().filter(|card| card == &&Land).count() > 3 && board.hand.contains(&ManaRock) {
            return true;
        }
    }

    false
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Default)]
struct Board {
    hand: Vec<Card>,
    deck: Vec<Card>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
enum Card {
    Land,
    ManaRock,
    OtherShit,
}
use self::Card::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let samples = 1_000_000;

    for turns in 1..=5 {
        let successes: u32 = (0..samples).into_par_iter().map(|_n| {
            if condition_in_n_turns(turns) {
                1
            } else {
                0
            }
        }).sum();

        let percentage = 100.0 * f64::from(successes) / f64::from(samples);
        println!(
            "{}/{} simulations ({}%) got hands of three lands and a rock by turn {} if they mulligained unless they had at least two and a rock.",
            successes, samples, percentage.round(), turns
        );
    }
    Ok(())
}
