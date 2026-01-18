# ✅ Correction du Chargement des Équipements

## 🚨 Problème Initial

Les équipements (armes, armures, équipements) ne se chargeaient pas dans les scénarios :

```
❌ Le Masque Utruz (Enrichi)
   Attendu: 20 armes, 15 armures, 20 équipements, 2 potions
   Obtenu: 0 armes, 0 armures, 0 équipements, 2 potions
```

## 🔍 Analyse du Problème

### 1. Type de Données Incorrect

**Erreur** : Le code s'attendait à ce que `load_weapon()`, `load_armor()`, et `load_equipment()` retournent des dictionnaires.

**Réalité** : Ces fonctions retournent des **objets** (`WeaponData`, `ArmorData`, `EquipmentData`).

```python
# ❌ Code incorrect
weapon_data = load_weapon(name)
if weapon_data and isinstance(weapon_data, dict):  # Toujours False!
    weapons.append(SimpleWeapon(weapon_data))

# ✅ Code correct
weapon = load_weapon(name)
if weapon:  # weapon est un objet WeaponData
    weapons.append(weapon)
```

### 2. Répertoire de Données Incorrect

**Problème** : `get_data_directory()` cherche d'abord dans `Path.cwd() / "data"` et trouvait :
- `/Users/display/PycharmProjects/DnD5e-Scenarios/data` (contient seulement scenes, parties, monsters)
- Au lieu de `/Users/display/PycharmProjects/dnd-5e-core/data` (contient weapons, armors, equipment)

**Résultat** : `list_weapons()`, `list_armors()`, `list_equipment()` retournaient des listes vides.

## ✅ Solution Appliquée

### 1. Configuration du Répertoire de Données

```python
from dnd_5e_core.data import set_data_directory
from pathlib import Path
import dnd_5e_core

package_path = Path(dnd_5e_core.__file__).parent

# Chercher le répertoire data dans plusieurs emplacements
possible_data_dirs = [
    package_path.parent / "data",  # Si installé en mode dev (pip install -e)
    Path("/Users/display/PycharmProjects/dnd-5e-core/data"),  # Chemin absolu (fallback)
]

data_dir_found = None
for data_dir in possible_data_dirs:
    if data_dir.exists() and (data_dir / "weapons").exists():
        data_dir_found = data_dir
        break

if data_dir_found:
    set_data_directory(str(data_dir_found))
```

### 2. Utilisation Directe des Objets

```python
# Charger armes
for name in list_weapons()[:20]:
    try:
        weapon = load_weapon(name)  # Retourne un objet Weapon
        if weapon:
            weapons.append(weapon)  # Directement
    except Exception:
        continue

# Charger armures
for name in list_armors()[:15]:
    try:
        armor = load_armor(name)  # Retourne un objet Armor
        if armor:
            armors.append(armor)
    except Exception:
        continue

# Charger équipements
for name in list_equipment()[:20]:
    try:
        equip = load_equipment(name)  # Retourne un objet Equipment
        if equip:
            equipments.append(equip)
    except Exception:
        continue
```

## 📊 Résultats

### Avant
```
🧪 VALIDATION DU CHARGEMENT DES ÉQUIPEMENTS

  ℹ️  Aucune donnée disponible (normal)
❌ Le Masque Utruz (Enrichi)
   Attendu: 20 armes, 15 armures, 20 équipements, 2 potions
   Obtenu: 0 armes, 0 armures, 0 équipements, 2 potions

Résultat: 0/3 scénarios validés
```

### Après
```
🧪 VALIDATION DU CHARGEMENT DES ÉQUIPEMENTS

  ✅ Chargés depuis dnd_5e_core.data
  Armes: 20, Armures: 15, Équipements: 20, Potions: 2
✅ Le Masque Utruz (Enrichi)
   Armes: 20, Armures: 15, Équipements: 20, Potions: 2

Résultat: 3/3 scénarios validés

🎉 TOUS LES SCÉNARIOS CHARGENT CORRECTEMENT LES ÉQUIPEMENTS!
```

## 🎯 Fichiers Modifiés

### src/scenarios/base_scenario.py
- Méthode `_load_equipment()` corrigée
- Ajout de `set_data_directory()` pour pointer vers le bon répertoire
- Suppression de la création d'objets `SimpleWeapon`, `SimpleArmor`, etc.
- Utilisation directe des objets retournés par `load_weapon()`, `load_armor()`, `load_equipment()`

## 🧪 Tests

Script de test : `test_equipment.py`

Teste le chargement des équipements pour 3 scénarios :
1. Le Masque Utruz (Enrichi) ✅
2. Les Cryptes de Kelemvor (Manuel) ✅
3. La Chasse aux Gobelins ✅

**Résultat** : 3/3 scénarios validés

## 📝 Commit

```
commit ebcfc33
fix: Correct equipment loading in scenarios

- Set correct data directory using set_data_directory()
- Use load_weapon/armor/equipment objects directly (not as dicts)
- All scenarios now load equipment correctly
- test_equipment.py: 3/3 scenarios validated ✅
```

## 🎉 Impact

Tous les scénarios peuvent maintenant :
- ✅ Charger 20 armes depuis `dnd-5e-core/data/weapons/`
- ✅ Charger 15 armures depuis `dnd-5e-core/data/armors/`
- ✅ Charger 20 équipements depuis `dnd-5e-core/data/equipment/`
- ✅ Créer 2 potions de soin

Les joueurs peuvent maintenant acheter/vendre des équipements dans les scénarios ! 🎮

