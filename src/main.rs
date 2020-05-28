use hyperspace::corporation::Corporation;
use hyperspace::galaxy::Galaxy;
use std::collections::HashMap;

fn main() {
    println!("Hello, world!");

    let my_galaxy = Galaxy::from_path("data/HabHyg.csv").expect("Failed to load star catalog");

    let neighbors = my_galaxy.stars.len();

    println!("{} nearby stars", neighbors);

    println!(
        "Sol: {:#?}",
        my_galaxy
            .star_by_name("Sol")
            .expect("Wait, where did our sun go??")
    );

    let corps =
        Corporation::list_from_path("data/corps.json").expect("Failed to load corporations");
    println!("{:#?}", corps);

    let mut buckets: HashMap<u32, Vec<usize>> = HashMap::new();

    my_galaxy.stars.iter()
        .enumerate()
        .for_each(|(i, star)| buckets.entry(star.bucket()).or_insert(Vec::<usize>::new()).push(i));

    println!("Total buckets: {}", buckets.len());
    println!("Smallest bucket: {:?}", buckets.iter().min_by_key(|(_, bucket)| bucket.len()).unwrap());
    println!("Largest bucket: {:?}", buckets.iter().max_by_key(|(_, bucket)| bucket.len()).unwrap());

    let avg = buckets
        .iter()
        .map(|(_, bucket)| bucket.len())
        .sum::<usize>() as f32
        / buckets.len() as f32;

    println!("Average bucket: {} stars", avg);
}
