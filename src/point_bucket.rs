use super::Point3d;
use super::galaxy::MAX_RANGE;

const BUCKET_RANGE: f32 = 6.0;

#[inline(always)]
fn cantor3(x: u32, y: u32, z: u32) -> u32 {
    cantor2(cantor2(x, y), z)
}

#[inline(always)]
fn cantor2(x: u32, y: u32) -> u32 {
    (x + y)*(x + y + 1)/2 + x
}

#[derive(Copy, Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct BucketPoint {
    x: u32,
    y: u32,
    z: u32,
}

impl BucketPoint {
    pub fn bucket(&self) -> u32 {
        cantor3(self.x, self.y, self.z)
    }
}

impl From<Point3d> for BucketPoint {
    fn from(point: Point3d) -> BucketPoint {
        BucketPoint::from(&point)
    }
}

impl From<&Point3d> for BucketPoint {
    fn from(point: &Point3d) -> BucketPoint {
        BucketPoint {
            x: ((point.x + MAX_RANGE) / BUCKET_RANGE).floor() as u32,
            y: ((point.y + MAX_RANGE) / BUCKET_RANGE).floor() as u32,
            z: ((point.z + MAX_RANGE) / BUCKET_RANGE).floor() as u32,
        }
    }
}

pub struct BucketIter {
    start: BucketPoint,
    end: BucketPoint,
    next: BucketPoint,
}

impl BucketIter {
    pub fn new(start: BucketPoint, end: BucketPoint) -> BucketIter {
        BucketIter {
            start,
            end,
            next: start,
        }
    }
}

impl Iterator for BucketIter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.next > self.end {
            return None;
        }

        let next = self.next;

        self.next.z += 1;

        if self.next.z > self.end.z {
            self.next.z = self.start.z;
            self.next.y += 1;

            if self.next.y > self.end.y {
                self.next.y = self.start.y;
                self.next.x += 1;
            }
        }

        Some(next.bucket())
    }
}
