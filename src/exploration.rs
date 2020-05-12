use super::galaxy::Galaxy;

#[derive(Clone, Copy, Debug)]
struct Route {
    from: usize,
    to: usize,
    time: f32,
}

type Routes = Vec<Route>;

#[derive(Debug)]
struct Explorer {
    max_dist: f32,
    position: usize,
    discovery_odds: f32,
    discoveries: u8,
}

impl Default for Explorer {
    fn default() -> Self {
        Explorer {
            max_dist: 5.3,
            position: 0,
            discovery_odds: 0.2,
            discoveries: 0,
        }
    }
}

