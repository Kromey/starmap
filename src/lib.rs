pub mod galaxy;

#[derive(Debug)]
pub struct Point3d {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Point3d {
    pub fn distance(&self, other: &Point3d) -> f32 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2) + (self.z - other.z).powi(2))
            .sqrt()
    }
}
