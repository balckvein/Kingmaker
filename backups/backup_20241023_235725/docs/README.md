# Kingmaker Game Project
--------------------------------------
Version .1 **Welcome to "Empress of the Isles"**

In a world where women have long dominated the realms, you are the Empress of a small island village. Your people live in harmony with nature, but your isolation has made them vulnerable to threats from neighboring islands.

To ensure the survival and prosperity of your people, you must secure the services of brave warriors and skilled laborers. However, your villages are all-female, and men are scarce. You'll need to venture out into the unknown, pillaging rival villages to find male captives who can be tamed and trained for battle.

Your village is home to many hardworking women, but they require sustenance to thrive. Food production is a constant challenge, and you must balance resource gathering with the needs of your population.

As your village grows in strength and prosperity, so too will its reputation. But beware: rival empresses will not hesitate to strike at your flank, seeking to claim your resources and your people for themselves.

To overcome these challenges, you'll need to:

* Recruit brave warriors from pillaged villages
* Establish trade networks with neighboring islands
* Breed the strongest heroes through strategic matchmaking
* Improve your village's infrastructure through resource gathering and construction
* Defeat rival empresses in epic battles

Your ultimate goal is to defeat the fearsome "Titan Queen," a legendary ruler who has long dominated the seas. To achieve this, you'll need to build up your army, upgrade your defenses, and master the art of war.

Will you rise to the challenge and become the greatest Empress the Isles have ever known? The fate of your village rests in your hands. Let the conquest begin!

Here's a refactored version of the game concept based on your feedback:

Version.2 (using) **Welcome to "Kingmaker"**

In a world where females have long dominated the realms, you are the Empress of a small island village. Your people live in harmony with nature, but their isolation has made them vulnerable to threats from neighboring islands.

Your culture demands a king, and he must be the strongest, bravest, and most superior male. The king is not just a ruler, but a symbol of power and fertility. His role is to lead your village, protect its people, and ensure its prosperity.

However, your village is all-female, and men are scarce. To address this imbalance, you have developed a brutal barbarian system similar to ancient Sparta. No currency exists in your society; everything belongs to the state and the king. Resources are gathered for the benefit of the entire community, not for individual wealth.

The king's role is not only to lead but also to breed with the highest females in your village. Only heroes can become kings, and they are chosen based on their strength, bravery, and genetic superiority. The king must be able to adapt to the female culture and recognize the importance of balance between male and female energies.

But beware: neighboring islands are home to savage males who pillage and plunder, taking your females as slaves. These villages are known as "Warrior Clans." They do not care about maintaining a balanced gender ratio in their own society; their sole focus is on conquest and domination.

Your goal is to defeat the male boss of the Warrior Clan that threatens your village's survival. This will allow you to protect your people, ensure their prosperity, and restore balance to your community.

**Gameplay Overview:**

* Manage your village's resources, including food, flint, and stone
* Recruit warriors and heroes to defend your village against Warrior Clans
* Breed the strongest heroes with the highest females in your village to produce a superior king
* Defeat the male boss of the Warrior Clan to ensure your village's survival and prosperity
* Balance your community's gender ratio by recognizing the importance of both male and female energies

**Game Mechanics:**

* Resource gathering and management
* Hero recruitment and training
* Breeding system for producing kings
* Brutal barbarian system similar to ancient Sparta
* Warrior Clan raids and defense mechanics
* Balanced gameplay with a focus on strategy, resource management, and social dynamics
-----------------------------------------------------------------------
## Overview
Kingmaker is a village management and combat card game where players build and manage their settlement while training warriors for raids and combat. The game combines resource management, character progression, and strategic combat elements.

## Core Features

### Village Management
- Resource collection and management (wood, stone, iron, etc.)
- Building construction and upgrades
- Population management through housing and recruitment
- Dynamic economy with market fluctuations

