"""
Test du système de rencontre D&D 5e avec un groupe d'aventuriers (4-6 personnages)
Utilise encounter_builder.py pour générer des rencontres équilibrées
AMÉLIORÉ: Gestion des conditions appliquées par les monstres et adaptation des actions
"""
from dnd_5e_core import load_monster
from dnd_5e_core.data.loaders import simple_character_generator
from dnd_5e_core.data import load_weapon, load_armor
from dnd_5e_core.data.collections import load_all_monsters
from dnd_5e_core.combat import CombatSystem
from dnd_5e_core.mechanics.encounter_builder import (
    select_monsters_by_encounter_table,
    generate_encounter_distribution,
    get_encounter_info
)
from dnd_5e_core.mechanics.gold_rewards import get_encounter_gold
from random import randint, choice


# =============================================================================
# FONCTIONS HELPER POUR LA GESTION DES CONDITIONS
# =============================================================================

def display_conditions(creature):
    """Affiche les conditions actives d'une créature"""
    if hasattr(creature, 'conditions') and creature.conditions:
        conditions_str = ", ".join([c.name for c in creature.conditions])
        return f"🔴 [{conditions_str}]"
    return ""


def check_condition_effects(character):
    """
    Vérifie les effets des conditions sur un personnage

    Returns:
        dict avec les informations sur les limitations
    """
    effects = {
        'can_move': True,
        'has_disadvantage': False,
        'is_incapacitated': False,
        'attacks_have_advantage': False,  # Les attaques contre ce personnage
        'speed_zero': False,
        'auto_fail_saves': [],  # Types de jets de sauvegarde automatiquement ratés
        'conditions_list': []
    }

    if not hasattr(character, 'conditions') or not character.conditions:
        return effects

    for condition in character.conditions:
        condition_name = condition.name.lower()
        effects['conditions_list'].append(condition.name)

        if condition_name == 'restrained':
            effects['speed_zero'] = True
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

        elif condition_name == 'grappled':
            effects['speed_zero'] = True

        elif condition_name == 'paralyzed':
            effects['is_incapacitated'] = True
            effects['auto_fail_saves'] = ['str', 'dex']
            effects['attacks_have_advantage'] = True

        elif condition_name == 'stunned':
            effects['is_incapacitated'] = True
            effects['auto_fail_saves'] = ['str', 'dex']
            effects['attacks_have_advantage'] = True

        elif condition_name == 'incapacitated':
            effects['is_incapacitated'] = True

        elif condition_name == 'poisoned':
            effects['has_disadvantage'] = True

        elif condition_name == 'frightened':
            effects['has_disadvantage'] = True

        elif condition_name == 'blinded':
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

        elif condition_name == 'prone':
            effects['has_disadvantage'] = True
            effects['attacks_have_advantage'] = True

    return effects


def attempt_escape_conditions(character, verbose=True):
    """
    Tente d'échapper aux conditions actives

    Returns:
        list: Liste des conditions dont le personnage s'est libéré
    """
    escaped = []

    if not hasattr(character, 'conditions') or not character.conditions:
        return escaped

    for condition in character.conditions[:]:  # Copie pour modification
        if condition.dc_type and condition.dc_value:
            if verbose:
                print(f"   🎲 {character.name} tente de se libérer de {condition.name} (DC {condition.dc_value} {condition.dc_type.value})...")

            if condition.attempt_save(character):
                if verbose:
                    print(f"      ✅ Réussi! {character.name} se libère de {condition.name}")
                escaped.append(condition.name)
            else:
                if verbose:
                    print(f"      ❌ Échoué! {character.name} reste {condition.name}")

    return escaped


def display_character_status(character, show_conditions=True):
    """Affiche le statut complet d'un personnage"""
    hp_percent = (character.hit_points / character.max_hit_points) * 100 if character.max_hit_points > 0 else 0

    status_icon = "❤️" if hp_percent > 75 else "💛" if hp_percent > 50 else "🧡" if hp_percent > 25 else "💔"

    status = f"{status_icon} {character.name}: {character.hit_points}/{character.max_hit_points} HP"

    if show_conditions:
        cond_str = display_conditions(character)
        if cond_str:
            status += f" {cond_str}"

    return status


# =============================================================================
# DÉBUT DU SCRIPT PRINCIPAL
# =============================================================================

print("="*80)
print("🎲 TEST DU SYSTÈME DE RENCONTRE D&D 5E")
print("="*80)

