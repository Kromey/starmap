mod catalog;

use super::Point3d;
use catalog::Record;
use std::collections::HashMap;
use std::error::Error;

pub const MAX_RANGE: f32 = 17.0;

#[derive(Debug)]
pub struct Galaxy {
    pub stars: Vec<Star>,
    pub buckets: HashMap<u32, Vec<usize>>,
    pub names: HashMap<String, usize>,
}

impl Galaxy {
    pub fn from_path(path: &str) -> Result<Self, Box<dyn Error>> {
        let sol = Point3d::origin();

        let stars: Vec<Star> = csv::Reader::from_path(path)?
            .deserialize::<Record>()
            .filter_map(|record| -> Option<Result<Star, Box<dyn Error>>> {
                match record {
                    Ok(record) => {
                        let star = Star::from(record);
                        if star.coords.distance(&sol) < MAX_RANGE {
                            Some(Ok(star))
                        } else {
                            None
                        }
                    }
                    Err(e) => Some(Err(Box::new(e))),
                }
            })
            .collect::<Result<_, Box<dyn Error>>>()?;

        let stars: Vec<Star> = stars
            .iter()
            .filter(|star| {
                // Filter out any stars if they're within 0.11 pc of a brighter star
                !stars.iter().any(|other| {
                    other.abs_mag < star.abs_mag && star.coords.distance(&other.coords) < 0.11f32
                })
            })
            .cloned() //Need to clone because we're taking ownership
            .collect();

        let mut buckets: HashMap<u32, Vec<usize>> = HashMap::new();

        stars.iter()
            .enumerate()
            .for_each(|(i, star)| buckets.entry(star.bucket()).or_insert(Vec::<usize>::new()).push(i));

        let names: HashMap<String, usize> = stars
            .iter()
            .enumerate()
            .map(|(i, star)| (star.name.clone(), i))
            .collect();

        Ok(Galaxy { stars, buckets, names })
    }

    pub fn star_by_name(&self, name: &str) -> Option<&Star> {
        let i = self.names.get(name)?;

        Some(&self.stars[*i])
    }

    pub fn stars_by_bucket(&self, bucket: u32) -> Option<Vec<&Star>> {
        let stars = self.buckets.get(&bucket)?;

        Some(stars.iter().map(|i| &self.stars[*i]).collect())
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

impl Star {
    pub fn bucket(&self) -> u32 {
        self.coords.bucket()
    }
}

impl From<Record> for Star {
    fn from(record: Record) -> Self {
        Star {
            is_habitable: record.is_habitable == "1",
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bucket() {
        let sol = Star {
            name: "Sol".into(),
            is_habitable: true,
            spectral_class: "G2V".into(),
            abs_mag: 4.85,
            coords: Point3d {
                x: 0.0,
                y: 0.0,
                z: 0.0,
            },
        };

        let procyon = Star {
            name: "Sol".into(),
            is_habitable: false,
            spectral_class: "F5IV-V".into(),
            abs_mag: 2.66,
            coords: Point3d {
                x: -2.8,
                y: -1.9,
                z: 0.8,
            },
        };

        assert_eq!(sol.bucket(), 2205);
        assert_eq!(procyon.bucket(), 1534);
    }
}
