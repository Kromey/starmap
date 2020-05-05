mod catalog;

use super::Point3d;
use catalog::Record;
use std::collections::HashMap;
use std::error::Error;

#[derive(Debug)]
pub struct Galaxy {
    pub stars: Vec<Star>,
    pub names: HashMap<String, usize>,
}

impl Galaxy {
    pub fn from_path(path: &str) -> Result<Self, Box<dyn Error>> {
        let sol = Point3d {
            x: 0.0,
            y: 0.0,
            z: 0.0,
        };

        let stars: Vec<Star> = csv::Reader::from_path(path)?
            .deserialize::<Record>()
            .filter_map(|record| {
                let star = Star::from(record.expect("Failed to read record from catalog"));
                if star.coords.distance(&sol) < 17f32 {
                    Some(star)
                } else {
                    None
                }
            })
            .collect();

        let names: HashMap<String, usize> = stars
            .iter()
            .enumerate()
            .map(|(i, star)| (star.name.clone(), i))
            .collect();

        Ok(Galaxy {
            stars,
            names,
        })
    }
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
