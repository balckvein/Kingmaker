# Kingmaker Game Mechanics Documentation

## Combat System

### Attack Calculations
- Base Formula: `attacker_str + weapon_bonus + crystal_bonus`
- Critical Chance: 15.0%
- Critical Multiplier: 1.5x

### Raid System
| Tier | Required Strength | Reward Multiplier | Captive Chance |
|------|------------------|------------------|----------------|
| tier_1 | 10 | 1.0x | 30.0% |
| tier_2 | 20 | 1.5x | 40.0% |
| tier_3 | 30 | 2.0x | 50.0% |

## Progression System

### Experience Gains
- Combat Victory: 100 EXP
- Raid Success: 200 EXP
- Resource Gathering: 50 EXP

### Skill Trees

#### Warrior Skills
| Level | Skill | Effect |
|-------|-------|--------|
| 1 | Power Strike | +20% damage |
| 5 | Battle Cry | Team buff |
| 10 | Berserker | Double damage |

#### Hero Skills
| Level | Skill | Effect |
|-------|-------|--------|
| 1 | Leadership | Team exp bonus |
| 5 | Rally | Prevent retreat |
| 10 | Heroic Stand | Team invulnerable |

## Resource System

### Gathering Rates
| Resource | Base Rate | Tool Bonus |
|----------|------------|------------|
| wood | 10 | +5 |
| stone | 8 | +4 |
| iron | 5 | +3 |

## Building System

| Building | Wood Cost | Stone Cost | Build Time | Special |
|----------|------------|------------|------------|---------||
| house | 4 | 2 | 2 days | Capacity: 4 |
| barracks | 6 | 4 | 3 days | Training +20.0% |
| workshop | 5 | 3 | 2 days | Crafting +25.0% |
