use hyperspace::galaxy;

fn main() {
    println!("Hello, world!");

    let my_galaxy = galaxy::from_path("data/HabHyg.csv");

    let neighbors = my_galaxy.len();

    println!("{} nearby stars", neighbors);
}
