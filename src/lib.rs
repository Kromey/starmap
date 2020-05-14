pub mod corporation;
pub mod exploration;
pub mod galaxy;

#[inline]
fn cantor3(x: i32, y: i32, z: i32) -> i32 {
    cantor2(cantor2(x, y), z)
}

#[inline]
fn cantor2(x: i32, y: i32) -> i32 {
    (x + y)*(x + y + 1)/2 + x
}

#[derive(Copy, Clone, Debug)]
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

    pub fn clamp_axes(self, min: f32, max: f32) -> Point3d {
        Point3d {
            // .max(min).min(max) looks backwards, but it's not...
            x: self.x.max(min).min(max),
            y: self.y.max(min).min(max),
            z: self.z.max(min).min(max),
        }
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
