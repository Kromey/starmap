use hyperspace::{Record, Star};


fn main() {
    println!("Hello, world!");

    let mut neighbors = 0;
    let mut total = 0;

    let mut rdr = csv::Reader::from_path("data/HabHyg.csv").unwrap();
    for result in rdr.deserialize() {
        let record: Record = result.unwrap();
        let star = Star::from(record);
        total += 1;

        let dist = (star.coords.x.powi(2) + star.coords.y.powi(2) + star.coords.z.powi(2)).sqrt();

        if dist < 17f32 {
            neighbors += 1;
            println!("{:#?}, {}", star, dist);
        }
    }

    println!("{} nearby stars out of {}", neighbors, total);
}
