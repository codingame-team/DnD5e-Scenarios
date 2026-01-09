# 🔄 Renommage du Projet: DnD5e-Test → DnD5e-Scenarios

**Date**: 9 janvier 2026  
**Status**: 🟡 EN COURS - Actions manuelles requises

---

## ✅ Étapes Complétées

### 1. Nettoyage du projet

✅ **Documents Markdown archivés** (11 fichiers)
- `CORRECTION_FINALE_COMBAT_V3.4.7.md`
- `DEMARRAGE_RAPIDE.md`
- `ETAT_PROJET.md`
- `GUIDE_CREATION_SCENARIOS.md`
- `INDEX_DOCUMENTATION_V2.md`
- `MIGRATION_COMPLETE.md`
- `RAPPORT_ARCHIVAGE_FINAL.md`
- `RESUME_DOCUMENTATION_ARCHIVE.md`
- `SESSION_RECAP.md`
- `CORRECTION_MAP_ASCII.txt`
- `LISEZ_MOI.txt`

**Destination**: `archive/docs_obsoletes/`

✅ **Scripts de développement archivés** (3 fichiers)
- `analyze_pdf.py`
- `verify_project.py`
- `reorganize_project.sh`

**Destination**: `archive/scripts_dev/`

### 2. Nouveau README.md

✅ **README.md complètement réécrit**
- Focus sur la création de scénarios JSON
- Documentation claire et accessible
- Exemples concrets
- Guide d'utilisation complet
- Orientation "créateurs de contenu"

✅ **Ancien README archivé**
- `archive/docs_obsoletes/README_OLD.md`

### 3. Renommage local

✅ **Dossier renommé**
```bash
/Users/display/PycharmProjects/DnD5e-Test
→ /Users/display/PycharmProjects/DnD5e-Scenarios
```

### 4. Git commit

✅ **Changements commitées**
```bash
git commit -m "♻️ Refactoring: Archivage docs obsolètes et focus scénarios JSON"
```

---

## 🔴 Étapes Restantes (MANUEL)

### 1. Renommer le dépôt GitHub

**Sur GitHub.com** :

1. Allez sur `https://github.com/codingame-team/DND5e-Test`
2. Cliquez sur **Settings** (Paramètres)
3. Dans la section **Repository name**, changez:
   - `DND5e-Test` → `DnD5e-Scenarios`
4. Cliquez sur **Rename** (Renommer)

⚠️ GitHub redirigera automatiquement l'ancienne URL vers la nouvelle

### 2. Mettre à jour le remote Git local

**Dans le terminal** :

```bash
cd /Users/display/PycharmProjects/DnD5e-Scenarios

# Vérifier le remote actuel
git remote -v

# Si le remote pointe toujours vers DND5e-Test, le mettre à jour:
git remote set-url origin https://github.com/codingame-team/DnD5e-Scenarios.git

# Vérifier
git remote -v
```

**Résultat attendu** :
```
origin  https://github.com/codingame-team/DnD5e-Scenarios.git (fetch)
origin  https://github.com/codingame-team/DnD5e-Scenarios.git (push)
```

### 3. Pousser les changements

```bash
cd /Users/display/PycharmProjects/DnD5e-Scenarios

# Pousser le commit d'archivage
git push origin main

# Si erreur, forcer (attention: seulement si vous êtes sûr)
git push -f origin main
```

### 4. Mettre à jour les références

**Fichiers à vérifier/mettre à jour** :

- [ ] `README.md` - Vérifier les liens GitHub
- [ ] `README_SCENARIOS_JSON.md` - Mettre à jour les URLs si nécessaire
- [ ] `.gitignore` - Vérifier qu'il est correct

**Dans README.md**, cherchez et remplacez:
```
DND5e-Test → DnD5e-Scenarios
```

### 5. Mettre à jour les badges

Dans `README.md`, vérifiez que les badges pointent vers le bon dépôt:

```markdown
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![dnd-5e-core](https://img.shields.io/badge/dnd--5e--core-0.1.8-success.svg)](https://pypi.org/project/dnd-5e-core/)
```

---

## 📋 Checklist de Validation

Après avoir renommé sur GitHub:

- [ ] Le dépôt GitHub s'appelle bien `DnD5e-Scenarios`
- [ ] L'ancienne URL redirige vers la nouvelle
- [ ] Le remote Git local pointe vers la nouvelle URL
- [ ] Les changements sont poussés sur GitHub
- [ ] Le README.md s'affiche correctement sur GitHub
- [ ] Les liens dans le README fonctionnent
- [ ] Les badges s'affichent correctement

---

## 🎯 Résultat Final Attendu

### Structure Locale
```
/Users/display/PycharmProjects/DnD5e-Scenarios/
├── README.md                    # Nouveau README orienté scénarios
├── README_SCENARIOS_JSON.md     # Documentation système JSON
├── data/
│   ├── scenes/                  # 3 scénarios JSON
│   └── parties/                 # Configurations groupes
├── src/                         # Code source factorisé
├── play_scenario_from_json.py   # Script démo
├── play_scenarios.py            # Lanceur
└── archive/
    ├── docs_obsoletes/          # 11+ docs archivés
    └── scripts_dev/             # 3 scripts dev
```

### GitHub
```
https://github.com/codingame-team/DnD5e-Scenarios
- Nom: DnD5e-Scenarios
- Description: "Créez et jouez des aventures D&D 5e sans coder !"
- Topics: dnd, dnd5e, scenarios, json, ttrpg, python
- README.md affiché avec le nouveau contenu
```

---

## 🚨 En cas de Problème

### Le push échoue

```bash
# Vérifier la branche
git branch

# Vérifier les commits
git log --oneline -5

# Si nécessaire, pull d'abord
git pull origin main --rebase

# Puis push
git push origin main
```

### Le remote ne se met pas à jour

```bash
# Supprimer le remote
git remote remove origin

# Re-ajouter avec la bonne URL
git remote add origin https://github.com/codingame-team/DnD5e-Scenarios.git

# Vérifier
git remote -v
```

### Conflit avec le README

```bash
# Garder votre version locale
git checkout --ours README.md
git add README.md
git commit -m "Résolution conflit README"
git push origin main
```

---

## 📝 Notes Importantes

### Pourquoi ce renommage ?

Le projet s'est transformé d'un **ensemble de tests** du package `dnd-5e-core` en un véritable **moteur de création de scénarios**. Le nouveau nom reflète mieux cette mission.

### Qu'est-ce qui change pour les utilisateurs ?

**GitHub redirigera automatiquement** :
- Ancienne URL: `https://github.com/codingame-team/DND5e-Test`
- Nouvelle URL: `https://github.com/codingame-team/DnD5e-Scenarios`

Les utilisateurs qui ont cloné l'ancien dépôt continueront de fonctionner grâce à la redirection, mais ils peuvent mettre à jour leur remote:

```bash
git remote set-url origin https://github.com/codingame-team/DnD5e-Scenarios.git
```

---

## ✅ Validation Finale

Une fois toutes les étapes manuelles effectuées, vérifiez:

1. ✅ Visitez `https://github.com/codingame-team/DnD5e-Scenarios`
2. ✅ Le README s'affiche correctement
3. ✅ Les fichiers sont présents
4. ✅ `git pull` fonctionne depuis le dossier local
5. ✅ `git push` fonctionne

---

**Auteur**: Migration Team  
**Date**: 9 janvier 2026  
**Prochaine étape**: Renommer le dépôt sur GitHub.com

