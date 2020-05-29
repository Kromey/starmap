use hyperspace::corporation::Corporation;
use hyperspace::galaxy::Galaxy;

fn main() {
    println!("Hello, world!");

    let my_galaxy = Galaxy::from_path("data/HabHyg.csv").expect("Failed to load star catalog");

    let neighbors = my_galaxy.stars.len();

    println!("{} nearby stars", neighbors);

    let sol = my_galaxy
            .star_by_name("Sol")
            .expect("Wait, where did our sun go??");
    println!("Sol: {:#?}", sol);

    let corps =
        Corporation::list_from_path("data/corps.json").expect("Failed to load corporations");
    println!("{:#?}", corps);

    let mut neighbors = 0;
    let mut raw_neighbors = 0;
    for bucket in sol.range(5.3) {
        if let Some(stars) = my_galaxy.stars_by_bucket(bucket) {
            println!("Bucket {} has {} stars", bucket, stars.len());
            raw_neighbors += stars.len();

            for star in stars {
                if star.distance(&sol) <= 5.3 {
                    neighbors += 1;
                }
            }
        } else {
            println!("Nothing in bucket {}", bucket);
        }
    }
    println!("Sol checked {} stars to find {} neighbors", raw_neighbors, neighbors);
}
