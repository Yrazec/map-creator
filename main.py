"""Run The Map Creator."""

from libs.map_creator import MapCreator


MAP_SIZE = 20
TREASURE_PROBABILITY = 0.5


if __name__ == "__main__":

    char_map = MapCreator.place_treasures(
        grid=MapCreator(size=MAP_SIZE).generate_map(),
        chance=TREASURE_PROBABILITY
    )

    MapCreator.print_char_map(char_map=char_map)

    MapCreator.dump_to_file(
        char_map=char_map,
        filepath=r"C:\Maps\map.txt"
    )
