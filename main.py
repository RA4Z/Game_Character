class Player:
    def __init__(self, name, stats=None, inventory=None, location=None):
        self.name = name
        self.stats = stats if stats else {"strength": 5, "intelligence": 5}
        self.inventory = inventory if inventory else []
        self.location = location

        self.body = {
            # Energia restante das partes do corpo (caso fique abaixo de zero irá gerar fadiga muscular)
            # Acompanha o nível de força (máximo 100)
            "leg_right_energy": 100,
            "leg_left_energy": 100,
            "arm_right_energy": 100,
            "arm_left_energy": 100,
            "chest_energy": 100,
            "back_energy": 100,

            # Nível de arranhões
            "leg_right_scratch_intensity": 0,
            "leg_left_scratch_intensity": 0,
            "arm_right_scratch_intensity": 0,
            "arm_left_scratch_intensity": 0,
            "chest_scratch_intensity": 0,
            "back_scratch_intensity": 0,

            # Energia restante dos ossos do corpo
            "leg_right_bone_hp": 100,
            "leg_left_bone_hp": 100,
            "arm_right_bone_hp": 100,
            "arm_left_bone_hp": 100,
            "chest_bone_hp": 100,
            "back_bone_hp": 100,
        }
        self.body_decay_rate = self.update_body_decay_info()
        self.needs = {
            # Necessidades básicas do jogo
            "hunger": 100,
            "thirst": 100,
            "sleep": 100,
            "sanity": 100,
            "hp": 100,
            "pain": 0
        }
        self.experience_points = {
            # Quantidade de pontos de experiência atual e para o próximo nível
            "strength_next_level": (self.stats["strength"] + 1) * 10,
            "strength_xp": 0,

            "intelligence_next_level": (self.stats["intelligence"] + 1) * 10,
            "intelligence_xp": 0,
        }
        self.needs_decay_rate = {
            # Taxa de decaimento por hora no jogo
            "hunger": -3,
            "thirst": -5,
            "sleep": -3,
            "sanity": 0,
        }

    # Regra para adicionar pontos de experiência, fazer a verificação e subir o nível da respectiva habilidade
    def lvl_up_skills(self, skill, xp):
        self.experience_points[f"{skill}_xp"] += xp
        if self.experience_points[f"{skill}_xp"] >= self.experience_points[f"{skill}_next_level"]:
            self.experience_points[f"{skill}_xp"] = self.experience_points[f"{skill}_xp"] - self.experience_points[f"{skill}_next_level"]
            self.stats[skill] += 1
            self.experience_points[f"{skill}_next_level"] = (self.stats[skill] + 1) * 10

    def verify_player_status(self):
        if self.needs["hp"] <= 0:
            return 'death'

        if self.needs["sleep"] <= 0:
            return 'tired'

    def update_body_decay_info(self):
        return {
            # Melhora de arranhões ao passar das horas
            "leg_right_scratch_intensity": -5,
            "leg_left_scratch_intensity": -5,
            "arm_right_scratch_intensity": -5,
            "arm_left_scratch_intensity": -5,
            "chest_scratch_intensity": -5,
            "back_scratch_intensity": -5,

            # Melhora de energia restante dos membros ao passar das horas
            "leg_right_energy": min(self.stats["strength"] * 0.8, 15),
            "leg_left_energy": min(self.stats["strength"] * 0.8, 15),
            "arm_right_energy": min(self.stats["strength"] * 0.8, 15),
            "arm_left_energy": min(self.stats["strength"] * 0.8, 15),
            "chest_energy": min(self.stats["strength"] * 0.8, 15),
            "back_energy": min(self.stats["strength"] * 0.8, 15),

            # Melhora de resistência dos ossos ao passar das horas
            "leg_right_bone_hp": self.stats["strength"] * 0.25,
            "leg_left_bone_hp": self.stats["strength"] * 0.25,
            "arm_right_bone_hp": self.stats["strength"] * 0.25,
            "arm_left_bone_hp": self.stats["strength"] * 0.25,
            "chest_bone_hp": self.stats["strength"] * 0.25,
            "back_bone_hp": self.stats["strength"] * 0.25,
        }

    def add_item(self, item, qty):
        self.inventory.append({'name': item, 'qty': qty})

    # ATUALIZAR STATUS DO CORPO DE ACORDO COM A QUANTIDADE DE HORAS PASSADAS
    def update_needs(self, time_passed):
        self.body_decay_rate = self.update_body_decay_info()
        for _ in range(time_passed):
            for need, decay_rate in self.needs_decay_rate.items():
                self.needs[need] += decay_rate
                self.needs[need] = max(0, self.needs[need])  # Impede que as necessidades fiquem negativas
                self.needs[need] = min(100, self.needs[need])  # Impede que as necessidades ultrapassem 100

            if self.needs["hunger"] == 0 or self.needs["thirst"] == 0:
                self.needs["hp"] -= 5
                self.needs["sanity"] -= 5
            else:
                self.needs["hp"] += 5
                self.needs["sanity"] += 2

            if self.needs["hunger"] == 0 and self.needs["thirst"] == 0:
                self.needs["hp"] -= 5
                self.needs["sanity"] -= 5

            self.needs["hp"] = min(100, self.needs["hp"])  # Impede que as necessidades ultrapassem 100
            self.needs["sanity"] = min(100, self.needs["sanity"])  # Impede que as necessidades ultrapassem 100

            for member, decay_rate in self.body_decay_rate.items():
                self.body[member] += decay_rate
                self.body[member] = max(0, self.body[member])  # Impede que as necessidades fiquem negativas
                self.body[member] = min(100, self.body[member])  # Impede que as necessidades ultrapassem 100

            self.verify_player_status()

    def consume_item(self, item):  # lógica para consumir itens (comida, água)
        if item in self.inventory:
            if item == "Food":  # exemplo
                self.needs["hunger"] += 25  # quanto a comida recupera a fome
                self.inventory.remove(item)
            elif item == "Water":
                self.needs["thirst"] += 30  # quanto a água recupera a sede
                self.inventory.remove(item)

            else:
                print("Não é possível consumir esse item!")
        else:
            print("Você não tem este item no inventário.")

    # Realizar Exercícios Físicos para evoluir o nível de força
    def physical_exercises(self, time_passed):
        for _ in range(time_passed):
            self.verify_bones()
            self.body["leg_right_energy"] -= 15
            self.body["leg_left_energy"] -= 15
            self.body["arm_right_energy"] -= 15
            self.body["arm_left_energy"] -= 15
            self.body["chest_energy"] -= 15
            self.body["back_energy"] -= 15
            self.lvl_up_skills("strength", (5 + self.stats["strength"]) * 0.85)
            self.update_needs(1)

    def verify_bones(self):
        body_parts = {
            "leg_right": "leg_right_bone_hp",
            "leg_left": "leg_left_bone_hp",
            "arm_right": "arm_right_bone_hp",
            "arm_left": "arm_left_bone_hp",
            "chest": "chest_bone_hp",
            "back": "back_bone_hp",
        }
        for part, bone_hp in body_parts.items():
            energy_key = f"{part}_energy"
            if self.body[energy_key] <= 0:
                self.body[bone_hp] -= 5

    def sleep(self, time_passed):
        self.needs["sleep"] += time_passed * 13
        self.needs["sleep"] = min(100, self.needs["sleep"])
        self.update_needs(time_passed)

    def get_need(self, need_name):
        return self.needs.get(need_name, 0)


if __name__ == '__main__':
    player = Player('Robert')
    player.physical_exercises(48)

    print(player.body)
    print(player.needs)
    print(player.experience_points)
    print(player.stats)
