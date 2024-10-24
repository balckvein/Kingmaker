# combat_constants.py

COMBAT_STATS = {
    "BASE_WARRIOR": {
        "strength": (3, 6),
        "health": (10, 15),
        "defense": 2,
        "breeding_success": 0.3
    },
    "ELITE_WARRIOR": {
        "strength": (6, 9),
        "health": (15, 20),
        "defense": 3,
        "breeding_success": 0.4
    },
    "CHAMPION": {
        "strength": (9, 12),
        "health": (20, 25),
        "defense": 4,
        "breeding_success": 0.5
    }
}

RAID_SETTINGS = {
    "BASE_SUCCESS_CHANCE": 0.4,
    "STRENGTH_MULTIPLIER": 1.5,
    "CAPTIVE_RATE": 0.4,
    "RESOURCE_MULTIPLIER": 2
}

PROGRESSION_TIERS = {
    "TIER_1": {
        "strength_threshold": 30,
        "required_champions": 1,
        "raid_difficulty": 1.0
    },
    "TIER_2": {
        "strength_threshold": 50,
        "required_champions": 2,
        "raid_difficulty": 1.5
    },
    "TIER_3": {
        "strength_threshold": 70,
        "required_champions": 3,
        "raid_difficulty": 2.0
    }
}

BREEDING_SYSTEM = {
    "BASE_SUCCESS_RATE": 0.3,
    "ELITE_BONUS": 0.2,
    "CHAMPION_BONUS": 0.4,
    "FESTIVAL_BONUS": 0.5,
    "MAX_PAIRS_PER_HOUSE": 3
}