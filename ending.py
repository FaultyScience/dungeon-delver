END_STATUS = ["abandoned", "dead", "escaped", "won"]


def process_ending(status):

    if status == "escaped":
        print("You escape!")
    elif status == "abandoned":
        print("Run abandoned.")
    elif status == "won":
        print("You win!")
    elif status == "dead":
        print("Splat! You die...")
