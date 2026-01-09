# ✅ Factorisation des 3 Scénarios - JSON vs Code Manuel

**Date**: 10 janvier 2026  
**Objectif**: Utiliser les fichiers JSON au lieu de construire les scènes manuellement

---

## 📊 Résultats de la Factorisation

### Réduction du Code

| Scénario | Avant | Après | Réduction |
|----------|-------|-------|-----------|
| **chasse_gobelins_refactored.py** | 272 lignes | 99 lignes | **-64%** |
| **tombe_rois_serpents_game.py** | 479 lignes | 97 lignes | **-80%** |
| **yawning_portal_game.py** | 593 lignes | 97 lignes | **-84%** |
| **TOTAL** | 1344 lignes | 293 lignes | **-78%** |

**1051 lignes de code supprimées** ! 🎉

---

## 🔄 Changements Effectués

### Avant : Construction Manuelle des Scènes

Chaque scénario contenait des centaines de lignes de code Python pour construire manuellement les scènes :

```python
def build_custom_scenes(self):
    # INTRO
    intro_text = """Le Village de Brume est en émoi..."""
    self.scene_manager.add_scene(NarrativeScene(
        scene_id="intro",
        title="🏰 VILLAGE DE BRUME",
        text=intro_text,
        next_scene_id="village_hub"
    ))
    
    # VILLAGE HUB
    self.scene_manager.add_scene(NarrativeScene(
        scene_id="village_hub",
        ...
    ))
    
    # VILLAGE CHOICE
    self.scene_manager.add_scene(ChoiceScene(
        scene_id="village_choice",
        ...
    ))
    
    # ... 50+ scènes de plus !
```

**Problèmes** :
- ❌ Code très long et répétitif
- ❌ Difficile à maintenir
- ❌ Mélange logique et données
- ❌ Duplication entre Python et JSON
- ❌ Impossible de modifier scénario sans toucher au code

### Après : Chargement depuis JSON

Le code est maintenant minimal et générique :

```python
def build_custom_scenes(self):
    """Charger les scènes depuis le fichier JSON"""
    json_path = Path("data/scenes/chasse_gobelins.json")
    
    if not json_path.exists():
        print(f"⚠️  Fichier JSON non trouvé: {json_path}")
        self._build_default_scenes()
        return
    
    # Charger les scènes depuis JSON avec SceneFactory
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        scenario_data = json.load(f)
    
    # Créer les scènes depuis le JSON
    for scene_data in scenario_data.get('scenes', []):
        scene = SceneFactory.create_scene_from_dict(scene_data, self.monster_factory)
        if scene:
            self.scene_manager.add_scene(scene)
    
    print(f"✅ Scénario chargé depuis JSON: {len(self.scene_manager.scenes)} scènes")

def _build_default_scenes(self):
    """Scènes par défaut si le JSON n'est pas trouvé"""
    # Scène d'intro minimale seulement
    self.scene_manager.add_scene(NarrativeScene(
        scene_id="intro",
        title="🏰 VILLAGE DE BRUME",
        text=intro_text,
        next_scene_id=None
    ))
```

**Avantages** :
- ✅ Code minimal (20 lignes vs 200+)
- ✅ Facile à maintenir
- ✅ Séparation données/logique
- ✅ Source unique de vérité (JSON)
- ✅ Modifier scénario = modifier JSON seulement
- ✅ Fallback si JSON manquant

---

## 📁 Fichiers JSON Utilisés

### chasse_gobelins_refactored.py
- **Fichier JSON**: `data/scenes/chasse_gobelins.json`
- **Scènes**: 10 scènes
- **Durée**: 1-2h
- **Niveau**: 3

### tombe_rois_serpents_game.py
- **Fichier JSON**: `data/scenes/tombe_rois_serpents.json`
- **Scènes**: ~20 scènes
- **Durée**: 2h
- **Niveau**: 2

### yawning_portal_game.py
- **Fichier JSON**: `data/scenes/sunless_citadel.json`
- **Scènes**: ~25 scènes
- **Durée**: 2-3h
- **Niveau**: 1

---

## 🏗️ Architecture Finale

```
Scénario (Python)
├── get_scenario_name()      # Nom du scénario
├── create_party()            # Création du groupe
├── build_custom_scenes()     # ⭐ Charge depuis JSON
│   ├── Lit data/scenes/XXX.json
│   ├── Utilise SceneFactory.create_scene_from_dict()
│   └── Ajoute chaque scène au scene_manager
└── _build_default_scenes()   # Fallback si JSON manquant

Fichier JSON (data/scenes/)
├── scenario_id
├── name
├── level
├── difficulty
└── scenes[]                  # ⭐ Définition des scènes
    ├── id
    ├── type (narrative, choice, combat, merchant, rest)
    ├── title
    ├── description/text
    └── ...paramètres spécifiques
```

