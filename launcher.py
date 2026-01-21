#!/usr/bin/env python3
"""
Launcher pour tous les scénarios D&D 5e enrichis
Permet de choisir et lancer facilement n'importe quel scénario
"""

import sys
import os
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Afficher un en-tête coloré"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}\n")


def print_scenario(num, emoji, name, level, duration, quality):
    """Afficher un scénario dans le menu"""
    quality_stars = "⭐" * quality
    print(f"{Colors.CYAN}{num:2d}.{Colors.END} {emoji} {Colors.BOLD}{name}{Colors.END}")
    print(f"     Niveau {level} | {duration} | {quality_stars}")


class GameConfig:
    """Configuration globale du jeu"""
    def __init__(self):
        self.text_speed = 'instant'  # 'slow', 'normal', 'fast', 'instant'
        self.auto_save = True
        self.combat_system = 'dnd_5e_core'  # 'dnd_5e_core' ou 'enhanced'
    
    def apply_to_env(self):
        """Appliquer la config aux variables d'environnement"""
        os.environ['DND_TEXT_SPEED'] = self.text_speed
        os.environ['DND_AUTO_SAVE'] = 'true' if self.auto_save else 'false'
        os.environ['DND_COMBAT_SYSTEM'] = self.combat_system


def show_settings_menu(config):
    """Afficher le menu de paramètres"""
    while True:
        print_header("⚙️ PARAMÈTRES")
        
        # Vitesse de texte
        speed_display = {
            'slow': '🐢 Lent',
            'normal': '🚶 Normal',
            'fast': '🏃 Rapide',
            'instant': '⚡ Instantané'
        }[config.text_speed]
        
        # Sauvegardes
        save_display = '✅ Automatiques' if config.auto_save else '🎮 Interactives'
        
        # Système de combat
        combat_display = {
            'dnd_5e_core': '📦 dnd-5e-core (Recommandé)',
            'enhanced': '⚔️ Enhanced Combat (Legacy)'
        }[config.combat_system]
        
        print(f"1. Vitesse de texte: {Colors.BOLD}{speed_display}{Colors.END}")
        print(f"2. Sauvegardes: {Colors.BOLD}{save_display}{Colors.END}")
        print(f"3. Système de combat: {Colors.BOLD}{combat_display}{Colors.END}")
        print(f"\n0. {Colors.GREEN}Retour au menu principal{Colors.END}")
        
        choice = input(f"\n{Colors.BOLD}Choisir un paramètre (0-3): {Colors.END}").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            print(f"\n{Colors.CYAN}Vitesse de texte:{Colors.END}")
            print("1. 🐢 Lent (immersif)")
            print("2. 🚶 Normal (équilibré)")
            print("3. 🏃 Rapide")
            print("4. ⚡ Instantané (pas d'attente)")
            speed_choice = input("Choix: ").strip()
            speed_map = {'1': 'slow', '2': 'normal', '3': 'fast', '4': 'instant'}
            if speed_choice in speed_map:
                config.text_speed = speed_map[speed_choice]
                print(f"{Colors.GREEN}✅ Vitesse changée{Colors.END}")
        
        elif choice == '2':
            config.auto_save = not config.auto_save
            mode = 'automatiques' if config.auto_save else 'interactives'
            print(f"{Colors.GREEN}✅ Sauvegardes {mode}{Colors.END}")
        
        elif choice == '3':
            print(f"\n{Colors.CYAN}Système de combat:{Colors.END}")
            print("1. 📦 dnd-5e-core (Recommandé, complet)")
            print("2. ⚔️ Enhanced Combat (Legacy, simple)")
            combat_choice = input("Choix: ").strip()
            if combat_choice == '1':
                config.combat_system = 'dnd_5e_core'
                print(f"{Colors.GREEN}✅ Système dnd-5e-core activé{Colors.END}")
            elif combat_choice == '2':
                config.combat_system = 'enhanced'
                print(f"{Colors.GREEN}✅ Système Enhanced Combat activé{Colors.END}")
        
        input("\nAppuyez sur ENTER pour continuer...")


