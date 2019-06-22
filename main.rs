use rand::{seq::SliceRandom, thread_rng};
use rayon::prelude::*;

static THREE_LANDS_AND_ROCK: &'static str = "three lands and a rock";

fn three_lands_and_rock(board: &Board) -> bool {
    board.hand.iter().filter(|card| card == &&Land).count() > 3 && board.hand.contains(&ManaRock)
}

static MANA_ROCK: &'static str = "any mana rock";

fn mana_rock(board: &Board) -> bool {
    board.hand.contains(&ManaRock)
}

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

fn condition_in_n_turns(n: usize, condition: impl Fn(&Board) -> bool) -> bool {
    let mut board = Board::new();

    if condition(&board) {
        return true;
    }

    // initial hand
    for _ in 0..7 {
        board.draw();
        if condition(&board) {
            return true;
        }
    }

    // mulligan
    let mut board = board.reset();

    for _ in 0..7 {
        board.draw();
        if condition(&board) {
            return true;
        }
    }

    // draw for first N turns
    for _ in 0..n {
        board.draw();
        if condition(&board) {
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
            if condition_in_n_turns(turns, three_lands_and_rock) {
                1
            } else {
                0
            }
        }).sum();

        let percentage = 100.0 * f64::from(successes) / f64::from(samples);
        println!(
            "{}/{} simulations ({}%) got hands of {} by turn {}.",
            successes, samples, percentage.round(), THREE_LANDS_AND_ROCK, turns
        );
    }

    for turns in 1..=5 {
        let successes: u32 = (0..samples).into_par_iter().map(|_n| {
            if condition_in_n_turns(turns, mana_rock) {
                1
            } else {
                0
            }
        }).sum();

        let percentage = 100.0 * f64::from(successes) / f64::from(samples);
        println!(
            "{}/{} simulations ({}%) got hands of {} by turn {}.",
            successes, samples, percentage.round(), MANA_ROCK, turns
        );
    }

    Ok(())
}