---

## 🎯 Utilisation de SceneFactory

Le `SceneFactory` transforme automatiquement le JSON en objets Python :

```python
# JSON
{
  "id": "combat1",
  "type": "combat",
  "title": "⚔️ Embuscade !",
  "description": "Des gobelins surgissent !",
  "monsters": ["goblin", "goblin", "goblin"],
  "on_victory": "victoire",
  "on_defeat": "defaite"
}

# Devient automatiquement
CombatScene(
    scene_id="combat1",
    title="⚔️ Embuscade !",
    description="Des gobelins surgissent !",
    enemies_factory=lambda ctx: create_monsters(["goblin", "goblin", "goblin"]),
    on_victory_scene="victoire",
    on_defeat_scene="defaite"
)
```

**Magie du Factory Pattern** ! ✨

---

## 📝 Types de Scènes Supportés

Le `SceneFactory` gère automatiquement :

1. **NarrativeScene** - Texte narratif
2. **ChoiceScene** - Choix multiples
3. **CombatScene** - Combats
4. **MerchantScene** - Marchands
5. **RestScene** - Repos

Chaque type est créé avec les bons paramètres à partir du JSON.

---

## ✅ Avantages de Cette Approche

### Pour les Développeurs

- ✅ **Moins de code** à écrire et maintenir
- ✅ **Pas de duplication** entre JSON et Python
- ✅ **Code générique** réutilisable
- ✅ **Tests plus faciles** (tester JSON séparément)
- ✅ **Modifications rapides** (changer JSON sans recompiler)

### Pour les Créateurs de Contenu

- ✅ **Pas besoin de Python** pour modifier un scénario
- ✅ **Édition directe** du JSON
- ✅ **Validation** du format JSON
- ✅ **Partage facile** des scénarios
- ✅ **Versionning** du contenu

### Pour les Joueurs

- ✅ **Mêmes scénarios**, même qualité
- ✅ **Chargement rapide**
- ✅ **Moins de bugs** (source unique)
- ✅ **Mises à jour faciles** du contenu

---

## 🔄 Migration des Anciens Scripts

Si vous avez des anciens scripts avec construction manuelle :

### Étape 1 : Extraire les Scènes en JSON

Convertir :
```python
self.scene_manager.add_scene(NarrativeScene(
    scene_id="intro",
    title="Titre",
    text="Texte...",
    next_scene_id="next"
))
```

En :
```json
{
  "id": "intro",
  "type": "narrative",
  "title": "Titre",
  "text": "Texte...",
  "next_scene": "next"
}
```

### Étape 2 : Remplacer build_custom_scenes()

Utiliser le code générique qui charge depuis JSON.

### Étape 3 : Tester

Vérifier que le scénario fonctionne toujours.

---

## 📊 Métriques de Qualité

### Avant Factorisation
- **Lignes de code** : 1344
- **Duplication** : Élevée (code + JSON)
- **Maintenabilité** : Difficile
- **Complexité** : Élevée
- **Temps de modification** : Long

### Après Factorisation
- **Lignes de code** : 293 (-78%)
- **Duplication** : Aucune (JSON seul)
- **Maintenabilité** : Facile
- **Complexité** : Faible
- **Temps de modification** : Rapide

---

## 🎉 Conclusion

La factorisation des 3 scénarios pour utiliser les fichiers JSON a permis de :

✅ **Supprimer 1051 lignes de code dupliqué**  
✅ **Simplifier la maintenance** des scénarios  
✅ **Séparer clairement** le code de la logique et les données  
✅ **Faciliter la création** de nouveaux scénarios  
✅ **Améliorer la qualité** du code (DRY principle)  

**Le système est maintenant beaucoup plus professionnel et maintenable !**

---

## 📚 Fichiers Modifiés

### Scripts Python (3 fichiers)
- `chasse_gobelins_refactored.py` - 272 → 99 lignes
- `tombe_rois_serpents_game.py` - 479 → 97 lignes
- `yawning_portal_game.py` - 593 → 97 lignes

### Fichiers JSON (déjà existants)
- `data/scenes/chasse_gobelins.json` - 123 lignes
- `data/scenes/tombe_rois_serpents.json` - ~200 lignes
- `data/scenes/sunless_citadel.json` - ~220 lignes

### Factory (déjà existant)
- `src/scenes/scene_factory.py` - 156 lignes

---

**Commit** : `♻️ Refactoring: Les 3 scénarios utilisent maintenant les fichiers JSON`  
**Date** : 10 janvier 2026  
**Impact** : -1051 lignes de code (-78%)  
**Status** : ✅ **TERMINÉ ET COMMITTÉ**

🎲 **Le code est maintenant beaucoup plus élégant !**

