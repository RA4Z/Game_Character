class Player:
    def __init__(self, name, stats=None, inventory=None, location=None):
        self.name = name
        self.stats = stats or {"strength": 5, "intelligence": 5}
        self.inventory = inventory or []
        self.location = location

        self.body = {
            part + suffix: 100
            for part in ("leg_right", "leg_left", "arm_right", "arm_left", "chest", "back")
            for suffix in ("_energy", "_scratch_intensity", "_bone_hp")
        }
        self.update_body_decay_rate()

        self.needs = {
            "hunger": 100,
            "thirst": 100,
            "sleep": 100,
            "sanity": 100,
            "hp": 100
        }

        self.experience_points = {
            skill + suffix: (self.stats[skill] + 1) * 10 if suffix == "_next_level" else 0
            for skill in ("strength", "intelligence")
            for suffix in ("_next_level", "_xp")
        }

        self.needs_decay_rate = {
            "hunger": -3,
            "thirst": -5,
            "sleep": -3,
            "sanity": 0,
        }

    def lvl_up_skills(self, skill, xp):
        self.experience_points[f"{skill}_xp"] += xp
        next_level = f"{skill}_next_level"
        if self.experience_points[f"{skill}_xp"] >= self.experience_points[next_level]:
            self.experience_points[f"{skill}_xp"] -= self.experience_points[next_level]
            self.stats[skill] += 1
            self.experience_points[next_level] = (self.stats[skill] + 1) * 10

    def update_body_decay_rate(self):
        strength = self.stats["strength"]
        self.body_decay_rate = {
            part + "_scratch_intensity": -5
            for part in ("leg_right", "leg_left", "arm_right", "arm_left", "chest", "back")
        }
        for part in ("leg_right", "leg_left", "arm_right", "arm_left", "chest", "back"):
            self.body_decay_rate[part + "_energy"] = min(strength * 0.8, 15)
            self.body_decay_rate[part + "_bone_hp"] = strength * 0.25

    def update_needs(self, time_passed):
        self.update_body_decay_rate()  # Only call this once per update

        for _ in range(time_passed):
            for need, decay_rate in self.needs_decay_rate.items():
                self.needs[need] = max(0, min(100, self.needs[need] + decay_rate))

            if self.needs["hunger"] == 0 or self.needs["thirst"] == 0:
                self.needs["hp"] -= 5
                self.needs["sanity"] -= 5
            else:
                self.needs["hp"] += 5
                self.needs["sanity"] += 2

            if self.needs["hunger"] == 0 and self.needs["thirst"] == 0:
                self.needs["hp"] -= 5  # This is applied twice if hunger and thirst are 0! Consider adjusting logic.
                self.needs["sanity"] -= 5

            self.needs["hp"] = min(100, self.needs["hp"])
            self.needs["sanity"] = min(100, self.needs["sanity"])

            for member, decay_rate in self.body_decay_rate.items():
                self.body[member] = max(0, min(100, self.body[member] + decay_rate))

    def add_item(self, item, qty):
        self.inventory.append({'name': item, 'qty': qty})

    def consume_item(self, item_name):  # Use item_name for clarity
        for item in self.inventory:
            if item['name'] == item_name:
                if item_name == "Food":
                    self.needs["hunger"] += 25
                elif item_name == "Water":
                    self.needs["thirst"] += 30
                else:
                    print("Não é possível consumir esse item!")
                # Remove only one of the item:
                item['qty'] -= 1
                if item['qty'] == 0:
                    self.inventory.remove(item)  #Remove item if its quantity goes to zero.
                return  # Stop searching after finding and consuming

        print("Você não tem este item no inventário.")

    def physical_exercises(self, time_passed):
        for _ in range(time_passed):
            self.verify_bones()
            for part in ("leg_right", "leg_left", "arm_right", "arm_left", "chest", "back"):
                self.body[part + "_energy"] -= 15
            self.lvl_up_skills("strength", (5 + self.stats["strength"]) * 0.85)
            self.update_needs(1)

    def verify_bones(self):
        for part in ("leg_right", "leg_left", "arm_right", "arm_left", "chest", "back"):
            if self.body[part + "_energy"] <= 0:
                self.body[part + "_bone_hp"] -= 5

    def sleep(self, time_passed):
        self.needs["sleep"] = min(100, self.needs["sleep"] + time_passed * 13)
        self.update_needs(time_passed)

    def get_need(self, need_name):
        return self.needs.get(need_name, 0)


if __name__ == '__main__':
    player = Player('Robert')
    player.physical_exercises(16)
    player.sleep(3)

    print(player.body)
    print(player.needs)
    print(player.experience_points)
    print(player.stats)
