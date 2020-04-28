use serde::Deserialize;

use serde::de::{self, Deserializer, Unexpected};


#[derive(Debug, Deserialize)]
pub struct Star {
    #[serde(rename(deserialize = "Display Name"))]
    pub name: String,
    #[serde(rename(deserialize = "Hab?"))]
    #[serde(deserialize_with = "is_habitable")]
    pub is_habitable: bool,
    #[serde(rename(deserialize = "Spectral Class"))]
    pub spectral_class: String,
    #[serde(rename(deserialize = "AbsMag"))]
    pub abs_mag: f32,
    #[serde(rename(deserialize = "Xg"))]
    pub xg: f32,
    #[serde(rename(deserialize = "Yg"))]
    pub yg: f32,
    #[serde(rename(deserialize = "Zg"))]
    pub zg: f32,
}

fn is_habitable<'de, D>(deserializer: D) -> Result<bool, D::Error>
where
    D: Deserializer<'de>,
{
    match Option::deserialize(deserializer).unwrap() {
        None => Ok(false),
        Some("1") => Ok(true),
        Some(other) => Err(de::Error::invalid_value(
            Unexpected::Str(other),
            &"zero or one",
        )),
    }
}
