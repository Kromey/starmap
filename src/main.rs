use hyperspace::corporation::Corporation;
use hyperspace::galaxy::Galaxy;

fn main() {
    println!("Hello, world!");

    let my_galaxy = Galaxy::from_path("data/HabHyg.csv").expect("Failed to load star catalog");

    let neighbors = my_galaxy.stars.len();

    println!("{} nearby stars", neighbors);

    println!(
        "Sol: {:#?}",
        my_galaxy
            .star_by_name("Sol")
            .expect("Wait, where did our sun go??")
    );

    let corps =
        Corporation::list_from_path("data/corps.json").expect("Failed to load corporations");
    println!("{:#?}", corps);
}
