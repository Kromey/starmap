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

        let stars: Vec<Star> = stars
            .iter()
            .filter(|star| {
                // Filter out any stars if they're within 0.11 pc of a brighter star
                !stars.iter().any(|other| {
                    star.coords.distance(&other.coords) < 0.11f32 && other.abs_mag < star.abs_mag
                })
            })
            .cloned() //Need to clone because we're taking ownership
            .collect();

        let names: HashMap<String, usize> = stars
            .iter()
            .enumerate()
            .map(|(i, star)| (star.name.clone(), i))
            .collect();

        Ok(Galaxy { stars, names })
    }

    pub fn star_by_name(&self, name: &str) -> Option<&Star> {
        let i = self.names.get(name)?;

        Some(&self.stars[*i])
    }
}

#[derive(Clone, Debug)]
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
