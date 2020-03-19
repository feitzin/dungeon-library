/**
 * The actual guts of the engine, but no story. I probably ought to spin this off into it's own
 * library at some point.
 *
 *
 *  - Wen
 */

use std::collections::HashMap;
use std::boxed::Box;

pub struct Context{
    name: String,
    args: Vec<String>,
}

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
    pub name: String,
    pub description: String,
    actions: HashMap<String, Box<dyn FnMut()>>,
    directions: HashMap<String, Area >,
}



impl Area {

    pub fn new() -> Self {
        Area {
            name:           String::new(),
            description:    String::new(),
            actions:        HashMap::new(),
            directions:     HashMap::new(),
        }
    }


    pub fn add_action(&mut self, descr: String, action: impl FnMut() + 'static) {
        self.actions.insert(descr, Box::new(action));
    }

    pub fn add_connection(&mut self, descr: String,  direction: Area) {
        self.directions.insert(descr, direction);
    }

    /**
     * Get a ref to the area connected to the current one in the specified direction.
     */
    pub fn go(&self, direction: &String) -> Option<&Area> {
        match self.directions.get(direction) {
            Some(area) => Some(area),
            None       => {
                println!("You can't get to {} from {}!", direction, self.name);
                None
            },
        }
    }

    /**
     * Get a reference to the function associated with a given action
     */
    pub fn act(&self, action: &String) -> Option<&dyn FnMut()> {
        match self.actions.get(action) {
            Some(act)  => Some(&*act),
            None       => {
                println!("You can't {} in here!", action);
                None
            },
        }
    }

}


/**
 * This structure describes a player character
 *   elem name          The name that should be displayed for the player
 *   elem description   The description of the player
 *   elem actions       Any generic actions that can be always be taken, like examining the current
 *                      area
 *   elem inventory     The player's inventory
 */
pub struct Player {
    pub name: String,
    pub description: String,
    actions: HashMap<String, Box<dyn FnMut()>>,
    inventory: HashMap<String, Item> ,
}



impl Player {

    pub fn new(name: String, description: String) -> Self {
        Player {
            name,
            description,
            actions: HashMap::new(),
            inventory: HashMap::new(),
        }
    }


    pub fn add_action(&mut self, descr: String, action: impl FnMut() + 'static) {
        self.actions.insert(descr, Box::new(action));
    }

    pub fn grab(&mut self, name: String, item: Item) {
        self.inventory.insert(name, item);
    }

    pub fn display_inventory(&self) {
        println!("You have:");
        if self.inventory.is_empty() {
            println!(concat!(
                   "\tThe bare scraps of lint in your pockets, the clothes you",
                   " are wearing, and a water-bottle plastered in stickers that",
                   " say thing like \"All are welcome here\" and \"Smash the",
                   " Patriarchy\". Also, 7 cents in assorted pennies. Not much",
                   " of use, anyway."
                ));
            return;
        }

        for (name, item) in self.inventory.iter() {
            let prefix = match item.quantity {
                0 => "All out of",
                1 => "A single",
                2 => "A pair of",
                3 => "Three",
                4 => "A handful of",
                5 => "Plenty of",
                6 => "Lots of",
                _ => "More than you care to count of",
            };

            println!("\t{} {}", prefix, name);
        }
    }
}

/**
 * This structure describes an item
 *   elem name          The name that should be displayed for the item
 *   elem description   The description of the item
 *   elem actions       Any actions that can be done on the item
 */

pub struct Item {
    pub name: String,
    pub description: String,
    pub quantity: u32,
    disposable: bool, 
    actions: HashMap<String, Box<dyn FnMut()>>,
}

impl Item {

    pub fn new(name: String, description: String, quantity: u32, disposable: bool) -> Self {
        Item {
            name,
            description,
            quantity,
            disposable,
            actions:        HashMap::new(),
        }
    }


    pub fn add_action(&mut self, descr: String, action: impl FnMut() + 'static) {
        self.actions.insert(descr, Box::new(action));
    }

    /**
     * Get a reference to the function associated with a given action
     */
    pub fn act(&self, action: &String) -> Option<&dyn FnMut()> {
        match self.actions.get(action) {
            Some(act)  => Some(&*act),
            None       => {
                println!("You can't {} on a {}!", action, self.name);
                None
            },
        }
    }

    /**
     * Use an item. This only does anything (right now) if the item is disposable. Returns `true`
     * if the item has been used up.
     */
    pub fn use_item(&mut self) -> bool {
        if self.disposable {
            self.quantity -= 1;
            if self.quantity == 0 {
                return true;
            }
        }
        false
    }
}

