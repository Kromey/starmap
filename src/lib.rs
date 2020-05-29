mod point_bucket;
pub mod corporation;
pub mod exploration;
pub mod galaxy;

use galaxy::MAX_RANGE;
use point_bucket::{BucketIter, BucketPoint};

#[derive(Copy, Clone, Debug, PartialEq, PartialOrd)]
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

    pub fn bucket_point(&self) -> BucketPoint {
        self.into()
    }

    pub fn bucket(&self) -> u32 {
        self.bucket_point().bucket()
    }

    pub fn bucket_range(&self, radius: f32) -> BucketIter {
        let start = Point3d {
            x: self.x - radius,
            y: self.y - radius,
            z: self.z - radius,
        }.clamp_axes(-MAX_RANGE, MAX_RANGE).bucket_point();
        let end = Point3d {
            x: self.x + radius,
            y: self.y + radius,
            z: self.z + radius,
        }.clamp_axes(-MAX_RANGE, MAX_RANGE).bucket_point();

        BucketIter::new(start, end)
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cantor_pairing() {
        assert_eq!(cantor2(0, 0), 0);
        assert_eq!(cantor2(1, 0), 2);
        assert_eq!(cantor2(0, 1), 1);
        assert_eq!(cantor2(10, 15), 335);
        assert_eq!(cantor2(15, 10), 340);
    }

    #[test]
    fn cantor_tripling() {
        assert_eq!(cantor3(0, 0, 0), 0);
        assert_eq!(cantor3(0, 0, 1), 1);
        assert_eq!(cantor3(0, 1, 0), 2);
        assert_eq!(cantor3(1, 0, 0), 5);
        assert_eq!(cantor3(1, 1, 1), 19);
    }

    #[test]
    fn point_clamping() {
        let origin = Point3d::origin();
        let too_small = Point3d::from((-18., -18., -18.));
        let too_big = Point3d::from((18., 18., 18.));
        let low = Point3d::from((-17., -17., -17.));
        let high = Point3d::from((17., 17., 17.));

        assert_eq!(origin, origin.clamp_axes(-17., 17.));
        assert!(too_small.clamp_axes(-17., 17.) >= low);
        assert!(too_big.clamp_axes(-17., 17.) <= high);
    }
}
