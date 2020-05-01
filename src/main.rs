use hyperspace::{Record, Star, Point3d};


fn main() {
    println!("Hello, world!");

    let mut neighbors = 0;
    let mut total = 0;

    let sol = Point3d {
        x: 0.0,
        y: 0.0,
        z: 0.0,
    };

    let mut rdr = csv::Reader::from_path("data/HabHyg.csv").unwrap();
    for result in rdr.deserialize::<Record>() {
        let star = Star::from(result.unwrap());
        total += 1;

        let dist = star.coords.distance(&sol);

        if dist < 17f32 {
            neighbors += 1;
            println!("{:#?}, {}", star, dist);
        }
    }

    println!("{} nearby stars out of {}", neighbors, total);
}