# =============================================================================
# ÉTAPE 1: Créer un groupe d'aventuriers (4-6 personnages)
# =============================================================================
print("\n📋 ÉTAPE 1: Création du groupe d'aventuriers")
print("-"*80)

# Nombre de personnages dans le groupe (entre 4 et 6)
party_size = randint(4, 6)
print(f"Taille du groupe: {party_size} aventuriers")

# Niveau du groupe (niveau 5 pour des combats intéressants)
party_level = 5

# Classes disponibles
available_classes = ["fighter", "wizard", "cleric", "rogue", "ranger", "paladin"]

# Créer le groupe
party = []
party_names = ["Conan", "Gandalf", "Friar", "Shadowblade", "Aragorn", "Lancelot"]

for i in range(party_size):
    # Varier les classes
    if i == 0:
        char_class = "fighter"
    elif i == 1:
        char_class = "fighter"
    elif i == 2:
        char_class = "cleric"
    elif i == 3:
        char_class = "wizard"
    elif i == 4:
        char_class = "ranger"
    else:
        char_class = "paladin"

    # Varier légèrement les niveaux (±1 niveau)
    char_level = party_level + randint(-1, 1)
    char_level = max(1, min(20, char_level))

    char = simple_character_generator(
        level=char_level,
        class_name=char_class,
        name=party_names[i]
    )
    party.append(char)
    print(f"  ✅ {char.name}: Niveau {char.level} {char.class_type.name} - {char.hit_points} HP")

# =============================================================================
# ÉTAPE 2: Équiper le groupe
# =============================================================================
print(f"\n⚔️ ÉTAPE 2: Équipement du groupe")
print("-"*80)

# Armes et armures
weapons = {
    "fighter": "longsword",
    "paladin": "greatsword",
    "ranger": "longbow",
    "cleric": "mace",
    "wizard": "dagger",
    "rogue": "shortsword"
}

armors = {
    "fighter": "chain-mail",
    "paladin": "chain-mail",
    "ranger": "scale-mail",
    "cleric": "chain-mail",
    "wizard": None,  # Les wizards n'ont pas d'armure lourde
    "rogue": "leather"
}

for char in party:
    class_name = char.class_type.index

    # Équiper arme
    weapon_name = weapons.get(class_name, "club")
    weapon = load_weapon(weapon_name)
    if weapon and char.inventory:
        for i, item in enumerate(char.inventory):
            if item is None:
                char.inventory[i] = weapon
                break
        char.equip(weapon)
        print(f"  {char.name}: {weapon.name}", end="")

    # Équiper armure
    armor_name = armors.get(class_name)
    if armor_name:
        armor = load_armor(armor_name)
        if armor and char.inventory:
            for i, item in enumerate(char.inventory):
                if item is None:
                    char.inventory[i] = armor
                    break
            char.equip(armor)
            print(f" + {armor.name} (AC {armor.armor_class['base']})")
    else:
        print(f" (Pas d'armure)")

# =============================================================================
# ÉTAPE 3: Charger les monstres disponibles
# =============================================================================
print(f"\n🐉 ÉTAPE 3: Chargement de la base de monstres")
print("-"*80)

try:
    all_monsters = load_all_monsters()
    print(f"✅ {len(all_monsters)} monstres chargés")
except Exception as e:
    print(f"⚠️  Erreur de chargement: {e}")
    print("   Utilisation de monstres de base...")
    all_monsters = [
        load_monster('goblin'),
        load_monster('orc'),
        load_monster('ogre'),
        load_monster('werewolf'),
        load_monster('troll'),
    ]
    all_monsters = [m for m in all_monsters if m is not None]
    print(f"   {len(all_monsters)} monstres de base chargés")

# =============================================================================
# ÉTAPE 4: Générer une rencontre avec l'encounter builder
# =============================================================================
print(f"\n🎯 ÉTAPE 4: Génération de la rencontre")
print("-"*80)

# Calculer le niveau moyen du groupe
avg_party_level = sum(c.level for c in party) // len(party)
print(f"Niveau moyen du groupe: {avg_party_level}")

# Obtenir les informations de rencontre
encounter_info = get_encounter_info(avg_party_level)
print(f"\nOptions de rencontre pour niveau {avg_party_level}:")
print(f"  - Paires possibles: CR {encounter_info['pair_crs'][0]} + CR {encounter_info['pair_crs'][1]}")
print(f"  - Groupes possibles:")
for size, crs in encounter_info['group_options'].items():
    print(f"    • {size} monstres de CR {crs}")

# Générer la rencontre
monsters, encounter_type = select_monsters_by_encounter_table(
    encounter_level=avg_party_level,
    available_monsters=all_monsters,
    allow_pairs=True
)

