import commands


def is_not_engaged(engaged):
    return (not engaged["melee"]) and (not engaged["polearm"])


def sort_second(val):
    return val[1]


def add_monsters_to_action_queue(level, game_clock, monster_clock_map, action_queue):

    present_monsters = level.present_monsters()

    for i in range(len(present_monsters)):

        monster = present_monsters[i]

        if not monster["active"]:

            monster["active"] = True
            monster_id = monster["id"]

            next_move = game_clock + monster["stats"]["move_speed"]
            monster_clock_map[monster_id] = next_move
            action_queue.append([monster_id, next_move])


# monsters added to action_queue when activated; monsters potentially activated during player move
def process_monster_actions(char, level, game_clock, monster_clock_map, monster_map, action_queue):

    monster_id = action_queue[0][0]

    while monster_id != "main":

        game_clock = action_queue[0][1]
        monster = monster_map[monster_id]

        print("Monster " + monster["display_id"] + " time: " + str(game_clock))
        stats = monster["stats"]

        if monster["position"] == level.position:

            print(monster["descriptor"].capitalize() + " scratches at a flea.")
            print("LOS: " + str(monster["current_los"]))

        if is_not_engaged(monster["engaged"]):
            speed_increment = stats["move_speed"]
        else:
            speed_increment = stats["combat_speed"]

        monster_clock_map[monster_id] += speed_increment
        action_queue[0][1] += speed_increment

        action_queue.sort(key=sort_second)
        monster_id = action_queue[0][0]


def process_action_sequence(char, level, game_clock, monster_clock_map, monster_map, action_queue, action):

    if action == "abandon":
        char.status = "abandoned"
    elif action in commands.MOVE_COMMANDS:

        if not level.valid_path(action):
            print("You can't go that way.")
        elif not is_not_engaged(char.engaged):
            print("You are engaged in combat! You must retreat first.")
        else:

            game_clock = action_queue[0][1]
            print("Start time: " + str(game_clock))

            position = level.process_move(action)
            char.current_los = level.room_los[position][char.los]
            level.print_room()
            print(position)
            print("Current LOS: " + str(char.current_los))

            monster_clock_map["main"] += char.move_speed
            action_queue[0][1] += char.move_speed

            add_monsters_to_action_queue(level, game_clock, monster_clock_map, action_queue)
            action_queue.sort(key=sort_second)

            process_monster_actions(char, level, game_clock, monster_clock_map, monster_map, action_queue)
            game_clock = action_queue[0][1]
            print("End time: " + str(game_clock))

    else:
        print("Unknown command")

    return game_clock
