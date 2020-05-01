use hyperspace::{Record, Star, Point3d};


fn main() {
    println!("Hello, world!");

    let sol = Point3d {
        x: 0.0,
        y: 0.0,
        z: 0.0,
    };

    let galaxy: Vec<_> = csv::Reader::from_path("data/HabHyg.csv")
        .unwrap()
        .deserialize::<Record>()
        .map(|record| Star::from(record.unwrap()))
        .filter(|star| star.coords.distance(&sol) < 17f32)
        .collect();

    let neighbors = galaxy.len();

    println!("{} nearby stars", neighbors);
}
