class Gem:
    def __init__(self, tier, health, energy, attack, healing, speed, facet_positions):
        self.tier = tier
        self.health = health
        self.energy = energy
        self.attack = attack
        self.healing = healing
        self.speed = speed
        self.facet_positions = facet_positions

    def to_custom_string(self):
        facet_positions_str = ":".join(map(str, self.facet_positions))
        return f"tier#{self.tier}&health#{self.health}&energy#{self.energy}&attack#{self.attack}&healing#{self.healing}&speed#{self.speed}&facetPositions:{facet_positions_str}"

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            tier=data["tier"],
            health=data["health"],
            energy=data["energy"],
            attack=data["attack"],
            healing=data["healing"],
            speed=data["speed"],
            facet_positions=data["facetPositions"]
        )




class BaseMinion:
    def __init__(self, minion_dex_id, base_minion_name, minion_battle_sprite, minion_icon_positioning_x,
                 minion_icon_positioning_y, base_health, base_energy, base_attack, base_healing, base_speed,
                 exp_gain_rate, minion_type1, minion_type2, number_of_gems, number_of_locked_gems, evolution_level,
                 spealization_moves, starting_moves):
        self.minion_dex_id = minion_dex_id
        self.base_minion_name = base_minion_name
        self.minion_battle_sprite = minion_battle_sprite
        self.minion_icon_positioning_x = minion_icon_positioning_x
        self.minion_icon_positioning_y = minion_icon_positioning_y
        self.base_health = base_health
        self.base_energy = base_energy
        self.base_attack = base_attack
        self.base_healing = base_healing
        self.base_speed = base_speed
        self.exp_gain_rate = exp_gain_rate
        self.minion_type1 = minion_type1
        self.minion_type2 = minion_type2
        self.number_of_gems = number_of_gems
        self.number_of_locked_gems = number_of_locked_gems
        self.evolution_level = evolution_level
        self.spealization_moves = spealization_moves
        self.starting_moves = starting_moves

    @classmethod
    def from_dict(cls, data):
        return cls(
            minion_dex_id=data["minionDexID"],
            base_minion_name=data["baseMinionName"],
            minion_battle_sprite=data["minionBattleSprite"],
            minion_icon_positioning_x=data["minionIconPositioningX"],
            minion_icon_positioning_y=data["minionIconPositioningY"],
            base_health=data["baseHealth"],
            base_energy=data["baseEnergy"],
            base_attack=data["baseAttack"],
            base_healing=data["baseHealing"],
            base_speed=data["baseSpeed"],
            exp_gain_rate=data["expGainRate"],
            minion_type1=data["minionType1"],
            minion_type2=data["minionType2"],
            number_of_gems=data["numberOfGems"],
            number_of_locked_gems=data["numberOfLockedGems"],
            evolution_level=data["evolutionLevel"],
            spealization_moves=data["spealizationMoves"],
            starting_moves=data["startingMoves"]
        )

    def to_custom_string(self):
        return f"minionDexID§{self.minion_dex_id}|baseMinionName§\"{self.base_minion_name}\""



