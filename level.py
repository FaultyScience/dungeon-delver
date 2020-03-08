import random
from monster_manager import MonsterManager

DIRECTION_STEP_MAP = {
    "northwest": [-1, -1],
    "north": [0, -1],
    "northeast": [1, -1],
    "east": [1, 0],
    "southeast": [1, 1],
    "south": [0, 1],
    "southwest": [-1, 1],
    "west": [-1, 0]
}

DIRECTION_MOVE_MAP = {
    "nw": "northwest",
    "7": "northwest",
    "n": "north",
    "8": "north",
    "ne": "northeast",
    "9": "northeast",
    "e": "east",
    "6": "east",
    "se": "southeast",
    "3": "southeast",
    "s": "south",
    "2": "south",
    "sw": "southwest",
    "1": "southwest",
    "w": "west",
    "4": "west"
}

# nw, n, ne, e, se, s, sw, w
LOS_1_PATHS = [
    [[-1, -1]],
    [[0, -1]],
    [[1, -1]],
    [[1, 0]],
    [[1, 1]],
    [[0, 1]],
    [[-1, 1]],
    [[-1, 0]]
]

# nw-nw, nw-n, n-n, ne-n, ne-ne, ne-e, e-e, se-e, se-se, se-s, s-s, sw-s, sw-sw, w-sw, w-w, nw-w
LOS_2_PATHS = [
    [[-2, -2], [-1, -1]],
    [[-1, -2], [-1, -1], [0, -1]],
    [[0, -2], [0, -1]],
    [[1, -2], [0, -1], [1, -1]],
    [[2, -2], [1, -1]],
    [[2, -1], [1, -1], [1, 0]],
    [[2, 0], [1, 0]],
    [[2, 1], [1, 0], [1, 1]],
    [[2, 2], [1, 1]],
    [[1, 2], [1, 1], [0, 1]],
    [[0, 2], [0, 1]],
    [[-1, 2], [0, 1], [-1, 1]],
    [[-2, 2], [-1, 1]],
    [[-2, 1], [-1, 1], [-1, 0]],
    [[-2, 0], [-1, 0]],
    [[-2, -1], [-1, 0], [-1, -1]]
]

# nw-nw-nw, nw-nw-n, nw-n-n, n-n-n, ne-n-n, ne-ne-n, ne-ne-ne, ne-ne-e, ne-e-e, e-e-e, se-e-e, se-se-e, se-se-se,
# se-se-s, se-s-s, s-s-s, sw-s-s, sw-sw-s, sw-sw-sw, sw-sw-w, sw-w-w, w-w-w, nw-w-w, nw-nw-w
LOS_3_PATHS = [
    [[-3, -3], [-2, -2], [-1, -1]],
    [[-2, -3], [-2, -2], [-1, -2], [-1, -1]],
    [[-1, -3], [-1, -2], [-1, -1], [0, -1], [0, -2]],
    [[0, -3], [0, -2], [0, -1]],
    [[1, -3], [0, -2], [0, -1], [1, -1], [1, -2]],
    [[2, -3], [1, -1], [1, -2], [2, -2]],
    [[3, -3], [1, -1], [2, -2]],
    [[3, -2], [1, -1], [2, -2], [2, -1]],
    [[3, -1], [1, -1], [2, -1], [1, 0], [2, 0]],
    [[3, 0], [1, 0], [2, 0]],
    [[3, 1], [1, 0], [2, 0], [1, 1], [2, 1]],
    [[3, 2], [1, 1], [2, 1], [2, 2]],
    [[3, 3], [1, 1], [2, 2]],
    [[2, 3], [1, 1], [2, 2], [1, 2]],
    [[1, 3], [1, 1], [1, 2], [0, 1], [0, 2]],
    [[0, 3], [0, 1], [0, 2]],
    [[-1, 3], [0, 1], [0, 2], [-1, 1], [-1, 2]],
    [[-2, 3], [-1, 1], [-1, 2], [-2, 2]],
    [[-3, 3], [-1, 1], [-2, 2]],
    [[-3, 2], [-1, 1], [-2, 2], [-2, 1]],
    [[-3, 1], [-1, 1], [-2, 1], [-1, 0], [-2, 0]],
    [[-3, 0], [-1, 0], [-2, 0]],
    [[-3, -1], [-1, 0], [-2, 0], [-1, -1], [-2, -1]],
    [[-3, -2], [-2, -2], [-1, -1], [-2, -1]]
]


