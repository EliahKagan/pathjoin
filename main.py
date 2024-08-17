from os.path import isabs, join
from pathlib import Path
import platform


def main() -> None:
    print(f"Python {platform.python_version()}")

    left = "C:\\"
    for right in "C:foo", "D:foo":
        print()
        print(f"{left=}, {right=}")
        oop = Path(left, right)
        classic = join(left, right)
        print(f"{oop = }")
        print(f"{oop.is_absolute() = }")
        print(f"{isabs(oop) = }")
        print(f"{classic = }")
        print(f"{isabs(classic) = }")


if __name__ == "__main__":
    main()
