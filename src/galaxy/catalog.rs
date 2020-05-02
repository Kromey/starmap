use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Record {
    #[serde(rename = "Display Name")]
    pub name: String,
    #[serde(rename = "Hab?")]
    pub is_habitable: String,
    #[serde(rename = "Spectral Class")]
    pub spectral_class: String,
    #[serde(rename = "AbsMag")]
    pub abs_mag: f32,
    #[serde(rename = "Xg")]
    pub x: f32,
    #[serde(rename = "Yg")]
    pub y: f32,
    #[serde(rename = "Zg")]
    pub z: f32,
}
