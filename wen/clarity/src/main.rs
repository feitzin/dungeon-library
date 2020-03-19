/**
 * A text-based interactive exploration of some buildings at my school.
 *
 * I,,,should update this comment to be actually useful at some point
 *
 *  - Wen
 *
 *
 *  TODO:
 *   * Finish engine
 *     * Need some map struct
 *     * Actions!
 *     * Nice display functions for things
 *     * ????
 *   * Implement a nicer UI? Curses? (Cursive crate looks neat)
 *   * Start writing the story
 *   * Start making maps
 *   * input loop?
 */

extern crate ansi_term;

use ansi_term::Color;

mod engine;

fn main() {

    println!("{}", Color::Purple.paint("Welcome to
┏━╸╻  ┏━┓┏━┓╻╺┳╸╻ ╻ 
┃  ┃  ┣━┫┣┳┛┃ ┃ ┗┳┛╹
┗━╸┗━╸╹ ╹╹┗╸╹ ╹  ╹ ╹ A text-based exploration


"));


    let mut play = engine::Player::new("Nausicaa".to_string(),
        "An average height girl, wearing a blue tunic and some form of cream leggings".to_string());

    play.display_inventory();

    play.grab("Teto".to_string(), engine::Item::new(
            "Teto".to_string(),
            "A small fox squirrel, with yellow and black stripes".to_string(),
            1,
            false
    ));

    println!("\n");
    play.display_inventory();
}
