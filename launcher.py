#!/usr/bin/env python3
"""
Launcher pour tous les scénarios D&D 5e enrichis
Permet de choisir et lancer facilement n'importe quel scénario
"""

import sys
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


def main():
    print_header("🎲 LAUNCHER DE SCÉNARIOS D&D 5e 🎲")

    print(f"{Colors.YELLOW}📖 SCÉNARIOS ENRICHIS MANUELLEMENT (Qualité ⭐⭐⭐⭐⭐){Colors.END}")
    print()
    print_scenario(1, "🎭", "Le Masque Utruz", 3, "3-4h", 5)
    print(f"     {Colors.GREEN}Cité sur faille, usurier, Utruz, Dieu-Poisson{Colors.END}")
    print()
    print_scenario(2, "⚰️", "Les Cryptes de Kelemvor", 4, "3-4h", 5)
    print(f"     {Colors.GREEN}Temple profané, 7 sceaux, braseros sacrés, nécrophage{Colors.END}")
    print()

    print(f"\n{Colors.YELLOW}📚 SCÉNARIOS ORIGINAUX (Qualité ⭐⭐⭐){Colors.END}")
    print()
    print_scenario(3, "🏰", "La Chasse aux Gobelins", 3, "1-2h", 3)
    print_scenario(4, "🏛️", "The Sunless Citadel", 1, "2-3h", 3)
    print_scenario(5, "🔺", "La Tombe des Rois Serpents", 2, "2h", 3)
    print_scenario(6, "👁️", "L'Oeil de Gruumsh", 3, "2-3h", 3)
    print_scenario(7, "💀", "La Secte du Crâne", 4, "2-3h", 3)
    print_scenario(8, "💎", "Le Collier de Zark", 2, "1-2h", 3)
    print_scenario(9, "🍺", "L'Auberge du Sanglier Gris", 1, "1-2h", 3)
    print()

    print(f"\n{Colors.YELLOW}🚀 SCÉNARIOS CRÉÉS (Qualité ⭐⭐⭐){Colors.END}")
    print()
    print_scenario(10, "⚰️", "Cryptes de Kelemvor (nouveau)", 3, "2-3h", 3)
    print_scenario(11, "🎭", "Le Masque Utruz (nouveau)", 2, "2-3h", 3)
    print_scenario(12, "🏰", "Défis à Phlan (nouveau)", 1, "1-2h", 3)
    print()

    print(f"{Colors.RED}📋 SCÉNARIOS PROTOTYPES (Qualité ⭐⭐){Colors.END}")
    print(f"     13-37. 25 scénarios enrichis automatiquement (prototypes)")
    print()

    print("=" * 80)

    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Choisissez un scénario (1-37) ou 'q' pour quitter: {Colors.END}").strip()

            if choice.lower() == 'q':
                print(f"\n{Colors.GREEN}À bientôt aventurier! 🎲{Colors.END}\n")
                sys.exit(0)

            choice_num = int(choice)

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
                print(f"\n{Colors.GREEN}🏰 Lancement de La Chasse aux Gobelins...{Colors.END}")
                from chasse_gobelins_refactored import ChasseGobelinsScenario
                scenario = ChasseGobelinsScenario()
                scenario.play()
                break

            elif choice_num == 4:
                print(f"\n{Colors.GREEN}🏛️ Lancement de The Sunless Citadel...{Colors.END}")
                from yawning_portal_game import SunlessCitadelScenario
                scenario = SunlessCitadelScenario()
                scenario.play()
                break

            elif choice_num == 5:
                print(f"\n{Colors.GREEN}🔺 Lancement de La Tombe des Rois Serpents...{Colors.END}")
                from tombe_rois_serpents_game import TombeRoisSerpentsScenario
                scenario = TombeRoisSerpentsScenario()
                scenario.play()
                break

            elif choice_num == 6:
                print(f"\n{Colors.GREEN}👁️ Lancement de L'Oeil de Gruumsh...{Colors.END}")
                from oeil_gruumsh_game import OeilDeGruumshScenario
                scenario = OeilDeGruumshScenario()
                scenario.play()
                break

            elif choice_num == 7:
                print(f"\n{Colors.GREEN}💀 Lancement de La Secte du Crâne...{Colors.END}")
                from secte_du_crane_game import SecteDuCraneScenario
                scenario = SecteDuCraneScenario()
                scenario.play()
                break

            elif choice_num == 8:
                print(f"\n{Colors.GREEN}💎 Lancement du Collier de Zark...{Colors.END}")
                from collier_de_zark_game import CollierDeZarkScenario
                scenario = CollierDeZarkScenario()
                scenario.play()
                break

            elif choice_num == 9:
                print(f"\n{Colors.GREEN}🍺 Lancement de L'Auberge du Sanglier Gris...{Colors.END}")
                from auberge_sanglier_gris_game import AubergeSanglierGrisScenario
                scenario = AubergeSanglierGrisScenario()
                scenario.play()
                break

            elif choice_num == 10:
                print(f"\n{Colors.GREEN}⚰️ Lancement de Cryptes de Kelemvor...{Colors.END}")
                from cryptes_de_kelemvor_game import CryptesDeKelemvorScenario
                scenario = CryptesDeKelemvorScenario()
                scenario.play()
                break

            elif choice_num == 11:
                print(f"\n{Colors.GREEN}🎭 Lancement du Masque Utruz...{Colors.END}")
                from masque_utruz_game import MasqueUtruzScenario
                scenario = MasqueUtruzScenario()
                scenario.play()
                break

            elif choice_num == 12:
                print(f"\n{Colors.GREEN}🏰 Lancement de Défis à Phlan...{Colors.END}")
                from defis_a_phlan_game import DefisAPlanScenario
                scenario = DefisAPlanScenario()
                scenario.play()
                break

            elif 13 <= choice_num <= 37:
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

