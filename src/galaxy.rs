mod catalog;


use catalog::Record;
use super::Point3d;


pub fn from_path(path: &str) -> Vec<Star> {
    let sol = Point3d {
        x: 0.0,
        y: 0.0,
        z: 0.0,
    };

    csv::Reader::from_path(path)
        .unwrap()
        .deserialize::<Record>()
        .map(|record| Star::from(record.unwrap()))
        .filter(|star| star.coords.distance(&sol) < 17f32)
        .collect()
}


#[derive(Debug)]
pub struct Star {
    pub name: String,
    pub is_habitable: bool,
    pub spectral_class: String,
    pub abs_mag: f32,
    pub coords: Point3d,
}

impl From<Record> for Star {
    fn from(record: Record) -> Self {
        Star {
            is_habitable: record.name == "1",
            name: record.name,
            spectral_class: record.spectral_class,
            abs_mag: record.abs_mag,

            coords: Point3d {
                x: record.x,
                y: record.y,
                z: record.z,
            },
        }
    }
}

