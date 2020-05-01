mod catalog;

pub use catalog::Record;

#[derive(Debug)]
pub struct Point3d {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Point3d {
    pub fn distance(&self, other: &Point3d) -> f32 {
        (
            (self.x - other.x).powi(2) +
            (self.y - other.y).powi(2) +
            (self.z - other.z).powi(2)
        ).sqrt()
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
