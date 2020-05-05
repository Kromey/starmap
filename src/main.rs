use hyperspace::galaxy::Galaxy;

fn main() {
    println!("Hello, world!");

    let my_galaxy = Galaxy::from_path("data/HabHyg.csv").expect("Failed to load star catalog");

    let neighbors = my_galaxy.stars.len();

    println!("{} nearby stars", neighbors);
}
