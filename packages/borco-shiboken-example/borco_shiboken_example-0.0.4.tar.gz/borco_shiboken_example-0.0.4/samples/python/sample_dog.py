"""Sample file showing how `Dog` class can be used."""

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
