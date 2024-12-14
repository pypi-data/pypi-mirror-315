# import sys
# from pathlib import Path

# top_dir = (Path(__file__).parent / "../../").resolve()
# bindings_dir = top_dir / "build/install/uv/borco_shiboken_example"

# if bindings_dir.exists():
#     print("extending python path...")
#     sys.path.append(bindings_dir.as_posix())

import borco_shiboken_example as bindings


def main() -> None:
    help(bindings)

    Dog = bindings.Dog

    print(f"Dog().bark() -> {Dog().bark()}")
    print(f"""Dog("Max").bark() -> {Dog("Max").bark()}""")

    dog = Dog()
    dog.name = "Charlie"
    print(f"""
dog = Dog()
dog.name = "Charlie"
dog.bark() -> {dog.bark()}""")


if __name__ == "__main__":
    main()
