"""
Enhanced Combat System - Améliore le CombatSystem de dnd-5e-core
Pour gérer les personnages sans méthode attack()
"""

from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics import DamageDice
from typing import List, Optional
from random import randint


class EnhancedCombatSystem(CombatSystem):
    """
    Système de combat amélioré qui calcule les dommages correctement
    même pour les personnages qui n'ont pas de méthode attack()
    """

    def character_turn(self,
                      character,
                      alive_chars: List,
                      alive_monsters: List,
                      party: List,
                      weapons: Optional[List] = None,
                      armors: Optional[List] = None,
                      equipments: Optional[List] = None,
                      potions: Optional[List] = None) -> None:
        """
        Tour de personnage avec calcul de dommages D&D 5e correct
        """
        if not alive_monsters:
            return

        # Même priorité de soins/potions que le parent
        # 1. Vérifier soins magiques
        healing_spells = []
        if hasattr(character, 'is_spell_caster') and character.is_spell_caster:
            if hasattr(character, 'sc') and hasattr(character.sc, 'learned_spells'):
                healing_spells = [s for s in character.sc.learned_spells
                                  if hasattr(s, 'heal_at_slot_level') and s.heal_at_slot_level
                                  and character.sc.spell_slots[s.level - 1] > 0]

        if healing_spells and any(c for c in alive_chars if c.hit_points < 0.5 * c.max_hit_points):
            # Appeler la version parente pour les soins
            super().character_turn(character, alive_chars, alive_monsters, party,
                                 weapons, armors, equipments, potions)
            return

        # 2. Potions
        if hasattr(character, 'healing_potions') and character.hit_points < 0.3 * character.max_hit_points and character.healing_potions:
            super().character_turn(character, alive_chars, alive_monsters, party,
                                 weapons, armors, equipments, potions)
            return

        # 3. ATTAQUE - Version améliorée
        monster = self._select_target_monster(character, alive_chars, alive_monsters)

        # Déterminer le nom de l'arme pour l'affichage
        weapon_name = "ses poings"
        if hasattr(character, 'weapon') and character.weapon:
            weapon_name = character.weapon.name.lower()
        elif hasattr(character, 'class_type'):
            class_name = character.class_type.index.lower()
            if 'fighter' in class_name or 'paladin' in class_name:
                weapon_name = "son épée"
            elif 'rogue' in class_name:
                weapon_name = "sa dague"
            elif 'cleric' in class_name:
                weapon_name = "sa masse"
            elif 'wizard' in class_name:
                weapon_name = "son bâton"

        self.log_message(f"{character.name} attacks {monster.name}!")

        # Calcul de dommages D&D 5e correct (ne pas utiliser character.attack())
        damage = self._calculate_character_damage(character)

        # Jet d'attaque
        attack_roll = randint(1, 20)
        str_mod = (character.abilities.str - 10) // 2
        dex_mod = (character.abilities.dex - 10) // 2

        # Choisir STR ou DEX selon la classe
        attack_bonus = str_mod
        if hasattr(character, 'class_type') and 'rogue' in character.class_type.index.lower():
            attack_bonus = dex_mod

        attack_bonus += character.level // 4 + 2  # Bonus de maîtrise

        total_attack = attack_roll + attack_bonus

        # CA du monstre
        monster_ac = getattr(monster, 'armor_class', 12)

        if attack_roll == 1:
            self.log_message(f"{character.name} misses {monster.name}!")
            return
        elif attack_roll == 20:
            damage *= 2  # Coup critique
            self.log_message(f"{character.name} strikes {monster.name} with {weapon_name} for {damage} hit points! (CRITICAL HIT)")
        elif total_attack >= monster_ac:
            self.log_message(f"{character.name} strikes {monster.name} with {weapon_name} for {damage} hit points!")
        else:
            self.log_message(f"{character.name} misses {monster.name}!")
            return

        # Appliquer dommages
        monster.hit_points -= damage

        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            self.log_message(f"{monster.name} is KILLED!")
            character.kills.append(monster)
            self._handle_victory(character, monster, weapons, armors, equipments, potions)

    def _calculate_character_damage(self, character) -> int:
        """
        Calculer les dommages d'un personnage selon D&D 5e
        Utilise l'arme équipée si disponible
        """
        # Modificateurs d'aptitudes
        str_mod = (character.abilities.str - 10) // 2
        dex_mod = (character.abilities.dex - 10) // 2

        # Déterminer l'arme et le modificateur
        damage_dice = "1d4"  # Par défaut (coup de poing)
        ability_mod = str_mod
        weapon_name = "poing"

        # ✅ PRIORITÉ 1: Utiliser l'arme équipée si elle existe
        if hasattr(character, 'weapon') and character.weapon:
            weapon = character.weapon
            weapon_name = weapon.name

            # Extraire les dés de dommages de l'arme
            if hasattr(weapon, 'damage_dice'):
                if hasattr(weapon.damage_dice, 'dd'):
                    damage_dice = weapon.damage_dice.dd
                else:
                    damage_dice = str(weapon.damage_dice)

            # Utiliser FOR pour armes de mêlée, DEX pour armes à distance/finesse
            if hasattr(weapon, 'range_type'):
                from dnd_5e_core.equipment import RangeType
                if weapon.range_type == RangeType.RANGED:
                    ability_mod = dex_mod
                else:
                    ability_mod = str_mod
            elif hasattr(weapon, 'properties'):
                # Vérifier si l'arme a la propriété "finesse"
                if any(hasattr(p, 'index') and p.index == 'finesse' for p in weapon.properties):
                    ability_mod = max(str_mod, dex_mod)  # Finesse = choisir le meilleur
                else:
                    ability_mod = str_mod
            else:
                ability_mod = str_mod

        # PRIORITÉ 2: Fallback selon la classe si pas d'arme équipée
        elif hasattr(character, 'class_type'):
            class_name = character.class_type.index.lower()

            if 'fighter' in class_name or 'paladin' in class_name:
                damage_dice = "1d8"  # Épée longue
                ability_mod = str_mod
                weapon_name = "épée longue"
            elif 'rogue' in class_name or 'ranger' in class_name:
                damage_dice = "1d6"  # Épée courte/arc
                ability_mod = dex_mod
                weapon_name = "épée courte"
            elif 'cleric' in class_name:
                damage_dice = "1d6"  # Masse d'armes
                ability_mod = str_mod
                weapon_name = "masse d'armes"
            elif 'wizard' in class_name or 'sorcerer' in class_name:
                damage_dice = "1d4"  # Dague
                ability_mod = dex_mod
                weapon_name = "dague"

        # Lancer les dés de dommages
        try:
            dice_parts = damage_dice.split('d')
            num_dice = int(dice_parts[0])
            dice_size = int(dice_parts[1])

            total_damage = sum(randint(1, dice_size) for _ in range(num_dice))
            total_damage += ability_mod
        except:
            # Fallback si parsing échoue
            total_damage = randint(1, 6) + ability_mod

        # Stocker le nom de l'arme pour l'affichage
        if not hasattr(character, '_last_weapon_used'):
            character._last_weapon_used = weapon_name

        # Minimum 1 dommage
        return max(1, total_damage)

