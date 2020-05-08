pub mod galaxy;

#[derive(Clone, Debug)]
pub struct Point3d {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Point3d {
    pub fn origin() -> Self {
        Point3d {
            x: 0.0,
            y: 0.0,
            z: 0.0,
        }
    }

    pub fn distance(&self, other: &Point3d) -> f32 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2) + (self.z - other.z).powi(2))
            .sqrt()
    }
}

impl From<(f32, f32, f32)> for Point3d {
    fn from(point: (f32, f32, f32)) -> Point3d {
        Point3d {
            x: point.0,
            y: point.1,
            z: point.2,
        }
    }
}

impl From<(usize, usize, usize)> for Point3d {
    fn from(point: (usize, usize, usize)) -> Point3d {
        Point3d {
            x: point.0 as f32,
            y: point.1 as f32,
            z: point.2 as f32,
        }
    }
}
