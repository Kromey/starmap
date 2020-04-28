use serde::Deserialize;

use serde::de::{self, Deserializer, Unexpected};


#[derive(Debug, Deserialize)]
pub struct Star {
    #[serde(alias = "Display Name")]
    pub name: String,
    #[serde(alias = "Hab?")]
    #[serde(deserialize_with = "is_habitable")]
    pub is_habitable: bool,
    #[serde(alias = "Spectral Class")]
    pub spectral_class: String,
    #[serde(alias = "AbsMag")]
    pub abs_mag: f32,
    #[serde(alias = "Xg")]
    pub x: f32,
    #[serde(alias = "Yg")]
    pub y: f32,
    #[serde(alias = "Zg")]
    pub z: f32,
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
