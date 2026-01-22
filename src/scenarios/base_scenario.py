"""
Classe de base pour tous les scénarios D&D 5e
Factorisation du code commun entre scénarios
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dnd_5e_core import Character, Monster
from dnd_5e_core.combat import CombatSystem

from ..utils.pdf_reader import PDFScenarioReader
from ..utils.save_manager import SaveGameManager, JSONLoader
from ..utils.exploration_map import ExplorationMap
from ..utils.level_manager import LevelUpManager, VillageRestManager
from ..utils.monster_factory import MonsterFactory
from ..scenes.scene_system import SceneManager
from ..rendering.renderer import create_renderer, Renderer
from ..systems.spellcasting_v2 import SpellcastingManager
from ..systems.merchant import MerchantSystem
from ..config import GameSettings


class BaseScenario(ABC):
    """
    Classe de base abstraite pour tous les scénarios
    Fournit les fonctionnalités communes
    """

    def __init__(self, pdf_path: str, use_ncurses: bool = False):
        """
        Initialiser le scénario

        Args:
            pdf_path: Chemin vers le PDF du scénario
            use_ncurses: Utiliser interface ncurses ou console
        """
        self.pdf_path = pdf_path

        # Systèmes de jeu
        self.renderer = create_renderer(use_ncurses)
        
        # Utiliser le CombatSystem de dnd-5e-core (ne pas réinventer la roue)
        self.combat_system = CombatSystem(verbose=True)
        self.spellcasting = SpellcastingManager()
        self.merchant_system = MerchantSystem()
        self.scene_manager = SceneManager()

        # 🆕 Nouveaux systèmes
        self.save_manager = SaveGameManager()
        self.json_loader = JSONLoader()
        self.exploration_map: Optional[ExplorationMap] = None
        self.level_manager = LevelUpManager()
        self.village_rest = VillageRestManager()

        # 🆕 Monster loader depuis fichiers JSON locaux + dnd_5e_core package
        from dnd_5e_core.data import load_monster
        from dnd_5e_core import Monster, Abilities
        from dnd_5e_core.combat import Action, ActionType, Damage
        from dnd_5e_core.mechanics import DamageDice
        from dnd_5e_core.equipment import DamageType
        import json
        from pathlib import Path

        # Créer un wrapper pour compatibilité avec l'ancienne interface
        class MonsterFactoryWrapper:
            def __init__(self):
                # Charger les monstres locaux depuis JSON
                local_monsters_path = Path(__file__).parent.parent.parent / "data" / "monsters" / "all_monsters.json"
                self.local_monsters = {}
                if local_monsters_path.exists():
                    try:
                        with open(local_monsters_path, 'r', encoding='utf-8') as f:
                            self.local_monsters = json.load(f)
                    except Exception as e:
                        print(f"⚠️ Erreur chargement monstres locaux: {e}")

            def create_monster(self, monster_id: str, name: Optional[str] = None):
                """Créer un monstre en utilisant les données locales ou dnd_5e_core.data.load_monster"""
                # 1. Essayer d'abord les monstres locaux
                if monster_id in self.local_monsters:
                    return self._create_from_local(monster_id, name)

                # 2. Sinon, essayer l'API dnd_5e_core
                normalized_id = monster_id.replace('_', '-')
                monster_data = load_monster(normalized_id)
                if not monster_data:
                    monster_data = load_monster(monster_id)

                if monster_data:
                    return self._create_from_api(monster_data, monster_id, name)

                print(f"⚠️ Monstre non trouvé: {monster_id}")
                return None

            def _create_from_local(self, monster_id: str, name: Optional[str] = None):
                """Créer un monstre depuis les données locales JSON"""
                data = self.local_monsters[monster_id]

                try:
                    abilities = Abilities(
                        str=data['abilities']['str'],
                        dex=data['abilities']['dex'],
                        con=data['abilities']['con'],
                        int=data['abilities']['int'],
                        wis=data['abilities']['wis'],
                        cha=data['abilities']['cha']
                    )

                    # Convertir les actions
                    actions = []
                    for action_data in data.get('actions', []):
                        # Ignorer les actions sans attaque (comme Multiattack)
                        if 'attack_bonus' not in action_data:
                            continue

                        damage_type_name = action_data.get('damage_type', 'slashing')
                        damage_type = DamageType(
                            index=damage_type_name.lower(),
                            name=damage_type_name.capitalize(),
                            desc=f"{damage_type_name} damage"
                        )

                        # Parser la portée (range)
                        range_str = action_data.get('range', '5 ft')
                        if '/' in range_str:
                            # Format: "80/320 ft"
                            normal_range = int(range_str.split('/')[0].replace(' ft', '').replace('ft', '').strip())
                        else:
                            # Format: "5 ft" ou "5"
                            normal_range = int(range_str.replace(' ft', '').replace('ft', '').strip())

                        action = Action(
                            name=action_data['name'],
                            desc=action_data.get('desc', ''),
                            type=ActionType.MELEE if normal_range <= 10 else ActionType.RANGED,
                            attack_bonus=action_data['attack_bonus'],
                            damages=[Damage(
                                type=damage_type,
                                dd=DamageDice(action_data.get('damage_dice', '1d6'))
                            )],
                            normal_range=normal_range
                        )
                        actions.append(action)

                    # Extraire la vitesse
                    speed_data = data.get('speed', {})
                    if isinstance(speed_data, dict):
                        walk_speed = speed_data.get('walk', '30 ft')
                    else:
                        walk_speed = '30 ft'
                    speed = int(walk_speed.replace(' ft', '').replace('ft', '').strip())

                    monster = Monster(
                        index=monster_id,
                        name=name if name else data['name'],
                        abilities=abilities,
                        proficiencies=[],
                        armor_class=data['armor_class'],
                        hit_points=data['hit_points'],
                        hit_dice=data['hit_dice'],
                        xp=data['xp'],
                        speed=speed,
                        challenge_rating=data['challenge_rating'],
                        actions=actions
                    )

                    return monster

                except Exception as e:
                    print(f"⚠️ Erreur lors de la création du monstre local {monster_id}: {e}")
                    import traceback
                    traceback.print_exc()
                    return None

            def _create_from_api(self, monster_data: dict, monster_id: str, name: Optional[str] = None):
                """Créer un monstre depuis les données de l'API dnd_5e_core"""
                try:
                    abilities = Abilities(
                        str=monster_data.get('strength', 10),
                        dex=monster_data.get('dexterity', 10),
                        con=monster_data.get('constitution', 10),
                        int=monster_data.get('intelligence', 10),
                        wis=monster_data.get('wisdom', 10),
                        cha=monster_data.get('charisma', 10)
                    )

                    # Convertir les actions
                    actions = []
                    for action_data in monster_data.get('actions', []):
                        if 'attack_bonus' in action_data and 'damage' in action_data:
                            damage_parts = action_data['damage'][0] if action_data['damage'] else {}
                            damage_type_name = damage_parts.get('damage_type', {}).get('name', 'slashing')

                            damage_type = DamageType(
                                index=damage_type_name.lower(),
                                name=damage_type_name,
                                desc=f"{damage_type_name} damage"
                            )

                            action = Action(
                                name=action_data.get('name', 'Attack'),
                                desc=action_data.get('desc', ''),
                                type=ActionType.MELEE,
                                attack_bonus=action_data.get('attack_bonus', 0),
                                damages=[Damage(
                                    type=damage_type,
                                    dd=DamageDice(damage_parts.get('damage_dice', '1d6'))
                                )],
                                normal_range=5
                            )
                            actions.append(action)

                    monster = Monster(
                        index=monster_data.get('index', monster_id),
                        name=name if name else monster_data.get('name', 'Unknown'),
                        abilities=abilities,
                        proficiencies=[],
                        armor_class=monster_data.get('armor_class', 10),
                        hit_points=monster_data.get('hit_points', 1),
                        hit_dice=monster_data.get('hit_dice', '1d8'),
                        xp=monster_data.get('xp', 0),
                        speed=monster_data.get('speed', {}).get('walk', '30 ft').replace(' ft', '').replace('ft', '').strip() if isinstance(monster_data.get('speed'), dict) else 30,
                        challenge_rating=monster_data.get('challenge_rating', 0),
                        actions=actions
                    )

                    return monster

                except Exception as e:
                    print(f"⚠️ Erreur lors de la création du monstre API {monster_id}: {e}")
                    import traceback
                    traceback.print_exc()
                    return None

        self.monster_factory = MonsterFactoryWrapper()

        # Données du scénario
        self.scenario_data: Optional[Dict] = None
        self.party: List[Character] = []

        # État du jeu
        self.game_state = self._init_game_state()

    def _init_game_state(self) -> Dict:
        """Initialiser l'état du jeu (peut être surchargé)"""
        return {
            'combat_victories': 0,
            'total_xp': 0,
            'gold': 0,
            'gold_spent': 0,
            'locations_visited': 0,
            'npcs_met': 0,
            'quests_completed': 0,
            'deaths': 0,
        }

    @abstractmethod
    def get_scenario_name(self) -> str:
        """Retourner le nom du scénario"""
        pass

    @abstractmethod
    def create_party(self) -> List[Character]:
        """Créer le groupe de personnages spécifique au scénario"""
        pass

    @abstractmethod
    def build_custom_scenes(self):
        """
        Construire les scènes personnalisées du scénario
        Cette méthode doit ajouter les scènes au scene_manager
        """
        pass

    def load_scenario_from_pdf(self):
        """Charger et analyser le PDF du scénario"""
        self.renderer.print_header(f"📖 CHARGEMENT: {self.get_scenario_name()}")

        print(f"Lecture du PDF...")

        try:
            with PDFScenarioReader(self.pdf_path) as reader:
                self.scenario_data = {
                    'title': reader.pdf_path.stem,
                    'sections': reader.extract_sections(),
                    'locations': reader.extract_locations(),
                    'npcs': reader.extract_npcs(),
                    'encounters': reader.extract_encounters(),
                    'maps': reader.extract_maps_as_ascii()
                }

            print(f"✅ Scénario chargé:")
            print(f"   - Titre: {self.scenario_data['title']}")
            print(f"   - Sections: {len(self.scenario_data['sections'])}")
            print(f"   - Lieux: {len(self.scenario_data['locations'])}")
            print(f"   - PNJs: {len(self.scenario_data['npcs'])}")

        except Exception as e:
            print(f"⚠️  Erreur lors du chargement du PDF: {e}")
            print("   Le jeu continuera avec les scènes prédéfinies.")
            self.scenario_data = {
                'title': self.get_scenario_name(),
                'sections': {},
                'locations': [],
                'npcs': [],
                'encounters': [],
                'maps': []
            }

        self.renderer.wait_for_input()

    def setup_party(self):
        """Configurer le groupe de personnages"""
        self.renderer.print_header("⚔️ CRÉATION DU GROUPE")

        # Si un fichier de groupe pré-généré existe pour ce scénario, proposer de le charger
        try:
            from pathlib import Path
            scenario_name = self.get_scenario_name()

            # Fonction helper pour normaliser un nom
            def normalize_name(name):
                """Convertir en minuscules avec underscores"""
                import re
                # Enlever les articles au début
                name = re.sub(r'^(Le|La|Les|L\')\s+', '', name, flags=re.IGNORECASE)
                # Remplacer espaces et tirets par underscores
                name = name.replace(' ', '_').replace('-', '_').replace("'", '')
                # Enlever parenthèses et leur contenu
                name = re.sub(r'\([^)]*\)', '', name)
                # Nettoyer underscores multiples
                name = re.sub(r'_+', '_', name).strip('_')
                # Minuscules
                return name.lower()

            # Essayer plusieurs patterns de noms de fichiers
            possible_files = [
                Path('data/parties') / f"{scenario_name}_party.json",
                Path('data/parties') / f"{normalize_name(scenario_name)}_party.json",
                # Essayer sans articles
                Path('data/parties') / f"{scenario_name.replace('Le ', '').replace('La ', '').replace('Les ', '').strip()}_party.json",
                # Essayer version simplifiée
                Path('data/parties') / f"{scenario_name.split('(')[0].strip()}_party.json",
            ]

            # Chercher le premier fichier qui existe
            scenario_party_file = None
            for file_path in possible_files:
                if file_path.exists():
                    scenario_party_file = file_path
                    break

            # Si toujours pas trouvé, chercher par correspondance partielle
            if not scenario_party_file:
                normalized_search = normalize_name(scenario_name)
                parties_dir = Path('data/parties')
                if parties_dir.exists():
                    for json_file in parties_dir.glob('*_party.json'):
                        if normalized_search in json_file.stem.lower():
                            scenario_party_file = json_file
                            break

            # Charger automatiquement si le fichier existe
            if scenario_party_file:
                print(f"📦 Fichier de groupe trouvé: {scenario_party_file.name}")
                loaded = self.load_party_from_json(str(scenario_party_file))
                if loaded:
                    print(f"✅ Groupe chargé depuis JSON")
                else:
                    print(f"⚠️ Échec du chargement, création par défaut")
                    self.party = self.create_party()
            else:
                print(f"📝 Aucun fichier de groupe trouvé pour '{scenario_name}'")
                print(f"   (recherché: {normalize_name(scenario_name)}_party.json)")
                self.party = self.create_party()
        except Exception as e:
            # En cas d'erreur, fallback à la création classique
            print(f"⚠️ Erreur lors du chargement: {e}")
            self.party = self.create_party()

        # Initialiser inventaires avec slots vides (20 slots par défaut)
        for char in self.party:
            if not char.inventory:
                char.inventory = []
            # Ajouter slots vides pour permettre le loot
            while len(char.inventory) < 20:
                char.inventory.append(None)

        print(f"\n👥 Groupe créé ({len(self.party)} membres):")
        for char in self.party:
            class_name = char.class_type.name if char.class_type else "Aventurier"
            print(f"  - {char.name} ({class_name} niveau {char.level})")
            print(f"    HP: {char.hit_points}/{char.max_hit_points}, "
                  f"CA: {char.armor_class}")
            
            # Afficher sorts si lanceur de sorts
            if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'spells') and char.sc.spells:
                spell_names = ', '.join([s.name for s in char.sc.spells[:3]])
                more = f" (+{len(char.sc.spells)-3} autres)" if len(char.sc.spells) > 3 else ""
                print(f"    📜 Sorts: {spell_names}{more}")
        
        # 🆕 Équiper le groupe avec équipement de base
        self._equip_party_with_starter_gear()
        
        # Note: simple_character_generator charge déjà les sorts automatiquement
        # mais on peut ajouter des sorts spécifiques si nécessaire
        self._init_spellcasters()

        self.renderer.wait_for_input()

    def build_scenes(self):
        """Construire toutes les scènes du scénario"""
        self.renderer.print_header("🎬 PRÉPARATION DE L'AVENTURE")

        print("Construction des scènes...")

        # Scènes personnalisées du scénario
        self.build_custom_scenes()

        # Scène de game over (commune à tous)
        from ..scenes.scene_system import NarrativeScene
        self.scene_manager.add_scene(NarrativeScene(
            scene_id="game_over",
            title="💀 GAME OVER",
            text="Votre groupe a été vaincu... L'aventure se termine ici.",
            next_scene_id=None
        ))

        print(f"✅ {len(self.scene_manager.scenes)} scènes créées")
        self.renderer.wait_for_input()

    def play(self):
        """Lancer le scénario complet"""
        self.renderer.print_header(f"🎲 {self.get_scenario_name().upper()}")

        print("Bienvenue dans cette aventure D&D 5e!")

        # 🆕 Proposer de charger une partie
        if self._ask_load_game():
            return

        self.renderer.wait_for_input()

        # 1. Charger le PDF
        # self.load_scenario_from_pdf()

        # 2. Créer le groupe
        self.setup_party()

        # 3. Construire les scènes
        self.build_scenes()

        # 3.5 🆕 Charger équipements pour le combat
        print(f"\n📦 Chargement des équipements...")
        weapons, armors, equipments, potions = self._load_equipment()
        print(f"  Armes: {len(weapons)}, Armures: {len(armors)}, Équipements: {len(equipments)}, Potions: {len(potions)}")

        # 3.6 🆕 Créer magic items comme trésors potentiels
        print(f"\n✨ Préparation des trésors magiques...")
        magic_items = self._create_magic_items_treasure()

        # 4. Préparer le contexte de jeu
        game_context = {
            'party': self.party,
            'game_state': self.game_state,
            'renderer': self.renderer,
            'combat_system': self.combat_system,
            'spellcasting': self.spellcasting,
            'merchant_system': self.merchant_system,
            'scenario_data': self.scenario_data,
            'weapons': weapons,        # 🆕
            'armors': armors,          # 🆕
            'equipments': equipments,  # 🆕
            'potions': potions,        # 🆕
            'magic_items': magic_items,  # 🆕 NEW: Magic items treasures
            'scenario': self           # 🆕 Pour permettre la sauvegarde depuis les scènes
        }

        # 5. Lancer le scénario
        self.renderer.print_header("🎬 DÉBUT DE L'AVENTURE")
        self.renderer.wait_for_input()

        self.scene_manager.run(game_context, start_scene_id=self.get_start_scene_id())

        # 6. Statistiques finales
        self.show_final_stats()

    def get_start_scene_id(self) -> str:
        """Retourner l'ID de la scène de départ (peut être surchargé)"""
        return "intro"

    def show_final_stats(self):
        """Afficher les statistiques finales"""
        self.renderer.print_header("📊 STATISTIQUES FINALES")

        print(f"\n⚔️  Victoires en combat: {self.game_state['combat_victories']}")
        print(f"⭐ XP total gagné: {self.game_state['total_xp']}")
        print(f"💰 Or gagné: {self.game_state['gold']} po")
        print(f"💸 Or dépensé: {self.game_state['gold_spent']} po")
        print(f"🗺️  Lieux visités: {self.game_state['locations_visited']}")
        print(f"👥 PNJs rencontrés: {self.game_state['npcs_met']}")
        print(f"🎯 Quêtes complétées: {self.game_state['quests_completed']}")

        print("\n👥 État du groupe:")
        survivors = [c for c in self.party if c.hit_points > 0]
        print(f"   Survivants: {len(survivors)}/{len(self.party)}")

        for char in self.party:
            if char.hit_points > 0:
                hp_percent = int((char.hit_points / char.max_hit_points) * 100)
                status = "✅" if hp_percent > 50 else "⚠️"
                print(f"   {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP ({hp_percent}%)")
            else:
                print(f"   ❌ {char.name}: KO")

        # Inventaires finaux
        print("\n📦 INVENTAIRES FINAUX:")
        for char in self.party:
            print(f"\n👤 {char.name}:")
            print(f"   💰 Or: {char.gold} po")
            
            # Sorts
            if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'spells') and char.sc.spells:
                print(f"   📜 Sorts ({len(char.sc.spells)}):")
                for spell in char.sc.spells:
                    print(f"      - {spell.name} (niveau {spell.level})")
            
            # Inventaire
            if hasattr(char, 'inventory') and char.inventory:
                equipped = [item for item in char.inventory if item and hasattr(item, 'equipped') and item.equipped]
                other = [item for item in char.inventory if item and not (hasattr(item, 'equipped') and item.equipped)]
                
                if equipped:
                    print(f"   ⚔️  Équipé:")
                    for item in equipped:
                        print(f"      - {item.name}")
                
                if other:
                    print(f"   🎒 Inventaire ({len(other)} objets):")
                    for item in other:
                        print(f"      - {item.name}")
            else:
                print(f"   📦 Inventaire vide")

        # Score final
        score = self._calculate_score()
        print(f"\n🏆 SCORE FINAL: {score} points")

        rank = self._get_rank(score)
        print(f"   Rang: {rank}")

        print("\n🎉 Merci d'avoir joué!")
        self.renderer.wait_for_input()

    def _calculate_score(self) -> int:
        """Calculer le score final"""
        score = 0

        # Points pour XP
        score += self.game_state['total_xp']

        # Points pour or (10 po = 1 point)
        score += (self.game_state['gold'] - self.game_state['gold_spent']) // 10

        # Bonus survivants
        survivors = [c for c in self.party if c.hit_points > 0]
        score += len(survivors) * 100

        # Bonus HP restants
        for char in survivors:
            hp_percent = (char.hit_points / char.max_hit_points)
            score += int(hp_percent * 50)

        # Bonus quêtes
        score += self.game_state['quests_completed'] * 200

        # Malus morts
        score -= self.game_state['deaths'] * 100

        return max(0, score)

    def _get_rank(self, score: int) -> str:
        """Obtenir le rang selon le score"""
        if score >= 2000:
            return "Légendaire 🏆✨"
        elif score >= 1500:
            return "Héroïque ⭐⭐⭐"
        elif score >= 1000:
            return "Vaillant ⭐⭐"
        elif score >= 500:
            return "Courageux ⭐"
        else:
            return "Débutant"

    def create_basic_fighter(self, name: str, level: int = 3) -> Character:
        """Utilitaire: créer un guerrier de base"""
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from ..core.adapters import CharacterExtensions

        race = Race(
            index='human', name='Humain', speed=30, ability_bonuses={},
            alignment='Any', age='Adult', size='Medium', size_description='5-6 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common', traits=[], subraces=[]
        )

        fighter_class = ClassType(
            index='fighter', name='Fighter', hit_die=10, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.STR, AbilityType.CON],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=0,
            spellcasting_ability=None, can_cast=False, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        char = Character(
            name=name, race=race, subrace=None, ethnic='Human', gender='Male',
            height='6ft', weight='180 lbs', age=30,
            class_type=fighter_class, proficiencies=[],
            abilities=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
            ability_modifiers=Abilities(str=16, dex=14, con=15, int=10, wis=12, cha=10),
            hit_points=10 + (level-1)*6 + level*2,  # HD + Con
            max_hit_points=10 + (level-1)*6 + level*2,
            speed=30, haste_timer=0.0, hasted=False,
            xp=level * 300, level=level,
            inventory=[], gold=50, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(char)
        return char

    def create_basic_cleric(self, name: str, level: int = 3) -> Character:
        """Utilitaire: créer un clerc de base"""
        from dnd_5e_core import Abilities
        from dnd_5e_core.races import Race
        from dnd_5e_core.classes import ClassType
        from dnd_5e_core.abilities import AbilityType
        from ..core.adapters import CharacterExtensions

        race = Race(
            index='human', name='Humain', speed=30, ability_bonuses={},
            alignment='Good', age='Adult', size='Medium', size_description='5-6 ft',
            starting_proficiencies=[], starting_proficiency_options=[],
            languages=[], language_desc='Common', traits=[], subraces=[]
        )

        cleric_class = ClassType(
            index='cleric', name='Cleric', hit_die=8, proficiency_choices=[],
            proficiencies=[], saving_throws=[AbilityType.WIS, AbilityType.CHA],
            starting_equipment=[], starting_equipment_options=[], class_levels=[],
            multi_classing=[], subclasses=[], spellcasting_level=level,
            spellcasting_ability='wis', can_cast=True, spell_slots={},
            spells_known=[], cantrips_known=[]
        )

        char = Character(
            name=name, race=race, subrace=None, ethnic='Human', gender='Female',
            height='5ft6', weight='140 lbs', age=28,
            class_type=cleric_class, proficiencies=[],
            abilities=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
            ability_modifiers=Abilities(str=12, dex=10, con=14, int=13, wis=16, cha=14),
            hit_points=8 + (level-1)*5 + level*2,
            max_hit_points=8 + (level-1)*5 + level*2,
            speed=30, haste_timer=0.0, hasted=False,
            xp=level * 300, level=level,
            inventory=[], gold=30, sc=None, conditions=[]
        )

        CharacterExtensions.add_inventory_management(char)
        CharacterExtensions.init_spell_slots(char)
        return char

    # 🆕 NOUVELLES MÉTHODES

    def save_game(self, slot_name: str = "autosave", silent: bool = False) -> bool:
        """Sauvegarder la partie en cours"""
        # Auto-save si activé
        if slot_name == "autosave" and not GameSettings.is_auto_save_enabled():
            return False
        
        # Mode silencieux pour les sauvegardes automatiques
        if slot_name == "autosave":
            silent = True
        
        return self.save_manager.save_game(
            scenario_name=self.get_scenario_name(),
            party=self.party,
            game_state=self.game_state,
            scene_id=self.scene_manager.current_scene_id,
            slot_name=slot_name,
            silent=silent
        )

    def load_game(self, slot_name: str = "autosave") -> bool:
        """Charger une partie sauvegardée"""
        save_data = self.save_manager.load_game(slot_name)

        if not save_data:
            return False

        self.party = save_data['party']
        self.game_state = save_data['game_state']
        self.scene_manager.current_scene_id = save_data['scene_id']

        return True

    def show_map(self):
        """Afficher la carte d'exploration"""
        if self.exploration_map:
            print(self.exploration_map.get_ascii_map())
            print()
            print(self.exploration_map.get_location_info())

            visited, total, percentage = self.exploration_map.get_exploration_progress()
            print(f"\n📊 Exploration: {visited}/{total} ({percentage:.1f}%)")
        else:
            print("⚠️ Carte non disponible pour ce scénario")

    def update_map_location(self, location_id: str):
        """Mettre à jour la position sur la carte"""
        if self.exploration_map:
            self.exploration_map.visit_location(location_id)

    def check_level_up(self):
        """Vérifier et gérer les montées de niveau"""
        leveled_up = []

        for char in self.party:
            while self.level_manager.can_level_up(char):
                old_level = char.level
                if self.level_manager.level_up(char):
                    summary = self.level_manager.get_level_up_summary(char, old_level, char.level)
                    print(summary)
                    leveled_up.append(char.name)
                    self.renderer.wait_for_input()

        return leveled_up

    def rest_at_village(self):
        """Repos au village avec montée de niveau possible"""
        self.renderer.print_header("🏘️ REPOS AU VILLAGE")

        print("Vous vous reposez à l'auberge du village...")
        print()

        results = self.village_rest.rest_at_village(self.party)

        # Afficher soins
        if results['healed']:
            print(f"✅ Soignés: {', '.join(results['healed'])}")

        # Afficher montées de niveau
        if results['leveled_up']:
            print("\n⭐ MONTÉE DE NIVEAU!")
            for level_up_info in results['leveled_up']:
                char_name = level_up_info['name']
                old_level = level_up_info['old_level']
                new_level = level_up_info['new_level']

                # Trouver le personnage
                char = next((c for c in self.party if c.name == char_name), None)
                if char:
                    summary = self.level_manager.get_level_up_summary(char, old_level, new_level)
                    print(summary)
                    self.renderer.wait_for_input()

        print(f"\n💰 Coût de l'auberge: {results['cost']} po")

        # Déduire le coût
        for char in self.party:
            if char.gold >= 5:
                char.gold -= 5
                break

        self.renderer.wait_for_input()

    def quit_menu(self) -> str:
        """
        Menu de sortie

        Returns:
            'save_quit', 'quit', 'continue'
        """
        self.renderer.print_header("⏸️ MENU")

        choice = self.renderer.get_choice([
            "💾 Sauvegarder et quitter",
            "🚪 Quitter sans sauvegarder",
            "▶️  Continuer l'aventure"
        ])

        if choice == 0:
            # Sauvegarder
            slot_name = input("\nNom de la sauvegarde (ou ENTER pour autosave): ").strip()
            if not slot_name:
                slot_name = "autosave"

            if self.save_game(slot_name):
                print(f"✅ Partie sauvegardée: {slot_name}")
            else:
                print("❌ Erreur de sauvegarde")

            return 'save_quit'

        elif choice == 1:
            confirm = input("\n⚠️ Quitter sans sauvegarder? (oui/non): ").strip().lower()
            if confirm in ['oui', 'o', 'yes', 'y']:
                return 'quit'
            return 'continue'

        else:
            return 'continue'

    def _ask_load_game(self) -> bool:
        """Demander si charger une partie sauvegardée"""
        saves = self.save_manager.list_saves()
        if not saves:
            return False

        print("\n💾 Parties sauvegardées trouvées:")
        for i, save in enumerate(saves, 1):
            print(f"  {i}. {save['slot_name']} - {save.get('scenario', 'Unknown')} - {save.get('timestamp', '')[:19]}")

        print(f"  0. Nouvelle partie")

        try:
            choice = input("\nCharger une partie? (numéro ou 0): ").strip()
            if choice and choice.isdigit():
                idx = int(choice)
                if idx == 0:
                    return False
                if 1 <= idx <= len(saves):
                    if self.load_game(saves[idx - 1]['slot_name']):
                        print("✅ Partie chargée!")
                        self._resume_game()
                        return True
        except Exception:
            pass

        return False

    def _resume_game(self):
        """Reprendre une partie chargée"""
        # À implémenter si nécessaire
        pass

    def load_party_from_json(self, json_path: str) -> bool:
        """
        Charge un groupe d'aventuriers depuis un fichier JSON.

        Compatible avec les fichiers générés par scripts/generate_scenario_characters.py
        Utilise simple_character_generator comme template puis applique les valeurs JSON.

        Args:
            json_path: Chemin vers le fichier JSON du groupe

        Returns:
            True si le chargement a réussi, False sinon
        """
        try:
            import json
            from pathlib import Path
            from dnd_5e_core.data.loaders import simple_character_generator
        except Exception as e:
            print(f"⚠️  Erreur d'import: {e}")
            return False

        # Vérifier existence du fichier
        json_file = Path(json_path)
        if not json_file.exists():
            print(f"⚠️  Fichier introuvable: {json_path}")
            return False

        # Charger le JSON
        try:
            with json_file.open('r', encoding='utf-8') as f:
                party_data = json.load(f)
        except Exception as e:
            print(f"⚠️  Erreur lecture JSON: {e}")
            return False

        if not isinstance(party_data, list):
            print("⚠️  Format JSON invalide (attendu: liste de personnages)")
            return False

        # Reconstruire chaque personnage
        loaded_party = []
        for char_data in party_data:
            char = self._character_from_dict(char_data)
            if char:
                loaded_party.append(char)
            else:
                print(f"⚠️  Échec chargement: {char_data.get('name', 'Unknown')}")

        if not loaded_party:
            print("⚠️  Aucun personnage chargé")
            return False

        self.party = loaded_party
        print(f"✅ {len(loaded_party)} personnages chargés depuis JSON")
        return True

    def _character_from_dict(self, data: dict):
        """
        Reconstruit un Character depuis un dictionnaire JSON.

        Utilise simple_character_generator comme base puis applique les attributs.
        Cette approche garantit que tous les objets internes (Race, ClassType, etc.)
        sont correctement initialisés.

        Args:
            data: Dictionnaire de données du personnage

        Returns:
            Instance de Character ou None en cas d'erreur
        """
        try:
            from dnd_5e_core.data.loaders import simple_character_generator
            from dnd_5e_core.data import load_spell
        except Exception:
            load_spell = None

        # Extraire les données de base
        name = data.get('name', 'Unknown')
        level = int(data.get('level', 1))
        race_name = data.get('race', 'human')
        class_name = data.get('class', 'fighter')

        # Normaliser les noms (race/class en minuscules)
        race_name = race_name.lower() if isinstance(race_name, str) else 'human'
        class_name = class_name.lower() if isinstance(class_name, str) else 'fighter'

        # Créer le personnage template via simple_character_generator
        try:
            char = simple_character_generator(
                level=level,
                race_name=race_name,
                class_name=class_name,
                name=name
            )
        except Exception as e:
            print(f"⚠️  Erreur création template {name}: {e}")
            return None

        # Appliquer les valeurs spécifiques du JSON
        try:
            # Caractéristiques
            if 'abilities' in data:
                abilities = data['abilities']
                char.abilities.str = int(abilities.get('str', char.abilities.str))
                char.abilities.dex = int(abilities.get('dex', char.abilities.dex))
                char.abilities.con = int(abilities.get('con', char.abilities.con))
                char.abilities.int = int(abilities.get('int', char.abilities.int))
                char.abilities.wis = int(abilities.get('wis', char.abilities.wis))
                char.abilities.cha = int(abilities.get('cha', char.abilities.cha))

            if 'ability_modifiers' in data and hasattr(char, 'ability_modifiers'):
                mods = data['ability_modifiers']
                char.ability_modifiers.str = int(mods.get('str', char.ability_modifiers.str))
                char.ability_modifiers.dex = int(mods.get('dex', char.ability_modifiers.dex))
                char.ability_modifiers.con = int(mods.get('con', char.ability_modifiers.con))
                char.ability_modifiers.int = int(mods.get('int', char.ability_modifiers.int))
                char.ability_modifiers.wis = int(mods.get('wis', char.ability_modifiers.wis))
                char.ability_modifiers.cha = int(mods.get('cha', char.ability_modifiers.cha))

            # Points de vie
            if 'hit_points' in data:
                char.hit_points = int(data['hit_points'])
            if 'max_hit_points' in data:
                char.max_hit_points = int(data['max_hit_points'])

            # Or
            if 'gold' in data:
                char.gold = int(data.get('gold', 0))

            # Sorts (spellcasting)
            if 'spellcasting' in data and hasattr(char, 'sc') and char.sc:
                sc_data = data['spellcasting']
                spell_list = sc_data.get('spell_list', [])

                # Charger les sorts réels si possible
                if spell_list and load_spell:
                    char.sc.spells = []  # Réinitialiser
                    for spell_name in spell_list:
                        try:
                            # Normaliser le nom pour l'API
                            spell_idx = spell_name.lower().replace(' ', '-').replace("'", '')
                            spell = load_spell(spell_idx)
                            if spell:
                                char.sc.spells.append(spell)
                        except Exception:
                            # Fallback: créer un placeholder simple
                            class SpellPlaceholder:
                                def __init__(self, name):
                                    self.name = name
                                    self.level = 0
                            char.sc.spells.append(SpellPlaceholder(spell_name))

            # Capacités spéciales de classe
            if 'extra_attacks' in data and hasattr(char, 'multi_attack_bonus'):
                char.multi_attack_bonus = int(data['extra_attacks'])
            if 'sneak_attack' in data and hasattr(char, 'sneak_attack_dice'):
                sneak = data['sneak_attack']
                if 'd' in str(sneak):
                    char.sneak_attack_dice = int(str(sneak).split('d')[0])
            if 'rage_uses' in data and hasattr(char, 'rage_uses_left'):
                char.rage_uses_left = int(data['rage_uses'])
            if 'ki_points' in data and hasattr(char, 'ki_points'):
                char.ki_points = int(data['ki_points'])
            if 'lay_on_hands' in data and hasattr(char, 'lay_on_hands_pool'):
                char.lay_on_hands_pool = int(data['lay_on_hands'])

        except Exception as e:
            print(f"⚠️  Erreur application attributs pour {name}: {e}")

        return char

    def _equip_party_with_starter_gear(self):
        """Équiper le groupe avec équipement de départ."""
        try:
            from dnd_5e_core.data import load_weapon, load_armor
            from dnd_5e_core.combat import Action, ActionType, Damage
            from dnd_5e_core.mechanics import DamageDice
        except Exception as e:
            print(f"⚠️  Import équipement impossible: {e}")
            return

        try:
            from ..core.adapters import CharacterExtensions
        except Exception:
            try:
                from src.core.adapters import CharacterExtensions
            except Exception:
                CharacterExtensions = None

        print("\n🎽 Équipement de départ...")

        weapon_map = {
            'fighter': 'longsword', 'paladin': 'longsword', 'barbarian': 'longsword',
            'ranger': 'longsword', 'rogue': 'shortsword', 'monk': 'shortsword',
            'cleric': 'mace', 'druid': 'mace', 'wizard': 'dagger'
        }
        armor_map = {
            'fighter': 'chain-mail', 'paladin': 'chain-mail',
            'cleric': 'scale-mail', 'barbarian': 'scale-mail', 'ranger': 'scale-mail',
            'rogue': 'leather-armor', 'bard': 'leather-armor', 'warlock': 'leather-armor'
        }

        for char in self.party:
            if not hasattr(char, 'inventory') or char.inventory is None:
                char.inventory = [None] * 20
            if CharacterExtensions:
                try:
                    CharacterExtensions.add_inventory_management(char)
                except Exception:
                    pass

            class_idx = 'fighter'
            if hasattr(char, 'class_type') and getattr(char.class_type, 'index', None):
                class_idx = char.class_type.index
            elif hasattr(char, 'class_type') and getattr(char.class_type, 'name', None):
                class_idx = char.class_type.name.lower()

            # Arme
            weapon_idx = weapon_map.get(class_idx, 'dagger')
            try:
                weapon_obj = load_weapon(weapon_idx)
                if weapon_obj:
                    # ✅ IMPORTANT: Marquer comme équipé AVANT d'ajouter à l'inventaire
                    weapon_obj.equipped = True

                    # Ajouter à l'inventaire
                    added = False
                    for i in range(len(char.inventory)):
                        if char.inventory[i] is None:
                            char.inventory[i] = weapon_obj
                            added = True
                            break

                    if added:
                        # Créer une action d'attaque basée sur l'arme
                        self._create_weapon_action(char, weapon_obj)
                        print(f"  ⚔️  {char.name}: {weapon_idx}")
            except Exception as e:
                # Debug
                print(f"  ⚠️  Erreur équipement arme {weapon_idx}: {e}")

            # Armure
            armor_idx = armor_map.get(class_idx)
            if armor_idx:
                try:
                    armor_obj = load_armor(armor_idx)
                    if armor_obj:
                        # ✅ IMPORTANT: Marquer comme équipé AVANT d'ajouter à l'inventaire
                        armor_obj.equipped = True

                        # Ajouter à l'inventaire
                        added = False
                        for i in range(len(char.inventory)):
                            if char.inventory[i] is None:
                                char.inventory[i] = armor_obj
                                added = True
                                break

                        if added:
                            # Appliquer le bonus de CA
                            if hasattr(armor_obj, 'armor_class') and hasattr(armor_obj.armor_class, 'base'):
                                char.armor_class = armor_obj.armor_class.base
                                # Ajouter bonus de DEX si armure légère/moyenne
                                if hasattr(armor_obj.armor_class, 'dex_bonus') and armor_obj.armor_class.dex_bonus:
                                    dex_mod = (char.abilities.dex - 10) // 2
                                    if hasattr(armor_obj.armor_class, 'max_bonus') and armor_obj.armor_class.max_bonus:
                                        dex_mod = min(dex_mod, armor_obj.armor_class.max_bonus)
                                    char.armor_class += dex_mod
                            print(f"  🛡️  {char.name}: {armor_idx} (CA: {char.armor_class})")
                except Exception as e:
                    # Debug
                    print(f"  ⚠️  Erreur équipement armure {armor_idx}: {e}")

        print("\n✅ Équipement appliqué")

    def _create_weapon_action(self, char, weapon):
        """Créer une action d'attaque pour une arme équipée."""
        try:
            from dnd_5e_core.combat import Action, ActionType, Damage
            from dnd_5e_core.mechanics import DamageDice

            # Calculer le bonus d'attaque
            # Utiliser FOR pour armes de mêlée, DEX pour armes à distance
            is_melee = True
            if hasattr(weapon, 'weapon_range') and weapon.weapon_range != 'Melee':
                is_melee = False
            elif hasattr(weapon, 'range') and hasattr(weapon.range, 'normal'):
                is_melee = weapon.range.normal <= 5

            # Bonus = modificateur de caractéristique + bonus de maîtrise
            if is_melee:
                ability_mod = (char.abilities.str - 10) // 2
            else:
                ability_mod = (char.abilities.dex - 10) // 2

            prof_bonus = 2 + ((char.level - 1) // 4)
            attack_bonus = ability_mod + prof_bonus

            # Créer l'action
            if not hasattr(char, 'actions') or char.actions is None:
                char.actions = []

            # Extraire les dégâts de l'arme
            damage_dice = "1d6"  # Par défaut
            damage_type = None

            if hasattr(weapon, 'damage') and weapon.damage:
                if hasattr(weapon.damage, 'damage_dice'):
                    damage_dice = weapon.damage.damage_dice
                if hasattr(weapon.damage, 'damage_type'):
                    damage_type = weapon.damage.damage_type

            # Créer l'action d'attaque
            action = Action(
                name=weapon.name,
                desc=f"Attaque avec {weapon.name}",
                type=ActionType.MELEE if is_melee else ActionType.RANGED,
                attack_bonus=attack_bonus,
                damages=[Damage(
                    type=damage_type if damage_type else weapon.damage.damage_type if hasattr(weapon, 'damage') else None,
                    dd=DamageDice(damage_dice)
                )],
                normal_range=5 if is_melee else (weapon.range.normal if hasattr(weapon, 'range') else 20)
            )

            # Ajouter l'action au personnage
            char.actions.append(action)

        except Exception as e:
            # Si la création d'action échoue, ce n'est pas grave
            # Le personnage utilisera les attaques par défaut
            pass

    def _init_spellcasters(self):
        """
        Initialiser les sorts pour les lanceurs.

        NOTE: simple_character_generator de dnd-5e-core charge déjà automatiquement
        les sorts pour les personnages créés. Cette méthode n'est utile QUE pour
        les personnages chargés depuis JSON qui n'ont pas de sorts.
        """
        # Vérifier si les personnages ont déjà des sorts chargés par simple_character_generator
        chars_needing_spells = []
        for char in self.party:
            if not hasattr(char, 'class_type') or not char.class_type:
                continue
            can_cast = getattr(char.class_type, 'can_cast', False)
            if not can_cast:
                continue

            # Vérifier si le personnage a déjà des sorts
            has_spells = (hasattr(char, 'sc') and char.sc and
                         hasattr(char.sc, 'learned_spells') and char.sc.learned_spells)

            if not has_spells:
                chars_needing_spells.append(char)

        if not chars_needing_spells:
            print('\n✨ Sorts déjà chargés par simple_character_generator')
            return

        # Charger des sorts de base uniquement pour les personnages qui n'en ont pas
        print(f'\n✨ Chargement de sorts de base pour {len(chars_needing_spells)} personnage(s)')

        try:
            from dnd_5e_core.data import load_spell
        except Exception:
            print("⚠️  Impossible de charger load_spell, sorts non initialisés")
            return

        spells_by_class = {
            'cleric': ['cure-wounds', 'bless', 'sacred-flame'],
            'wizard': ['magic-missile', 'fire-bolt'],
            'druid': ['cure-wounds', 'produce-flame'],
            'warlock': ['eldritch-blast'],
            'sorcerer': ['magic-missile', 'fire-bolt'],
            'bard': ['cure-wounds', 'vicious-mockery'],
            'paladin': ['cure-wounds', 'bless']
        }

        for char in chars_needing_spells:
            class_idx = getattr(char.class_type, 'index', None) or getattr(char.class_type, 'name', '').lower()

            if class_idx not in spells_by_class:
                continue

            # S'assurer que char.sc existe
            if not hasattr(char, 'sc') or char.sc is None:
                from dnd_5e_core.spells.spellcaster import SpellCaster
                char.sc = SpellCaster(
                    level=char.level,
                    spell_slots=[0] * 10,
                    learned_spells=[],
                    dc_type='wis',
                    dc_value=10,
                    ability_modifier=0
                )

            # Charger quelques sorts de base
            if not hasattr(char.sc, 'learned_spells'):
                char.sc.learned_spells = []

            spell_names = spells_by_class[class_idx]
            for sname in spell_names:
                try:
                    sp = load_spell(sname)
                    if sp and sp not in char.sc.learned_spells:
                        char.sc.learned_spells.append(sp)
                except Exception:
                    pass

    def _load_equipment(self):
        """
        Charge les équipements depuis dnd-5e-core pour utilisation dans les scénarios.

        Returns:
            Tuple (weapons, armors, equipments, potions) - Listes d'équipements
        """
        weapons = []
        armors = []
        equipments = []
        potions = []

        try:
            from dnd_5e_core.data import load_weapon, load_armor
        except Exception as e:
            print(f"⚠️  Impossible de charger les loaders d'équipement: {e}")
            return weapons, armors, equipments, potions

        # Charger quelques armes de base
        weapon_list = ['longsword', 'shortsword', 'dagger', 'mace', 'battleaxe',
                       'greatsword', 'rapier', 'shortbow', 'longbow', 'crossbow-light']
        for weapon_id in weapon_list:
            try:
                weapon = load_weapon(weapon_id)
                if weapon:
                    weapons.append(weapon)
            except Exception:
                pass

        # Charger quelques armures de base
        armor_list = ['leather-armor', 'chain-mail', 'scale-mail', 'plate-armor',
                     'hide-armor', 'studded-leather-armor', 'breastplate']
        for armor_id in armor_list:
            try:
                armor = load_armor(armor_id)
                if armor:
                    armors.append(armor)
            except Exception:
                pass

        # Créer équipements simples (puisque load_equipment n'existe pas)
        try:
            from dnd_5e_core.equipment import Equipment
            equipments = [
                Equipment(index='rope', name='Corde (15m)', equipment_category={'index': 'adventuring-gear'},
                         cost={'quantity': 1, 'unit': 'gp'}, weight=10, desc=['Corde en chanvre robuste']),
                Equipment(index='torch', name='Torche', equipment_category={'index': 'adventuring-gear'},
                         cost={'quantity': 1, 'unit': 'cp'}, weight=1, desc=['Torche pour éclairer']),
                Equipment(index='backpack', name='Sac à dos', equipment_category={'index': 'adventuring-gear'},
                         cost={'quantity': 2, 'unit': 'gp'}, weight=5, desc=['Sac à dos en cuir']),
            ]
        except Exception:
            # Si Equipment n'est pas disponible, créer des objets simples
            class SimpleEquipment:
                def __init__(self, name, desc, weight=1):
                    self.name = name
                    self.desc = desc
                    self.weight = weight

            equipments = [
                SimpleEquipment('Corde (15m)', 'Corde en chanvre robuste', 10),
                SimpleEquipment('Torche', 'Torche pour éclairer', 1),
                SimpleEquipment('Sac à dos', 'Sac à dos en cuir', 5),
                SimpleEquipment('Gourde', 'Gourde en cuir', 2),
                SimpleEquipment('Rations (1 jour)', 'Nourriture pour une journée', 2),
            ]

        # Créer des potions simples
        try:
            from ..core.adapters import Potion
            potions = [
                Potion("Potion de Soins", "Restaure 2d4+2 HP", 50, "healing", "2d4+2"),
                Potion("Potion de Soins Supérieure", "Restaure 4d4+4 HP", 150, "healing", "4d4+4"),
                Potion("Antidote", "Soigne l'empoisonnement", 50, "cure", "0"),
            ]
        except Exception:
            # Fallback si Potion n'est pas disponible
            class SimplePotion:
                def __init__(self, name, desc, value, effect_type, effect_value):
                    self.name = name
                    self.desc = desc
                    self.value = value
                    self.effect_type = effect_type
                    self.effect_value = effect_value

            potions = [
                SimplePotion("Potion de Soins", "Restaure 2d4+2 HP", 50, "healing", "2d4+2"),
                SimplePotion("Potion de Soins Supérieure", "Restaure 4d4+4 HP", 150, "healing", "4d4+4"),
            ]

        return weapons, armors, equipments, potions

    def _create_magic_items_treasure(self):
        """
        Crée une liste d'objets magiques utilisables comme trésors.

        Returns:
            List - Liste d'objets magiques
        """
        magic_items = []

        try:
            from dnd_5e_core.data import load_magic_item
        except Exception:
            load_magic_item = None

        if not load_magic_item:
            # Créer des objets magiques simples si le loader n'est pas disponible
            class SimpleMagicItem:
                def __init__(self, name, desc, rarity, value):
                    self.name = name
                    self.desc = desc
                    self.rarity = rarity
                    self.value = value

            magic_items = [
                SimpleMagicItem("Anneau de Protection", "+1 CA et jets de sauvegarde", "Rare", 1000),
                SimpleMagicItem("Potion de Soins Supérieure", "4d4+4 HP", "Rare", 150),
                SimpleMagicItem("Amulette de Santé", "Constitution devient 19", "Rare", 2000),
                SimpleMagicItem("Bottes Ailées", "Vitesse de vol 4h/jour", "Rare", 1500),
                SimpleMagicItem("Cape de Protection", "+1 CA et jets de sauvegarde", "Rare", 1000),
            ]
        else:
            # Charger depuis dnd-5e-core si disponible
            magic_item_ids = [
                'ring-of-protection',
                'cloak-of-protection',
                'boots-of-speed',
                'amulet-of-health'
            ]
            for item_id in magic_item_ids:
                try:
                    item = load_magic_item(item_id)
                    if item:
                        magic_items.append(item)
                except Exception:
                    pass

        return magic_items