def main():
    # Initialiser la configuration
    config = GameConfig()
    config.apply_to_env()  # Appliquer immédiatement
    
    print_header("🎲 LAUNCHER DE SCÉNARIOS D&D 5e 🎲")
    
    # Afficher les paramètres actifs
    speed_display = {
        'slow': '🐢 Lent',
        'normal': '🚶 Normal',
        'fast': '🏃 Rapide',
        'instant': '⚡ Instantané'
    }[config.text_speed]
    save_display = '✅ Auto' if config.auto_save else '🎮 Manuel'
    combat_display = '📦 Core' if config.combat_system == 'dnd_5e_core' else '⚔️ Legacy'
    
    print(f"{Colors.CYAN}Paramètres: {speed_display} | {save_display} | {combat_display}{Colors.END}")
    print()

    print(f"{Colors.YELLOW}📖 SCÉNARIOS ENRICHIS MANUELLEMENT (Qualité ⭐⭐⭐⭐⭐){Colors.END}")
    print()
    print_scenario(1, "🎭", "Le Masque Utruz", 3, "3-4h", 5)
    print(f"     {Colors.GREEN}Cité sur faille, usurier, Utruz, Dieu-Poisson{Colors.END}")
    print()
    print_scenario(2, "⚰️", "Les Cryptes de Kelemvor", 4, "3-4h", 5)
    print(f"     {Colors.GREEN}Temple profané, 7 sceaux, braseros sacrés, nécrophage{Colors.END}")
    print()
    print_scenario(3, "🗼", "La Tour du Mage Fou", 3, "3-4h", 5)
    print(f"     {Colors.GREEN}Mage corrompu, élémentaires, golem, cristal de folie{Colors.END}")
    print()

    print(f"\n{Colors.YELLOW}📚 SCÉNARIOS ORIGINAUX (Qualité ⭐⭐⭐){Colors.END}")
    print()
    print_scenario(4, "🏰", "La Chasse aux Gobelins", 3, "1-2h", 3)
    print_scenario(5, "🏛️", "The Sunless Citadel", 1, "2-3h", 3)
    print_scenario(6, "🔺", "La Tombe des Rois Serpents", 2, "2h", 3)
    print_scenario(7, "👁️", "L'Oeil de Gruumsh", 3, "2-3h", 3)
    print_scenario(8, "💀", "La Secte du Crâne", 4, "2-3h", 3)
    print_scenario(9, "💎", "Le Collier de Zark", 2, "1-2h", 3)
    print_scenario(10, "🍺", "L'Auberge du Sanglier Gris", 1, "1-2h", 3)
    print()

    print(f"\n{Colors.YELLOW}🚀 SCÉNARIOS CRÉÉS (Qualité ⭐⭐⭐){Colors.END}")
    print()
    print_scenario(11, "⚰️", "Cryptes de Kelemvor (nouveau)", 3, "2-3h", 3)
    print_scenario(12, "🎭", "Le Masque Utruz (nouveau)", 2, "2-3h", 3)
    print_scenario(13, "🏰", "Défis à Phlan (nouveau)", 1, "1-2h", 3)
    print()

    print(f"{Colors.RED}📋 SCÉNARIOS PROTOTYPES (Qualité ⭐⭐){Colors.END}")
    print(f"     14-37. 24 scénarios enrichis automatiquement (prototypes)")
    print()

    print("=" * 80)
    print(f"\n{Colors.BOLD}s.{Colors.END} ⚙️  Paramètres | {Colors.BOLD}q.{Colors.END} Quitter")

    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Choisissez un scénario (1-37), 's' pour paramètres ou 'q' pour quitter: {Colors.END}").strip()

            if choice.lower() == 'q':
                print(f"\n{Colors.GREEN}À bientôt aventurier! 🎲{Colors.END}\n")
                sys.exit(0)
            
            if choice.lower() == 's':
                show_settings_menu(config)
                config.apply_to_env()  # Réappliquer après changement
                # Afficher confirmation
                print(f"\n{Colors.GREEN}✅ Paramètres appliqués{Colors.END}")
                input("Appuyez sur ENTER pour continuer...")
                continue

            choice_num = int(choice)

            # Appliquer la configuration
            config.apply_to_env()
            
            if choice_num == 1:
                print(f"\n{Colors.GREEN}🎭 Lancement du Masque Utruz (Version Enrichie)...{Colors.END}")
                from masque_utruz_enrichi_game import MasqueUtruzEnrichiScenario
                scenario = MasqueUtruzEnrichiScenario()
                scenario.play()
                break

            elif choice_num == 2:
                print(f"\n{Colors.GREEN}⚰️ Lancement des Cryptes de Kelemvor (Version Enrichie)...{Colors.END}")
                from cryptes_de_kelemvor_manual_game import CryptesDeKelemvorManualScenario
                scenario = CryptesDeKelemvorManualScenario()
                scenario.play()
                break

            elif choice_num == 3:
                print(f"\n{Colors.GREEN}🗼 Lancement de La Tour du Mage Fou...{Colors.END}")
                from tour_mage_fou_game import TourMageFouScenario
                scenario = TourMageFouScenario()
                scenario.play()
                break

            elif choice_num == 4:
                print(f"\n{Colors.GREEN}🏰 Lancement de La Chasse aux Gobelins...{Colors.END}")
                from chasse_gobelins_refactored import ChasseGobelinsScenario
                scenario = ChasseGobelinsScenario()
                scenario.play()
                break

            elif choice_num == 5:
                print(f"\n{Colors.GREEN}🏛️ Lancement de The Sunless Citadel...{Colors.END}")
                from yawning_portal_game import SunlessCitadelScenario
                scenario = SunlessCitadelScenario()
                scenario.play()
                break

            elif choice_num == 6:
                print(f"\n{Colors.GREEN}🔺 Lancement de La Tombe des Rois Serpents...{Colors.END}")
                from tombe_rois_serpents_game import TombeRoisSerpentsScenario
                scenario = TombeRoisSerpentsScenario()
                scenario.play()
                break

            elif choice_num == 7:
                print(f"\n{Colors.GREEN}👁️ Lancement de L'Oeil de Gruumsh...{Colors.END}")
                from oeil_gruumsh_game import OeilDeGruumshScenario
                scenario = OeilDeGruumshScenario()
                scenario.play()
                break

            elif choice_num == 8:
                print(f"\n{Colors.GREEN}💀 Lancement de La Secte du Crâne...{Colors.END}")
                from secte_du_crane_game import SecteDuCraneScenario
                scenario = SecteDuCraneScenario()
                scenario.play()
                break

            elif choice_num == 9:
                print(f"\n{Colors.GREEN}💎 Lancement du Collier de Zark...{Colors.END}")
                from collier_de_zark_game import CollierDeZarkScenario
                scenario = CollierDeZarkScenario()
                scenario.play()
                break

            elif choice_num == 10:
                print(f"\n{Colors.GREEN}🍺 Lancement de L'Auberge du Sanglier Gris...{Colors.END}")
                from auberge_sanglier_gris_game import AubergeSanglierGrisScenario
                scenario = AubergeSanglierGrisScenario()
                scenario.play()
                break

            elif choice_num == 11:
                print(f"\n{Colors.GREEN}⚰️ Lancement de Cryptes de Kelemvor...{Colors.END}")
                from cryptes_de_kelemvor_game import CryptesDeKelemvorScenario
                scenario = CryptesDeKelemvorScenario()
                scenario.play()
                break

            elif choice_num == 12:
                print(f"\n{Colors.GREEN}🎭 Lancement du Masque Utruz...{Colors.END}")
                from masque_utruz_game import MasqueUtruzScenario
                scenario = MasqueUtruzScenario()
                scenario.play()
                break

            elif choice_num == 13:
                print(f"\n{Colors.GREEN}🏰 Lancement de Défis à Phlan...{Colors.END}")
                from defis_a_phlan_game import DefisAPlanScenario
                scenario = DefisAPlanScenario()
                scenario.play()
                break

            elif 14 <= choice_num <= 37:
                print(f"\n{Colors.YELLOW}⚠️  Scénarios prototypes (enrichissement automatique){Colors.END}")
                print(f"Ces scénarios sont des prototypes et nécessitent un enrichissement manuel.")
                print(f"Utilisez plutôt les scénarios enrichis manuellement (1-2) pour une meilleure expérience.")
                break

            else:
                print(f"{Colors.RED}❌ Choix invalide. Veuillez entrer 1-37 ou 'q'{Colors.END}")

        except ValueError:
            print(f"{Colors.RED}❌ Veuillez entrer un nombre valide{Colors.END}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}À bientôt aventurier! 🎲{Colors.END}\n")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}❌ Erreur: {e}{Colors.END}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