class Level(object):

    def __init__(self):

        self.__generate_map()
        self.__set_start()
        self.__set_monster_table()
        self.__spawn_monsters()
        self.__available_paths = self.__calc_available_paths(self.position)

    def __generate_map(self):

        self.__level_map = [[False for i in range(88)] for j in range(88)]
        self.__room_monster_map = {}
        self.__open_rooms = {}

        def set_room(rng, j):

            for i in rng:

                self.__level_map[i][j] = True

                coord_str_key = Level.pos_key_str([i, j])
                self.__room_monster_map[coord_str_key] = []
                self.__open_rooms[coord_str_key] = [i, j]

        def set_ranges(ranges_arr):

            range_tups = []

            for i in range(len(ranges_arr)):

                tup = ranges_arr[i]

                out_tup = (int(len(tup) / 2), [])

                for j in range(0, len(tup), 2):
                    out_tup[1].append(range(tup[j], tup[j + 1]))

                range_tups.append(out_tup)

            return range_tups

        ranges = [
                    (51, 52),
                    (51, 52),
                    (45, 65),
                    (35, 37, 38, 41, 45, 46, 51, 52, 64, 65, 72, 78),
                    (35, 37, 38, 39, 40, 41, 45, 46, 51, 61, 64, 65, 72, 73, 76, 77),
                    (35, 37, 38, 39, 40, 41, 45, 46, 50, 52, 61, 65, 72, 73, 76, 77),
                    (35, 39, 40, 41, 42, 45, 50, 52, 61, 63, 64, 65, 71, 74, 76, 77),
                    (35, 36, 37, 39, 40, 45, 51, 52, 54, 56, 60, 61, 64, 72, 73, 74, 76, 77),
                    (35, 36, 37, 41, 42, 45, 51, 60, 66, 67, 69, 70, 71, 72, 73, 74, 76, 77),
                    (33, 39, 41, 42, 51, 53, 58, 59, 66, 67, 69, 70, 71, 72, 73, 74, 76, 77),
                    (33, 34, 35, 36, 38, 39, 40, 41, 58, 59, 65, 69, 70, 71, 77, 78),
                    (34, 35, 38, 39, 40, 41, 52, 53, 58, 59),
                    (32, 33, 36, 37, 38, 41, 53, 55, 56, 59, 62, 74),
                    (32, 38, 53, 59, 60, 62, 73, 74),
                    (32, 33, 34, 37, 38, 39, 51, 53, 57, 62, 73, 74),
                    (32, 33, 39, 41, 51, 53, 56, 58, 64, 74),
                    (32, 33, 39, 41, 51, 54),
                    (32, 33, 40, 41, 61, 64, 65, 68),
                    (32, 33, 38, 41, 42, 45, 61, 68),
                    (32, 33, 38, 45, 49, 55, 61, 64, 65, 68),
                    (32, 33, 38, 41, 42, 45, 49, 52, 54, 55, 62, 63),
                    (32, 33, 38, 41, 43, 44, 45, 48, 49, 52, 54, 55, 61, 64),
                    (32, 33, 34, 36, 43, 44, 45, 48, 49, 52, 54, 55, 61, 64),
                    (32, 33, 34, 36, 43, 44, 49, 50, 54, 55, 61, 64, 65, 67),
                    (32, 33, 35, 36, 37, 52, 54, 55, 64, 66, 67, 68),
                    (32, 38, 41, 42, 43, 51, 51, 52, 54, 55, 65, 66, 67, 68),
                    (32, 33, 35, 36, 43, 44, 48, 52, 54, 55, 65, 67),
                    (35, 36, 37, 44, 46, 47, 48, 49, 50, 52, 54, 55, 64, 65),
                    (35, 36, 40, 41, 46, 47, 48, 49, 51, 52, 54, 55, 64, 65),
                    (35, 36, 38, 40, 42, 46, 47, 49, 51, 52, 54, 55, 63, 64),
                    (35, 36, 41, 42, 45, 46, 51, 53, 54, 55, 63, 64),
                    (35, 41, 47, 53, 54, 55, 63, 64),
                    (40, 41, 42, 46, 51, 53, 54, 55, 62, 63),
                    (40, 41, 42, 43, 45, 46, 52, 53, 54, 62),
                    (40, 41, 42, 46, 51, 53, 58, 59),
                    (40, 41, 45, 46, 47, 53, 58, 59),
                    (40, 46, 47, 48, 51, 52, 58, 59),
                    (42, 43, 47, 48, 51, 59),
                    (42, 43, 47, 48),
                    (42, 43, 47, 48),
                    (42, 48),
                    (42, 43)
                 ]

        range_tups = set_ranges(ranges)

        for i in range(2, 44):

            for j in range(range_tups[i - 2][0]):

                rng = range_tups[i - 2][1][j]
                set_room(rng, i)

        self.room_los = {}
        open_rooms = list(self.__open_rooms.keys())
        los_paths = [LOS_1_PATHS, LOS_2_PATHS, LOS_3_PATHS]

        for pos in iter(open_rooms):

            self.room_los[pos] = []

            los = [pos]
            self.room_los[pos].append(los)

            for path in iter(los_paths):

                los = [*los, *self.__calc_valid_los(pos, path)]
                self.room_los[pos].append(los)

    @staticmethod
    def pos_key_str(position):
        return str(position[0]).zfill(2) + str(position[1]).zfill(2)

    def __set_start(self):

        self.__start_position = [66, 20]
        self.position = [66, 20]
        self.__open_rooms.pop(Level.pos_key_str([66, 20]))

    # tables should be imported and selection passed during initialization
    def __set_monster_table(self):

        self.__monster_table = {

            "kobold": {
                "name": "kobold",
                "descriptor": "a kobold",
                "description": "Small yet vicious, kobolds tend to hunt in large packs, but are wanting in bravery.",
                "spawn_count": 4,
                "propogation": 60,

                "stats": {
                    "HP": 7,
                    "move_speed": 48,
                    "combat_speed": 25,
                    "los": 1
                },

                "actions": ["move", "engage", "attack", "block", "dodge", "retreat"],

                "engaged": {
                    "melee": False,
                    "polearm": False
                },

                "current_los": []
            }
        }

    def __spawn_monsters(self):

        # move all actual creation and tables to MonsterManager, but spawning logic stays here
        def spawn_monster(template, display_id, location):

            name = template["name"]
            monster_id = name + "_" + str(MonsterManager.next_id(name))

            monster = {
                "name": name,
                "descriptor": template["descriptor"],
                "description": template["description"],
                "id": monster_id,
                "display_id": str(display_id),
                "stats": template["stats"],
                "actions": template["actions"],
                "engaged": template["engaged"],
                "position": location,
                "active": False,
                "current_los": self.room_los[self.pos_key_str(location)][template["stats"]["los"]]
            }

            MonsterManager.add_monster(monster_id, monster)
            return monster

        ttl_spawns = round(random.uniform(8, 12))
        open_rooms = list(self.__open_rooms.keys())
        monsters = list(self.__monster_table.keys())

        # BEGIN_TESTING

        spawn_location = "6519"
        spawn_type = monsters[round(random.uniform(0, len(monsters) - 1))]
        monster_template = self.__monster_table[spawn_type]

        spawn_count = round(random.uniform(round(0.8 * monster_template["spawn_count"]),
                                           round(1.2 * monster_template["spawn_count"])))

        for j in range(spawn_count):
            # take out current_spawn_numbers, populate display id's when printing room, permanent id at spawn
            current_spawn_number = len(self.__room_monster_map[spawn_location])
            loc_coord = self.__open_rooms[spawn_location]
            self.__room_monster_map[spawn_location].append(spawn_monster(monster_template,
                                                                         current_spawn_number + 1, loc_coord))

        # END_TESTING

        for i in range(ttl_spawns):

            spawn_location = open_rooms[round(random.uniform(0, len(open_rooms) - 1))]
            spawn_type = monsters[round(random.uniform(0, len(monsters) - 1))]
            monster_template = self.__monster_table[spawn_type]

            spawn_count = round(random.uniform(round(0.8 * monster_template["spawn_count"]),
                                               round(1.2 * monster_template["spawn_count"])))

            print(spawn_location)

            for j in range(spawn_count):
                # take out current_spawn_numbers, populate display id's when printing room, permanent id at spawn
                current_spawn_number = len(self.__room_monster_map[spawn_location])
                loc_coord = self.__open_rooms[spawn_location]
                self.__room_monster_map[spawn_location].append(spawn_monster(monster_template,
                                                                             current_spawn_number + 1, loc_coord))

            propogation = monster_template["propogation"]
            recursive_spawn_loc = spawn_location

            while propogation >= 10:

                if round(random.uniform(1, 100)) <= propogation:

                    available_paths = self.__calc_available_paths(self.__open_rooms[recursive_spawn_loc])
                    path = available_paths[round(random.uniform(0, len(available_paths) - 1))]
                    recursive_spawn_loc = self.__calc_direction(self.__open_rooms[recursive_spawn_loc], path)

                    if recursive_spawn_loc == Level.pos_key_str(self.__start_position):

                        available_paths = self.__calc_available_paths(self.__start_position)
                        path = available_paths[round(random.uniform(0, len(available_paths) - 1))]
                        recursive_spawn_loc = self.__calc_direction(self.__start_position, path)

                    recursive_spawn_count = round(random.uniform(round(0.8 * monster_template["spawn_count"]),
                                                                 round(1.2 * monster_template["spawn_count"])))

                    print(recursive_spawn_loc)

                    for k in range(recursive_spawn_count):

                        current_spawn_number = len(self.__room_monster_map[recursive_spawn_loc])
                        recursive_loc_coord = self.__open_rooms[recursive_spawn_loc]
                        self.__room_monster_map[recursive_spawn_loc].append(spawn_monster(monster_template,
                                                                                          current_spawn_number + 1,
                                                                                          recursive_loc_coord))

                propogation *= 0.5

    def __calc_direction(self, position, direction):

        x_step = position[0] + DIRECTION_STEP_MAP[direction][0]
        y_step = position[1] + DIRECTION_STEP_MAP[direction][1]

        return Level.pos_key_str([x_step, y_step])

    def __calc_available_paths(self, position):

        nw = self.__level_map[position[0] - 1][position[1] - 1]
        n = self.__level_map[position[0]][position[1] - 1]
        ne = self.__level_map[position[0] + 1][position[1] - 1]
        e = self.__level_map[position[0] + 1][position[1]]
        se = self.__level_map[position[0] + 1][position[1] + 1]
        s = self.__level_map[position[0]][position[1] + 1]
        sw = self.__level_map[position[0] - 1][position[1] + 1]
        w = self.__level_map[position[0] - 1][position[1]]

        directions = [nw, n, ne, e, se, s, sw, w]
        paths = ["northwest", "north", "northeast", "east", "southeast", "south", "southwest", "west"]
        available_paths = []

        for i in range(len(paths)):

            if directions[i]:
                available_paths.append(paths[i])

        return available_paths

    def __calc_valid_los(self, position, paths):

        def valid_los(pos, los):

            for space in iter(los):

                x = pos[0] + space[0]
                y = pos[1] + space[1]

                if not self.__level_map[x][y]:
                    return False

            return True

        spaces_in_los = []

        for path in iter(paths):

            pos_coord = self.__open_rooms[position]

            if valid_los(pos_coord, path):

                x = pos_coord[0] + path[0][0]
                y = pos_coord[1] + path[0][1]

                spaces_in_los.append(self.pos_key_str([x, y]))

        return spaces_in_los

    def __get_available_paths_str(self):
        return ", ".join(self.__available_paths)

    def present_monsters(self):
        return self.__room_monster_map[Level.pos_key_str(self.position)]

    def valid_path(self, path):
        return DIRECTION_MOVE_MAP[path] in self.__available_paths

    def print_room(self):

        room_desc_str = "\n[Dusty Corridor]\n\n" \
                    "The stone floor is covered in a thick layer of dust and grime.\n\n"

        available_paths_str = "Available paths: " + self.__get_available_paths_str()
        monsters_str = ""

        monsters = self.present_monsters()
        monsters_len = len(monsters)

        if monsters_len > 0:

            monsters_str = "\n\nYou see "

            if monsters_len > 2:

                for i in range(monsters_len):

                    if i == 0:
                        monsters_str += monsters[i]["descriptor"] + " [" + monsters[i]["display_id"] + "]"
                    elif i < (monsters_len - 1):
                        monsters_str += ", " + monsters[i]["descriptor"] + " [" + monsters[i]["display_id"] + "]"
                    else:
                        monsters_str += ", and " + monsters[i]["descriptor"] + " [" + monsters[i]["display_id"] + "]."

            elif monsters_len == 2:

                monsters_str += monsters[0]["descriptor"] + " [" + monsters[0]["display_id"] + "]"
                monsters_str += "and " + monsters[1]["descriptor"] + " [" + monsters[1]["display_id"] + "]."

            else:
                monsters_str += monsters[0]["descriptor"] + " [" + monsters[0]["display_id"] + "]."

        print(room_desc_str + available_paths_str + monsters_str)

    def process_move(self, move):

        mapped_direction = DIRECTION_MOVE_MAP[move]

        if mapped_direction == "northwest":

            self.position[0] -= 1
            self.position[1] -= 1

        elif mapped_direction == "north":
            self.position[1] -= 1
        elif mapped_direction == "northeast":

            self.position[0] += 1
            self.position[1] -= 1

        elif mapped_direction == "east":
            self.position[0] += 1
        elif mapped_direction == "southeast":

            self.position[0] += 1
            self.position[1] += 1

        elif mapped_direction == "south":
            self.position[1] += 1
        elif mapped_direction == "southwest":

            self.position[0] -= 1
            self.position[1] += 1

        elif mapped_direction == "west":
            self.position[0] -= 1

        self.__available_paths = self.__calc_available_paths(self.position)
        return self.pos_key_str(self.position)
