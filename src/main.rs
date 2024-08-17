use std::path::Path;

fn main() {
    let left = Path::new("C:\\");

    for right in ["C:foo", "D:foo"] {
        println!();
        println!("left={left:?}, right={right:?}");
        let joined = left.join(right);
        println!("joined = {:?}", joined);
        println!("joined.is_absolute() = {:?}", joined.is_absolute());
        println!("joined.is_relative() = {:?}", joined.is_relative());
    }
}
