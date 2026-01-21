#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎲 DÉMARRAGE RAPIDE - Génération de Personnages DnD 5e

Ce script affiche un guide de démarrage rapide pour la génération de personnages.
"""

def print_quick_start():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🎲 GÉNÉRATION DE PERSONNAGES DnD 5e - DÉMARRAGE RAPIDE                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📋 SCRIPTS DISPONIBLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. create_character.py       - Créer un personnage individuel
2. create_party.py            - Créer un groupe d'aventuriers
3. create_scenario_parties.py - Groupes pré-configurés pour scénarios
4. example_usage.py           - Exemples d'utilisation

🚀 COMMANDES RAPIDES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─ Créer un personnage ──────────────────────────────────────────────────────┐
│ python scripts/create_character.py --name Gandalf --class wizard \\        │
│        --race elf --level 10                                               │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Créer un groupe classique ────────────────────────────────────────────────┐
│ python scripts/create_party.py --classic --level 5 \\                      │
│        --out data/party.json                                               │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Groupes pour scénarios ───────────────────────────────────────────────────┐
│ python scripts/create_scenario_parties.py                                  │
│ (Interactif - choisissez votre scénario)                                   │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Voir des exemples ────────────────────────────────────────────────────────┐
│ python scripts/example_usage.py                                            │
└────────────────────────────────────────────────────────────────────────────┘

✨ FONCTIONNALITÉS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Génération automatique des caractéristiques (4d6 drop lowest)
✓ Capacités de classe appliquées automatiquement
  - Fighter: Extra Attack
  - Rogue: Sneak Attack
  - Barbarian: Rage
  - Monk: Ki Points
  - Paladin: Lay on Hands

✓ Traits raciaux appliqués automatiquement
  - Elf: Darkvision, Fey Ancestry, Trance
  - Dwarf: Darkvision, Dwarven Resilience
  - Halfling: Lucky, Brave, Nimbleness
  - Half-Orc: Relentless Endurance, Savage Attacks

✓ Sorts générés pour les lanceurs
  - Sélection aléatoire appropriée au niveau
  - Emplacements de sorts calculés automatiquement
  - DD des sorts et modificateurs

✓ Export JSON pour réutilisation

📖 CLASSES DISPONIBLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• fighter    - Guerrier (Extra Attack)
• wizard     - Magicien (sorts INT)
• rogue      - Roublard (Sneak Attack)
• cleric     - Clerc (sorts SAG)
• ranger     - Rôdeur (demi-lanceur SAG)
• paladin    - Paladin (demi-lanceur CHA, Lay on Hands)
• barbarian  - Barbare (Rage)
• monk       - Moine (Ki Points)
• bard       - Barde (sorts CHA)
• druid      - Druide (sorts SAG)
• sorcerer   - Ensorceleur (sorts CHA)
• warlock    - Occultiste (sorts CHA)

🧝 RACES DISPONIBLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• human      - Humain
• elf        - Elfe
• dwarf      - Nain
• halfling   - Halfelin
• half-elf   - Demi-elfe
• half-orc   - Demi-orque
• tiefling   - Tieffelin
• gnome      - Gnome
• dragonborn - Drakéide

📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• scripts/README.md        - Documentation des scripts
• scripts/GUIDE_COMPLET.md - Guide complet et détaillé

💡 EXEMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Groupe pour "La Chasse aux Gobelins" (niveau 3):
   python scripts/create_scenario_parties.py
   → Choisir "1"

2. Personnage Gandalf niveau 10:
   python scripts/create_character.py --name Gandalf --class wizard \\
          --race elf --level 10 --out data/gandalf.json

3. Groupe aléatoire de 6 personnages niveau 5:
   python scripts/create_party.py --level 5 --size 6 \\
          --out data/my_party.json

🎯 PROCHAINES ÉTAPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Créez votre premier personnage ou groupe
2. Chargez-le dans un scénario existant
3. Lancez votre aventure avec le launcher:
   python launcher.py

Bon jeu ! 🎲✨

╔═══════════════════════════════════════════════════════════════════════════════╗
║  Pour plus d'aide, consultez scripts/GUIDE_COMPLET.md                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == '__main__':
    print_quick_start()
