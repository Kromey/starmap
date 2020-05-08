use serde::Deserialize;

use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

#[derive(Debug, Deserialize)]
pub struct RGBColor {
    r: u8,
    g: u8,
    b: u8,
}

#[derive(Debug, Deserialize)]
#[serde(from = "OptionCorporation")]
pub struct Corporation {
    name: String,
    short_name: String,
    color: RGBColor,
}

impl Corporation {
    pub fn list_from_path<P: AsRef<Path>>(path: P) -> Result<Vec<Corporation>, Box<dyn Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);

        let corps = serde_json::from_reader(reader)?;

        Ok(corps)
    }
}

#[derive(Deserialize)]
struct OptionCorporation {
    name: String,
    short_name: Option<String>,
    color: (u8,u8,u8),
}

impl OptionCorporation {
    fn make_short_name(&self) -> String {
        self.name
            .chars()
            .filter(|c| c.is_uppercase())
            .collect()
    }
}

impl From<OptionCorporation> for Corporation {
    fn from(corp: OptionCorporation) -> Self {
        let short_name = match corp.short_name {
            Some(name) => name,
            None => corp.make_short_name(),
        };

        Self {
            name: corp.name,
            short_name,
            color: RGBColor { r: corp.color.0, g: corp.color.1, b: corp.color.2 },
        }
    }
}

