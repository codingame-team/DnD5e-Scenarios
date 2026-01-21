"""
Configuration globale du jeu
Lit les paramètres depuis les variables d'environnement
"""

import os


class GameSettings:
    """Paramètres globaux du jeu"""
    
    @staticmethod
    def get_text_speed():
        """
        Obtenir la vitesse de défilement du texte
        
        Returns:
            float: Délai en secondes (0 = instantané)
        """
        speed = os.environ.get('DND_TEXT_SPEED', 'normal')
        speed_map = {
            'slow': 0.05,
            'normal': 0.03,
            'fast': 0.01,
            'instant': 0
        }
        return speed_map.get(speed, 0.03)
    
    @staticmethod
    def is_auto_save_enabled():
        """
        Vérifier si les sauvegardes automatiques sont activées
        
        Returns:
            bool: True si auto-save activé
        """
        return os.environ.get('DND_AUTO_SAVE', 'true').lower() == 'true'
    
    @staticmethod
    def get_combat_system():
        """
        Obtenir le système de combat à utiliser
        
        Returns:
            str: 'dnd_5e_core' ou 'enhanced'
        """
        return os.environ.get('DND_COMBAT_SYSTEM', 'dnd_5e_core')