print(f"\n✨ Rencontre générée: Type '{encounter_type}'")
print(f"   Nombre de monstres: {len(monsters)}")

# Afficher les monstres
monster_summary = {}
for monster in monsters:
    name = monster.name
    monster_summary[name] = monster_summary.get(name, 0) + 1

print(f"   Composition:")
for name, count in monster_summary.items():
    monster = next(m for m in monsters if m.name == name)
    cr = monster.challenge_rating
    hp = monster.hit_points
    ac = monster.armor_class if hasattr(monster, 'armor_class') else '?'
    print(f"     • {count}x {name} (CR {cr}, {hp} HP, AC {ac})")

# Calculer la récompense en or
gold_reward = get_encounter_gold(avg_party_level)
print(f"\n💰 Récompense potentielle: {gold_reward} pièces d'or")

# =============================================================================
# ÉTAPE 5: Combat
# =============================================================================
print(f"\n⚔️ ÉTAPE 5: COMBAT!")
print("="*80)

# Formation du groupe: guerriers/paladins devant, autres derrière
front_row_classes = ["fighter", "paladin", "cleric"]
party_sorted = sorted(party, key=lambda c: 0 if c.class_type.index in front_row_classes else 1)

print(f"\n📊 Formation du groupe:")
for i, char in enumerate(party_sorted):
    position = "Front (Mêlée)" if i < 3 else "Back (Distance/Sorts)"
    print(f"  [{i}] {char.name} ({char.class_type.name} Niv.{char.level}): {position} - {char.hit_points} HP")

print(f"\n👹 Ennemis:")
for name, count in monster_summary.items():
    monster = next(m for m in monsters if m.name == name)
    print(f"  • {count}x {name} ({monster.hit_points} HP chacun)")

print("\n⚔️ DÉMARRAGE DU COMBAT!")
print("-"*80)

# Démarrer le combat
combat = CombatSystem(verbose=True)
alive_chars = [c for c in party_sorted if c.hit_points > 0]
alive_monsters = monsters.copy()

round_num = 1
max_rounds = 20

while alive_chars and alive_monsters and round_num <= max_rounds:
    print(f"\n{'='*80}")
    print(f"🎲 ROUND {round_num}")
    print(f"{'='*80}")

    # Afficher le statut au début du round
    print(f"\n📊 Statut du groupe:")
    for char in alive_chars:
        print(f"   {display_character_status(char)}")

    print(f"\n👹 Statut des ennemis:")
    enemy_summary = {}
    for monster in alive_monsters:
        name = monster.name
        if name not in enemy_summary:
            enemy_summary[name] = {'count': 0, 'total_hp': 0, 'max_hp': 0}
        enemy_summary[name]['count'] += 1
        enemy_summary[name]['total_hp'] += monster.hit_points
        enemy_summary[name]['max_hp'] += monster.max_hit_points if hasattr(monster, 'max_hit_points') else monster.hit_points

    for name, stats in enemy_summary.items():
        print(f"   • {stats['count']}x {name}: {stats['total_hp']}/{stats['max_hp']} HP total")

    # Tours des personnages
    print(f"\n⚔️ PHASE DES AVENTURIERS")
    print("-" * 80)

    for char in alive_chars[:]:
        if not alive_monsters:
            break
        if char.hit_points <= 0:
            if char in alive_chars:
                alive_chars.remove(char)
            continue

        print(f"\n🎯 Tour de {char.name}")

        # Vérifier les conditions
        effects = check_condition_effects(char)

        if effects['conditions_list']:
            print(f"   🔴 Conditions actives: {', '.join(effects['conditions_list'])}")

        # Si incapacité, pas d'action
        if effects['is_incapacitated']:
            print(f"   ⚠️  {char.name} est incapable d'agir (Incapacitated/Paralyzed/Stunned)")

            # Tenter de se libérer
            escaped = attempt_escape_conditions(char, verbose=True)
            if escaped:
                # Recalculer les effets
                effects = check_condition_effects(char)
                if not effects['is_incapacitated']:
                    print(f"   ✅ {char.name} peut maintenant agir!")
                else:
                    continue
            else:
                continue

        # Tenter de se libérer des conditions au début du tour
        if effects['conditions_list']:
            escaped = attempt_escape_conditions(char, verbose=True)
            if escaped:
                # Recalculer les effets après libération
                effects = check_condition_effects(char)

        # Action normale avec effets de conditions
        if effects['has_disadvantage']:
            print(f"   ⚠️  Désavantage aux attaques (conditions actives)")

        if effects['speed_zero']:
            print(f"   ⚠️  Vitesse = 0, ne peut pas se déplacer")

        # Effectuer l'action de combat
        combat.character_turn(
            character=char,
            alive_chars=alive_chars,
            alive_monsters=alive_monsters,
            party=party_sorted
        )

    # Tours des monstres
    print(f"\n👹 PHASE DES MONSTRES")
    print("-" * 80)

    for monster in alive_monsters[:]:
        if not alive_chars:
            break
        if monster.hit_points <= 0:
            if monster in alive_monsters:
                alive_monsters.remove(monster)
            continue

        print(f"\n🐉 Tour de {monster.name}")

        # Vérifier les conditions des personnages pour cibler intelligemment
        # Préférer attaquer les personnages avec des conditions (advantage)
        targets_with_advantage = [
            c for c in alive_chars
            if check_condition_effects(c)['attacks_have_advantage']
        ]

        if targets_with_advantage:
            print(f"   🎯 Cibles avec advantage détectées: {', '.join([c.name for c in targets_with_advantage])}")

        combat.monster_turn(
            monster=monster,
            alive_monsters=alive_monsters,
            alive_chars=alive_chars,
            party=party_sorted,
            round_num=round_num
        )

        # Afficher les conditions appliquées
        for char in alive_chars:
            if hasattr(char, 'conditions') and char.conditions:
                # Vérifier si de nouvelles conditions ont été ajoutées
                cond_str = display_conditions(char)
                if cond_str and "applied this turn" not in str(char):
                    print(f"      {cond_str} appliquées à {char.name}")

    round_num += 1

    # Pause visuelle entre les rounds
    if round_num <= max_rounds and alive_chars and alive_monsters:
        input(f"\n⏸️  Appuyez sur ENTRÉE pour continuer au Round {round_num}...")


