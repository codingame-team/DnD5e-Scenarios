"""
Factory pour créer des monstres depuis le package dnd_5e_core
"""
from typing import Optional, List
from dnd_5e_core import Monster, Abilities
from dnd_5e_core.combat import Action, ActionType, Damage
from dnd_5e_core.mechanics import DamageDice
from dnd_5e_core.equipment import DamageType
from dnd_5e_core.data.loader import load_monster


class MonsterFactory:
    """Factory pour créer monstres depuis dnd_5e_core"""

    def __init__(self, monsters_data=None):
        """
        Args:
            monsters_data: Paramètre optionnel pour compatibilité (ignoré)
        """
        # Le paramètre est gardé pour compatibilité mais n'est plus utilisé
        pass

    def create_monster(self, monster_id: str, name: Optional[str] = None) -> Optional[Monster]:
        """
        Créer un monstre depuis son ID en utilisant dnd_5e_core.data.loader

        Args:
            monster_id: ID du monstre (ex: "goblin", "magmin")
            name: Nom personnalisé (optionnel)

        Returns:
            Monster ou None si non trouvé
        """
        # Charger les données depuis dnd_5e_core
        data = load_monster(monster_id)

        if not data:
            print(f"⚠️ Monstre non trouvé: {monster_id}")
            return None

        try:
            # Nom
            monster_name = name if name else data.get('name', monster_id.replace('-', ' ').title())

            # Abilities
            abilities_data = data.get('strength', 10), data.get('dexterity', 10), data.get('constitution', 10), \
                           data.get('intelligence', 10), data.get('wisdom', 10), data.get('charisma', 10)

            abilities = Abilities(
                str=abilities_data[0],
                dex=abilities_data[1],
                con=abilities_data[2],
                int=abilities_data[3],
                wis=abilities_data[4],
                cha=abilities_data[5]
            )

            # Actions
            actions = []
            for action_data in data.get('actions', []):
                if 'damage' not in action_data:
                    # Action sans dégâts (ex: grapple)
                    continue

                # Type de dégâts
                damage_list = action_data.get('damage', [])
                if not damage_list:
                    continue

                damage_info = damage_list[0] if isinstance(damage_list, list) else damage_list
                damage_type_data = damage_info.get('damage_type', {})

                damage_type = DamageType(
                    index=damage_type_data.get('index', 'bludgeoning'),
                    name=damage_type_data.get('name', 'Bludgeoning'),
                    desc=f"{damage_type_data.get('name', 'bludgeoning')} damage"
                )

                # Formule de dégâts
                damage_dice_str = damage_info.get('damage_dice', '1d4')

                damages = [Damage(
                    type=damage_type,
                    dd=DamageDice(damage_dice_str)
                )]

                # Type d'action
                action_type = ActionType.MELEE if 'melee' in action_data.get('desc', '').lower() else ActionType.RANGED

                action = Action(
                    name=action_data.get('name', 'Attack'),
                    desc=action_data.get('desc', ''),
                    type=action_type,
                    attack_bonus=action_data.get('attack_bonus', 0),
                    damages=damages,
                    normal_range=action_data.get('range', '5 ft')
                )
                actions.append(action)

            # Armor class
            armor_class_data = data.get('armor_class', [])
            if isinstance(armor_class_data, list) and armor_class_data:
                armor_class = armor_class_data[0].get('value', 10)
            elif isinstance(armor_class_data, int):
                armor_class = armor_class_data
            else:
                armor_class = 10

            # Hit points
            hit_points = data.get('hit_points', 10)
            hit_dice = data.get('hit_points_roll', data.get('hit_dice', '1d8'))

            # Speed
            speed_data = data.get('speed', {})
            speed = speed_data.get('walk', '30 ft').replace(' ft', '').strip()
            try:
                speed = int(speed)
            except:
                speed = 30

            # Challenge rating
            challenge_rating = data.get('challenge_rating', 0)
            if isinstance(challenge_rating, str):
                # Handle fractional CR like "1/2", "1/4"
                if '/' in challenge_rating:
                    num, denom = challenge_rating.split('/')
                    challenge_rating = float(num) / float(denom)
                else:
                    challenge_rating = float(challenge_rating)

            # XP
            xp = data.get('xp', 0)

            # Créer le monstre
            monster = Monster(
                index=data.get('index', monster_id),
                name=monster_name,
                abilities=abilities,
                proficiencies=[],
                armor_class=armor_class,
                hit_points=hit_points,
                hit_dice=hit_dice,
                xp=xp,
                speed=speed,
                challenge_rating=challenge_rating,
                actions=actions
            )

            return monster

        except Exception as e:
            print(f"⚠️ Erreur lors de la création du monstre {monster_id}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_monsters(self, monster_ids: list) -> list:
        """
        Créer plusieurs monstres

        Args:
            monster_ids: Liste d'IDs (peut inclure tuples (id, name))

        Returns:
            Liste de Monster
        """
        monsters = []

        for item in monster_ids:
            if isinstance(item, tuple):
                monster_id, name = item
                monster = self.create_monster(monster_id, name)
            else:
                monster = self.create_monster(item)

            if monster:
                monsters.append(monster)

        return monsters