class Minion:
    def __init__(self, minion_id, minion_dex_id, minion_name, is_players_minion, trainer_type, stat_bonus,
                 curr_health_stat, curr_energy_stat, curr_attack_stat, curr_healing_stat, curr_speed_stat,
                 current_exp, trained_move, ivs, gems, curr_health, curr_energy, curr_shield, max_shield,
                 is_battle_mod_shield_active, is_extra_battle_mod_minion, curr_exhaust, curr_stat_stages,
                 move_order_position, has_moved_on_this_turn, is_frozen, turns_frozen, is_stunned, curr_charge_move,
                 charge_allies_it_hits, charge_enemies_it_hits, curr_charge, curr_level, curr_exp_percentage_to_next_level,
                 all_moves, active_moves, global_moves, available_talent_points, curr_health_percentage,
                 curr_energy_percentage, max_health_stat, max_energy_stat, max_attack_stat, max_healing_stat,
                 curr_crit_chance, curr_armor_mod_rate, curr_reflect_damage_percentage, curr_redirect_damage, base_minion):
        self.minion_id = minion_id
        self.minion_dex_id = minion_dex_id
        self.minion_name = minion_name
        self.is_players_minion = is_players_minion
        self.trainer_type = trainer_type
        self.stat_bonus = stat_bonus
        self.curr_health_stat = curr_health_stat
        self.curr_energy_stat = curr_energy_stat
        self.curr_attack_stat = curr_attack_stat
        self.curr_healing_stat = curr_healing_stat
        self.curr_speed_stat = curr_speed_stat
        self.current_exp = current_exp
        self.trained_move = trained_move
        self.ivs = ivs
        self.gems = gems
        self.curr_health = curr_health
        self.curr_energy = curr_energy
        self.curr_shield = curr_shield
        self.max_shield = max_shield
        self.is_battle_mod_shield_active = is_battle_mod_shield_active
        self.is_extra_battle_mod_minion = is_extra_battle_mod_minion
        self.curr_exhaust = curr_exhaust
        self.curr_stat_stages = curr_stat_stages
        self.move_order_position = move_order_position
        self.has_moved_on_this_turn = has_moved_on_this_turn
        self.is_frozen = is_frozen
        self.turns_frozen = turns_frozen
        self.is_stunned = is_stunned
        self.curr_charge_move = curr_charge_move
        self.charge_allies_it_hits = charge_allies_it_hits
        self.charge_enemies_it_hits = charge_enemies_it_hits
        self.curr_charge = curr_charge
        self.curr_level = curr_level
        self.curr_exp_percentage_to_next_level = curr_exp_percentage_to_next_level
        self.all_moves = all_moves
        self.active_moves = active_moves
        self.global_moves = global_moves
        self.available_talent_points = available_talent_points
        self.curr_health_percentage = curr_health_percentage
        self.curr_energy_percentage = curr_energy_percentage
        self.max_health_stat = max_health_stat
        self.max_energy_stat = max_energy_stat
        self.max_attack_stat = max_attack_stat
        self.max_healing_stat = max_healing_stat
        self.curr_crit_chance = curr_crit_chance
        self.curr_armor_mod_rate = curr_armor_mod_rate
        self.curr_reflect_damage_percentage = curr_reflect_damage_percentage
        self.curr_redirect_damage = curr_redirect_damage
        self.base_minion = base_minion

    @classmethod
    def from_dict(cls, data):
        owned_data = data["ownedMinion"]
        base_minion_data = BaseMinion.from_dict(data["baseMinion"])

        # Create Gem instances from gems list
        gems = [Gem.from_dict(gem) for gem in owned_data["gems"]]

        return cls(
            minion_id=owned_data["minionID"],
            minion_dex_id=owned_data["minionDexID"],
            minion_name=owned_data["minionName"],
            is_players_minion=owned_data["isPlayersMinion"],
            trainer_type=owned_data["trainerType"],
            stat_bonus=owned_data["statBonus"],
            curr_health_stat=owned_data["currHealthStat"],
            curr_energy_stat=owned_data["currEnergyStat"],
            curr_attack_stat=owned_data["currAttackStat"],
            curr_healing_stat=owned_data["currHealingStat"],
            curr_speed_stat=owned_data["currSpeedStat"],
            current_exp=owned_data["currentExp"],
            trained_move=owned_data["trainedMove"],
            ivs=owned_data["IVs"],
            gems=gems,
            curr_health=owned_data["currHealth"],
            curr_energy=owned_data["currEnergy"],
            curr_shield=owned_data["currShield"],
            max_shield=owned_data["maxShield"],
            is_battle_mod_shield_active=owned_data["isBattleModShieldActive"],
            is_extra_battle_mod_minion=owned_data["isExtraBattleModMinion"],
            curr_exhaust=owned_data["currExhaust"],
            curr_stat_stages=owned_data["currStatStages"],
            move_order_position=owned_data["moveOrderPosition"],
            has_moved_on_this_turn=owned_data["hasMovedOnThisTurn"],
            is_frozen=owned_data["isFrozen"],
            turns_frozen=owned_data["turnsFrozen"],
            is_stunned=owned_data["isStunned"],
            curr_charge_move=owned_data["currChargeMove"],
            charge_allies_it_hits=owned_data["chargeAlliesItHits"],
            charge_enemies_it_hits=owned_data["chargeEnemiesItHits"],
            curr_charge=owned_data["currCharge"],
            curr_level=owned_data["currLevel"],
            curr_exp_percentage_to_next_level=owned_data["currExpPercentageToNextLevel"],
            all_moves=owned_data["allMoves"],
            active_moves=owned_data["activeMoves"],
            global_moves=owned_data["globalMoves"],
            available_talent_points=owned_data["availableTalentPoints"],
            curr_health_percentage=owned_data["currHealthPercentage"],
            curr_energy_percentage=owned_data["currEnergyPercentage"],
            max_health_stat=owned_data["maxHealthStat"],
            max_energy_stat=owned_data["maxEnergyStat"],
            max_attack_stat=owned_data["maxAttackStat"],
            max_healing_stat=owned_data["maxHealingStat"],
            curr_crit_chance=owned_data["currCritChance"],
            curr_armor_mod_rate=owned_data["currArmorModRate"],
            curr_reflect_damage_percentage=owned_data["currReflectDamagePercentage"],
            curr_redirect_damage=owned_data["currRedirectDamage"],
            base_minion=base_minion_data
        )

    def to_custom_string(self):
        ivs_str = "~".join(map(str, self.ivs))
        gems_str = "~".join([gem.to_custom_string() if gem is not None else "null" for gem in self.gems])
        charge_allies_it_hits_str = "~".join(map(str, self.charge_allies_it_hits))
        charge_enemies_it_hits_str = "~".join(map(str, self.charge_enemies_it_hits))
        all_moves_str = "~".join(map(str, self.all_moves))

        return (
            f"minionID§{self.minion_id}|minionDexID§{self.minion_dex_id}|minionName§\"{self.minion_name}\"|"
            f"isPlayersMinion§{str(self.is_players_minion).lower()}|trainerType§{self.trainer_type}|statBonus§{self.stat_bonus}|"
            f"currHealthStat§{self.curr_health_stat}|currEnergyStat§{self.curr_energy_stat}|currAttackStat§{self.curr_attack_stat}|"
            f"currHealingStat§{self.curr_healing_stat}|currSpeedStat§{self.curr_speed_stat}|currentExp§{self.current_exp}|"
            f"trainedMove§{self.trained_move}|IVs§{ivs_str}|gems§{gems_str}|currHealth§{self.curr_health}|currEnergy§{self.curr_energy}|"
            f"currShield§{self.curr_shield}|maxShield§{self.max_shield}|isBattleModShieldActive§{str(self.is_battle_mod_shield_active).lower()}|"
            f"allMoves§{all_moves_str}|"
        )

    def save_to_text(self):
        with open(f"minions/minion_{self.minion_id}.txt", "w", encoding="utf-8") as file:
            file.write(self.to_custom_string())