### Character System
- Multiple character classes (Warrior, Ranger, Mage, Paladin, Berserker)
- Progression system with experience and levels
- Skill point allocation
- Equipment customization
- Status effects (ready, tired, injured)

### Combat System
- Arena combat between warriors
- Raid system with multiple tiers
- Boss battles
- Captive mechanics
- Victory bonuses and rewards

### Equipment System
- Weapons and armor with unique stats
- Durability mechanics
- Rarity system (Common to Legendary)
- Equipment repair and upgrading
- Tier-based progression

## Technical Architecture

### Project Structure
```
Kingmaker/
│
├── game_interface.py          # Main game entry point
├── card_game.py              # Core card game mechanics
├── combat.py                 # Combat system
├── raid_systems.py           # Raid mechanics
├── progression_system.py     # Character progression
├── equipment_system.py       # Equipment and items
├── economy_system.py         # Resource management
├── menu_system.py           # User interface
└── constants.py             # Game constants
```

### Key Systems

#### Character Classes
```python
class CharacterClass:
    WARRIOR = "Warrior"
    RANGER = "Ranger"
    MAGE = "Mage"
    PALADIN = "Paladin"
    BERSERKER = "Berserker"
```

#### Combat Stats
```python
COMBAT_STATS = {
    "BASE_WARRIOR": {
        "strength": (3, 6),
        "health": (10, 15),
        "defense": 2,
        "breeding_success": 0.3
    }
}
```

#### Raid Tiers
```python
RAID_SETTINGS = {
    "BASE_SUCCESS_CHANCE": 0.4,
    "STRENGTH_MULTIPLIER": 1.5,
    "CAPTIVE_RATE": 0.4,
    "RESOURCE_MULTIPLIER": 2
}
```

## Game Mechanics

### Character Progression
- Experience gain through combat and raids
- Level-based stat increases
- Skill point allocation
- Equipment bonuses
- Class-specific abilities

### Combat Resolution
1. Calculate effective strength including:
   - Base stats
   - Equipment bonuses
   - Victory bonuses
   - Raid experience

2. Determine success chance:
   - Party strength vs difficulty
   - Equipment modifiers
   - Status effects

3. Process rewards:
   - Experience gain
   - Resource rewards
   - Potential captives
   - Equipment drops

### Economy System
- Dynamic pricing based on market fluctuations
- Resource gathering and production
- Building costs and upkeep
- Equipment repair and upgrade costs

## Development Guidelines

### Adding New Features
1. Implement core mechanics in appropriate system file
2. Update constants.py with new configurations
3. Integrate with existing systems through game_interface.py
4. Add menu options in menu_system.py
5. Update save/load functionality

### Balance Considerations
1. Experience Curve: 1.5x multiplier per level
2. Resource Generation: Balanced against consumption
3. Combat Difficulty: Scales with day count
4. Equipment Power: Tier-based with rarity multipliers

### Testing
```python
def test_game():
    game = CardGame()
    game.combat_system = EnhancedCombatSystem()
    
    # Add initial population
    for _ in range(3):
        card = game.create_card("warrior")
        game.village.population.append(card)
```

## Save System
- JSON-based save format
- Stores complete game state:
  - Village resources
  - Population details
  - Equipment status
  - Progress metrics

## Future Enhancements
1. Combat System
   - Status effects
   - Combat modifiers
   - Tactical options

2. Equipment System
   - Set bonuses
   - Enchantment system
   - Degradation effects

3. Economy
   - Market cycles
   - Resource sinks
   - Trading system

4. Progression
   - Specialization trees
   - Prestige system
   - Achievements

## Getting Started

### Prerequisites
- Python 3.7+
- Required packages: random, math, json

### Installation
1. Clone the repository
2. Install dependencies
3. Run game_interface.py

### Basic Usage
```python
from game_interface import GameInterface

game = GameInterface()
game.start_game()
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Submit pull request with detailed description

## License
[Insert License Information]

## Credits
- Game Design: [Your Name]
- Development: [Your Team]
- Testing: [Testing Team]