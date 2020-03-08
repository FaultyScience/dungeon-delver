import level as lvl
import action_sequence as act_seq
import ending
from monster_manager import MonsterManager


def run(char):

    level = lvl.Level()
    game_clock = 0
    monster_clock_map = {"main": 0}
    action_queue = [["main", 0]]
    char.current_los = level.room_los[level.pos_key_str(level.position)][char.los]

    level.print_room()
    print("CurrentLOS: " + str(char.current_los))

    while 1:

        action = input("\nEnter action: ")
        game_clock = act_seq.process_action_sequence(char, level, game_clock, monster_clock_map,
                                                     MonsterManager.monster_map, action_queue, action)

        if char.status in ending.END_STATUS:

            ending.process_ending(char.status)
            break