# =============================================================================
# RÉSULTATS
# =============================================================================
print(f"\n{'='*80}")
print("📊 RÉSULTATS DU COMBAT")
print(f"{'='*80}")

if alive_chars:
    print(f"\n✅ VICTOIRE! Le groupe l'emporte!")
    print(f"\n   Survivants ({len(alive_chars)}/{len(party_sorted)}):")
    for char in party_sorted:
        if char.hit_points > 0:
            hp_percent = (char.hit_points / char.max_hit_points) * 100
            status = "❤️" if hp_percent > 50 else "💔" if hp_percent > 0 else "💀"
            print(f"     {status} {char.name}: {char.hit_points}/{char.max_hit_points} HP ({hp_percent:.0f}%)")
        else:
            print(f"     💀 {char.name}: MORT")

    # Afficher les sorts utilisés
    for char in party_sorted:
        if hasattr(char, 'sc') and char.sc and hasattr(char.sc, 'spell_slots'):
            slots_used = 0
            for i in range(1, 6):
                if i < len(char.sc.spell_slots):
                    # Calcul approximatif des slots utilisés (si on avait la valeur initiale)
                    pass
            if hasattr(char, 'is_spell_caster') and char.is_spell_caster:
                print(f"\n   🔮 {char.name} - Slots de sorts restants: {char.sc.spell_slots[1:6]}")

    print(f"\n   💰 Le groupe obtient {gold_reward} pièces d'or!")

    # Calculer les XP (basé sur le CR des monstres)
    total_xp = 0
    for monster in monsters:
        if hasattr(monster, 'experience_points'):
            total_xp += monster.experience_points
        elif hasattr(monster, 'xp'):
            total_xp += monster.xp

    if total_xp > 0:
        print(f"   ⭐ XP gagnés: {total_xp} XP")

elif alive_monsters:
    print(f"\n❌ DÉFAITE! Les monstres ont gagné!")
    print(f"   Monstres survivants: {len(alive_monsters)}")
    for monster in alive_monsters:
        print(f"     • {monster.name}: {monster.hit_points} HP")
else:
    print(f"\n🤝 MATCH NUL! Tous les combattants sont tombés!")

print(f"\n📈 Statistiques:")
print(f"   - Nombre de rounds: {round_num - 1}")
print(f"   - Type de rencontre: {encounter_type}")
print(f"   - Niveau de rencontre: {avg_party_level}")
print(f"   - Taille du groupe: {len(party_sorted)} aventuriers")
print(f"   - Nombre de monstres: {len(monsters)}")

print(f"\n{'='*80}")
print("✅ TEST TERMINÉ")
print(f"{'='*80}")

