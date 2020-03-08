import re
from character import Character


RACE_MAP = ["Human", "Tower Elf", "Tree Elf", "Dwarf", "Halfling", "Gnome"]

RACE_CLASS_MAP = {
    "Human": ["Mercenary", "Berserker", "Cleric", "Monk", "Archer", "Outlander", "Sneak", "Fatespinner",
              "Arcanist", "Elementalist", "Wood Seer", "Doom Mage", "Fool"],
    "Tower Elf": ["Mercenary", "Archer", "Fatespinner", "Arcanist", "Elementalist"],
    "Tree Elf": ["Archer", "Outlander", "Wood Seer"],
    "Dwarf": ["Mercenary", "Berserker", "Cleric", "Runesmith"],
    "Halfling": ["Archer", "Sneak", "Fool"],
    "Gnome": ["Fatespinner", "Arcanist", "Elementalist", "Wood Seer", "Doom Mage", "Fool"]
}

HUMAN_STATS = {
    "HP": 25,
    "move_speed": 50,
    "combat_speed": 33,
    "los": 1
}


def build_selections(selections):

    selection_list = ""

    for x in range(1, len(selections) + 1):
        selection_list += str(x) + ") " + selections[x - 1] + "\n"

    return selection_list


def build_selection_regex(ttl_selections):

    regex_str = None

    if ttl_selections <= 9:
        regex_str = "^[1-" + str(ttl_selections) + "]$"
    else:

        last_digit = str(ttl_selections)[1]
        regex_str = "^([1-9]|1[0-" + last_digit + "])$"

    return re.compile(regex_str)


def selection_intake(valid_selection_init, confirm_init, selection_type, selection_ttl, available_selections):

    valid_selection = valid_selection_init
    confirm = confirm_init

    while (not valid_selection) or (not confirm):

        selection = input("Select a " + selection_type + ". Enter a number between 1 and " + str(selection_ttl) + "): ")

        selection_numbers = build_selection_regex(selection_ttl)
        valid_selection = selection_numbers.match(selection)

        if not valid_selection:
            print("Invalid selection. Try again.")
        else:

            selection = int(selection)
            valid_response = False

            while not valid_response:

                response = input("You have selected " + available_selections[selection - 1] + ". Are you sure? [y/n] ")

                yes_or_no = re.compile("^[yn]$")
                valid_response = yes_or_no.match(response)
                confirm = True if response == "y" else False

                if confirm:
                    return selection

                if not valid_response:
                    print("Invalid response. Try again.")


def create_character():

    print("\nSelect a race:\n\n" + build_selections(RACE_MAP))

    valid_selection = False
    confirm = False
    ttl_races = len(RACE_MAP)

    race = selection_intake(valid_selection, confirm, "race", ttl_races, RACE_MAP)

    available_classes = RACE_CLASS_MAP[RACE_MAP[race - 1]]
    print("\nSelect a class:\n\n" + build_selections(available_classes))

    valid_selection = False
    confirm = False
    ttl_classes = len(available_classes)

    selection_intake(valid_selection, confirm, "class", ttl_classes, available_classes)
    char = Character(HUMAN_STATS)

    return char
