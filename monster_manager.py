class MonsterManager(object):
    """Track and manage monsters"""

    monster_id_counter = {
        "kobold": 0
    }

    monster_map = {}

    @staticmethod
    def next_id(monster_type):

        MonsterManager.monster_id_counter[monster_type] += 1
        return MonsterManager.monster_id_counter[monster_type]

    @staticmethod
    def add_monster(monster_id, monster):
        MonsterManager.monster_map[monster_id] = monster
