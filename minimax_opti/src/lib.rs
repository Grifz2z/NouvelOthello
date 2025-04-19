use pyo3::prelude::*;

pub type Grille = [[u8; 8]; 8];
pub type Coup = (usize, usize);

#[no_mangle] // ensures the function name is not mangled
pub extern "C" fn parite_pions(a: i32, b: i32) -> i32 {
    return a + b;
}


fn main() {
    println!("Hello, world!");
}
