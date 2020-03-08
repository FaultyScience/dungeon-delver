class Character(object):
    """Store character data"""

    def __init__(self, stats):

        self.status = "alive"

        self.HP = stats["HP"]
        self.move_speed = stats["move_speed"]
        self.combat_speed = stats["combat_speed"]
        self.los = stats["los"]

        self.engaged = {
            "melee": False,
            "polearm": False
        }

        self.current_los = []
