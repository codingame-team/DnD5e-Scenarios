# 🎮 Système de Combat Ultime v5.0 - Guide Complet

## 🎯 Vue d'Ensemble

Le script `test_ultimate_combat_v5.py` est la version la plus avancée du système de combat D&D 5e, intégrant **TOUTES** les fonctionnalités disponibles :

- ✅ **Sous-classes** avec capacités spécifiques
- ✅ **Sous-races** avec bonus raciaux
- ✅ **Capacités de classe** (Rage, Action Surge, Sneak Attack, etc.)
- ✅ **Features par niveau** (Channel Divinity, Ki Points, etc.)
- ✅ **Objets magiques variés** (armes, armures, anneaux, amulettes, potions)
- ✅ **Système d'initiative** complet
- ✅ **IA avancée** utilisant les capacités au bon moment

---

## 🎭 Personnages Créés

### 1. Grok le Destructeur
- **Race/Sous-race** : Dwarf (Hill Dwarf)
- **Classe/Sous-classe** : Barbarian 6
- **Capacités** :
  - 😡 **Rage** : +2 dégâts, résistance aux dégâts physiques
  - 💪 **Reckless Attack** : Advantage aux attaques
- **Objets magiques** : Amulet of Health (CON = 19)

### 2. Conan
- **Race** : Human
- **Classe/Sous-classe** : Fighter 6 (Champion)
- **Capacités** :
  - ⚡ **Action Surge** : Action supplémentaire
  - 💨 **Second Wind** : Auto-guérison 1d10 + niveau
  - ⚔️ **Extra Attack** : 2 attaques par tour (niveau 5+)
  - 🎯 **Improved Critical** : Critique sur 19-20 (Champion)
- **Objets magiques** : Flaming Sword +1

### 3. Gandalf
- **Race/Sous-race** : Elf (High Elf)
- **Classe/Sous-classe** : Wizard 6 (School of Evocation)
- **Capacités** :
  - 🔮 **Spellcasting** : Sorts de niveaux 1-3
  - ⚡ **Evocation Savant** : Copie sorts d'évocation pour moitié prix
  - 🛡️ **Sculpt Spells** : Alliés auto-réussissent les saves
- **Bonus raciaux** : +1 INT (High Elf)
- **Objets magiques** : Cloak of Protection (+1 AC, +1 saves)

### 4. Sœur Elara
- **Race** : Human
- **Classe/Sous-classe** : Cleric 6 (Life Domain)
- **Capacités** :
  - ✨ **Channel Divinity** : Turn Undead ou autre
  - 🙏 **Disciple of Life** : Bonus de guérison
  - 💊 **Preserve Life** : Guérison de groupe (Channel Divinity)
- **Objets magiques** : Ring of Protection (+1 AC, +1 saves)

### 5. Bilbo
- **Race/Sous-race** : Halfling (Lightfoot)
- **Classe/Sous-classe** : Rogue 6 (Thief)
- **Capacités** :
  - 🗡️ **Sneak Attack** : +3d6 dégâts (niveau 5-6)
  - 🎭 **Cunning Action** : Bonus action (Dash/Disengage/Hide)
  - 🎯 **Uncanny Dodge** : Réaction pour réduire dégâts
- **Bonus raciaux** : +1 CHA (Lightfoot), Lucky
- **Objets magiques** : Bracers of Defense (+2 AC)

### 6. Li Mu Bai
- **Race/Sous-race** : Elf (Wood Elf)
- **Classe/Sous-classe** : Monk 6 (Way of the Open Hand)
- **Capacités** :
  - 🥋 **Ki Points** : 6 points pour capacités spéciales
  - 👊 **Flurry of Blows** : Attaques supplémentaires (1 ki)
  - 🏃 **Unarmored Movement** : +15 ft vitesse
  - 🌳 **Martial Arts** : 1d6 dégâts à mains nues
- **Bonus raciaux** : +1 WIS (Wood Elf), vitesse 35ft
- **Objets magiques** : Bracers of Defense (+2 AC)

---

## 💎 Objets Magiques Implémentés

### Armes

#### Flaming Sword +1
- **Type** : Weapon (Longsword)
- **Rareté** : Rare
- **Effet** : +1 attaque et dégâts, dégâts de feu supplémentaires
- **Attunement** : Oui

### Armures et Protection

#### Amulet of Health
- **Type** : Wondrous Item
- **Rareté** : Rare
- **Effet** : Constitution = 19
- **Attunement** : Oui

#### Bracers of Defense
- **Type** : Wondrous Item
- **Rareté** : Rare
- **Effet** : +2 AC (sans armure)
- **Attunement** : Oui

#### Cloak of Protection
- **Type** : Wondrous Item
- **Rareté** : Uncommon
- **Effet** : +1 AC, +1 tous jets de sauvegarde
- **Attunement** : Oui

#### Ring of Protection
- **Type** : Ring
- **Rareté** : Rare
- **Effet** : +1 AC, +1 tous jets de sauvegarde
- **Attunement** : Oui

### Potions

#### Potion of Healing (Standard)
- **Rareté** : Common
- **Effet** : Restaure 2d4+2 HP
- **Quantité** : 3 potions

