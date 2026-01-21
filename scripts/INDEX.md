# 📑 Index des Scripts de Génération de Personnages

## 🚀 Démarrage Rapide

**Nouveau utilisateur ?** Commencez ici :
```bash
python scripts/quick_start.py
```

## 📚 Scripts Disponibles

### 1️⃣ Créer un Personnage Individuel
**Fichier:** `create_character.py`  
**Usage:** Créer un seul personnage avec affichage détaillé  
**Exemple:**
```bash
python scripts/create_character.py --name Gandalf --class wizard --race elf --level 10
```
[📖 Documentation complète](README.md#1-create_characterpy---créer-un-personnage-individuel)

---

### 2️⃣ Créer un Groupe d'Aventuriers
**Fichier:** `create_party.py`  
**Usage:** Créer un groupe complet (classique ou personnalisé)  
**Exemple:**
```bash
python scripts/create_party.py --classic --level 5 --out data/party.json
```
[📖 Documentation complète](README.md#2-create_partypy---créer-un-groupe-daventuriers)

---

### 3️⃣ Groupes Pré-configurés pour Scénarios
**Fichier:** `create_scenario_parties.py`  
**Usage:** Générer des groupes adaptés à chaque scénario  
**Exemple:**
```bash
python scripts/create_scenario_parties.py
# Choisir "1" pour "La Chasse aux Gobelins"
```
[📖 Documentation complète](README.md#3-create_scenario_partiespy---créer-des-groupes-pour-des-scénarios-spécifiques)

---

### 4️⃣ Exemples d'Utilisation
**Fichier:** `example_usage.py`  
**Usage:** Voir des exemples complets d'utilisation  
**Exemple:**
```bash
python scripts/example_usage.py
```

---

### 5️⃣ Générateur Avancé
**Fichier:** `generate_scenario_characters.py`  
**Usage:** Version avancée avec plus d'options  
**Exemple:**
```bash
python scripts/generate_scenario_characters.py --count 5 --level 7 --out data/chars.json
```

---

## 📖 Documentation

| Document | Description | Utilisation |
|----------|-------------|-------------|
| **[README.md](README.md)** | Documentation principale | Pour comprendre les scripts |
| **[GUIDE_COMPLET.md](GUIDE_COMPLET.md)** | Guide détaillé | Pour tout savoir sur la génération |
| **[quick_start.py](quick_start.py)** | Guide visuel rapide | Pour démarrer rapidement |

---

## 🎯 Cas d'Usage Courants

### Cas 1 : Je veux un personnage unique pour tester
```bash
python scripts/create_character.py --class fighter --level 5
```

### Cas 2 : Je veux un groupe pour jouer un scénario
```bash
python scripts/create_party.py --classic --level 5
```

### Cas 3 : Je veux créer des personnages pour "La Chasse aux Gobelins"
```bash
python scripts/create_scenario_parties.py
# Choisir "1"
```

### Cas 4 : Je veux voir comment ça marche
```bash
python scripts/example_usage.py
```

### Cas 5 : Je veux un personnage spécifique
```bash
python scripts/create_character.py --name "Elminster" --class wizard --race human --level 20
```

---

## 🔧 Classes et Races

### Classes Disponibles
- `fighter` (Guerrier) - Extra Attack
- `wizard` (Magicien) - Sorts INT
- `rogue` (Roublard) - Sneak Attack
- `cleric` (Clerc) - Sorts SAG
- `ranger` (Rôdeur) - Half-caster SAG
- `paladin` (Paladin) - Half-caster CHA, Lay on Hands
- `barbarian` (Barbare) - Rage
- `monk` (Moine) - Ki Points
- `bard` (Barde) - Sorts CHA
- `druid` (Druide) - Sorts SAG
- `sorcerer` (Ensorceleur) - Sorts CHA
- `warlock` (Occultiste) - Sorts CHA

### Races Disponibles
- `human` (Humain)
- `elf` (Elfe) - Darkvision, Fey Ancestry
- `dwarf` (Nain) - Darkvision, Resilience
- `halfling` (Halfelin) - Lucky, Brave
- `half-elf` (Demi-elfe)
- `half-orc` (Demi-orque) - Relentless Endurance
- `tiefling` (Tieffelin) - Darkvision, Hellish Resistance
- `gnome` (Gnome) - Darkvision, Cunning
- `dragonborn` (Drakéide) - Breath Weapon

---

## 📂 Fichiers Générés

Les fichiers JSON sont sauvegardés dans :
- `data/` - Fichiers généraux
- `data/parties/` - Groupes pour scénarios spécifiques

**Format JSON :** Voir [GUIDE_COMPLET.md](GUIDE_COMPLET.md#format-json-des-personnages)

---

## 🆘 Aide

**Problème ?** Consultez :
1. [README.md](README.md) - Documentation des scripts
2. [GUIDE_COMPLET.md](GUIDE_COMPLET.md) - Guide détaillé avec dépannage
3. Les exemples : `python scripts/example_usage.py`

**Besoin d'aide rapide ?**
```bash
python scripts/create_character.py --help
python scripts/create_party.py --help
```

---

## 🎲 Bon jeu !

Vous avez maintenant tout ce qu'il faut pour créer des personnages riches et complets pour vos aventures D&D 5e !
