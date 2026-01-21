"""
Shared Boltac Merchant Adapter for DnD5e-Scenarios
Integrates with the persistent Boltac shop system
"""
import sys
import os
from typing import List, Optional

# Add paths to dnd-5e-core and DnD-5th-Edition-API
_current_dir = os.path.dirname(os.path.abspath(__file__))
_scenarios_root = os.path.dirname(os.path.dirname(_current_dir))

# Add dnd-5e-core
_dnd_5e_core_path = os.path.join(os.path.dirname(_scenarios_root), 'dnd-5e-core')
if os.path.exists(_dnd_5e_core_path) and _dnd_5e_core_path not in sys.path:
    sys.path.insert(0, _dnd_5e_core_path)

# Add DnD-5th-Edition-API for boltac_inventory
_api_path = os.path.join(os.path.dirname(_scenarios_root), 'DnD-5th-Edition-API')
if os.path.exists(_api_path) and _api_path not in sys.path:
    sys.path.insert(0, _api_path)

try:
    from boltac_inventory import get_boltac_shop, BoltacInventory
    from dnd_5e_core.equipment import get_magic_item, get_special_weapon, get_special_armor
    BOLTAC_AVAILABLE = True
except ImportError:
    BOLTAC_AVAILABLE = False
    print("⚠️  Boltac shared inventory not available - using local merchant system")


class SharedMerchant:
    """
    Adapter for shared Boltac merchant system.
    Falls back to local system if Boltac not available.
    """

    def __init__(self):
        """Initialize merchant - connects to shared Boltac if available"""
        if BOLTAC_AVAILABLE:
            try:
                self.shop = get_boltac_shop()
                self.using_shared = True
                print("✅ Connected to shared Boltac inventory")
            except Exception as e:
                self.shop = None
                self.using_shared = False
                print(f"⚠️  Could not connect to Boltac: {e}")
        else:
            self.shop = None
            self.using_shared = False

    def get_available_items(self) -> List:
        """Get all items available for purchase"""
        if self.using_shared and self.shop:
            try:
                return self.shop.get_all_available_items()
            except Exception:
                pass
        return []

    def buy_item(self, character, item_index: str) -> tuple[bool, str]:
        """
        Character buys an item from shop.

        Args:
            character: Character buying (must have 'gold' and 'inventory')
            item_index: Index of item to buy

        Returns:
            (success: bool, message: str)
        """
        if not self.using_shared:
            return (False, "Shared merchant not available")

        try:
            # Get item
            item = get_magic_item(item_index)
            if not item:
                item = get_special_weapon(item_index)
            if not item:
                item = get_special_armor(item_index)

            if not item:
                return (False, f"Item {item_index} not found")

            # Get cost
            if hasattr(item, 'cost'):
                if hasattr(item.cost, 'quantity'):
                    cost_copper = item.cost.quantity
                elif hasattr(item.cost, 'value'):
                    cost_copper = item.cost.value
                else:
                    cost_copper = 0
            else:
                return (False, "Item has no cost")

            cost_gold = cost_copper / 100

            # Check if affordable
            if character.gold < cost_gold:
                return (False, f"Not enough gold (need {cost_gold} gp, have {character.gold} gp)")

            # Check inventory space
            empty_slots = [i for i, inv_item in enumerate(character.inventory) if inv_item is None]
            if not empty_slots:
                return (False, "No inventory space")

            # Purchase
            character.gold -= cost_gold
            slot_idx = min(empty_slots)
            character.inventory[slot_idx] = item

            # Remove from shop
            self.shop.sell_to_player(item, cost_copper)

            return (True, f"Bought {item.name} for {cost_gold} gp")

        except Exception as e:
            return (False, f"Error buying item: {e}")

    def sell_item(self, character, item) -> tuple[bool, str]:
        """
        Character sells an item to shop.

        Args:
            character: Character selling
            item: Item to sell

        Returns:
            (success: bool, message: str)
        """
        if not self.using_shared:
            return (False, "Shared merchant not available")

        try:
            # Get cost
            if hasattr(item, 'cost'):
                if hasattr(item.cost, 'quantity'):
                    cost_copper = item.cost.quantity
                elif hasattr(item.cost, 'value'):
                    cost_copper = item.cost.value
                else:
                    cost_copper = 0
            else:
                return (False, "Item has no cost")

            # Sell price is 50% of buy price
            sell_price_copper = cost_copper // 2
            sell_price_gold = sell_price_copper / 100

            # Sell to shop
            if self.shop.buy_from_player(item, sell_price_copper):
                character.gold += sell_price_gold

                # Remove from inventory
                if item in character.inventory:
                    idx = character.inventory.index(item)
                    character.inventory[idx] = None

                return (True, f"Sold {item.name} for {sell_price_gold} gp")
            else:
                return (False, "Shop cannot buy item (not enough gold)")

        except Exception as e:
            return (False, f"Error selling item: {e}")

    def display_shop(self, verbose: bool = True):
        """Display available items"""
        if not self.using_shared:
            if verbose:
                print("⚠️  Shared shop not available")
            return

        items = self.get_available_items()

        if verbose:
            print("\n" + "="*70)
            print("  BOLTAC'S TRADING POST")
            print("="*70)
            print(f"\nAvailable Items ({len(items)}):\n")

            for i, item in enumerate(items, 1):
                if hasattr(item, 'cost'):
                    if hasattr(item.cost, 'quantity'):
                        cost = item.cost.quantity / 100
                    elif hasattr(item.cost, 'value'):
                        cost = item.cost.value / 100
                    else:
                        cost = 0
                else:
                    cost = 0

                rarity = item.rarity.value if hasattr(item, 'rarity') else '?'
                print(f"   {i:2}. {item.name:40} [{rarity:12}] {cost:>7.0f} gp")

            print("="*70)


# Convenience function for scenarios
def get_merchant() -> SharedMerchant:
    """Get merchant instance (cached)"""
    global _merchant_instance
    if '_merchant_instance' not in globals():
        _merchant_instance = SharedMerchant()
    return _merchant_instance


__all__ = ['SharedMerchant', 'get_merchant', 'BOLTAC_AVAILABLE']