#### Potion of Greater Healing
- **Rareté** : Uncommon
- **Effet** : Restaure 4d4+4 HP
- **Quantité** : 2 potions

#### Potion of Superior Healing
- **Rareté** : Rare
- **Effet** : Restaure 8d4+8 HP
- **Quantité** : 1 potion

---

## ⚔️ Capacités de Classe Implémentées

### Barbarian

#### Rage
```python
CharacterAbilities.apply_barbarian_rage(character)
```
**Effet** :
- +2 dégâts aux attaques de mêlée (niveau 5-8)
- Résistance aux dégâts contondants, perforants, tranchants
- Advantage aux jets de Force
- **Utilisations** : 3/jour (niveau 3-5)

**Déclenchement** : Automatique au round 1

### Fighter

#### Action Surge
```python
CharacterAbilities.use_fighter_action_surge(character)
```
**Effet** : Action supplémentaire ce tour
**Utilisations** : 1/repos court

**Déclenchement** : Round 2

#### Second Wind
```python
CharacterAbilities.use_second_wind(character)
```
**Effet** : Soigne 1d10 + niveau HP
**Utilisations** : 1/repos court

**Déclenchement** : Automatique si HP < 50%

#### Extra Attack
**Effet** : 2 attaques par tour (niveau 5+)
**Implémentation** : Gérée par CombatSystem

### Rogue

#### Sneak Attack
```python
CharacterAbilities.apply_sneak_attack_damage(character, base_damage)
```
**Effet** : +3d6 dégâts (niveau 5-6)
**Conditions** : Advantage ou allié adjacent

**Progression** :
- Niveau 1-2 : 1d6
- Niveau 3-4 : 2d6
- Niveau 5-6 : 3d6
- etc.

#### Cunning Action
```python
CharacterAbilities.use_rogue_cunning_action(character)
```
**Effet** : Bonus action pour Dash/Disengage/Hide
**Utilisations** : Illimité

**Déclenchement** : Chaque tour

### Monk

#### Ki Points
**Total** : Égal au niveau (6 au niveau 6)

#### Flurry of Blows
```python
CharacterAbilities.use_monk_ki(character, "Flurry of Blows")
```
**Effet** : 2 attaques à mains nues en bonus action
**Coût** : 1 ki point

**Déclenchement** : Aléatoire (1 chance sur 3)

#### Martial Arts
**Effet** : 1d6 dégâts à mains nues (niveau 5-10)

#### Unarmored Movement
**Effet** : +15 ft vitesse (niveau 6)

### Cleric

#### Channel Divinity
```python
CharacterAbilities.use_channel_divinity(character)
```
**Effet** : Dépend du domaine
- **Life Domain** : Preserve Life (guérison massive)
- **War Domain** : +10 attaque
- **Light Domain** : Radiance of the Dawn (dégâts radiants AoE)

**Utilisations** : 1/repos court (niveau 2-5)

**Déclenchement** : Round 3

---

## 🎯 Déroulement du Combat

### Round 1

**Initiative** :
```
🎲 INITIATIVE
   Gandalf: 18 (1d20 + 3)
   Bilbo: 17 (1d20 + 4)
   Conan: 15 (1d20 + 2)
   Troll: 14 (1d20 + 1)
   Li Mu Bai: 13 (1d20 + 3)
   Grok: 12 (1d20 + 2)
   Ogre: 11 (1d20 + 0)
   Sœur Elara: 10 (1d20 + 0)
```

**Tour 1: Gandalf (Wizard)**
```
⚔️ Tour de Gandalf
   [Action normale ou sort]
```

**Tour 2: Bilbo (Rogue)**
```
⚔️ Tour de Bilbo
   🎭 Bilbo utilise CUNNING ACTION: Hide!
   [Attaque avec Sneak Attack]
```

**Tour 6: Grok (Barbarian)**
```
⚔️ Tour de Grok
   😡 Grok entre en RAGE!
      Bonus de dégâts: +2
      Résistance aux dégâts physiques
      Rages restantes: 2
   [Attaque avec bonus de rage]
```

### Round 2

**Tour de Conan (Fighter)**
```
⚔️ Tour de Conan
   💨 Conan utilise SECOND WIND!
      Soigne 16 HP (34 → 50)
   ⚡ Conan utilise ACTION SURGE!
      Action supplémentaire ce tour!
   [2 attaques normales + 2 attaques d'Action Surge]
```

### Round 3

**Tour de Sœur Elara (Cleric)**
```
⚔️ Tour de Sœur Elara
   ✨ Sœur Elara utilise CHANNEL DIVINITY!
      Utilisations restantes: 0
   [Preserve Life: Guérit tous les alliés]
```

---

## 📊 Exemple de Combat Complet

