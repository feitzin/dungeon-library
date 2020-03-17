/**
 * The actual guts of the engine, but no story. I probably ought to spin this off into it's own
 * library at some point.
 *
 *
 *  - Wen
 */

use std::collections::HashMap;


/**
 * This structure describes a given area/room.
 *   elem name          The name that should be displayed for the area
 *   elem description   The description of the area
 *   elem actions       Any area-specific actions that can be taken, like interacting with a statue
 *                      or similar 
 *   elem directions    The connections to other Areas. The first element of each tuple is the
 *                      string description for the direction, like "northwest", while the second
 *                      element is the Area connected to.
 */
pub struct Area {
    pub name: str,
    pub description: String,
    actions: Vec<T>,
    directions: HashMap<(String, Area)>,
}



impl Area {

    pub fn new() -> Self {
        Area {
            name:           "",
            description:    String::new(),
            actions:        Vec::new(),
            directions:     HashMap::new(),
        }
    }

    pub fn go(&self, direction: &String) -> Option<Area> {
        match directions.get(direction) {
            Some(area) => area,
            None       => {
                println!("You can't get to {} from {}!", direction, self.name);
                None
            },
        }
    }