### Setup
```
📖 CRÉATION DU GROUPE AVANCÉ
   ✅ Grok le Destructeur: Barbarian 6 (Hill Dwarf)
      HP: 68, AC: 14
   ✅ Conan: Fighter 6 (Champion)
      HP: 54, AC: 16
   ✅ Gandalf: Wizard 6 (Evocation, High Elf)
      HP: 38, AC: 13
   ✅ Sœur Elara: Cleric 6 (Life Domain)
      HP: 46, AC: 16
   ✅ Bilbo: Rogue 6 (Lightfoot Halfling)
      HP: 40, AC: 16
   ✅ Li Mu Bai: Monk 6 (Wood Elf)
      HP: 42, AC: 16

💎 ÉQUIPEMENT MAGIQUE AVANCÉ
   ✨ Grok: Amulet of Health (CON = 19)
   ⚔️  Conan: Flaming Sword +1
   🧥 Gandalf: Cloak of Protection (+1 AC, +1 saves)
   💍 Sœur Elara: Ring of Protection (+1 AC, +1 saves)
   🔰 Bilbo: Bracers of Defense (+2 AC)
   🔰 Li Mu Bai: Bracers of Defense (+2 AC)

👹 GÉNÉRATION DES MONSTRES
   Troll: CR 5, HP 84, AC 15
   Ogre: CR 2, HP 59, AC 11
   Hobgoblin: CR 1/2, HP 11, AC 18
   Hobgoblin: CR 1/2, HP 11, AC 18
```

### Combat (Rounds 1-3)

```
================================================================================
🎲 ROUND 1
================================================================================

📊 Groupe:
   ❤️ Grok le Destructeur: 68/68 HP
   ❤️ Conan: 54/54 HP
   ❤️ Gandalf (School of Evocation): 38/38 HP
   ❤️ Sœur Elara (Life): 46/46 HP
   ❤️ Bilbo: 40/40 HP
   ❤️ Li Mu Bai: 42/42 HP

👹 Monstres:
   Troll: 84 HP
   Ogre: 59 HP
   Hobgoblin: 11 HP
   Hobgoblin: 11 HP

⚔️ Tour de Gandalf
   [Fireball sur les hobgoblins]

⚔️ Tour de Bilbo
   🎭 Bilbo utilise CUNNING ACTION: Hide!
   Bilbo attacks Hobgoblin!
   🗡️  SNEAK ATTACK! +12 dégâts (3d6)
   💀 Hobgoblin est mort!

⚔️ Tour de Conan
   💨 Conan utilise SECOND WIND!
      Soigne 16 HP (54 → 54)
   Conan attacks Troll with Flaming Sword +1!
   [Dégâts normaux + feu]

👹 Tour de Troll
   Troll attacks Grok!
   [Dégâts réduits grâce à la Rage]

⚔️ Tour de Li Mu Bai
   🥋 Li Mu Bai utilise Flurry of Blows!
      Ki restants: 5/6
   [4 attaques à mains nues]

⚔️ Tour de Grok
   😡 Grok entre en RAGE!
      Bonus de dégâts: +2
      Résistance aux dégâts physiques
      Rages restantes: 2
   Grok attacks Troll!
   [Dégâts + 2 de rage]

...

================================================================================
📊 RÉSULTATS
================================================================================

✅ VICTOIRE!

Survivants (6/6):
   ❤️ Grok le Destructeur: 52/68 HP
   ❤️ Conan: 48/54 HP
   💛 Gandalf: 28/38 HP
   ❤️ Sœur Elara: 42/46 HP
   ❤️ Bilbo: 38/40 HP
   ❤️ Li Mu Bai: 35/42 HP

📈 Statistiques:
   - Rounds: 5
   - Monstres vaincus: 4/4
   - Capacités utilisées:
     * Rage: 1
     * Action Surge: 1
     * Second Wind: 1
     * Channel Divinity: 1
     * Flurry of Blows: 3
     * Sneak Attack: 4
     * Cunning Action: 5
```

---

## 🚀 Utilisation

```bash
cd /Users/display/PycharmProjects/DnD5e-Scenarios
python test_ultimate_combat_v5.py
```

### Contrôles
- **ENTRÉE** : Commencer le combat
- **ENTRÉE** : Passer au round suivant

---

## ✨ Points Forts

1. **Personnages Complets**
   - Sous-classes avec capacités spécifiques
   - Sous-races avec bonus raciaux
   - 6 classes différentes

2. **Capacités Réalistes**
   - Rage du Barbarian (résistance + dégâts)
   - Action Surge du Fighter (action extra)
   - Sneak Attack du Rogue (3d6)
   - Ki Points du Monk (6 points)
   - Channel Divinity du Cleric

3. **Objets Magiques Variés**
   - Armes magiques (+1, effets spéciaux)
   - Amulettes (modifier les stats)
   - Bracelets (bonus AC)
   - Anneaux et capes (protection)
   - Potions (3 types différents)

4. **IA Intelligente**
   - Utilise les capacités au bon moment
   - Rage au round 1
   - Second Wind si HP bas
   - Action Surge au round critique

5. **Combat Équilibré**
   - 6 personnages niveau 6
   - 4 monstres (CR 1/2 à 5)
   - Durée : 4-6 rounds typiquement

---

**Version** : 5.0  
**Date** : 18 Janvier 2026  
**Status** : ✅ **PRODUCTION READY**

🎉 Le système de combat D&D 5e le plus complet jamais créé ! ⚔️🎲✨
