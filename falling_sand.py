#!/usr/bin/env python3
"""
Falling Sand Simulation — 121 Elements | 11 Categories
"""

import pygame, random, sys
from collections import defaultdict
import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
CELL = 4
GW, GH = 240, 160
UI_W = 250
SW = GW * CELL + UI_W
SH = GH * CELL

# ═══════════════════════════════════════════════════════════════════════════════
# ELEMENT IDS
# ═══════════════════════════════════════════════════════════════════════════════
EMPTY = 0
SAND,GRAVEL,DIRT,COAL,SUGAR,SALT,ASH,GUNPOWDER,SNOW,DUST = range(1,11)
CONCRETE_POWDER,SULFUR,PHOSPHORUS,SEED,GLASS_SHARD,CHARCOAL = range(51,57)
WATER,OIL,LAVA,ACID,MERCURY,MILK,HONEY,MUD,SLIME,MOLTEN_GLASS,MOLTEN_METAL,NITROGLYCERIN,WINE = range(11,24)
SALTWATER,NUCLEAR_WASTE,CHLORINE,INK,LIQUID_NITROGEN = range(57,62)
STEAM,SMOKE,NATURAL_GAS,POISON_GAS,HELIUM,HYDROGEN,OXYGEN,CO2,NEON = range(24,33)
CLOUD,FOG,SPORE,AMMONIA = range(62,66)
STONE,WOOD,ICE,GLASS,METAL,RUBBER,PLASTIC,FUSE,PLANT,MUSHROOM,CRYSTAL,DIAMOND,BRICK,OBSIDIAN = range(33,47)
TNT,C4,CACTUS,GRASS,WIRE,URANIUM,BATTERY,MOSS = range(66,74)
FIRE,CLONE,VOID,WALL = 47,48,49,50
ELECTRICITY,ANT,PLASMA = 74,75,76
FISH,BIRD,SPIDER,BACTERIA,TERMITE,WORM,JELLYFISH = range(77,84)
THERMITE,DYNAMITE,FLASH_POWDER,PROPANE,PETN,SMOKE_BOMB = range(84,90)
BREAD,MEAT,EGG,CHEESE,FRUIT,HAY = range(90,96)
LED,SOLAR_CELL,SENSOR,LASER_E,MAGNET,GENERATOR = range(96,102)
STEEL,BRONZE,COPPER,GOLD,SILVER,RUST = range(102,108)
SOAP,LYE,WAX,RESIN,PAPER,FLOUR,COKE,NAPALM,DRY_ICE,IODINE,TAR,ZINC,POTASSIUM,CALCIUM = range(108,122)

# ═══════════════════════════════════════════════════════════════════════════════
# ELEMENT TRAITS (bit flags for O(1) property queries)
# ═══════════════════════════════════════════════════════════════════════════════
T_FLAM=0x001; T_COND=0x002; T_ORG=0x004; T_LIVE=0x008; T_TOXIC=0x010
T_EXPL=0x020; T_RADIO=0x040; T_CORR=0x080; T_CRYO=0x100; T_HEAT=0x200
T_MAG=0x400; T_OXID=0x800; T_POW=0x1000; T_LIQ=0x2000; T_GAS=0x4000
T_CATALYST=0x8000  # element that speeds up reactions but isn't consumed

ET = {
    SAND:0, GRAVEL:0, DIRT:T_ORG, COAL:T_FLAM|T_ORG, SUGAR:T_FLAM|T_ORG,
    SALT:0, ASH:0, GUNPOWDER:T_EXPL|T_FLAM, SNOW:0, DUST:T_FLAM|T_ORG,
    CONCRETE_POWDER:0, SULFUR:T_FLAM, PHOSPHORUS:T_FLAM, SEED:T_ORG,
    GLASS_SHARD:0, CHARCOAL:T_FLAM|T_ORG,
    WATER:T_COND|T_LIQ, OIL:T_FLAM|T_LIQ, LAVA:T_HEAT|T_LIQ, ACID:T_CORR|T_LIQ,
    MERCURY:T_COND|T_TOXIC|T_LIQ, MILK:T_LIQ, HONEY:T_FLAM|T_LIQ, MUD:T_LIQ,
    SLIME:T_LIQ, MOLTEN_GLASS:T_HEAT|T_LIQ, MOLTEN_METAL:T_HEAT|T_LIQ,
    NITROGLYCERIN:T_EXPL|T_FLAM|T_LIQ, WINE:T_FLAM|T_LIQ,
    SALTWATER:T_COND|T_TOXIC|T_LIQ, NUCLEAR_WASTE:T_RADIO|T_TOXIC|T_LIQ,
    CHLORINE:T_TOXIC|T_CORR|T_LIQ, INK:T_LIQ, LIQUID_NITROGEN:T_CRYO|T_LIQ,
    STEAM:T_GAS, SMOKE:T_GAS, NATURAL_GAS:T_FLAM|T_GAS, POISON_GAS:T_TOXIC|T_GAS,
    HELIUM:T_GAS, HYDROGEN:T_FLAM|T_GAS, OXYGEN:T_OXID|T_GAS, CO2:T_GAS, NEON:T_GAS,
    CLOUD:T_GAS, FOG:T_GAS, SPORE:T_GAS, AMMONIA:T_TOXIC|T_GAS,
    STONE:0, WOOD:T_FLAM|T_ORG, ICE:0, GLASS:0, METAL:T_COND,
    RUBBER:T_FLAM|T_ORG, PLASTIC:T_FLAM|T_ORG, FUSE:T_FLAM|T_ORG,
    PLANT:T_ORG|T_FLAM, MUSHROOM:T_ORG, CRYSTAL:0, DIAMOND:0,
    BRICK:0, OBSIDIAN:0, TNT:T_EXPL, C4:T_EXPL, CACTUS:T_ORG|T_FLAM,
    GRASS:T_ORG|T_FLAM, WIRE:T_COND, URANIUM:T_RADIO|T_COND,
    BATTERY:T_COND, MOSS:T_ORG,
    FIRE:T_HEAT|T_FLAM, CLONE:0, VOID:0, WALL:0,
    ELECTRICITY:0, ANT:T_LIVE|T_ORG, PLASMA:T_HEAT,
    FISH:T_LIVE|T_ORG, BIRD:T_LIVE|T_ORG, SPIDER:T_LIVE|T_ORG,
    BACTERIA:T_LIVE|T_ORG, TERMITE:T_LIVE|T_ORG, WORM:T_LIVE|T_ORG,
    JELLYFISH:T_LIVE|T_TOXIC|T_LIQ,
    THERMITE:T_EXPL, DYNAMITE:T_EXPL, FLASH_POWDER:T_EXPL,
    PROPANE:T_EXPL, PETN:T_EXPL, SMOKE_BOMB:T_EXPL,
    BREAD:T_ORG|T_FLAM, MEAT:T_ORG|T_FLAM, EGG:T_ORG,
    CHEESE:T_ORG|T_FLAM, FRUIT:T_ORG|T_FLAM, HAY:T_ORG|T_FLAM,
    LED:T_COND, SOLAR_CELL:T_COND, SENSOR:T_COND,
    LASER_E:T_COND, MAGNET:T_COND|T_MAG, GENERATOR:T_COND,
    STEEL:T_COND, BRONZE:T_COND, COPPER:T_COND,
    GOLD:T_COND, SILVER:T_COND, RUST:0,
    SOAP:T_LIQ, LYE:T_CORR|T_LIQ, WAX:T_FLAM|T_LIQ, RESIN:T_FLAM|T_ORG,
    PAPER:T_FLAM|T_ORG, FLOUR:T_FLAM|T_POW|T_ORG, COKE:T_FLAM|T_ORG,
    NAPALM:T_FLAM|T_LIQ, DRY_ICE:T_CRYO|T_POW, IODINE:T_FLAM|T_POW,
    TAR:T_FLAM|T_LIQ, ZINC:T_COND, POTASSIUM:T_FLAM|T_EXPL|T_POW,
    CALCIUM:T_FLAM|T_POW,
}

# Derive trait-based sets from ET
FLAMMABLES   = frozenset(e for e,t in ET.items() if t & T_FLAM)
CONDUCTIVE   = frozenset(e for e,t in ET.items() if t & T_COND)
ORGANIC      = frozenset(e for e,t in ET.items() if t & T_ORG)
CREATURES    = frozenset(e for e,t in ET.items() if t & T_LIVE)
TOXIC_SET    = frozenset(e for e,t in ET.items() if t & T_TOXIC)
RADIOACTIVE  = frozenset(e for e,t in ET.items() if t & T_RADIO)
CORROSIVE    = frozenset(e for e,t in ET.items() if t & T_CORR)
CRYOGENIC    = frozenset(e for e,t in ET.items() if t & T_CRYO)
HEAT_SOURCES = frozenset(e for e,t in ET.items() if t & T_HEAT)
CATALYSTS    = frozenset(e for e,t in ET.items() if t & T_CATALYST)

# ═══════════════════════════════════════════════════════════════════════════════
# ELEMENT METADATA
# ═══════════════════════════════════════════════════════════════════════════════
ELEM = {
    SAND:("Sand",(194,178,128),4), GRAVEL:("Gravel",(140,140,140),5),
    DIRT:("Dirt",(139,90,43),3), COAL:("Coal",(54,54,54),3),
    SUGAR:("Sugar",(255,250,240),2), SALT:("Salt",(240,240,240),2),
    ASH:("Ash",(100,100,100),1), GUNPOWDER:("Gunpowder",(60,60,60),2),
    SNOW:("Snow",(240,248,255),1), DUST:("Dust",(180,160,130),1),
    CONCRETE_POWDER:("ConcPowder",(170,165,155),4), SULFUR:("Sulfur",(210,200,50),3),
    PHOSPHORUS:("Phosphorus",(240,220,180),2), SEED:("Seed",(100,70,30),1),
    GLASS_SHARD:("GlassShard",(190,220,240),2), CHARCOAL:("Charcoal",(40,38,36),2),
    WATER:("Water",(30,100,200),2), OIL:("Oil",(80,60,20),1),
    LAVA:("Lava",(207,50,20),6), ACID:("Acid",(120,255,30),2),
    MERCURY:("Mercury",(180,190,200),8), MILK:("Milk",(245,240,230),2),
    HONEY:("Honey",(218,160,32),3), MUD:("Mud",(100,70,30),3),
    SLIME:("Slime",(50,200,50),3), MOLTEN_GLASS:("MolGlass",(255,200,100),5),
    MOLTEN_METAL:("MolMetal",(255,120,30),7), NITROGLYCERIN:("NitroGlyc",(180,180,60),2),
    WINE:("Wine",(120,20,60),2), SALTWATER:("Saltwater",(40,90,180),3),
    NUCLEAR_WASTE:("NucWaste",(50,220,50),3), CHLORINE:("Chlorine",(140,230,100),2),
    INK:("Ink",(10,10,30),2), LIQUID_NITROGEN:("LiqNitro",(180,210,255),1),
    STEAM:("Steam",(200,210,230),0), SMOKE:("Smoke",(80,80,80),0),
    NATURAL_GAS:("NatGas",(200,255,200),-1), POISON_GAS:("PoisonGas",(140,0,200),0),
    HELIUM:("Helium",(230,230,255),-1), HYDROGEN:("Hydrogen",(180,180,255),-2),
    OXYGEN:("Oxygen",(180,230,255),0), CO2:("CO2",(160,160,160),1),
    NEON:("Neon",(255,80,150),-1), CLOUD:("Cloud",(220,225,235),0),
    FOG:("Fog",(200,200,210),0), SPORE:("Spore",(160,130,90),-1),
    AMMONIA:("Ammonia",(200,200,180),-1),
    STONE:("Stone",(128,128,128),99), WOOD:("Wood",(160,100,40),99),
    ICE:("Ice",(180,220,255),99), GLASS:("Glass",(200,230,255),99),
    METAL:("Metal",(170,170,180),99), RUBBER:("Rubber",(50,50,50),99),
    PLASTIC:("Plastic",(220,200,160),99), FUSE:("Fuse",(200,50,50),99),
    PLANT:("Plant",(34,139,34),99), MUSHROOM:("Mushroom",(180,120,180),99),
    CRYSTAL:("Crystal",(150,200,255),99), DIAMOND:("Diamond",(220,240,255),99),
    BRICK:("Brick",(178,80,60),99), OBSIDIAN:("Obsidian",(30,10,50),99),
    TNT:("TNT",(200,50,50),99), C4:("C4",(210,200,170),99),
    CACTUS:("Cactus",(30,140,30),99), GRASS:("Grass",(60,170,30),99),
    WIRE:("Wire",(200,140,50),99), URANIUM:("Uranium",(80,200,80),99),
    BATTERY:("Battery",(50,50,200),99), MOSS:("Moss",(60,120,60),99),
    FIRE:("Fire",(255,100,20),-1), CLONE:("Clone",(0,220,180),0),
    VOID:("Void",(20,0,40),0), WALL:("Wall",(100,100,100),0),
    ELECTRICITY:("Electric",(100,180,255),0), ANT:("Ant",(80,40,20),0),
    PLASMA:("Plasma",(200,100,255),0),
    FISH:("Fish",(60,120,220),0), BIRD:("Bird",(140,100,60),0),
    SPIDER:("Spider",(50,30,50),0), BACTERIA:("Bacteria",(100,200,100),0),
    TERMITE:("Termite",(160,100,40),0), WORM:("Worm",(180,100,120),0),
    JELLYFISH:("Jellyfish",(200,150,255),0),
    THERMITE:("Thermite",(180,100,40),99), DYNAMITE:("Dynamite",(200,60,60),99),
    FLASH_POWDER:("FlashPow",(220,220,200),99), PROPANE:("Propane",(100,100,120),99),
    PETN:("PETN",(180,180,160),99), SMOKE_BOMB:("SmokeBmb",(80,80,80),99),
    BREAD:("Bread",(210,180,120),99), MEAT:("Meat",(180,60,60),99),
    EGG:("Egg",(240,235,220),99), CHEESE:("Cheese",(240,200,60),99),
    FRUIT:("Fruit",(220,40,60),99), HAY:("Hay",(200,180,60),99),
    LED:("LED",(0,200,50),99), SOLAR_CELL:("SolarCell",(30,30,160),99),
    SENSOR:("Sensor",(100,200,200),99), LASER_E:("Laser",(255,30,30),99),
    MAGNET:("Magnet",(180,30,30),99), GENERATOR:("Generator",(150,150,50),99),
    STEEL:("Steel",(160,165,175),99), BRONZE:("Bronze",(180,140,70),99),
    COPPER:("Copper",(180,110,50),99), GOLD:("Gold",(255,210,50),99),
    SILVER:("Silver",(200,200,210),99), RUST:("Rust",(160,80,40),99),
    SOAP:("Soap",(240,240,230),3), LYE:("Lye",(200,200,150),2),
    WAX:("Wax",(240,230,180),2), RESIN:("Resin",(180,140,60),99),
    PAPER:("Paper",(240,235,220),1), FLOUR:("Flour",(245,240,230),2),
    COKE:("Coke",(40,35,35),4), NAPALM:("Napalm",(220,120,30),3),
    DRY_ICE:("DryIce",(200,220,240),2), IODINE:("Iodine",(100,50,150),3),
    TAR:("Tar",(30,25,25),4), ZINC:("Zinc",(170,175,180),99),
    POTASSIUM:("Potassium",(180,180,200),2), CALCIUM:("Calcium",(210,210,210),3),
}

COLOR_VAR = {
    SAND:15,GRAVEL:20,DIRT:15,COAL:10,SUGAR:5,SALT:5,ASH:10,GUNPOWDER:10,
    SNOW:5,DUST:15,WATER:20,OIL:10,LAVA:40,ACID:15,MERCURY:10,MILK:10,
    HONEY:15,MUD:10,SLIME:15,WOOD:15,STONE:15,PLANT:20,MUSHROOM:15,
    CRYSTAL:15,FIRE:50,SMOKE:15,BRICK:12,GLASS:10,WINE:10,SULFUR:12,
    PHOSPHORUS:10,CONCRETE_POWDER:8,SALTWATER:12,NUCLEAR_WASTE:25,CHLORINE:12,
    INK:5,LIQUID_NITROGEN:8,CLOUD:8,FOG:6,SPORE:12,AMMONIA:10,GRASS:18,
    CACTUS:15,WIRE:8,URANIUM:20,BATTERY:10,MOSS:12,CHARCOAL:8,GLASS_SHARD:10,
    SEED:8,ELECTRICITY:30,PLASMA:40,FISH:15,BIRD:12,SPIDER:8,BACTERIA:15,
    TERMITE:10,WORM:10,JELLYFISH:20,THERMITE:10,DYNAMITE:12,FLASH_POWDER:8,
    PROPANE:8,PETN:8,SMOKE_BOMB:6,BREAD:10,MEAT:15,EGG:8,CHEESE:12,
    FRUIT:15,HAY:10,LED:20,SOLAR_CELL:8,SENSOR:10,LASER_E:15,MAGNET:8,
    GENERATOR:10,STEEL:8,BRONZE:10,COPPER:12,GOLD:8,SILVER:8,RUST:12,
    SOAP:8,LYE:10,WAX:10,RESIN:15,PAPER:8,FLOUR:5,COKE:8,NAPALM:12,
    DRY_ICE:8,IODINE:15,TAR:8,ZINC:8,POTASSIUM:10,CALCIUM:8,
}

# Explicit category sets
POWDERS  = frozenset(list(range(1,11))+list(range(51,57)))
LIQUIDS  = frozenset(list(range(11,24))+list(range(57,62))+[SOAP, LYE])
GASES    = frozenset(list(range(24,33))+list(range(62,66)))
SOLIDS   = frozenset(list(range(33,47))+list(range(66,74)))
SPECIALS = frozenset([47,48,49,50,74,75,76])
LIFE_S   = frozenset(range(77,84))
EXPL_S   = frozenset(range(84,90))
FOOD_S   = frozenset(range(90,96))
ELEC_S   = frozenset(range(96,102))
ALLOY_S  = frozenset(range(102,108))
MATERIALS = frozenset(range(108,122))

CATEGORIES = [
    ("POWDERS",    sorted(POWDERS),  (194,178,128)),
    ("LIQUIDS",    sorted(LIQUIDS),  (30,100,200)),
    ("GASES",      sorted(GASES),    (200,210,230)),
    ("SOLIDS",     sorted(SOLIDS),   (128,128,128)),
    ("SPECIAL",    sorted(SPECIALS), (255,100,20)),
    ("LIFE",       sorted(LIFE_S),   (100,200,100)),
    ("EXPLOSIVES", sorted(EXPL_S),   (220,60,60)),
    ("FOOD",       sorted(FOOD_S),   (210,180,120)),
    ("ELECTRONICS",sorted(ELEC_S),   (100,180,255)),
    ("ALLOYS",     sorted(ALLOY_S),  (200,200,210)),
    ("MATERIALS",  sorted(MATERIALS),(210,180,120)),
]

# Source/target element groups
HEAT_SRC  = (FIRE, LAVA, PLASMA, MOLTEN_METAL, MOLTEN_GLASS)
ELEC_SRC  = (ELECTRICITY, PLASMA)
COLD_SRC  = (ICE, LIQUID_NITROGEN, DRY_ICE)
ALL_HEAT  = HEAT_SRC + ELEC_SRC

# Elements that emit light (for glow/bloom rendering)
GLOW_SET = frozenset([FIRE, PLASMA, ELECTRICITY, NEON, LAVA, MOLTEN_METAL,
                       MOLTEN_GLASS, LASER_E, URANIUM, NUCLEAR_WASTE])


# ═══════════════════════════════════════════════════════════════════════════════
# PER-CELL STATE TRACKING
# ═══════════════════════════════════════════════════════════════════════════════
# Each cell tracks temperature (-100..200) and moisture (0..100).
# Temperature: ambient=20, heat sources raise it, cold sources lower it.
# Moisture: water/rain raises it, heat evaporates it.
# State decays toward ambient each tick.
# Reactions can check/modify state for conditional interactions.

AMBIENT_TEMP = 20
MIN_TEMP, MAX_TEMP = -100, 200
AMBIENT_MOIST = 0
MAX_MOIST = 100

temp_grid  = [[AMBIENT_TEMP]*GW for _ in range(GH)]
moist_grid = [[AMBIENT_MOIST]*GW for _ in range(GH)]
pressure_grid = [[0]*GW for _ in range(GH)]
cooldown_grid = [[0]*GW for _ in range(GH)]

def get_temp(x, y):
    return temp_grid[y][x] if ib(x, y) else AMBIENT_TEMP

def get_moist(x, y):
    return moist_grid[y][x] if ib(x, y) else AMBIENT_MOIST

def set_temp(x, y, t):
    if ib(x, y): temp_grid[y][x] = max(MIN_TEMP, min(MAX_TEMP, t))

def set_moist(x, y, m):
    if ib(x, y): moist_grid[y][x] = max(0, min(MAX_MOIST, m))

def add_temp(x, y, dt):
    if ib(x, y): temp_grid[y][x] = max(MIN_TEMP, min(MAX_TEMP, temp_grid[y][x] + dt))

def add_moist(x, y, dm):
    if ib(x, y): moist_grid[y][x] = max(0, min(MAX_MOIST, moist_grid[y][x] + dm))

def reset_state(x, y):
    """Reset state when cell becomes EMPTY."""
    if ib(x, y):
        temp_grid[y][x] = AMBIENT_TEMP
        moist_grid[y][x] = AMBIENT_MOIST
        pressure_grid[y][x] = 0
        cooldown_grid[y][x] = 0

def get_pressure(x, y):
    if not ib(x, y): return 0
    return sum(1 for _,_,n in neighbors(x, y) if n != EMPTY and n != -1)

def get_cooldown(x, y):
    return cooldown_grid[y][x] if ib(x, y) else 0

def set_cooldown(x, y, ticks):
    if ib(x, y): cooldown_grid[y][x] = ticks

def decay_state(x, y):
    """Per-tick decay toward ambient."""
    if not ib(x, y): return
    t = temp_grid[y][x]
    temp_grid[y][x] = t + int((AMBIENT_TEMP - t) * 0.05)
    m = moist_grid[y][x]
    moist_grid[y][x] = m + int((AMBIENT_MOIST - m) * 0.02)
    if cooldown_grid[y][x] > 0:
        cooldown_grid[y][x] -= 1
    pressure_grid[y][x] = get_pressure(x, y)

def propagate_heat(x, y):
    """Heat sources spread temperature to neighbors."""
    t = get_temp(x, y)
    if abs(t - AMBIENT_TEMP) < 3: return
    dt = (t - AMBIENT_TEMP) // 8
    if dt == 0: return
    for nx, ny, _ in neighbors(x, y):
        add_temp(nx, ny, dt)


# ═══════════════════════════════════════════════════════════════════════════════
# GRID & HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
grid  = [[EMPTY]*GW for _ in range(GH)]
cgrid = [[(0,0,0)]*GW for _ in range(GH)]
moved = [[False]*GW for _ in range(GH)]

def ib(x,y): return 0<=x<GW and 0<=y<GH
def g(x,y): return grid[y][x] if ib(x,y) else -1
def s(x,y,e,c=None):
    if not ib(x,y): return
    old_e = grid[y][x]
    grid[y][x]=e
    if c is None:
        if e!=EMPTY:
            b=ELEM[e][1]; v=COLOR_VAR.get(e,8)
            c=tuple(max(0,min(255,ch+random.randint(-v,v))) for ch in b)
        else: c=(0,0,0)
    cgrid[y][x]=c
    if e == EMPTY: reset_state(x, y)
    # Heat sources set temperature on placement
    elif e in (FIRE, PLASMA): set_temp(x, y, 180 + random.randint(0, 20))
    elif e == LAVA: set_temp(x, y, 120 + random.randint(0, 30))
    elif e == MOLTEN_METAL: set_temp(x, y, 100 + random.randint(0, 20))
    elif e == MOLTEN_GLASS: set_temp(x, y, 80 + random.randint(0, 20))
    elif e in (ICE, LIQUID_NITROGEN): set_temp(x, y, -40 + random.randint(-20, 0))
    # Moisture sources
    elif e in (WATER, SALTWATER, MUD, MILK, SLIME): add_moist(x, y, 30)
    elif e in (STEAM, CLOUD, FOG): add_moist(x, y, 15)
    # Moisture decreases when replacing wet elements
    elif old_e in (WATER, SALTWATER, MUD, MILK, SLIME, STEAM, CLOUD, FOG, OIL, HONEY, SOAP, WINE, LYE, NUCLEAR_WASTE, CHLORINE, INK, MERCURY):
        if e not in (WATER, SALTWATER, MUD, MILK, SLIME, STEAM, CLOUD, FOG, OIL, HONEY, SOAP, WINE, LYE, NUCLEAR_WASTE, CHLORINE, INK, MERCURY):
            add_moist(x, y, -10)

def sw(x1,y1,x2,y2):
    grid[y1][x1],grid[y2][x2]=grid[y2][x2],grid[y1][x1]
    cgrid[y1][x1],cgrid[y2][x2]=cgrid[y2][x2],cgrid[y1][x1]
    moved[y2][x2]=True
    # Swap state too
    temp_grid[y1][x1],temp_grid[y2][x2]=temp_grid[y2][x2],temp_grid[y1][x1]
    moist_grid[y1][x1],moist_grid[y2][x2]=moist_grid[y2][x2],moist_grid[y1][x1]
    pressure_grid[y1][x1],pressure_grid[y2][x2]=pressure_grid[y2][x2],pressure_grid[y1][x1]
    cooldown_grid[y1][x1],cooldown_grid[y2][x2]=cooldown_grid[y2][x2],cooldown_grid[y1][x1]

def empt(x,y): return ib(x,y) and grid[y][x]==EMPTY
def dens(e): return 0 if e==EMPTY else ELEM[e][2]
def is_gas(e): return e in GASES
def is_liq(e): return e in LIQUIDS
def is_pow(e): return e in POWDERS
def is_sol(e): return e in SOLIDS

def can_disp(em, et):
    if et==EMPTY: return True
    if et==-1: return False
    dm,dt=dens(em),dens(et)
    if is_gas(em) and is_gas(et): return dm<dt
    if is_liq(em) and is_liq(et): return dm>dt
    if is_pow(em) and is_liq(et): return dm>dt
    if is_pow(em) and is_pow(et): return dm>dt
    if is_gas(et): return True
    # Materials with T_POW trait should fall through liquids
    if (ET.get(em,0) & T_POW) and is_liq(et):
        return dm > dt
    # Materials with T_LIQ trait but not in LIQUIDS set
    if (ET.get(em,0) & T_LIQ) and (ET.get(et,0) & T_LIQ):
        return dm > dt
    # Fallback: unclassified elements (materials acting as liquids/powders)
    if (is_liq(et) or is_pow(et)) and dm >= dt:
        return True
    return False

def neighbors(x,y,diag=False):
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    if diag: dirs=dirs+[(-1,-1),(1,-1),(-1,1),(1,1)]
    for dx,dy in dirs: yield x+dx,y+dy,g(x+dx,y+dy)

def has_neighbor(x,y,elems,diag=False):
    return any(n in elems for _,_,n in neighbors(x,y,diag))

def count_neighbors(x,y,elems,diag=False):
    return sum(1 for _,_,n in neighbors(x,y,diag) if n in elems)

def explode(x,y,radius,fc=0.7):
    for ex in range(-radius,radius+1):
        for ey in range(-radius,radius+1):
            if ex*ex+ey*ey<=radius*radius:
                nx,ny=x+ex,y+ey
                if ib(nx,ny) and grid[ny][nx]!=WALL and random.random()<fc:
                    s(nx,ny,FIRE)
    add_temp(x, y, 100)

def explode_themo(x,y,radius):
    for ex in range(-radius,radius+1):
        for ey in range(-radius,radius+1):
            if ex*ex+ey*ey<=radius*radius:
                nx,ny=x+ex,y+ey
                if ib(nx,ny) and grid[ny][nx]!=WALL:
                    r=random.random()
                    if r<0.3: s(nx,ny,MOLTEN_METAL)
                    elif r<0.6: s(nx,ny,FIRE)
                    elif r<0.8: s(nx,ny,PLASMA)
    add_temp(x, y, 150)


# ─── Movement Primitives ─────────────────────────────────────────────────────
def try_fall(x,y,e):
    if y < GH-1 and can_disp(e,g(x,y+1)): sw(x,y,x,y+1); return True
    dirs=[-1,1]; random.shuffle(dirs)
    for dx in dirs:
        nx=x+dx
        if y < GH-1 and ib(nx,y+1) and can_disp(e,g(nx,y+1)): sw(x,y,nx,y+1); return True
    return False

def try_spread(x,y,e,dist=4):
    dirs=[-1,1]; random.shuffle(dirs)
    for dx in dirs:
        for d in range(1,dist+1):
            nx=x+dx*d; t=g(nx,y)
            if not ib(nx, y): break
            if t==e: continue
            if can_disp(e,t): sw(x,y,nx,y); return True
            if t==EMPTY: break
            break
    return False

def try_rise(x,y,e):
    if y > 0 and can_disp(e,g(x,y-1)): sw(x,y,x,y-1); return True
    dirs=[-1,1]; random.shuffle(dirs)
    for dx in dirs:
        nx=x+dx
        if y > 0 and ib(nx,y-1) and can_disp(e,g(nx,y-1)): sw(x,y,nx,y-1); return True
    for dx in dirs:
        nx=x+dx
        if ib(nx,y) and can_disp(e,g(nx,y)): sw(x,y,nx,y); return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# REACTION ENGINE — Declarative, priority-based, condition-aware
# ═══════════════════════════════════════════════════════════════════════════════
#
# Architecture:
#   ReactionEngine stores reactions in indexed lookup tables:
#     _specific[(elem, neighbor)]  -> list of (priority, chance, cond_fn, handler_fn)
#     _trait_rules                 -> list of (priority, chance, trait_mask_req, trait_mask_nbr, handler_fn)
#     _state_rules                 -> list of (priority, chance, temp_range, moist_range, elem_set, handler_fn)
#
# Processing order per cell:
#   1. state_rules  — temperature/moisture conditional (auto-ignition, evaporation, frost)
#   2. specific     — exact element pair reactions (O(1) lookup)
#   3. trait_rules  — bit-flag universal rules (flammable+heat, toxic+living, etc.)
#   4. Physics      — movement (fall/spread/rise) or element-specific behavior
#
# Each rule has a priority (0=highest). Within same priority, random order.
# Conditions can check: temperature, moisture, neighbor counts, specific elements.
# ═══════════════════════════════════════════════════════════════════════════════

class ReactionEngine:
    def __init__(self):
        # (elem, neighbor) -> [(priority, chance, cond_fn, handler_fn), ...]
        self._specific = defaultdict(list)
        # [(priority, chance, self_traits_req, nbr_traits_req, handler_fn), ...]
        self._trait_rules = []
        # [(priority, chance, temp_min, temp_max, moist_min, moist_max, elem_filter, handler_fn), ...]
        self._state_rules = []
        self._stats = {"specific_hits": 0, "trait_hits": 0, "state_hits": 0}

    # ─── Registration API ─────────────────────────────────────────────────
    def add(self, elem, neighbor, handler, chance=0.1, priority=5, cond=None):
        """Register a specific pairwise reaction."""
        self._specific[(elem, neighbor)].append((priority, chance, cond, handler))
        # Sort by priority (lower = higher priority)
        self._specific[(elem, neighbor)].sort(key=lambda r: r[0])

    def add_trait(self, handler, chance=0.1, priority=10,
                  self_traits=0, nbr_traits=0):
        """Register a trait-based universal reaction rule.
        self_traits: bitmask that the element must have (any bit match)
        nbr_traits: bitmask that the neighbor must have (any bit match)"""
        self._trait_rules.append((priority, chance, self_traits, nbr_traits, handler))
        self._trait_rules.sort(key=lambda r: r[0])

    def add_state(self, handler, chance=0.1, priority=8,
                  temp_min=-999, temp_max=999, moist_min=-1, moist_max=999,
                  elem_filter=None):
        """Register a state-based reaction.
        elem_filter: set of elements this applies to (None = all non-empty)."""
        self._state_rules.append((priority, chance, temp_min, temp_max,
                                  moist_min, moist_max, elem_filter, handler))
        self._state_rules.sort(key=lambda r: r[0])

    def add_sym(self, e1, e2, handler1, handler2, chance=0.1, priority=5):
        """Bidirectional reaction: e1 sees e2 -> handler1, e2 sees e1 -> handler2."""
        self.add(e1, e2, handler1, chance, priority)
        self.add(e2, e1, handler2, chance, priority)

    # ─── Batch Registration Helpers ────────────────────────────────────────
    def reg_melt(self, elem, prod, sources=HEAT_SRC, chance=1.0, priority=5):
        """Element melts to prod when adjacent to any heat source."""
        h = lambda x,y,e,nx,ny,n: (s(x,y,prod), True)[-1]
        for src in sources: self.add(elem, src, h, chance, priority)

    def reg_ignite(self, elem, sources=ALL_HEAT, chance=0.08, priority=5):
        """Element catches fire near heat/electricity."""
        self.reg_melt(elem, FIRE, sources, chance, priority)

    def reg_freeze(self, elem, prod, sources=COLD_SRC, chance=0.1, priority=5):
        """Element freezes to prod near cold sources."""
        h = lambda x,y,e,nx,ny,n: (s(x,y,prod), True)[-1]
        for src in sources: self.add(elem, src, h, chance, priority)

    def reg_kill(self, elem, sources, chance=0.02, priority=10):
        """Element dies (->EMPTY) near sources."""
        h = lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), True)[-1]
        for src in sources: self.add(elem, src, h, chance, priority)

    def reg_to_set(self, elem, neighbor_set, prod, chance=0.1, priority=5):
        """Element reacts with any element in neighbor_set."""
        h = lambda x,y,e,nx,ny,n: (s(x,y,prod), True)[-1]
        for n in neighbor_set: self.add(elem, n, h, chance, priority)

    # ─── Processing ────────────────────────────────────────────────────────
    def process(self, x, y, e, diag=False):
        """Run all reaction systems for element e at (x,y).
        Returns True if any reaction fired (skip physics).
        v4: cooldown check - cells on cooldown skip reactions."""
        if cooldown_grid[y][x] > 0:
            return False
        # Stage 0: State-based rules (temperature/moisture)
        if self._process_state(x, y, e):
            return True
        # Stage 1: Specific registered reactions
        if self._process_specific(x, y, e, diag):
            return True
        # Stage 2: Trait-based universal rules
        if self._process_traits(x, y, e, diag):
            return True
        return False

    def _process_state(self, x, y, e):
        """Check temperature/moisture state rules."""
        if e <= 0: return False
        t = get_temp(x, y)
        m = get_moist(x, y)
        for priority, chance, t_min, t_max, m_min, m_max, elem_f, handler in self._state_rules:
            if elem_f is not None and e not in elem_f: continue
            if not (t_min <= t <= t_max): continue
            if not (m_min <= m <= m_max): continue
            if random.random() < chance:
                result = handler(x, y, e)
                if result:
                    self._stats["state_hits"] += 1
                    return True
        return False

    def _process_specific(self, x, y, e, diag):
        """Process specific registered reactions for element e.
        v5: Temperature/moisture scaling — reactions are faster at extreme temps."""
        t = get_temp(x, y)
        # Scale factor: reactions accelerate at high temp, slow at very low temp
        temp_scale = 1.0
        if t > 60:
            temp_scale = 1.0 + (t - 60) / 100.0  # up to 2.4x at max temp
        elif t < -20:
            temp_scale = 0.3  # much slower when frozen
        for nx, ny, n in neighbors(x, y, diag):
            if n <= 0: continue
            rules = self._specific.get((e, n))
            if not rules: continue
            for priority, chance, cond_fn, handler in rules:
                if cond_fn and not cond_fn(x, y, e, nx, ny, n):
                    continue
                scaled_chance = min(0.95, chance * temp_scale)
                if random.random() < scaled_chance:
                    if handler(x, y, e, nx, ny, n):
                        self._stats["specific_hits"] += 1
                        return True
        return False

    def _process_traits(self, x, y, e, diag):
        """Process trait-based universal reaction rules."""
        et = ET.get(e, 0)
        # Only skip if element has no traits AND no neighbors could match
        if et == 0: return False
        for priority, chance, st_req, nt_req, handler in self._trait_rules:
            if st_req and not (et & st_req): continue
            fired = False
            for nx, ny, n in neighbors(x, y, diag):
                if n <= 0: continue
                nt = ET.get(n, 0)
                if nt_req and not (nt & nt_req): continue
                if random.random() < chance:
                    if handler(x, y, e, nx, ny, n):
                        fired = True
                        break
            if fired:
                self._stats["trait_hits"] += 1
                return True
        return False

    def count_rules(self):
        """Return (specific_count, trait_count, state_count)."""
        total_spec = sum(len(v) for v in self._specific.values())
        return total_spec, len(self._trait_rules), len(self._state_rules)


# ═══════════════════════════════════════════════════════════════════════════════
# INSTANTIATE ENGINE AND REGISTER ALL REACTIONS
# ═══════════════════════════════════════════════════════════════════════════════
RX = ReactionEngine()

# ─── Handler Factories ─────────────────────────────────────────────────────
def _to(prod):
    return lambda x,y,e,nx,ny,n: (s(x,y,prod), True)[-1]

def _nb(prod):
    return lambda x,y,e,nx,ny,n: (s(nx,ny,prod), True)[-1]

def _both(p1, p2):
    return lambda x,y,e,nx,ny,n: (s(x,y,p1), s(nx,ny,p2), True)[-1]

def _cond(cond_fn, action_fn):
    return lambda x,y,e,nx,ny,n: action_fn(x,y,e,nx,ny,n) if cond_fn(x,y,e,nx,ny,n) else False

def _explode(radius, fc=0.7):
    return lambda x,y,e,nx,ny,n: (explode(x,y,radius,fc), True)[-1]

def _smoke(r=4):
    def fn(x,y,e,nx,ny,n):
        for sx in range(-r,r+1):
            for sy in range(-r,r+1):
                if sx*sx+sy*sy<=r*r and ib(x+sx,y+sy) and empt(x+sx,y+sy) and random.random()<0.5:
                    s(x+sx,y+sy,SMOKE)
        s(x,y,EMPTY); return True
    return fn

def _emit_elec():
    def fn(x,y,e,nx,ny,n):
        for ex,ey,_ in neighbors(x,y):
            if empt(ex,ey): s(ex,ey,ELECTRICITY); break
        return True
    return fn

def _emit_elec_and_degrade():
    def fn(x,y,e,nx,ny,n):
        _emit_elec()(x,y,e,nx,ny,n)
        if random.random()<0.1: s(x,y,METAL)
        return True
    return fn

def _needs_below(*elems):
    """Condition: element below (x,y+1) is in elems."""
    return lambda x,y,e,nx,ny,n: g(x,y+1) in elems

def _temp_above(threshold):
    """Condition: cell temperature > threshold."""
    return lambda x,y,e,nx,ny,n: get_temp(x,y) > threshold

def _temp_below(threshold):
    return lambda x,y,e,nx,ny,n: get_temp(x,y) < threshold

def _moist_above(threshold):
    return lambda x,y,e,nx,ny,n: get_moist(x,y) > threshold

def _neighbor_count(elems, count, diag=False):
    """Condition: count of neighbors in elems meets threshold."""
    def cond(x,y,e,nx,ny,n):
        return count_neighbors(x,y,elems,diag) >= count
    return cond


# ═══════════════════════════════════════════════════════════════════════════════
# STATE-BASED RULES (temperature/moisture driven — NEW in v3)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Auto-ignition: flammable materials spontaneously ignite at high temperature
def _auto_ignite(x, y, e):
    # Check for oxidizer nearby — catalytic acceleration
    has_oxidizer = any(ET.get(g(ox,oy),0) & T_OXID for ox,oy,_ in neighbors(x,y))
    if has_oxidizer:
        s(x, y, FIRE)
        # Oxidizer chain: oxygen consumed in combustion
        for ox,oy,oe in neighbors(x,y):
            if oe == OXYGEN and random.random() < 0.3:
                s(ox, oy, CO2)
                break
    else:
        s(x, y, FIRE)
    return True

RX.add_state(_auto_ignite, chance=0.15, priority=2,
             temp_min=80, temp_max=999, elem_filter=FLAMMABLES)

# ── Spontaneous hydrogen combustion at lower temp (H2 is highly reactive)
RX.add_state(lambda x,y,e: (s(x,y,FIRE), True)[-1], chance=0.1, priority=2,
             temp_min=50, temp_max=999, elem_filter=frozenset([HYDROGEN]))

# ── Evaporation: water turns to steam at high temp (state-driven, no neighbor needed!)
RX.add_state(lambda x,y,e: (s(x,y,STEAM), True)[-1], chance=0.05, priority=3,
             temp_min=100, temp_max=999, elem_filter=frozenset([WATER, SALTWATER, MUD]))

# ── Ice melting at 0°C (state-driven, no direct cold source needed)
RX.add_state(lambda x,y,e: (s(x,y,WATER), True)[-1], chance=0.08, priority=3,
             temp_min=5, temp_max=999, elem_filter=frozenset([ICE]))

# ── Snow melting
RX.add_state(lambda x,y,e: (s(x,y,WATER), True)[-1], chance=0.1, priority=3,
             temp_min=2, temp_max=999, elem_filter=frozenset([SNOW]))

# ── Frost formation: high moisture + cold temp = water->ice
def _frost_form(x, y, e):
    s(x, y, ICE)
    add_moist(x, y, -30)
    return True
RX.add_state(_frost_form, chance=0.02, priority=4,
             temp_min=-999, temp_max=-5, moist_min=40, moist_max=999,
             elem_filter=frozenset([WATER]))

# ── Rust accelerates with moisture (wet rust crumbles faster)
RX.add_state(lambda x,y,e: (s(x,y,DUST), True)[-1], chance=0.003, priority=8,
             moist_min=50, moist_max=999, elem_filter=frozenset([RUST]))

# ── Wet organic decay accelerates (moisture-driven decomposition)
RX.add_state(lambda x,y,e: (s(x,y,DIRT), True)[-1], chance=0.0005, priority=8,
             moist_min=60, temp_min=20, temp_max=60,
             elem_filter=frozenset([BREAD, MEAT, CHEESE, FRUIT, HAY]))

# ── Extreme cold kills creatures (frostbite — no neighbor needed)
RX.add_state(lambda x,y,e: (s(x,y,ICE), True)[-1], chance=0.04, priority=3,
             temp_min=-999, temp_max=-30, elem_filter=CREATURES)

# ── Extreme heat kills creatures (no neighbor needed — ambient heat)
RX.add_state(lambda x,y,e: (s(x,y,ASH), True)[-1], chance=0.1, priority=3,
             temp_min=100, temp_max=999, elem_filter=CREATURES)

# ── Molten materials cool slowly over time (state-driven)
RX.add_state(lambda x,y,e: (s(x,y,GLASS), True)[-1], chance=0.006, priority=9,
             temp_min=-999, temp_max=40, elem_filter=frozenset([MOLTEN_GLASS]))
RX.add_state(lambda x,y,e: (s(x,y,METAL), True)[-1], chance=0.004, priority=9,
             temp_min=-999, temp_max=30, elem_filter=frozenset([MOLTEN_METAL]))

# ── Lava cools to stone when temp drops (state-driven self-reaction)
RX.add_state(lambda x,y,e: (s(x,y,STONE,(90,80,80)), True)[-1], chance=0.003, priority=7,
             temp_min=-999, temp_max=50, elem_filter=frozenset([LAVA]))

# ── Slime evaporates in heat (state-driven)
RX.add_state(lambda x,y,e: (s(x,y,EMPTY), True)[-1], chance=0.01, priority=6,
             temp_min=80, temp_max=999, elem_filter=frozenset([SLIME]))

# ── High humidity accelerates mushroom growth (moisture + mushroom)
def _mushroom_grow_moist(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n==EMPTY: s(nx,ny,MUSHROOM); return True
    return False
RX.add_state(_mushroom_grow_moist, chance=0.005, priority=7,
             moist_min=60, temp_min=5, temp_max=40,
             elem_filter=frozenset([MUSHROOM]))

# ── High temp + moisture: bacteria thrive (accelerated decomposition)
def _bacteria_boom(x, y, e):
    if not has_neighbor(x,y,(WATER,MUD)): return False
    for nx,ny,n in neighbors(x,y):
        if n==EMPTY and random.random()<0.3:
            s(nx,ny,BACTERIA); return True
    return False
RX.add_state(_bacteria_boom, chance=0.01, priority=7,
             temp_min=20, temp_max=50, moist_min=50,
             elem_filter=frozenset([BACTERIA]))

# ── High moisture accelerates plant growth (state-driven photosynthesis)
def _plant_moisture_growth(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n==EMPTY and random.random()<0.3:
            s(nx,ny,PLANT,(30+random.randint(0,20),140+random.randint(0,20),30))
            return True
    return False
RX.add_state(_plant_moisture_growth, chance=0.003, priority=7,
             moist_min=40, temp_min=15, temp_max=45,
             elem_filter=frozenset([PLANT]))

# ── Grass spreads in warm, moist conditions
def _grass_spread_moist(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n==DIRT and random.random()<0.3:
            s(nx,ny,GRASS,(50+random.randint(0,30),150+random.randint(0,30),20))
            return True
    return False
RX.add_state(_grass_spread_moist, chance=0.004, priority=7,
             moist_min=30, temp_min=15, temp_max=40,
             elem_filter=frozenset([GRASS]))

# ── Extreme heat evaporates ALL liquids (state-driven)
def _liquid_evaporate(x, y, e):
    s(x, y, STEAM); add_moist(x, y, -20); return True
RX.add_state(_liquid_evaporate, chance=0.04, priority=3,
             temp_min=110, temp_max=999,
             elem_filter=frozenset([MILK, HONEY, SLIME, WINE, INK]))

# ── Cold radiation: ice/LN freezes nearby water
def _cold_radiation(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n == WATER and random.random()<0.02:
            s(nx,ny,ICE); return True
    return False
RX.add_state(_cold_radiation, chance=0.01, priority=6,
             temp_min=-999, temp_max=-20,
             elem_filter=frozenset([ICE, LIQUID_NITROGEN]))

# ── Heat radiation from hot metals/conductors
def _heat_radiate(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n in (WATER,ICE,SNOW) and random.random()<0.01:
            if n == WATER: s(nx,ny,STEAM)
            elif n == ICE: s(nx,ny,WATER)
            elif n == SNOW: s(nx,ny,WATER)
            return True
    return False
RX.add_state(_heat_radiate, chance=0.005, priority=7,
             temp_min=80, temp_max=999,
             elem_filter=frozenset([METAL, STEEL, BRONZE, COPPER, GOLD, SILVER, STONE, BRICK]))

# ── Moisture + cold: frost forms on solid surfaces
def _frost_on_surface(x, y, e):
    s(x, y, ICE); add_moist(x, y, -20); return True
RX.add_state(_frost_on_surface, chance=0.008, priority=5,
             temp_min=-999, temp_max=-10, moist_min=50,
             elem_filter=frozenset([STONE, BRICK, METAL, WOOD, WIRE, GLASS]))

# ── High moisture + warm: rust crumbles faster
RX.add_state(lambda x,y,e: (s(x,y,DUST), True)[-1], chance=0.002, priority=7,
             moist_min=70, temp_min=25, temp_max=60,
             elem_filter=frozenset([RUST]))

# ── Heat accelerates radioactive decay
def _radioactive_accel(x, y, e):
    add_temp(x, y, 3)
    for nx,ny,n in neighbors(x,y):
        if n==EMPTY and random.random()<0.02:
            s(nx,ny,POISON_GAS); return True
    return False
RX.add_state(_radioactive_accel, chance=0.005, priority=6,
             temp_min=60, temp_max=999,
             elem_filter=frozenset([URANIUM, NUCLEAR_WASTE]))

# ── Worms reproduce in warm moist soil
def _worm_reproduce_state(x, y, e):
    return _spawn_near(x, y, WORM)
RX.add_state(_worm_reproduce_state, chance=0.002, priority=7,
             moist_min=50, temp_min=15, temp_max=35,
             elem_filter=frozenset([WORM]))

# ── Spontaneous food rotting in warm moist conditions
RX.add_state(lambda x,y,e: (s(x,y,DIRT), True)[-1], chance=0.0002, priority=9,
             moist_min=30, temp_min=30, temp_max=50,
             elem_filter=frozenset([MEAT, FRUIT, CHEESE]))

# ── Cold makes rubber/plastic brittle (shatter)
def _brittle_shatter(x, y, e):
    s(x, y, DUST); return True
RX.add_state(_brittle_shatter, chance=0.01, priority=4,
             temp_min=-999, temp_max=-40,
             elem_filter=frozenset([RUBBER, PLASTIC]))


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIFIC REACTIONS — organized by type
# ═══════════════════════════════════════════════════════════════════════════════

# ── 1. Phase Changes (melting/freezing with neighbor trigger) ──────────────
RX.reg_melt(SNOW, WATER)
RX.reg_melt(ICE, WATER)
RX.reg_melt(GLASS_SHARD, MOLTEN_GLASS, HEAT_SRC, 0.01)

RX.reg_freeze(WATER, ICE, COLD_SRC, 0.15)
RX.reg_freeze(SALTWATER, ICE, COLD_SRC, 0.12)
RX.reg_freeze(PLANT, ICE, COLD_SRC, 0.06)
RX.reg_freeze(GRASS, ICE, COLD_SRC, 0.06)
RX.reg_freeze(MUSHROOM, ICE, COLD_SRC, 0.06)
RX.reg_freeze(MUD, DIRT, (LIQUID_NITROGEN,), 0.04)
RX.reg_freeze(LAVA, OBSIDIAN, (LIQUID_NITROGEN,), 0.3)
RX.reg_freeze(MOLTEN_GLASS, GLASS, COLD_SRC, 1.0)
RX.reg_freeze(MOLTEN_METAL, METAL, COLD_SRC, 1.0)

# Water + Lava -> Steam + Stone (bidirectional)
RX.add_sym(WATER, LAVA,
    lambda x,y,e,nx,ny,n: (s(x,y,STEAM), s(nx,ny,STONE,(90,80,80)), True)[-1],
    lambda x,y,e,nx,ny,n: (s(x,y,STONE,(90,80,80)), s(nx,ny,STEAM), True)[-1],
    0.15)
RX.add_sym(SALTWATER, LAVA,
    lambda x,y,e,nx,ny,n: (s(x,y,STEAM), s(nx,ny,STONE,(90,80,80)), True)[-1],
    lambda x,y,e,nx,ny,n: (s(x,y,STONE,(90,80,80)), s(nx,ny,STEAM), True)[-1],
    0.15)

# Water + Fire -> Steam
RX.add_sym(WATER, FIRE, _to(STEAM), _to(STEAM), 0.3)
RX.add_sym(SALTWATER, FIRE, _to(STEAM), _to(STEAM), 0.25)
RX.add_sym(WATER, PLASMA, _to(STEAM), _to(STEAM), 0.4)

# Lava + Ice -> Water + stone
RX.add(LAVA, ICE, lambda x,y,e,nx,ny,n: (s(nx,ny,WATER), s(x,y,STONE,(90,80,80)) if random.random()<0.2 else None, True)[-1], 1.0)

# Bug 41: Fire gains heat from nearby lava
RX.add(FIRE, LAVA, lambda x,y,e,nx,ny,n: (add_temp(x,y,20), True)[-1] if random.random()<0.1 else (False,)[-1], 0.1, priority=6)

# Bug 41: Fire gains heat from nearby lava
RX.add(FIRE, LAVA, lambda x,y,e,nx,ny,n: (add_temp(x,y,20), True)[-1] if random.random()<0.1 else (False,)[-1], 0.1, priority=6)

# Lava slowly self-cools (also handled by state rule above)
RX.add(LAVA, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,OBSIDIAN), True)[-1] if random.random()<0.001 else (False,)[-1], 1.0, priority=9)

# ── 2. Dissolution / Mixing ────────────────────────────────────────────────
RX.add(SALT, WATER, _to(SALTWATER), 0.08)
RX.add(SUGAR, WATER, lambda x,y,e,nx,ny,n: (s(x,y,WATER,(180,160,100)), True)[-1], 0.05)
RX.add(WATER, DIRT, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,MUD), True)[-1], 0.008)
RX.add(CONCRETE_POWDER, WATER, _to(STONE), 0.1)
RX.add(CONCRETE_POWDER, SALTWATER, _to(STONE), 0.1)
RX.add(CONCRETE_POWDER, MUD, _to(STONE), 0.1)
RX.add(SALTWATER, ICE, lambda x,y,e,nx,ny,n: (s(nx,ny,WATER), False)[-1], 0.004)
RX.add(INK, WATER, _nb(INK), 0.03)
RX.add(INK, SALTWATER, _nb(INK), 0.03)

# ── 3. Acid Chemistry (corrosion + neutralization chains) ──────────────────
def _acid_metal(x,y,e,nx,ny,n):
    s(x,y,EMPTY); s(nx,ny,RUST)
    if empt(x,y-1): s(x,y-1,HYDROGEN)
    return True
for m in (METAL,WIRE,STEEL,BRONZE,COPPER,GOLD,SILVER):
    RX.add(ACID, m, _acid_metal, 0.04)

# Acid + Ammonia -> Salt + Water (neutralization chain!)
RX.add_sym(ACID, AMMONIA, _to(WATER), _to(SALT), 1.0)

# Acid + Rust -> dissolves completely
RX.add(ACID, RUST, _both(EMPTY, EMPTY), 0.04)

# Acid dissolves non-resistant solids (with condition: 50% chance acid consumed)
def _acid_dissolve(consume_chance=0.5):
    def fn(x,y,e,nx,ny,n):
        s(nx,ny,EMPTY)
        if random.random() < consume_chance: s(x,y,EMPTY)
        return True
    return fn
for target in (WOOD, PLANT, PLASTIC, RUBBER):
    RX.add(ACID, target, _acid_dissolve(0.5), 0.04)

# NEW: Acid + Diamond -> nothing (diamond is acid-resistant, but heat it enough...)
# NEW: Acid + Glass -> very slow etching
RX.add(ACID, GLASS, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY) if random.random()<0.002 else None, True)[-1], 0.002, priority=8)
# NEW: Acid + Obsidian -> dissolves slowly (obsidian is volcanic glass)
RX.add(ACID, OBSIDIAN, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), s(x,y,EMPTY) if random.random()<0.3 else None, True)[-1], 0.001, priority=8)

# ── 4. Combustion (flammable + heat -> fire) ───────────────────────────────
# Instant ignition
for e in [GUNPOWDER, SULFUR, PHOSPHORUS, HYDROGEN, NITROGLYCERIN]:
    RX.reg_ignite(e, ALL_HEAT, 1.0)

# Fast ignition
RX.reg_ignite(OIL, ALL_HEAT, 0.4)
RX.reg_ignite(NATURAL_GAS, ALL_HEAT, 0.5)
RX.reg_ignite(WINE, ALL_HEAT, 0.3)
RX.reg_ignite(COAL, ALL_HEAT, 0.03)
RX.reg_ignite(CHARCOAL, ALL_HEAT, 0.08)

# Oxygen + Phosphorus -> fire (spontaneous! phosphorus is pyrophoric)
RX.add(PHOSPHORUS, OXYGEN, _to(FIRE), 1.0, priority=2)
# Oxygen feeds existing fire
RX.add(OXYGEN, FIRE, _to(FIRE), 0.02)

# Hydrogen explosion chain
RX.add(HYDROGEN, FIRE, _explode(4), 1.0)
RX.add(HYDROGEN, LAVA, _explode(4), 1.0)
RX.add(HYDROGEN, ELECTRICITY, _explode(4), 1.0)

# Oxygen + Hydrogen -> Water (slow synthesis — reverse of electrolysis)
RX.add_sym(OXYGEN, HYDROGEN, _to(WATER), _to(WATER), 0.001)

# CHAIN: Neon glow (moved to gas_post)

# ── 5. Explosive Detonations ───────────────────────────────────────────────
for trig in (FIRE, LAVA, PLASMA):
    RX.add(TNT, trig, _explode(4), 0.1)

# C4: ONLY electricity/plasma
for trig in (ELECTRICITY, PLASMA):
    RX.add(C4, trig, lambda x,y,e,nx,ny,n: (explode(x,y,6,0.85), True)[-1], 0.2)

# Thermite: ONLY extreme heat
for trig in (LAVA, PLASMA, MOLTEN_METAL):
    RX.add(THERMITE, trig, lambda x,y,e,nx,ny,n: (explode_themo(x,y,3), True)[-1], 0.05)

for trig in (FIRE, LAVA, PLASMA):
    RX.add(DYNAMITE, trig, _explode(5), 0.12)

# Flash Powder
def _flash(x,y,e,nx,ny,n):
    for fx in range(-2,3):
        for fy in range(-2,3):
            if fx*fx+fy*fy<=4 and ib(x+fx,y+fy) and g(x+fx,y+fy)==EMPTY and random.random()<0.3:
                s(x+fx,y+fy,STEAM)
    explode(x,y,1,0.15); s(x,y,EMPTY); return True
for trig in (ELECTRICITY, FIRE, PLASMA):
    RX.add(FLASH_POWDER, trig, _flash, 0.2)

for trig in (FIRE, ELECTRICITY, LAVA):
    RX.add(PROPANE, trig, _explode(6), 0.15)

RX.add(PETN, ELECTRICITY, lambda x,y,e,nx,ny,n: (explode(x,y,7,0.9), True)[-1], 0.15)
RX.add(PETN, PLASMA, lambda x,y,e,nx,ny,n: (explode(x,y,7,0.9), True)[-1], 0.15)

for trig in (FIRE, LAVA, PLASMA, ELECTRICITY):
    RX.add(SMOKE_BOMB, trig, _smoke(4), 0.1)

for trig in (FIRE, LAVA, ELECTRICITY, PLASMA):
    RX.add(NITROGLYCERIN, trig, _explode(3), 1.0)

# NEW: Gunpowder + Electricity -> fire (not explosion, but ignition)
RX.add(GUNPOWDER, ELECTRICITY, _to(FIRE), 0.3)
# NEW: Flash powder + Flash powder -> chain detonation (adjacent flash powder detonates)
RX.add(FLASH_POWDER, FLASH_POWDER, _flash, 0.05, priority=3)
# NEW: Dynamite + Dynamite -> chain explosion
RX.add(DYNAMITE, FIRE, lambda x,y,e,nx,ny,n: (explode(x,y,5), True)[-1], 0.1)

# ── 6. Electricity Chemistry ───────────────────────────────────────────────
RX.add(WATER, ELECTRICITY, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,HYDROGEN if random.random()<0.5 else OXYGEN), True)[-1], 0.3)
RX.add(SALTWATER, ELECTRICITY, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,CHLORINE if random.random()<0.5 else HYDROGEN), True)[-1], 0.3)
# Water+Water does nothing (prevent self-interaction noise)
RX.add(WATER, WATER, lambda x,y,e,nx,ny,n: False, 0.0, priority=99)
RX.add(SALTWATER, SALTWATER, lambda x,y,e,nx,ny,n: False, 0.0, priority=99)
RX.add(MUD, MUD, lambda x,y,e,nx,ny,n: False, 0.0, priority=99)
RX.add(MERCURY, MERCURY, lambda x,y,e,nx,ny,n: False, 0.0, priority=99)
for _noop_e in (OIL, HONEY, INK, WINE, SLIME, LYE, SOAP, NAPALM, TAR, WAX, CHLORINE, ACID, SAND):
    RX.add(_noop_e, _noop_e, lambda x,y,e,nx,ny,n: False, 0.0, priority=99)

for wet in (WATER, SALTWATER, MUD, SLIME):
    RX.add(BATTERY, wet, _emit_elec_and_degrade(), 1.0)

for src in (FIRE, LAVA, PLASMA, NEON):
    RX.add(SOLAR_CELL, src, _emit_elec(), 0.08)

RX.add(GENERATOR, WATER, _emit_elec(), 0.02)
RX.add(GENERATOR, SALTWATER, _emit_elec(), 0.04)

# NEW: Electricity + Sand -> Glass (fulgurite formation!)
RX.add(SAND, ELECTRICITY, _nb(GLASS), 0.08, priority=6)
# CHAIN: Salt glow (moved to powder behavior)
# NEW: Electricity + Snow -> Water (resistive heating melts snow)
RX.add(SNOW, ELECTRICITY, _to(WATER), 0.2)
# NEW: Electricity + Diamond -> nothing (diamond is an insulator, not a conductor)
# NEW: Electricity + Rubber -> rubber insulates (no reaction, rubber is non-conductive)
# CHAIN: Honey caramel (moved to liquid_post)

# ── 7. Nuclear / Radioactive Chains ────────────────────────────────────────
RX.add(URANIUM, LAVA, lambda x,y,e,nx,ny,n: (s(nx,ny,PLASMA), s(x,y,OBSIDIAN), explode(x,y,3,0.5), True)[-1], 0.002)
RX.add(LAVA, URANIUM, lambda x,y,e,nx,ny,n: (s(nx,ny,PLASMA), s(x,y,OBSIDIAN), explode(x,y,3,0.5), True)[-1], 0.005)

RX.add(NUCLEAR_WASTE, WATER, _nb(STEAM), 0.03)
RX.add(NUCLEAR_WASTE, ICE, _nb(WATER), 0.03)
RX.add(NUCLEAR_WASTE, FIRE, _nb(POISON_GAS), 0.05)

# CHAIN: Nuc waste plant glow (moved to liquid_post)
# NEW: Nuclear waste + Mushroom -> toxic mushroom (becomes dangerous)
def _nuc_mushroom_mutate(x,y,e,nx,ny,n):
    s(nx,ny,MUSHROOM); cgrid[ny][nx]=(200,50,255); return True
RX.add(NUCLEAR_WASTE, MUSHROOM, _nuc_mushroom_mutate, 0.005, priority=8)
# NEW: Nuclear waste + Creature -> mutation (may die or become resistant)
RX.add(NUCLEAR_WASTE, FISH, lambda x,y,e,nx,ny,n: (s(nx,ny,JELLYFISH) if random.random()<0.01 else (s(nx,ny,EMPTY) if random.random()<0.05 else None), True)[-1], 0.01, priority=8)
# NEW: Uranium + Water -> slow heating (nuclear reactor concept)
RX.add(URANIUM, WATER, lambda x,y,e,nx,ny,n: (add_temp(x,y,5), s(nx,ny,STEAM) if random.random()<0.01 else None, False)[-1], 0.01, priority=7)

# ── 8. Chlorine / Ammonia Chemistry ────────────────────────────────────────
RX.add(CHLORINE, AMMONIA, lambda x,y,e,nx,ny,n: (explode(x,y,2,0.5), True)[-1], 1.0)
RX.add(AMMONIA, CHLORINE, lambda x,y,e,nx,ny,n: (explode(x,y,2,0.5), True)[-1], 1.0)

# NEW: Chlorine + Metal -> corrosive gas (chlorine gas formation)
RX.add(CHLORINE, METAL, lambda x,y,e,nx,ny,n: (s(nx,ny,RUST), s(x,y,EMPTY), True)[-1], 0.02, priority=6)
# NEW: Chlorine + Plant -> withered plant
RX.add(CHLORINE, PLANT, lambda x,y,e,nx,ny,n: (s(nx,ny,DIRT), True)[-1], 0.01, priority=6)
# NEW: Ammonia + Plant -> fertilized (accelerated growth)
RX.add(AMMONIA, PLANT, lambda x,y,e,nx,ny,n: (s(nx,ny,PLANT,(30+random.randint(0,30),160+random.randint(0,30),30)), True)[-1], 0.02, priority=7)

# ── 9. Plant / Biological Growth Chains ───────────────────────────────────
RX.add(SEED, WATER, _cond(
    _needs_below(DIRT, GRASS, MUD),
    lambda x,y,e,nx,ny,n: (s(x,y,PLANT,(30+random.randint(0,20),130+random.randint(0,20),30)), True)[-1]
), 0.015)

def _plant_water_grow(x,y,e,nx,ny,n):
    grew = False
    if random.random() < 0.5:
        s(nx,ny,PLANT,(20+random.randint(0,30),150+random.randint(0,30),20))
        grew = True
    if ib(x,y-1) and grid[y-1][x] == EMPTY:
        s(x,y-1,PLANT,(34+random.randint(0,20),130+random.randint(0,30),34))
        grew = True
    return grew
RX.add(PLANT, WATER, _plant_water_grow, 0.008)

RX.add(PLANT, SALTWATER, lambda x,y,e,nx,ny,n: (s(x,y,DIRT) if random.random()<0.3 else None, True)[-1], 0.003)
RX.add(GRASS, SALTWATER, lambda x,y,e,nx,ny,n: (s(x,y,DIRT) if random.random()<0.3 else None, True)[-1], 0.003)
RX.add(GRASS, WATER, _nb(GRASS), 0.01)
RX.add(GRASS, DIRT, lambda x,y,e,nx,ny,n: (s(nx,ny,GRASS,(50+random.randint(0,30),150+random.randint(0,30),20)), True)[-1], 0.004)
RX.add(CO2, PLANT, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), True)[-1], 0.002)
RX.add(CO2, FIRE, lambda x,y,e,nx,ny,n: (s(nx,ny,SMOKE), s(x,y,EMPTY), True)[-1], 0.1)

RX.add(MUSHROOM, POISON_GAS, lambda x,y,e,nx,ny,n: (s(x,y,POISON_GAS) if random.random()<0.3 else None, True)[-1], 0.01)
RX.add(MUSHROOM, NUCLEAR_WASTE, lambda x,y,e,nx,ny,n: (s(x,y,POISON_GAS) if random.random()<0.3 else None, True)[-1], 0.01)

RX.add(CLOUD, STEAM, _nb(CLOUD), 0.05)
RX.add(CLOUD, ICE, _to(WATER), 0.1)
RX.add(CLOUD, LIQUID_NITROGEN, _to(WATER), 0.1)

# NEW: Slime + Plant -> slime-covered plant (slime mold growth)
RX.add(SLIME, PLANT, lambda x,y,e,nx,ny,n: (s(nx,ny,SLIME), True)[-1], 0.003, priority=7)
# NEW: Honey + Plant -> crystallized honey (plant + sugar)
RX.add(HONEY, PLANT, lambda x,y,e,nx,ny,n: (s(x,y,SUGAR), True)[-1], 0.001, priority=8)
# NEW: Seed + Mud -> plant faster (nutrient-rich soil)
RX.add(SEED, MUD, _cond(
    _needs_below(DIRT, MUD),
    lambda x,y,e,nx,ny,n: (s(x,y,PLANT,(30+random.randint(0,20),140+random.randint(0,20),30)), True)[-1]
), 0.025, priority=5)
# NEW: Worm + DIRT -> grass nearby (ecosystem: worms aerate soil)
# Worm + DIRT interaction handled in worm AI; no reaction registration needed

# ── 10. Sulfur Special Chemistry ──────────────────────────────────────────
def _sulfur_burn(x,y,e,nx,ny,n):
    s(x,y,FIRE)
    if empt(x,y-1): s(x,y-1,POISON_GAS)
    return True
RX.add(SULFUR, FIRE, _sulfur_burn, 1.0)

# NEW: Sulfur + Copper -> tarnish (copper sulfate formation — blue-green)
def _sulfur_copper_tarnish(x,y,e,nx,ny,n):
    cgrid[ny][nx]=(50,100,180); return True
RX.add(SULFUR, COPPER, _sulfur_copper_tarnish, 0.01, priority=7)
# NEW: Sulfur + Water -> weak acid rain (slow acidification)
RX.add(SULFUR, WATER, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,ACID) if random.random()<0.1 else None, True)[-1], 0.0005, priority=9)

# ── 11. Sand -> Glass ─────────────────────────────────────────────────────
RX.add(LAVA, SAND, _nb(GLASS), 0.01)
RX.add(MOLTEN_METAL, SAND, _nb(GLASS), 0.02)

# ── 12. Molten Metal/Glass cooling ────────────────────────────────────────
RX.add(MOLTEN_GLASS, WATER, lambda x,y,e,nx,ny,n: (s(x,y,GLASS), s(nx,ny,STEAM), True)[-1], 1.0)
RX.add(MOLTEN_GLASS, SALTWATER, lambda x,y,e,nx,ny,n: (s(x,y,GLASS), s(nx,ny,STEAM), True)[-1], 1.0)
RX.add(MOLTEN_GLASS, LIQUID_NITROGEN, lambda x,y,e,nx,ny,n: (s(x,y,GLASS), s(nx,ny,STEAM), True)[-1], 1.0)
RX.add(MOLTEN_METAL, WATER, lambda x,y,e,nx,ny,n: (s(nx,ny,STEAM), explode(x,y,2,0.3), True)[-1], 0.3, priority=2)
RX.add(MOLTEN_METAL, SALTWATER, lambda x,y,e,nx,ny,n: (s(nx,ny,STEAM), explode(x,y,2,0.3), True)[-1], 0.3, priority=2)
RX.add(MOLTEN_METAL, LIQUID_NITROGEN, lambda x,y,e,nx,ny,n: (s(x,y,METAL), s(nx,ny,STEAM), set_cooldown(x,y,20), True)[-1], 0.8, priority=3)

# NEW: Molten metal + Molten metal -> combine (alloy formation!)
def _alloy_form(x,y,e,nx,ny,n):
    alloys = [(STEEL,0.3),(BRONZE,0.2),(COPPER,0.2),(GOLD,0.01),(SILVER,0.05)]
    for alloy, chance in alloys:
        if random.random() < chance:
            s(x,y,alloy); s(nx,ny,EMPTY); return True
    return False
RX.add(MOLTEN_METAL, MOLTEN_METAL, _alloy_form, 0.05, priority=5)
# NEW: Molten metal + Carbon (coal/charcoal) -> steel (steelmaking!)
def _steelmaking(x,y,e,nx,ny,n):
    s(nx,ny,EMPTY)
    s(x,y,STEEL)
    add_temp(x,y,20)
    return True
RX.add(MOLTEN_METAL, COAL, _steelmaking, 0.02, priority=5)
RX.add(MOLTEN_METAL, CHARCOAL, _steelmaking, 0.03, priority=5)

# ── 13. Food Reactions ────────────────────────────────────────────────────
RX.add(FRUIT, FRUIT, lambda x,y,e,nx,ny,n: (s(x,y,WINE), True)[-1], 0.0003)

# CHAIN: Bread sogginess (moved to food_behavior)
# CHAIN: Egg cooking (moved to food_behavior)
# CHAIN: Cheese melting (handled by existing food_behavior)
# NEW: Meat + Fire -> cooked meat (color change + smell via smoke)
def _meat_cook(x,y,e,nx,ny,n):
    cgrid[y][x]=(100,40,30); empt(x,y-1) and s(x,y-1,SMOKE); return True
RX.add(MEAT, FIRE, _meat_cook, 0.1, priority=6)
# NEW: Fruit + Fire -> caramelized fruit
def _fruit_caramelize(x,y,e,nx,ny,n):
    cgrid[y][x]=(180,80,30); return True
RX.add(FRUIT, FIRE, _fruit_caramelize, 0.08, priority=6)
# NEW: Hay + Fire -> very fast ignition (hay is extremely flammable)
RX.reg_ignite(HAY, ALL_HEAT, 0.25)

# ── 14. Electronics Activation ────────────────────────────────────────────
# CHAIN: LED neon (moved to solid_behavior)
# NEW: Sensor + Creature -> motion detection (creatures trigger sensor)
RX.add(SENSOR, FISH, _emit_elec(), 0.05, priority=6)
RX.add(SENSOR, BIRD, _emit_elec(), 0.05, priority=6)
RX.add(SENSOR, ANT, _emit_elec(), 0.03, priority=6)
# CHAIN: Magnet repel (moved to solid_behavior)
# NEW: Generator + Generator -> doubled output
RX.add(GENERATOR, GENERATOR, lambda x,y,e,nx,ny,n: (_emit_elec()(x,y,e,nx,ny,n), _emit_elec()(nx,ny,n,x,y,e), True)[-1], 0.04, priority=6)

# ── 15. Alloy Corrosion ───────────────────────────────────────────────────
RX.add(WATER, COPPER, _nb(RUST), 0.0005)
RX.add(WATER, SILVER, _nb(RUST), 0.0002)
RX.add(SALTWATER, COPPER, _nb(RUST), 0.003)
RX.add(SALTWATER, SILVER, _nb(RUST), 0.003)
RX.add(SALTWATER, STEEL, _nb(RUST), 0.003)
RX.add(SALTWATER, BRONZE, _nb(RUST), 0.003)
RX.add(COPPER, SULFUR, _nb(RUST), 0.01)
RX.add(COPPER, POISON_GAS, _nb(RUST), 0.01)
RX.add(SILVER, SULFUR, _nb(RUST), 0.01)

# NEW: Steel + Acid -> very slow corrosion (steel is resistant)
RX.add(ACID, STEEL, lambda x,y,e,nx,ny,n: (s(nx,ny,RUST), s(x,y,EMPTY) if random.random()<0.1 else None, True)[-1], 0.005, priority=7)
# NEW: Gold + Acid -> nothing (gold is inert!)
# NEW: Rust + Fire -> iron reduction (smelting reverse)
RX.add(RUST, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,METAL), True)[-1], 0.002, priority=7)
# NEW: Rust + Water -> rust spreads (oxidation chain)
RX.add(RUST, METAL, _nb(RUST), 0.002, priority=8)
RX.add(RUST, STEEL, _nb(RUST), 0.003, priority=8)
# CHAIN: Copper patina (moved to alloy_behavior)

# ── 16. NEW: Complex Multi-Step Chains ────────────────────────────────────

# CHAIN: Slime + Bacteria -> decomposition -> fertile soil -> grass
RX.add(SLIME, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,DIRT), s(nx,ny,GRASS,(50+random.randint(0,30),150+random.randint(0,30),20)), True)[-1], 0.01, priority=6)

# CHAIN: Mercury + Gold -> amalgam (gold dissolves in mercury!)
def _mercury_gold_amalgam(x,y,e,nx,ny,n):
    s(nx,ny,MERCURY); cgrid[y][x]=(200,190,60); return True
RX.add(MERCURY, GOLD, _mercury_gold_amalgam, 0.01, priority=5)

# CHAIN: Oil + Lava -> coke (carbonized oil) + more fire
RX.add(OIL, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,COAL), s(nx,ny,FIRE), True)[-1], 0.02, priority=5)

# CHAIN: Milk + Acid -> curdling (cheese formation!)
RX.add(MILK, ACID, lambda x,y,e,nx,ny,n: (s(x,y,CHEESE), s(nx,ny,WATER), True)[-1], 0.05, priority=5)

# CHAIN: Wine + Bacteria -> vinegar (acetic acid) -> acid
RX.add(WINE, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,ACID), True)[-1], 0.003, priority=6)

# CHAIN: Toxic fog (moved to gas_post)

# CHAIN: Spore + Water -> accelerated mushroom growth
RX.add(SPORE, WATER, lambda x,y,e,nx,ny,n: (s(x,y,MUSHROOM), True)[-1], 0.01, priority=5)
# Spore + Spore -> mushroom cluster
RX.add(SPORE, SPORE, lambda x,y,e,nx,ny,n: (s(x,y,MUSHROOM), True)[-1] if random.random()<0.002 else (False,)[-1], 0.001, priority=8)

# CHAIN: Dust + Water -> mud (reversible)
RX.add(DUST, WATER, lambda x,y,e,nx,ny,n: (s(x,y,MUD), True)[-1], 0.05, priority=6)
# Mud + excess water -> slowly settles to dirt
RX.add(MUD, WATER, lambda x,y,e,nx,ny,n: (s(x,y,DIRT) if random.random()<0.002 else None, True)[-1], 0.002, priority=8)

# CHAIN: Glass + Sand -> nothing (glass is already melted sand)
# CHAIN: Crystal refraction (moved to solid_behavior)

# CHAIN: Plasma + Diamond -> nothing (diamond is the toughest material)
# CHAIN: Plasma + Water -> hydrogen + oxygen (plasma electrolysis)
RX.add(PLASMA, WATER, lambda x,y,e,nx,ny,n: (s(nx,ny,HYDROGEN if random.random()<0.5 else OXYGEN), True)[-1], 0.1, priority=5)

# CHAIN: Concrete powder + Mud -> reinforced stone
RX.add(CONCRETE_POWDER, MUD, lambda x,y,e,nx,ny,n: (s(x,y,BRICK), True)[-1], 0.05, priority=5)

# CHAIN: Cactus + Water -> cactus grows
def _cactus_water_grow(x,y,e,nx,ny,n):
    if empt(x,y-1):
        s(x,y-1,CACTUS)
        return True
    return False
RX.add(CACTUS, WATER, _cactus_water_grow, 0.005, priority=7)

# CHAIN: Moss sunlight/charge glow (moved to solid_behavior)

# CHAIN: Jellyfish + Electricity -> bioluminescent burst (moved to creature AI)

# CHAIN: Termite + Metal -> nothing (termites eat wood, not metal)
# CHAIN: Bird + Fruit -> eats fruit (energy gain -> reproduce)
RX.add(BIRD, FRUIT, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), random.random()<0.05 and _spawn_near(x,y,BIRD), True)[-1], 0.03, priority=6)

# CHAIN: Worm + Plant -> compost (worm eats plant, creates fertile soil)
RX.add(WORM, PLANT, lambda x,y,e,nx,ny,n: (s(nx,ny,DIRT), random.random()<0.02 and _spawn_near(x,y,WORM), True)[-1], 0.008, priority=6)

# CHAIN: Spider + Spider -> web? (reproduction when food available)
def _spider_reproduce(x,y,e,nx,ny,n):
    if has_neighbor(x,y,ORGANIC) and random.random()<0.002:
        return _spawn_near(x,y,SPIDER)
    return False
RX.add(SPIDER, SPIDER, _spider_reproduce, 0.001, priority=8)


def _spawn_near(x, y, elem):
    """Spawn elem in an adjacent empty cell."""
    for nx, ny, _ in neighbors(x, y):
        if empt(nx, ny):
            s(nx, ny, elem)
            return True
    return False


# ── 17. Deeper Chemistry & Material Science ─────────────────────────────────

# CHAIN: Charcoal + Water -> lye (alkaline solution, historically important!)
# Lye is a strong base — it accelerates organic dissolution
def _charcoal_lye(x,y,e,nx,ny,n):
    s(x,y,EMPTY); s(nx,ny,LYE)
    cgrid[ny][nx]=(180,180,100)  # yellowish tint for lye
    return True
RX.add(CHARCOAL, WATER, _charcoal_lye, 0.001, priority=8)

# CHAIN: Oil + Fire -> sustained burn (oil burns longer, produces thick smoke)
def _oil_burn(x,y,e,nx,ny,n):
    s(x,y,FIRE)
    for dx in range(-1,2):
        if empt(x+dx,y-1) and random.random()<0.4:
            s(x+dx,y-1,SMOKE)
    return True
RX.add(OIL, FIRE, _oil_burn, 0.15, priority=4)

# CHAIN: Oil slick visual (moved to liquid_post)

# CHAIN: Oil + Bird -> bird gets oiled (dies slowly — oil kills birds)
RX.add(OIL, BIRD, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.01, priority=6)

# CHAIN: Oil + Fish -> fish suffocates (oil depletes oxygen)
RX.add(OIL, FISH, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.005, priority=6)

# CHAIN: Coal + Steam -> water gas (syngas — CO+H2, represented as natural gas)
def _coal_gasification(x,y,e,nx,ny,n):
    s(x,y,ASH); s(nx,ny,NATURAL_GAS)
    empt(x,y-1) and s(x,y-1,CO2)
    return True
RX.add(COAL, STEAM, _coal_gasification, 0.01, priority=5)

# CHAIN: Ash + Water -> lye water (alkaline)
def _ash_water(x,y,e,nx,ny,n):
    s(x,y,EMPTY); s(nx,ny,LYE,(160,170,140)); return True
RX.add(ASH, WATER, _ash_water, 0.005, priority=9)

# CHAIN: Plastic + Fire -> toxic smoke (dioxins, not just regular smoke)
def _plastic_burn_toxic(x,y,e,nx,ny,n):
    s(x,y,FIRE)
    for dx in range(-2,3):
        if empt(x+dx,y-1) and random.random()<0.5:
            s(x+dx,y-1,POISON_GAS)
    return True
RX.add(PLASTIC, FIRE, _plastic_burn_toxic, 0.12, priority=4)

# CHAIN: Rubber + Fire -> thick toxic smoke
def _rubber_burn(x,y,e,nx,ny,n):
    s(x,y,FIRE)
    for dx in range(-1,2):
        if empt(x+dx,y-1) and random.random()<0.6:
            s(x+dx,y-1,SMOKE)
    if random.random()<0.3 and empt(x,y-1):
        s(x,y-1,POISON_GAS)
    return True
RX.add(RUBBER, FIRE, _rubber_burn, 0.1, priority=4)

# CHAIN: Diamond + extreme heat -> GRAPHITE then nothing (diamond is metastable carbon)
# Only the absolute hottest sources (plasma) can begin breaking diamond bonds
RX.add(DIAMOND, PLASMA, lambda x,y,e,nx,ny,n: (s(x,y,ASH) if random.random()<0.01 else None, True)[-1], 0.01, priority=8)

# CHAIN: Glass + extreme heat -> molten glass (glass has no fixed melting point, it flows)
RX.add(GLASS, LAVA, _to(MOLTEN_GLASS), 0.005, priority=7)
RX.add(GLASS, PLASMA, _to(MOLTEN_GLASS), 0.02, priority=7)
RX.add(GLASS, MOLTEN_METAL, _to(MOLTEN_GLASS), 0.01, priority=7)

# CHAIN: Brick + extreme heat -> crumbles (thermal shock)
RX.add(BRICK, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,STONE) if random.random()<0.005 else None, True)[-1], 0.005, priority=8)

# CHAIN: Stone + Lava -> slow melting (igneous re-melting)
RX.add(STONE, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,LAVA), True)[-1], 0.003, priority=7)

# CHAIN: Obsidian + extreme heat -> lava (reverse of cooling)
RX.add(OBSIDIAN, LAVA, _to(LAVA), 0.002, priority=7)
RX.add(OBSIDIAN, PLASMA, _to(LAVA), 0.01, priority=7)

# ── 18. Ecosystem & Food Web Chains ────────────────────────────────────────

# CHAIN: Fish + Bacteria -> fish gets sick
RX.add(FISH, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY) if random.random()<0.003 else None, True)[-1], 0.003, priority=7)

# CHAIN: Ant + Food -> ants eat and carry food (bread, cheese, fruit, meat)
def _ant_eat_food(x,y,e,nx,ny,n):
    s(nx,ny,EMPTY)
    # Ants reproduce when well-fed
    if random.random()<0.02:
        _spawn_near(x,y,ANT)
    return True
for food in (BREAD, CHEESE, FRUIT, MEAT, SUGAR, HAY):
    RX.add(food, ANT, _ant_eat_food, 0.01, priority=6)

# CHAIN: Bird + BREAD -> bird eats bread
RX.add(BIRD, BREAD, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.01, priority=6)

# CHAIN: Spider + Insect food web
RX.add(SPIDER, BIRD, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY) if random.random()<0.005 else None, True)[-1], 0.005, priority=6)

# CHAIN: Bacteria + DIRT -> enriched soil (nitrogen fixation cycle)
def _bacteria_nitrogen_fix(x,y,e,nx,ny,n):
    s(nx,ny,GRASS,(50+random.randint(0,30),150+random.randint(0,30),20))
    return True
RX.add(BACTERIA, DIRT, _bacteria_nitrogen_fix, 0.003, priority=7)

# CHAIN: Jellyfish + Fish -> jellyfish stuns fish
RX.add(JELLYFISH, FISH, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.02, priority=5)

# CHAIN: Termite + WOOD -> dust + reproduce (colony growth)
def _termite_eat_wood(x,y,e,nx,ny,n):
    s(nx,ny,DUST)
    if random.random()<0.06:
        _spawn_near(x,y,TERMITE)
    return True
RX.add(TERMITE, WOOD, _termite_eat_wood, 0.02, priority=5)

# CHAIN: Worm + Mushroom -> worm eats mushroom (detritivore)
RX.add(WORM, MUSHROOM, lambda x,y,e,nx,ny,n: (s(nx,ny,DIRT), random.random()<0.01 and _spawn_near(x,y,WORM), True)[-1], 0.005, priority=6)

# CHAIN: Worm + Worm -> reproduce (when well-fed nearby)
def _worm_reproduce(x,y,e,nx,ny,n):
    if random.random()<0.003:
        return _spawn_near(x,y,WORM)
    return False
RX.add(WORM, WORM, _worm_reproduce, 0.001, priority=8)

# CHAIN: Ant + Ant -> colony expansion (when food nearby)
def _ant_reproduce(x,y,e,nx,ny,n):
    if has_neighbor(x,y,ORGANIC) and random.random()<0.003:
        return _spawn_near(x,y,ANT)
    return False
RX.add(ANT, ANT, _ant_reproduce, 0.001, priority=8)

# CHAIN: Bacteria + Meat/Food -> accelerated decomposition (pathogen)
for food in (MEAT, BREAD, CHEESE, FRUIT, EGG):
    RX.add(food, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,DIRT) if random.random()<0.01 else None, True)[-1], 0.005, priority=6)

# ── 19. Weather & Atmospheric Chains ───────────────────────────────────────

# CHAIN: Steam + cold surface -> condensation (water droplets = fog)
def _steam_condense(x,y,e,nx,ny,n):
    if get_temp(x,y) < 30:
        s(x,y,FOG)
        add_moist(x,y,10)
        return True
    return False
for cold in (ICE, LIQUID_NITROGEN):
    RX.add(STEAM, cold, _steam_condense, 0.05, priority=5)

# CHAIN: Water + high heat -> steam rises, then cools -> rain cycle
# (Already handled by state rules + cloud mechanics)

# CHAIN: Fog + heat -> evaporates (fog disperses)
RX.add(FOG, FIRE, _to(EMPTY), 0.1, priority=5)
RX.add(FOG, LAVA, _to(EMPTY), 0.2, priority=5)

# CHAIN: Cloud + Cloud -> merge (bigger cloud, more rain potential)
RX.add(CLOUD, CLOUD, lambda x,y,e,nx,ny,n: (s(x,y,CLOUD), s(nx,ny,CLOUD), False)[-1], 0.0, priority=99)

# CHAIN: CO2 + Water -> carbonic acid (very weak, represented as slight acid)
RX.add(CO2, WATER, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), add_moist(nx,ny,5), False)[-1], 0.002, priority=9)

# CHAIN: Natural gas pool + oxygen -> explosion when critical mass
def _gas_explosion_check(x,y,e,nx,ny,n):
    gas_count = count_neighbors(x,y,(NATURAL_GAS,),diag=True)
    if gas_count >= 4:
        explode(x,y,3,0.6)
        return True
    return False
RX.add(NATURAL_GAS, OXYGEN, _gas_explosion_check, 0.3, priority=3)

# CHAIN: Hydrogen pool + oxygen -> bigger explosion (H2 is more energetic)
def _h2_o2_explosion(x,y,e,nx,ny,n):
    h2_count = count_neighbors(x,y,(HYDROGEN,),diag=True)
    radius = min(8, 3 + h2_count)
    explode(x,y,radius,0.8)
    return True
RX.add(HYDROGEN, OXYGEN, _h2_o2_explosion, 0.5, priority=2)

# CHAIN: Helium + Fire -> nothing (helium is inert, fire goes out — fire extinguisher)
# (moved to helium gas_post — helium is inert, extinguishes fire)

# ── 20. Electronics & Electromagnetic Chains ───────────────────────────────

# CHAIN: Wire glow (moved to solid_behavior)

# CHAIN: Laser + Mirror (glass/crystal) -> reflected beam
def _laser_reflect(x,y,e,nx,ny,n):
    cgrid[ny][nx]=(255,50,50)
    # Find direction to laser and fire in reflected direction
    ldirs=[(-1,0),(1,0),(0,-1),(0,1)]
    ldx,ldy=random.choice(ldirs)
    for dist in range(1,20):
        lx,ly=nx+ldx*dist,ny+ldy*dist
        if not ib(lx,ly): break
        lt=g(lx,ly)
        if lt!=EMPTY:
            if lt in FLAMMABLES and random.random()<0.2: s(lx,ly,FIRE)
            break
        cgrid[ly][lx]=(255,0,0)
    return False
RX.add(LASER_E, GLASS, _laser_reflect, 0.15, priority=6)
RX.add(LASER_E, CRYSTAL, _laser_reflect, 0.2, priority=6)

# CHAIN: Solar cell + Neon -> enhanced electricity (neon lamps power solar conceptually)
RX.add(SOLAR_CELL, NEON, _emit_elec(), 0.05, priority=6)

# CHAIN: Generator + Wind (gas flow) -> more electricity
for gas in (STEAM, NATURAL_GAS, HYDROGEN, SMOKE):
    RX.add(GENERATOR, gas, _emit_elec(), 0.01, priority=7)

# CHAIN: Battery + Battery -> series circuit (more powerful output)
def _battery_series(x,y,e,nx,ny,n):
    for ex,ey,_ in neighbors(x,y):
        if empt(ex,ey):
            s(ex,ey,ELECTRICITY)
            add_temp(ex,ey,30)
            return True
    return False
RX.add(BATTERY, BATTERY, _battery_series, 0.01, priority=5)

# CHAIN: Sensor + Lava -> heat sensor triggers alarm (electricity + smoke)
def _sensor_heat_alarm(x,y,e,nx,ny,n):
    for ex,ey,_ in neighbors(x,y):
        if empt(ex,ey):
            s(ex,ey,ELECTRICITY)
            if ib(x,y-1) and empt(x,y-1): s(x,y-1,SMOKE)
            return True
    return False
RX.add(SENSOR, LAVA, _sensor_heat_alarm, 0.08, priority=5)
RX.add(SENSOR, FIRE, _sensor_heat_alarm, 0.06, priority=5)

# CHAIN: Magnet + Metal through wall -> magnetic attraction through 1 solid
def _magnet_attract_through(x,y,e,nx,ny,n):
    # Check 2 cells away in each direction for metal
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        mx,my = x+dx*2, y+dy*2
        mid_g = g(x+dx, y+dy)
        if ib(mx,my) and g(mx,my) in (METAL,STEEL,BRONZE,COPPER,GOLD,SILVER,WIRE,RUST,MERCURY):
            if mid_g in SOLIDS:  # through solid wall
                tx = mx + (1 if dx>0 else -1 if dx<0 else 0)
                ty = my + (1 if dy>0 else -1 if dy<0 else 0)
                if empt(tx,ty) and ib(tx,ty):
                    sw(mx,my,tx,ty)
                    return False
    return False
RX.add(MAGNET, STONE, _magnet_attract_through, 0.01, priority=8)
RX.add(MAGNET, BRICK, _magnet_attract_through, 0.01, priority=8)
RX.add(MAGNET, WOOD, _magnet_attract_through, 0.01, priority=8)

# ── 21. Deeper Alloys & Metallurgy ────────────────────────────────────────

# CHAIN: Bronze + extreme heat -> copper + tin vapor (decomposition)
def _bronze_decompose(x,y,e,nx,ny,n):
    s(x,y,COPPER)
    if empt(x,y-1): s(x,y-1,SMOKE)
    return True
RX.add(BRONZE, PLASMA, _bronze_decompose, 0.005, priority=7)

# CHAIN: Steel + Oxygen + Heat -> rapid rusting (accelerated oxidation)
def _steel_oxidize(x,y,e,nx,ny,n):
    if get_temp(x,y) > 40:
        s(x,y,RUST)
        s(nx,ny,CO2)
        return True
    return False
RX.add(STEEL, OXYGEN, _steel_oxidize, 0.005, priority=6)

# CHAIN: Gold + Mercury -> amalgam (reverse: gold dissolves)
# (Already have MERCURY+GOLD, add reverse registration)
def _gold_amalgam(x,y,e,nx,ny,n):
    s(x,y,MERCURY); cgrid[y][x]=(200,190,60); return True
RX.add(GOLD, MERCURY, _gold_amalgam, 0.005, priority=5)

# CHAIN: Copper + Silver (contact) -> galvanic corrosion (the less noble metal corrodes)
RX.add(COPPER, SILVER, lambda x,y,e,nx,ny,n: (s(x,y,RUST) if random.random()<0.5 else (s(nx,ny,RUST)), True)[-1], 0.001, priority=8)

# CHAIN: Molten metal + Sand -> glass (silica reduction)
RX.add(MOLTEN_METAL, SAND, _nb(MOLTEN_GLASS), 0.03, priority=6)

# CHAIN: Molten metal + Water -> steam explosion (handled above at priority 2)

# CHAIN: Molten glass + Sand -> more molten glass (dissolves silica)
RX.add(MOLTEN_GLASS, SAND, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), False)[-1], 0.005, priority=8)

# ── 22. Advanced Fire & Combustion ─────────────────────────────────────────

# CHAIN: Fire merge glow (handled in update_special)

# CHAIN: Fire + Gunpowder -> explosion (not just ignition)
def _gunpowder_detonate(x,y,e,nx,ny,n):
    explode(nx,ny,3,0.8)
    s(x,y,FIRE)
    return True
RX.add(FIRE, GUNPOWDER, _gunpowder_detonate, 0.15, priority=3)

# CHAIN: Fire + Dust -> dust explosion (real industrial hazard!)
def _dust_explosion(x,y,e,nx,ny,n):
    # Count nearby dust for chain reaction
    dust_n = count_neighbors(nx,ny,(DUST,SUGAR,FLOUR),diag=True)
    radius = min(5, 2 + dust_n)
    explode(nx,ny,radius,0.5)
    s(x,y,FIRE)
    return True
RX.add(FIRE, DUST, _dust_explosion, 0.08, priority=3)

# CHAIN: Fire + Natural gas -> backfire (fire pushes into gas pocket)
def _gas_backfire(x,y,e,nx,ny,n):
    s(nx,ny,FIRE)
    # Flash back through gas
    gas_dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    random.shuffle(gas_dirs)
    for dx,dy in gas_dirs:
        cx,cy = nx+dx,ny+dy
        if g(cx,cy)==NATURAL_GAS:
            s(cx,cy,FIRE)
    return True
RX.add(FIRE, NATURAL_GAS, _gas_backfire, 0.4, priority=3)

# CHAIN: Fire + Oil -> oil fire spreads (floating fire)
def _fire_oil(x,y,e,nx,ny,n):
    s(nx,ny,FIRE)
    if empt(nx,ny-1): s(nx,ny-1,SMOKE)
    return True
RX.add(FIRE, OIL, _fire_oil, 0.2, priority=4)

# CHAIN: Fire + Wine -> alcohol flame (blueish)
def _wine_flame(x,y,e,nx,ny,n):
    s(nx,ny,FIRE)
    cgrid[ny][nx]=(100,100,255)  # blue alcohol flame
    return True
RX.add(FIRE, WINE, _wine_flame, 0.15, priority=4)

# CHAIN: Fire + Honey -> sugar caramelizes and burns (sticky fire)
def _fire_honey(x,y,e,nx,ny,n):
    s(nx,ny,FIRE)
    if empt(nx,ny-1): s(nx,ny-1,SMOKE)
    return True
RX.add(FIRE, HONEY, _fire_honey, 0.1, priority=4)

# CHAIN: Fire + Nitroglycerin -> massive explosion (shock-sensitive!)
def _nitro_shock(x,y,e,nx,ny,n):
    explode(nx,ny,4,0.9)
    # Chain: shockwave triggers nearby explosives
    for ex,ey,ee in neighbors(nx,ny,diag=True):
        if ee in (TNT,DYNAMITE,PROPANE,GUNPOWDER) and random.random()<0.3:
            explode(ex,ey,4,0.7)
    return True
RX.add(FIRE, NITROGLYCERIN, _nitro_shock, 0.5, priority=2)

# ── 23. Exotic & Fun Interactions ─────────────────────────────────────────

# CHAIN: Clone + Void -> annihilation (matter + anti-matter)
RX.add(CLONE, VOID, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,EMPTY), True)[-1], 0.5, priority=1)

# CHAIN: Clone + Water -> clones water (infinite water source!)
def _clone_water(x,y,e,nx,ny,n):
    if empt(x,y+1): s(x,y+1,WATER); return True
    return False
RX.add(CLONE, WATER, _clone_water, 0.5, priority=1)

# CHAIN: Clone + Lava -> clones lava (dangerous!)
def _clone_lava(x,y,e,nx,ny,n):
    if empt(x,y+1): s(x,y+1,LAVA); return True
    return False
RX.add(CLONE, LAVA, _clone_lava, 0.3, priority=1)

# CHAIN: Void + Fire -> fire extinguished
RX.add(VOID, FIRE, _nb(EMPTY), 0.3, priority=2)

# CHAIN: Void + Lava -> absorbs lava
RX.add(VOID, LAVA, _nb(EMPTY), 0.3, priority=2)

# CHAIN: Void + Water -> absorbs water
RX.add(VOID, WATER, _nb(EMPTY), 0.3, priority=2)
RX.add(VOID, SALTWATER, _nb(EMPTY), 0.3, priority=2)

# CHAIN: Void + Acid -> neutralized (void absorbs everything)
RX.add(VOID, ACID, _nb(EMPTY), 0.3, priority=2)
RX.add(VOID, SMOKE, _nb(EMPTY), 0.2, priority=2)
RX.add(VOID, POISON_GAS, _nb(EMPTY), 0.2, priority=2)
RX.add(VOID, STEAM, _nb(EMPTY), 0.2, priority=2)

# CHAIN: Liquid nitrogen + Fire -> fire extinguished + nitrogen boils
# (duplicate, named function version already exists above)
RX.add(LIQUID_NITROGEN, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,CO2) if random.random()<0.3 else s(x,y,EMPTY), s(nx,ny,EMPTY), True)[-1], 0.5, priority=3)
RX.add(DRY_ICE, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,CO2), s(nx,ny,EMPTY), True)[-1], 0.8, priority=3)

# CHAIN: Liquid nitrogen + Lava -> obsidian (thermal shock vitrification)
RX.add(LIQUID_NITROGEN, LAVA, lambda x,y,e,nx,ny,n: (s(nx,ny,OBSIDIAN), s(x,y,STEAM), True)[-1], 0.1, priority=4)

# CHAIN: Liquid nitrogen + Molten Metal -> shatters (brittle transition)
def _cryo_shatter(x,y,e,nx,ny,n):
    s(nx,ny,GLASS_SHARD)
    s(x,y,STEAM)
    return True
RX.add(LIQUID_NITROGEN, MOLTEN_METAL, _cryo_shatter, 0.05, priority=4)

# CHAIN: Plasma + Ice -> steam + pressure (rapid phase change)
def _plasma_ice(x,y,e,nx,ny,n):
    s(nx,ny,STEAM)
    # Pressure wave pushes neighbors
    for dx,dy in [(-1,0),(1,0),(0,-1)]:
        px,py = nx+dx,ny+dy
        if empt(px,py):
            s(px,py,STEAM)
    return True
RX.add(PLASMA, ICE, _plasma_ice, 0.5, priority=3)

# CHAIN: Plasma + Sand -> glass (plasma vitrification)
RX.add(PLASMA, SAND, _nb(GLASS), 0.15, priority=4)

# CHAIN: Plasma + Stone -> lava (plasma melts stone)
RX.add(PLASMA, STONE, _nb(LAVA), 0.05, priority=4)

# CHAIN: Fuse + Fire -> propagating fuse (fuse transmits fire along its length)
def _fuse_burn(x,y,e,nx,ny,n):
    # Fire travels along fuse to the next fuse cell
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        fx,fy = x+dx,y+dy
        if g(fx,fy)==FUSE:
            s(fx,fy,FIRE)
            return True
    s(x,y,FIRE)
    return True
RX.add(FUSE, FIRE, _fuse_burn, 0.2, priority=3)
RX.add(FUSE, ELECTRICITY, _fuse_burn, 0.15, priority=3)

# CHAIN: Fuse + TNT -> reliable detonation (fuse-triggered explosives)
def _fuse_detonate(x,y,e,nx,ny,n):
    explode(nx,ny,4)
    s(x,y,FIRE)  # fuse continues burning
    return True
RX.add(FUSE, TNT, _fuse_detonate, 0.3, priority=2)
RX.add(FUSE, DYNAMITE, lambda x,y,e,nx,ny,n: (explode(nx,ny,5), s(x,y,FIRE), True)[-1], 0.3, priority=2)
RX.add(FUSE, FLASH_POWDER, _flash, 0.25, priority=2)
RX.add(FUSE, GUNPOWDER, lambda x,y,e,nx,ny,n: (explode(nx,ny,3,0.6), s(x,y,FIRE), True)[-1], 0.3, priority=2)

# CHAIN: Uranium + Uranium -> critical mass! (nuclear chain reaction)
def _critical_mass(x,y,e,nx,ny,n):
    u_count = count_neighbors(x,y,(URANIUM,),diag=True)
    if u_count >= 3:
        explode(x,y,8,0.95)
        # Spawn nuclear waste and plasma
        for ex,ey,ee in neighbors(x,y,diag=True):
            if ee==EMPTY:
                r=random.random()
                if r<0.3: s(ex,ey,NUCLEAR_WASTE)
                elif r<0.5: s(ex,ey,PLASMA)
                elif r<0.7: s(ex,ey,FIRE)
        return True
    return False
RX.add(URANIUM, URANIUM, _critical_mass, 0.01, priority=2)

# CHAIN: Nuclear waste intensify (moved to liquid_post — plasma part kept as reaction)

# CHAIN: Nuclear waste + Fire -> radioactive fire (Chernobyl scenario)
def _radioactive_fire(x,y,e,nx,ny,n):
    s(nx,ny,FIRE)
    # Spread radiation
    for ex,ey,ee in neighbors(x,y,diag=True):
        if ee==EMPTY and random.random()<0.1:
            s(ex,ey,POISON_GAS)
    return True
RX.add(NUCLEAR_WASTE, FIRE, _radioactive_fire, 0.02, priority=5)

# CHAIN: Infection — Poison gas + Creature = disease spread
def _poison_infect(x,y,e,nx,ny,n):
    # Creature becomes a poison gas source before dying
    s(nx,ny,POISON_GAS)
    return True
RX.add(POISON_GAS, FISH, _poison_infect, 0.01, priority=6)
RX.add(POISON_GAS, BIRD, _poison_infect, 0.008, priority=6)


# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
# V4: NEW STATE-BASED RULES
# ═══════════════════════════════════════════════════════════════════════════════

# Sugar caramelization
def _sugar_caramelize(x, y, e):
    cgrid[y][x] = (180+random.randint(0,40), 120+random.randint(0,30), 30+random.randint(0,20))
    add_moist(x, y, -5)
    return True
RX.add_state(_sugar_caramelize, chance=0.005, priority=5,
             temp_min=120, temp_max=999, elem_filter=frozenset([SUGAR]))

# Resin melts at moderate temp -> wax
RX.add_state(lambda x,y,e: (s(x,y,WAX), set_cooldown(x,y,15), True)[-1],
             chance=0.01, priority=6, temp_min=50, temp_max=999,
             elem_filter=frozenset([RESIN]))

# Dry ice sublimates to CO2
def _dry_ice_sublime(x, y, e):
    s(x, y, CO2)
    add_moist(x, y, -10)
    for nx,ny,n in neighbors(x,y):
        if n == WATER and random.random() < 0.15:
            s(nx, ny, ICE)
    return True
RX.add_state(_dry_ice_sublime, chance=0.02, priority=3,
             temp_min=-999, temp_max=-5, elem_filter=frozenset([DRY_ICE]))
RX.add_state(_dry_ice_sublime, chance=0.003, priority=8,
             temp_min=-5, temp_max=30, elem_filter=frozenset([DRY_ICE]))

# Iodine sublimates with purple vapor
def _iodine_sublime(x, y, e):
    s(x, y, POISON_GAS)
    cgrid[y][x] = (120, 50, 180)
    return True
RX.add_state(_iodine_sublime, chance=0.01, priority=4,
             temp_min=60, temp_max=999, elem_filter=frozenset([IODINE]))

# Paper yellows with age/heat
def _paper_age(x, y, e):
    cgrid[y][x] = (200+random.randint(0,30), 190+random.randint(0,20), 160+random.randint(0,20))
    return False
RX.add_state(_paper_age, chance=0.005, priority=9,
             temp_min=40, temp_max=80, elem_filter=frozenset([PAPER]))

# Flour dust explosion at high temp
def _flour_dust_explode(x, y, e):
    count = count_neighbors(x, y, (FLOUR,), diag=True)
    if count >= 3:
        radius = min(6, 2 + count)
        explode(x, y, radius, 0.6)
        return True
    return False
RX.add_state(_flour_dust_explode, chance=0.05, priority=2,
             temp_min=50, temp_max=999, elem_filter=frozenset([FLOUR]))

# Napalm burns persistently
def _napalm_burn(x, y, e):
    s(x, y, FIRE)
    set_cooldown(x, y, 30)
    add_temp(x, y, 20)
    return True
RX.add_state(_napalm_burn, chance=0.03, priority=3,
             temp_min=60, temp_max=999, elem_filter=frozenset([NAPALM]))

# Tar softens in heat
def _tar_soften(x, y, e):
    cgrid[y][x] = (50+random.randint(0,20), 40+random.randint(0,15), 35+random.randint(0,15))
    return False
RX.add_state(_tar_soften, chance=0.01, priority=8,
             temp_min=50, temp_max=999, elem_filter=frozenset([TAR]))

# Soap dissolves in high moisture
RX.add_state(lambda x,y,e: (s(x,y,EMPTY), True)[-1],
             chance=0.002, priority=7, moist_min=70, moist_max=999,
             elem_filter=frozenset([SOAP]))

# Lye corrosive spread
def _lye_spread(x, y, e):
    for nx,ny,n in neighbors(x,y):
        if n in ORGANIC and random.random() < 0.03:
            s(nx, ny, EMPTY)
            return True
    return False
RX.add_state(_lye_spread, chance=0.005, priority=6,
             moist_min=30, temp_min=15, temp_max=60,
             elem_filter=frozenset([LYE]))

# Potassium auto-ignites in moisture
def _potassium_moist_ignite(x, y, e):
    s(x, y, FIRE)
    for nx,ny,n in neighbors(x,y):
        if n == WATER and random.random() < 0.3:
            s(nx, ny, HYDROGEN)
    return True
RX.add_state(_potassium_moist_ignite, chance=0.08, priority=2,
             moist_min=20, moist_max=999, elem_filter=frozenset([POTASSIUM]))

# Calcium reacts with moisture
def _calcium_moist(x, y, e):
    s(x, y, LYE)
    for nx,ny,n in neighbors(x,y):
        if n == WATER and random.random() < 0.1:
            s(nx, ny, HYDROGEN)
    return True
RX.add_state(_calcium_moist, chance=0.01, priority=4,
             moist_min=30, moist_max=999, elem_filter=frozenset([CALCIUM]))

# Zinc corrosion in moisture
RX.add_state(lambda x,y,e: (s(x,y,RUST), True)[-1],
             chance=0.0005, priority=8, moist_min=50, moist_max=999,
             elem_filter=frozenset([ZINC]))

# Coke burns very hot and long
def _coke_burn(x, y, e):
    s(x, y, FIRE)
    add_temp(x, y, 40)
    set_cooldown(x, y, 20)
    return True
RX.add_state(_coke_burn, chance=0.01, priority=3,
             temp_min=80, temp_max=999, elem_filter=frozenset([COKE]))


# ═══════════════════════════════════════════════════════════════════════════════
# V4: NEW SPECIFIC REACTIONS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Soap & Cleaning ───────────────────────────────────────────────
def _soap_clean_oil(x,y,e,nx,ny,n):
    s(nx,ny,SOAP)
    cgrid[ny][nx]=(200,190,160)
    set_cooldown(x,y,10)
    return True
RX.add(SOAP, OIL, _soap_clean_oil, 0.03, priority=5)
RX.add(SOAP, TAR, _soap_clean_oil, 0.02, priority=5)
RX.add(SOAP, MUD, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,WATER), True)[-1], 0.02, priority=5)
RX.add(SOAP, INK, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), s(nx,ny,WATER,(100,100,140)), True)[-1], 0.01, priority=6)

# ── Lye Chemistry ──────────────────────────────────────────────────
def _saponification(x,y,e,nx,ny,n):
    s(x, y, SOAP); s(nx, ny, EMPTY)
    return True
RX.add(LYE, OIL, _saponification, 0.01, priority=4)
RX.add(OIL, LYE, _saponification, 0.01, priority=4)
RX.add(LYE, MEAT, _to(SOAP), 0.005, priority=5)
RX.add(LYE, CHEESE, _to(SOAP), 0.005, priority=5)
RX.add(LYE, WOOD, lambda x,y,e,nx,ny,n: (s(nx,ny,PAPER if random.random()<0.3 else EMPTY), True)[-1], 0.002, priority=6)
def _lye_metal(x,y,e,nx,ny,n):
    s(nx,ny,RUST)
    if empt(x,y-1): s(x,y-1,HYDROGEN)
    add_temp(x,y,15)
    return True
RX.add(LYE, METAL, _lye_metal, 0.005, priority=5)
RX.add(LYE, PLANT, lambda x,y,e,nx,ny,n: (s(nx,ny,DIRT), True)[-1], 0.008, priority=5)
def _lye_acid_neutralize(x,y,e,nx,ny,n):
    s(x, y, SALT); s(nx, ny, WATER); add_temp(x, y, 30)
    return True
RX.add(LYE, ACID, _lye_acid_neutralize, 0.1, priority=3)
RX.add(ACID, LYE, _lye_acid_neutralize, 0.1, priority=3)
# Lye + extreme heat -> boils away
RX.add(LYE, FIRE, _to(EMPTY), 0.05, priority=5)
RX.add(LYE, LAVA, _to(EMPTY), 0.1, priority=5)
RX.add(LYE, PLASMA, _to(EMPTY), 0.2, priority=5)

# ── Wax Chemistry ──────────────────────────────────────────────────
def _wax_candle(x,y,e,nx,ny,n):
    s(x, y, FIRE); set_cooldown(x, y, 25)
    return True
RX.add(WAX, FIRE, _wax_candle, 0.05, priority=4)
RX.add(WAX, LYE, lambda x,y,e,nx,ny,n: (s(x,y,SOAP), s(nx,ny,EMPTY), True)[-1], 0.005, priority=5)
RX.reg_freeze(WAX, WAX, (ICE, LIQUID_NITROGEN, DRY_ICE), 0.03)  # Bug 20: hardens in place

# ── Resin Chemistry ────────────────────────────────────────────────
def _resin_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE); set_cooldown(x, y, 15)
    for dx in range(-1,2):
        if empt(x+dx,y-1) and random.random()<0.5: s(x+dx, y-1, SMOKE)
    return True
RX.add(RESIN, FIRE, _resin_burn, 0.06, priority=4)
RX.add(RESIN, LAVA, _to(GLASS), 0.01, priority=6)
RX.add(RESIN, PLASMA, _to(GLASS), 0.02, priority=6)

# ── Paper Chemistry ────────────────────────────────────────────────
def _paper_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE); empt(x,y-1) and s(x,y-1,ASH)
    set_cooldown(x, y, 5)
    return True
RX.add(PAPER, FIRE, _paper_burn, 0.2, priority=4)
RX.add(PAPER, LAVA, _paper_burn, 0.3, priority=4)
RX.add(PAPER, WATER, lambda x,y,e,nx,ny,n: (s(x,y,MUD), True)[-1], 0.005, priority=6)
def _paper_ink(x,y,e,nx,ny,n):
    cgrid[y][x]=(30+random.randint(0,20),30+random.randint(0,20),40+random.randint(0,20))
    return False
RX.add(PAPER, INK, _paper_ink, 0.05, priority=8)
RX.add(ACID, PAPER, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), s(x,y,EMPTY) if random.random()<0.3 else None, True)[-1], 0.03, priority=5)

# ── Flour & Baking ─────────────────────────────────────────────────
RX.add(FLOUR, WATER, lambda x,y,e,nx,ny,n: (s(x,y,MUD,(220,200,160)), True)[-1], 0.03, priority=5)
RX.reg_ignite(FLOUR, ALL_HEAT, 0.05)
RX.add(FLOUR, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,BREAD), s(nx,ny,EMPTY), True)[-1], 0.001, priority=5)
RX.add(FLOUR, EGG, lambda x,y,e,nx,ny,n: (s(x,y,BREAD,(230,210,160)), True)[-1], 0.005, priority=5)
RX.add(FLOUR, SUGAR, lambda x,y,e,nx,ny,n: (s(x,y,BREAD,(210,190,130)), True)[-1], 0.003, priority=6)

# ── Coke ───────────────────────────────────────────────────────────
def _coke_clean_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE); add_temp(x, y, 50); set_cooldown(x, y, 30); s(nx, ny, CO2)
    return True
RX.add(COKE, OXYGEN, _coke_clean_burn, 0.02, priority=4)
RX.add(COKE, STEAM, _coal_gasification, 0.03, priority=4)
RX.add(COKE, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,ASH), add_temp(nx,ny,30), True)[-1], 0.01, priority=5)

# ── Napalm ─────────────────────────────────────────────────────────
RX.add(NAPALM, WATER, lambda x,y,e,nx,ny,n: (s(nx,ny,STEAM), add_temp(x,y,10), False)[-1], 0.01, priority=7)
RX.add(NAPALM, SAND, _nb(GLASS), 0.005, priority=7)
RX.add(NAPALM, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,FIRE), add_temp(x,y,50), set_cooldown(x,y,40), True)[-1], 0.1, priority=3)
RX.add(NAPALM, METAL, _nb(MOLTEN_METAL), 0.002, priority=6)

# ── Dry Ice ────────────────────────────────────────────────────────
def _dryice_water(x,y,e,nx,ny,n):
    s(x, y, CO2); add_temp(nx, ny, -15)
    if random.random() < 0.15: s(nx, ny, ICE)
    else: s(nx, ny, SALTWATER)
    return True
RX.add(DRY_ICE, WATER, _dryice_water, 0.1, priority=3)
RX.add(DRY_ICE, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,CO2), s(nx,ny,OBSIDIAN), add_temp(x,y,-30), True)[-1], 0.15, priority=3)
RX.add(DRY_ICE, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,CO2), s(nx,ny,EMPTY), True)[-1], 0.8, priority=3)
RX.add(DRY_ICE, MOLTEN_METAL, lambda x,y,e,nx,ny,n: (s(nx,ny,GLASS_SHARD), s(x,y,CO2), True)[-1], 0.05, priority=4)
RX.add(DRY_ICE, MOLTEN_GLASS, lambda x,y,e,nx,ny,n: (s(x,y,CO2), s(nx,ny,GLASS), True)[-1], 0.3, priority=3)

# ── Iodine ──────────────────────────────────────────────────────────
def _iodine_water(x,y,e,nx,ny,n):
    s(x, y, EMPTY); cgrid[ny][nx]=(80,60,60)
    return True
RX.add(IODINE, WATER, _iodine_water, 0.01, priority=6)
def _iodine_flame(x,y,e,nx,ny,n):
    s(x, y, FIRE); cgrid[y][x]=(150,50,200)
    return True
RX.add(IODINE, FIRE, _iodine_flame, 0.15, priority=4)
def _iodine_starch(x,y,e,nx,ny,n):
    cgrid[ny][nx]=(20,20,80)
    return True
RX.add(IODINE, FLOUR, _iodine_starch, 0.1, priority=6)
RX.add(IODINE, PAPER, _iodine_starch, 0.1, priority=6)
RX.add(IODINE, BREAD, _iodine_starch, 0.1, priority=6)

# ── Tar ────────────────────────────────────────────────────────────
def _tar_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE); set_cooldown(x, y, 30)
    for dx in range(-2,3):
        if empt(x+dx,y-1) and random.random()<0.5:
            s(x+dx, y-1, SMOKE if random.random()<0.7 else POISON_GAS)
    return True
RX.add(TAR, FIRE, _tar_burn, 0.08, priority=4)
RX.add(TAR, SAND, lambda x,y,e,nx,ny,n: (s(x,y,STONE,(40,35,35)), s(nx,ny,EMPTY), True)[-1], 0.005, priority=6)
def _tar_water_slick(x,y,e,nx,ny,n):
    cgrid[ny][nx]=(40,35,35)
    return False
RX.add(TAR, WATER, _tar_water_slick, 0.01, priority=9)
RX.add(TAR, BIRD, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.05, priority=5)
RX.add(TAR, ANT, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.03, priority=5)
RX.add(TAR, SPIDER, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.03, priority=5)

# ── Zinc ───────────────────────────────────────────────────────────
def _zinc_acid(x,y,e,nx,ny,n):
    s(x, y, EMPTY); empt(x,y-1) and s(x,y-1, HYDROGEN)
    return True
RX.add(ZINC, ACID, _zinc_acid, 0.02, priority=5)
RX.add(ZINC, COPPER, lambda x,y,e,nx,ny,n: (s(x,y,RUST), s(nx,ny,COPPER), True)[-1], 0.001, priority=8)
def _zinc_galvanize(x,y,e,nx,ny,n):
    for ox,oy,on in neighbors(x,y):
        if on == RUST and random.random()<0.05:
            s(ox, oy, STEEL); return True
    return False
RX.add(ZINC, ELECTRICITY, _zinc_galvanize, 0.05, priority=6)
RX.reg_melt(ZINC, MOLTEN_METAL, (LAVA, PLASMA, MOLTEN_METAL), 0.01)

# ── Potassium (EXTREMELY reactive!) ────────────────────────────────
def _potassium_water_explode(x,y,e,nx,ny,n):
    s(x, y, FIRE); s(nx, ny, HYDROGEN); add_temp(x, y, 60)
    for ex in range(-1,2):
        for ey in range(-1,2):
            if ex*ex+ey*ey<=1 and ib(x+ex,y+ey) and empt(x+ex,y+ey):
                s(x+ex, y+ey, STEAM)
    return True
RX.add(POTASSIUM, WATER, _potassium_water_explode, 0.3, priority=2)
RX.add(POTASSIUM, SALTWATER, _potassium_water_explode, 0.25, priority=2)
RX.reg_ignite(POTASSIUM, ALL_HEAT, 0.5)
RX.add(POTASSIUM, ACID, lambda x,y,e,nx,ny,n: (s(x,y,FIRE), s(nx,ny,WATER), add_temp(x,y,40), True)[-1], 0.2, priority=3)
RX.add(POTASSIUM, ICE, lambda x,y,e,nx,ny,n: (s(x,y,FIRE), s(nx,ny,WATER), add_temp(x,y,30), True)[-1], 0.15, priority=3)
RX.add(POTASSIUM, OXYGEN, lambda x,y,e,nx,ny,n: (s(x,y,FIRE), True)[-1], 0.01, priority=2)
RX.add(POTASSIUM, CHLORINE, lambda x,y,e,nx,ny,n: (explode(x,y,2,0.5), True)[-1], 0.2, priority=2)

# ── Calcium ────────────────────────────────────────────────────────
def _calcium_water(x,y,e,nx,ny,n):
    s(x, y, LYE); empt(x,y-1) and s(x,y-1, HYDROGEN); add_temp(x, y, 15)
    return True
RX.add(CALCIUM, WATER, _calcium_water, 0.05, priority=4)
RX.add(CALCIUM, SALTWATER, _calcium_water, 0.04, priority=4)
RX.add(CALCIUM, ACID, lambda x,y,e,nx,ny,n: (s(x,y,STONE), s(nx,ny,WATER), add_temp(x,y,20), True)[-1], 0.05, priority=4)
def _calcium_flame(x,y,e,nx,ny,n):
    s(x, y, FIRE); cgrid[y][x]=(255,120,30)
    return True
RX.add(CALCIUM, FIRE, _calcium_flame, 0.2, priority=4)
RX.reg_melt(CALCIUM, MOLTEN_METAL, (LAVA, PLASMA), 0.02)

# ── New Cross-Element Reactions ───────────────────────────────────
def _mercury_silver(x,y,e,nx,ny,n):
    s(nx, ny, MERCURY); cgrid[y][x] = (190, 190, 200)
    return True
RX.add(MERCURY, SILVER, _mercury_silver, 0.008, priority=5)
RX.add(MERCURY, COPPER, _mercury_silver, 0.005, priority=5)
RX.add(CHLORINE, WATER, lambda x,y,e,nx,ny,n: (s(x,y,ACID), s(nx,ny,EMPTY), True)[-1], 0.002, priority=6)
RX.add(AMMONIA, FIRE, _to(FIRE), 0.05, priority=4)
RX.add(AMMONIA, LAVA, _to(FIRE), 0.08, priority=4)
def _ammonia_co2_fertilize(x,y,e,nx,ny,n):
    s(x, y, EMPTY)
    for ox,oy,on in neighbors(x,y):
        if on in (PLANT, GRASS) and random.random()<0.1:
            cgrid[oy][ox]=(30+random.randint(0,30),170+random.randint(0,30),30)
    return True
RX.add(AMMONIA, CO2, _ammonia_co2_fertilize, 0.005, priority=7)
def _neon_merge(x,y,e,nx,ny,n):
    cgrid[y][x]=(255,random.randint(100,200),random.randint(150,255))
    cgrid[ny][nx]=(255,random.randint(100,200),random.randint(150,255))
    return False
RX.add(NEON, NEON, _neon_merge, 0.01, priority=9)
def _helium_lift(x,y,e,nx,ny,n):
    if n in POWDERS and random.random()<0.01:
        if ib(nx,ny-1) and grid[ny-1][nx]==EMPTY: sw(nx,ny,nx,ny-1)
    return False
RX.add(HELIUM, SNOW, _helium_lift, 0.01, priority=8)
RX.add(HELIUM, DUST, _helium_lift, 0.01, priority=8)
RX.add(HELIUM, ASH, _helium_lift, 0.005, priority=8)
RX.reg_ignite(INK, (FIRE, LAVA), 0.1)
def _ink_bleach(x,y,e,nx,ny,n):
    cgrid[y][x]=(200,200,200)
    return False
RX.add(INK, CHLORINE, _ink_bleach, 0.02, priority=7)
RX.add(CONCRETE_POWDER, ACID, _acid_dissolve(0.3), 0.02, priority=6)
RX.add(GLASS_SHARD, FIRE, _to(MOLTEN_GLASS), 0.002, priority=7)
RX.add(GLASS_SHARD, LAVA, _to(MOLTEN_GLASS), 0.01, priority=6)
RX.add(ACID, BRICK, lambda x,y,e,nx,ny,n: (s(nx,ny,STONE) if random.random()<0.002 else None, True)[-1], 0.002, priority=8)
RX.add(CHARCOAL, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,COKE), True)[-1], 0.01, priority=5)
RX.add(COAL, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,COKE), True)[-1], 0.005, priority=5)
RX.add(SNOW, SALT, lambda x,y,e,nx,ny,n: (s(x,y,WATER), True)[-1], 0.05, priority=5)
RX.add(ICE, SALT, lambda x,y,e,nx,ny,n: (s(x,y,WATER), True)[-1], 0.03, priority=5)
def _salt_flame(x,y,e,nx,ny,n):
    cgrid[y][x]=(255,200,50)
    return False
RX.add(SALT, FIRE, _salt_flame, 0.1, priority=9)
def _plant_photosynthesis(x,y,e,nx,ny,n):
    if random.random() < 0.002:
        for ox,oy,_ in neighbors(x,y):
            if empt(ox,oy): s(ox,oy,OXYGEN); break
    return False
RX.add(PLANT, WATER, _plant_photosynthesis, 0.005, priority=10)
RX.add(BIRD, SPIDER, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.02, priority=5)
def _fruit_ferment(x,y,e,nx,ny,n):
    s(x, y, WINE); s(nx, ny, EMPTY)
    return True
RX.add(FRUIT, BACTERIA, _fruit_ferment, 0.002, priority=5)
# Bacteria colony growth (slow reproduction without water)
RX.add(BACTERIA, BACTERIA, lambda x,y,e,nx,ny,n: (_spawn_near(x,y,BACTERIA) if random.random()<0.001 else None, True)[-1], 0.001, priority=8)
def _meat_rot(x,y,e,nx,ny,n):
    s(x, y, DIRT); empt(x,y-1) and s(x,y-1, POISON_GAS)
    return True
RX.add(MEAT, BACTERIA, _meat_rot, 0.003, priority=5)
RX.add(EGG, BIRD, lambda x,y,e,nx,ny,n: (s(nx,ny,BIRD), True)[-1], 0.005, priority=5)
def _dynamite_chain(x,y,e,nx,ny,n):
    explode(x, y, 5); explode(nx, ny, 5)
    return True
RX.add(DYNAMITE, DYNAMITE, _dynamite_chain, 0.01, priority=2)
def _propane_o2(x,y,e,nx,ny,n):
    p_count = count_neighbors(x, y, (PROPANE,), diag=True)
    radius = min(8, 4 + p_count)
    explode(x, y, radius, 0.8)
    return True
RX.add(PROPANE, OXYGEN, _propane_o2, 0.2, priority=2)
RX.add(BATTERY, ELECTRICITY, lambda x,y,e,nx,ny,n: (explode(x,y,2,0.4), True)[-1], 0.005, priority=4)
def _electromagnet(x,y,e,nx,ny,n):
    magnetic = (METAL,MERCURY,STEEL,BRONZE,COPPER,GOLD,SILVER,WIRE,RUST,ZINC)
    cgrid[y][x]=(220,50,50)
    for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
        mx,my = x+dx, y+dy
        if ib(mx,my) and g(mx,my) in magnetic:
            tdx = 1 if dx>0 else (-1 if dx<0 else 0)
            tdy = 1 if dy>0 else (-1 if dy<0 else 0)
            tx, ty = mx+tdx, my+tdy
            if empt(tx,ty) and (tx!=x or ty!=y):
                sw(mx,my,tx,ty); break
    return False
RX.add(MAGNET, ELECTRICITY, _electromagnet, 0.15, priority=5)
def _laser_amplify(x,y,e,nx,ny,n):
    cgrid[y][x]=(255,0,0); cgrid[ny][nx]=(255,0,0)
    ldx,ldy = random.choice([(-1,0),(1,0),(0,-1),(0,1)])
    for dist in range(1,80):
        lx,ly = x+ldx*dist, y+ldy*dist
        if not ib(lx,ly): break
        lt = g(lx,ly)
        if lt != EMPTY:
            if lt in FLAMMABLES: s(lx,ly,FIRE)
            break
        if dist < 79: cgrid[ly][lx] = (255,50,50)
    return False
RX.add(LASER_E, LASER_E, _laser_amplify, 0.02, priority=5)
RX.add(SENSOR, PLASMA, _sensor_heat_alarm, 0.1, priority=5)
RX.add(SENSOR, MOLTEN_METAL, _sensor_heat_alarm, 0.06, priority=5)
RX.add(CLONE, PLANT, lambda x,y,e,nx,ny,n: (empt(x,y+1) and s(x,y+1,PLANT), True)[-1], 0.3, priority=1)
RX.add(CLONE, METAL, lambda x,y,e,nx,ny,n: (empt(x,y+1) and s(x,y+1,METAL), True)[-1], 0.3, priority=1)
RX.add(CLONE, SAND, lambda x,y,e,nx,ny,n: (empt(x,y+1) and s(x,y+1,SAND), True)[-1], 0.3, priority=1)
# (moved to uranium solid_behavior)
RX.add(NUCLEAR_WASTE, STEEL, lambda x,y,e,nx,ny,n: (s(nx,ny,RUST) if random.random()<0.002 else None, True)[-1], 0.002, priority=8)
RX.add(PLASMA, RUBBER, lambda x,y,e,nx,ny,n: (s(nx,ny,FIRE), True)[-1], 0.1, priority=4)
RX.add(PLASMA, PLASTIC, lambda x,y,e,nx,ny,n: (s(nx,ny,POISON_GAS), True)[-1], 0.1, priority=4)
def _silver_tarnish(x,y,e,nx,ny,n):
    cgrid[y][x]=(80,80,90)
    return True
RX.add(SILVER, SULFUR, _silver_tarnish, 0.005, priority=7)
RX.add(ACID, MOSS, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.02, priority=6)
def _cactus_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE); empt(x,y-1) and s(x,y-1, STEAM)
    return True
RX.add(CACTUS, FIRE, _cactus_burn, 0.03, priority=5)
RX.add(SEED, GRASS, _cond(
    _needs_below(DIRT, MUD, GRASS),
    lambda x,y,e,nx,ny,n: (s(x,y,PLANT,(30+random.randint(0,20),140+random.randint(0,20),30)), True)[-1]
), 0.01, priority=6)
RX.add(HONEY, BACTERIA, lambda x,y,e,nx,ny,n: (s(x,y,WINE,(180,140,40)), s(nx,ny,EMPTY), True)[-1], 0.001, priority=6)
RX.add(SLIME, FIRE, _to(FIRE), 0.05, priority=5)
def _mushroom_burn(x,y,e,nx,ny,n):
    s(x, y, FIRE)
    for dx in range(-1,2):
        if empt(x+dx,y-1) and random.random()<0.3: s(x+dx, y-1, SPORE)
    return True
RX.add(MUSHROOM, FIRE, _mushroom_burn, 0.05, priority=5)

# ── 24. V5: New Chemistry Chains ──────────────────────────────────────────────

# CHAIN: Sand + Water + Plant → accelerated growth (wet sand = fertile)
RX.add(SAND, WATER, lambda x,y,e,nx,ny,n: (add_moist(x,y,5), False)[-1], 0.01, priority=9, cond=lambda x,y,e,nx,ny,n: False)

# CHAIN: Water + Lava + Sand → obsidian + steam (geological process)
def _lava_sand_water(x,y,e,nx,ny,n):
    # Lava sees water and sand nearby -> obsidian formation
    for sx,sy,sn in neighbors(x,y):
        if sn == SAND and random.random()<0.02:
            s(sx,sy,OBSIDIAN)
            s(x,y,STONE)
            empt(x,y-1) and s(x,y-1,STEAM)
            return True
    return False
RX.add(LAVA, WATER, _lava_sand_water, 0.005, priority=7)

# CHAIN: Diamond + Diamond -> crystal growth (diamond lattice)
def _diamond_grow(x,y,e,nx,ny,n):
    for cx,cy,cn in neighbors(x,y):
        if cn==EMPTY and random.random()<0.001:
            s(cx,cy,DIAMOND); return True
    return False
RX.add(DIAMOND, DIAMOND, _diamond_grow, 0.001, priority=9)

# CHAIN: Glass + Glass -> crystal (slow devitrification)
def _glass_devitrify(x,y,e,nx,ny,n):
    if random.random()<0.001:
        s(x,y,CRYSTAL)
    return False
RX.add(GLASS, GLASS, _glass_devitrify, 0.001, priority=9)

# CHAIN: Crystal + Crystal -> larger crystal cluster
def _crystal_cluster(x,y,e,nx,ny,n):
    for cx,cy,cn in neighbors(x,y):
        if cn==EMPTY and random.random()<0.002:
            s(cx,cy,CRYSTAL); return True
    return False
RX.add(CRYSTAL, CRYSTAL, _crystal_cluster, 0.001, priority=9)

# CHAIN: Oil + Oil -> tar (polymerization over time)
RX.add(OIL, OIL, lambda x,y,e,nx,ny,n: (s(x,y,TAR), True)[-1], 0.0003, priority=9)

# CHAIN: Smoke acid rain (moved to gas_post)

# CHAIN: Gas pool heating (moved to gas_post)

# CHAIN: Mercury shimmer (moved to liquid_post)

# CHAIN: Stone + Acid -> sand (chemical weathering)
RX.add(ACID, STONE, lambda x,y,e,nx,ny,n: (s(nx,ny,SAND), s(x,y,EMPTY) if random.random()<0.3 else None, True)[-1], 0.002, priority=7)

# CHAIN: Brick + LYE -> crumbles (base attacks cement)
RX.add(LYE, BRICK, lambda x,y,e,nx,ny,n: (s(nx,ny,STONE) if random.random()<0.003 else None, True)[-1], 0.003, priority=7)

# CHAIN: Napalm + Napalm -> bigger napalm pool
RX.add(NAPALM, NAPALM, lambda x,y,e,nx,ny,n: (add_temp(x,y,5), add_temp(nx,ny,5), False)[-1], 0.01, priority=9, cond=lambda x,y,e,nx,ny,n: False)

# CHAIN: Neon merge brightness (moved to gas_post)

# CHAIN: Water + Plant + Sunlight (neon/fire acts as sun) -> O2 + growth
def _photosynthesis_boost(x,y,e,nx,ny,n):
    s(x,y,OXYGEN)
    # Grow plant taller
    if empt(nx,ny-1):
        s(nx,ny-1,PLANT,(30+random.randint(0,20),150+random.randint(0,30),30))
    return True
RX.add(NEON, PLANT, _photosynthesis_boost, 0.002, priority=7)

# CHAIN: Dry ice + Lye -> frozen lye (cryogenic base)
RX.add(DRY_ICE, LYE, lambda x,y,e,nx,ny,n: (s(nx,ny,STONE,(180,180,140)), s(x,y,CO2), True)[-1], 0.02, priority=4)

# CHAIN: Potassium + Chlorine -> salt (classic synthesis)
def _k_cl_synthesis(x,y,e,nx,ny,n):
    s(x, y, SALT); s(nx, ny, EMPTY); add_temp(x, y, 40)
    return True
RX.add(POTASSIUM, CHLORINE, _k_cl_synthesis, 0.1, priority=2)

# CHAIN: Calcium + Acid -> gypsum + water + CO2
def _calcium_acid(x,y,e,nx,ny,n):
    s(x, y, STONE); s(nx, ny, WATER)
    empt(x,y-1) and s(x,y-1,CO2)
    return True
RX.add(CALCIUM, ACID, _calcium_acid, 0.03, priority=4)

# CHAIN: Zinc + Sulfur -> zinc sulfide (glow!)
def _zinc_sulfide(x,y,e,nx,ny,n):
    s(nx, ny, EMPTY)
    cgrid[y][x]=(150, 200, 100)  # zinc sulfide phosphorescence
    add_temp(x, y, 10)
    return True
RX.add(ZINC, SULFUR, _zinc_sulfide, 0.01, priority=5)

# CHAIN: Ink + Fire -> burns away
RX.add(INK, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,SMOKE), True)[-1], 0.15, priority=5)

# CHAIN: Paper + Oil -> oil-soaked paper (very flammable)
def _paper_oil(x,y,e,nx,ny,n):
    cgrid[y][x]=(60,50,30)
    # Oil-soaked paper is much more flammable (handled by trait system)
    return False
RX.add(PAPER, OIL, _paper_oil, 0.02, priority=8)

# CHAIN: Resin + Water -> amber (fossilization, very slow)
RX.add(RESIN, WATER, lambda x,y,e,nx,ny,n: (s(x,y,CRYSTAL,(200,180,50)) if random.random()<0.0005 else None, True)[-1], 0.0005, priority=9)


# ── 25. v6: New Reaction Chains ──────────────────────────────────────────

# Cloud + cold source -> snow (precipitation)
def _cloud_snow(x,y,e,nx,ny,n):
    if empt(x,y+1): s(x,y+1,SNOW); return True
    return False
RX.add(CLOUD, ICE, _cloud_snow, 0.008, priority=5)
RX.add(CLOUD, LIQUID_NITROGEN, _cloud_snow, 0.01, priority=5)
RX.add(CLOUD, DRY_ICE, _cloud_snow, 0.006, priority=5)

# Cloud + heat -> accelerated rain
RX.add(CLOUD, FIRE, lambda x,y,e,nx,ny,n: (s(x,y,WATER) if random.random()<0.3 else None, True)[-1], 0.1, priority=4)
RX.add(CLOUD, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,STEAM) if random.random()<0.3 else None, True)[-1], 0.15, priority=4)

# Spider + Fruit -> spider eats fruit
RX.add(SPIDER, FRUIT, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), random.random()<0.01 and _spawn_near(x,y,SPIDER), True)[-1], 0.02, priority=6)

# Spider + Worm -> spider eats worm
RX.add(SPIDER, WORM, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.015, priority=6)

# Acid + Sand -> slow dissolving (chemical weathering)
RX.add(ACID, SAND, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), s(x,y,EMPTY) if random.random()<0.3 else None, True)[-1], 0.003, priority=7)

# Acid + Gravel -> dissolves
RX.add(ACID, GRAVEL, lambda x,y,e,nx,ny,n: (s(nx,ny,SAND), s(x,y,EMPTY) if random.random()<0.2 else None, True)[-1], 0.003, priority=7)

# Bread + moderate heat -> toast (color change)
def _bread_toast(x,y,e,nx,ny,n):
    if get_temp(x,y) > 50 and get_temp(x,y) < 120:
        cgrid[y][x]=(180,140,80); return True
    return False
RX.add(BREAD, FIRE, _bread_toast, 0.05, priority=6)
RX.add(BREAD, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,ASH), True)[-1], 0.1, priority=4)

# Egg + heat -> cooked egg
def _egg_cook(x,y,e,nx,ny,n):
    cgrid[y][x]=(240,240,230); return True
RX.add(EGG, FIRE, _egg_cook, 0.03, priority=6)
RX.add(EGG, ICE, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), True)[-1], 0.003, priority=7)
RX.add(EGG, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,ASH), True)[-1], 0.08, priority=4)

# Cheese + heat -> melted cheese
def _cheese_melt(x,y,e,nx,ny,n):
    cgrid[y][x]=(240,210,80); return True
RX.add(CHEESE, FIRE, _cheese_melt, 0.05, priority=6)

# Smoke accumulation (smoke + smoke -> darker, thicker)
def _smoke_accum(x,y,e,nx,ny,n):
    sr,sg,sb = cgrid[y][x]; cgrid[y][x]=(max(0,sr-10),max(0,sg-10),max(0,sb-10)); return False
RX.add(SMOKE, SMOKE, _smoke_accum, 0.01, priority=9)

# Water + Gravel -> natural sediment (gravel settles, water clears)
RX.add(GRAVEL, WATER, lambda x,y,e,nx,ny,n: (add_moist(x,y,5), False)[-1], 0.01, priority=9)

# Honey + Water -> diluted honey (mead precursor)
def _honey_dilute(x,y,e,nx,ny,n):
    cgrid[y][x]=(200,170,60); return False
RX.add(HONEY, WATER, _honey_dilute, 0.002, priority=9)

# Lye + Fruit -> saponification
RX.add(LYE, FRUIT, lambda x,y,e,nx,ny,n: (s(nx,ny,SOAP), s(x,y,EMPTY), True)[-1], 0.003, priority=5)

# Wax + Oil -> candle wax (thickened)
def _wax_oil_thicken(x,y,e,nx,ny,n):
    cgrid[y][x]=(200,180,100); return False
RX.add(WAX, OIL, lambda x,y,e,nx,ny,n: (_wax_oil_thicken(x,y,e,nx,ny,n) if random.random()<0.3 else False), 0.005, priority=8)

# Resin + Fire -> burns with thick smoke and bright flame
def _resin_fire(x,y,e,nx,ny,n):
    s(x,y,FIRE); set_cooldown(x,y,20); add_temp(x,y,30)
    for dx in range(-1,2):
        if empt(x+dx,y-1) and random.random()<0.6: s(x+dx,y-1,SMOKE)
    return True
RX.add(RESIN, FIRE, _resin_fire, 0.08, priority=4)

# Napalm + Fire -> intensified burn (napalm IS fire fuel)
def _napalm_fire(x,y,e,nx,ny,n):
    s(x,y,FIRE); set_cooldown(x,y,40); add_temp(x,y,30)
    if empt(x,y-1) and random.random()<0.4: s(x,y-1,SMOKE)
    return True
RX.add(NAPALM, FIRE, _napalm_fire, 0.15, priority=3)

# Chlorine gas + Water -> acid rain (gas dissolves)
def _chlorine_dissolve_water(x,y,e,nx,ny,n):
    s(x,y,EMPTY); cgrid[ny][nx]=(40,110,50)  # slightly greenish water
    return True
RX.add(CHLORINE, WATER, _chlorine_dissolve_water, 0.01, priority=6)
RX.add(CHLORINE, SALTWATER, _chlorine_dissolve_water, 0.008, priority=6)

# Concrete powder + Sand -> reinforced (stronger concrete)
RX.add(CONCRETE_POWDER, SAND, lambda x,y,e,nx,ny,n: (s(x,y,BRICK), s(nx,ny,EMPTY), True)[-1], 0.02, priority=6)
# Concrete powder hardens slowly in moisture
RX.add(CONCRETE_POWDER, CONCRETE_POWDER, lambda x,y,e,nx,ny,n: (s(x,y,STONE) if get_moist(x,y)>30 and random.random()<0.001 else None, True)[-1], 0.001, priority=8)

# Glass shard + Acid -> slow etching
RX.add(ACID, GLASS_SHARD, lambda x,y,e,nx,ny,n: (s(nx,ny,SAND) if random.random()<0.003 else None, True)[-1], 0.003, priority=8)

# Fish + Worm -> fish eats worm (fishing!)
RX.add(FISH, WORM, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), random.random()<0.02 and _spawn_near(x,y,FISH), True)[-1], 0.008, priority=5)
# Fish eat small food particles in water
for food in (BREAD, FRUIT, MEAT, CHEESE):
    RX.add(food, FISH, lambda x,y,e,nx,ny,n: (s(x,y,EMPTY), True)[-1], 0.005, priority=6)

# Bird + Worm -> bird eats worm
RX.add(BIRD, WORM, lambda x,y,e,nx,ny,n: (s(nx,ny,EMPTY), True)[-1], 0.015, priority=5)

# Ant + Spider -> ants swarm and kill spider (if enough ants)
def _ant_swarm_spider_v2(x,y,e,nx,ny,n):
    ant_count = count_neighbors(nx, ny, (ANT,), diag=True)
    if ant_count >= 3: s(nx, ny, EMPTY); return True
    return False
# (override the old one)
RX.add(ANT, SPIDER, _ant_swarm_spider_v2, 0.01, priority=5)

# Steam + cold -> water condensation (improved)
def _steam_rain(x,y,e,nx,ny,n):
    if random.random() < 0.15:
        if empt(x,y+1): s(x,y+1,WATER)
        else: s(x,y,FOG)
        return True
    return False
RX.add(STEAM, ICE, _steam_rain, 0.03, priority=5)
RX.add(STEAM, STONE, _steam_rain, 0.01, priority=6)

# Lava + Lava -> obsidian formation (slow cooling at contact)
RX.add(LAVA, LAVA, lambda x,y,e,nx,ny,n: (s(x,y,OBSIDIAN) if random.random()<0.002 else None, True)[-1], 0.002, priority=8)

# Nuclear waste + Nuclear waste -> criticality (rare)
def _waste_critical(x,y,e,nx,ny,n):
    w_count = count_neighbors(x,y,(NUCLEAR_WASTE,),diag=True)
    if w_count >= 5 and random.random()<0.01:
        explode(x,y,3,0.5)
        for ex,ey,ee in neighbors(x,y,diag=True):
            if ee==EMPTY:
                r=random.random()
                if r<0.4: s(ex,ey,PLASMA)
                elif r<0.7: s(ex,ey,FIRE)
        return True
    return False
RX.add(NUCLEAR_WASTE, NUCLEAR_WASTE, _waste_critical, 0.005, priority=3)


# TRAIT-BASED UNIVERSAL REACTION RULES
# ═══════════════════════════════════════════════════════════════════════════════

def _trait_flammable_heat(x, y, e, nx, ny, n):
    """FLAMMABLE + HEAT -> Fire (universal combustion)."""
    has_oxidizer = any(ET.get(g(ox,oy),0) & T_OXID for ox,oy,_ in neighbors(x,y))
    c = 0.24 if has_oxidizer else 0.08
    if random.random() < c:
        s(x, y, FIRE)
        if has_oxidizer:
            for ox,oy,oe in neighbors(x,y):
                if oe == OXYGEN and random.random() < 0.3:
                    s(ox, oy, CO2)
                    break
        return True
    return False

def _trait_live_toxic(x, y, e, nx, ny, n):
    if random.random() < 0.02: s(x, y, EMPTY); return True
    return False

def _trait_live_heat(x, y, e, nx, ny, n):
    if random.random() < 0.4: s(x, y, EMPTY); return True
    return False

def _trait_live_elec(x, y, e, nx, ny, n):
    # Only trigger near actual electricity or plasma
    if n in (ELECTRICITY, PLASMA) and random.random() < 0.15:
        s(x, y, EMPTY); return True
    return False

def _trait_live_cryo(x, y, e, nx, ny, n):
    if random.random() < 0.03: s(x, y, ICE); return True
    return False

def _trait_org_cryo(x, y, e, nx, ny, n):
    if random.random() < 0.06: s(x, y, ICE); return True
    return False

def _trait_org_corr(x, y, e, nx, ny, n):
    if random.random() < 0.01: s(x, y, EMPTY); return True
    return False

def _trait_radio_org(x, y, e, nx, ny, n):
    if random.random() < 0.008: s(nx, ny, ASH); return True
    return False

def _trait_radio_live(x, y, e, nx, ny, n):
    if random.random() < 0.005: s(nx, ny, ASH); return True
    return False

def _trait_radio_water(x, y, e, nx, ny, n):
    if n in (WATER, SALTWATER, MUD, SLIME, MILK) and random.random() < 0.005:
        s(nx, ny, STEAM)
        add_temp(x, y, 5)
        return True
    return False

def _trait_heat_cond(x, y, e, nx, ny, n):
    if random.random() < 0.01: s(nx, ny, MOLTEN_METAL)
    return False

# Register trait rules with priorities
RX.add_trait(_trait_flammable_heat, chance=1.0, priority=5,
             self_traits=T_FLAM, nbr_traits=T_HEAT)
RX.add_trait(_trait_live_toxic, chance=1.0, priority=6,
             self_traits=T_LIVE, nbr_traits=T_TOXIC)
RX.add_trait(_trait_live_heat, chance=1.0, priority=4,
             self_traits=T_LIVE, nbr_traits=T_HEAT)
RX.add_trait(_trait_live_elec, chance=1.0, priority=6,
             self_traits=T_LIVE, nbr_traits=0)  # v6: nbr_traits=0, handler checks for actual elec/plasma
RX.add_trait(_trait_live_cryo, chance=1.0, priority=7,
             self_traits=T_LIVE, nbr_traits=T_CRYO)
RX.add_trait(_trait_org_cryo, chance=1.0, priority=7,
             self_traits=T_ORG, nbr_traits=T_CRYO)
RX.add_trait(_trait_org_corr, chance=1.0, priority=8,
             self_traits=T_ORG, nbr_traits=T_CORR)
RX.add_trait(_trait_radio_org, chance=1.0, priority=9,
             self_traits=T_RADIO, nbr_traits=T_ORG)
RX.add_trait(_trait_radio_live, chance=1.0, priority=9,
             self_traits=T_RADIO, nbr_traits=T_LIVE)
RX.add_trait(_trait_radio_water, chance=1.0, priority=9,
             self_traits=T_RADIO, nbr_traits=0)  # water check in handler
RX.add_trait(_trait_heat_cond, chance=1.0, priority=8,
             self_traits=T_HEAT, nbr_traits=T_COND)

# -- V4: New Trait Rules --
def _trait_expl_heat(x, y, e, nx, ny, n):
    if random.random() < 0.08:
        explode(x, y, 4, 0.6)
        return True
    return False
RX.add_trait(_trait_expl_heat, chance=1.0, priority=3,
             self_traits=T_EXPL, nbr_traits=T_HEAT)

def _trait_flam_oxy(x, y, e, nx, ny, n):
    if random.random() < 0.005:
        s(x, y, FIRE)
        return True
    return False
RX.add_trait(_trait_flam_oxy, chance=1.0, priority=6,
             self_traits=T_FLAM, nbr_traits=T_OXID)

def _trait_corr_cond(x, y, e, nx, ny, n):
    if ET.get(n, 0) & T_COND and random.random() < 0.002:
        s(nx, ny, RUST)
        return True
    return False
RX.add_trait(_trait_corr_cond, chance=1.0, priority=8,
             self_traits=T_CORR, nbr_traits=T_COND)

def _trait_toxic_live(x, y, e, nx, ny, n):
    if random.random() < 0.005:
        s(nx, ny, EMPTY)
        return True
    return False
RX.add_trait(_trait_toxic_live, chance=1.0, priority=7,
             self_traits=T_TOXIC, nbr_traits=T_LIVE)

def _trait_mag_cond(x, y, e, nx, ny, n):
    if random.random() < 0.003:
        for ex, ey, _ in neighbors(x, y):
            if empt(ex, ey):
                s(ex, ey, ELECTRICITY)
                break
        return False
    return False
RX.add_trait(_trait_mag_cond, chance=1.0, priority=8,
             self_traits=T_MAG, nbr_traits=T_COND)


# ═══════════════════════════════════════════════════════════════════════════════
# ELECTRICITY PROPAGATION
# ═══════════════════════════════════════════════════════════════════════════════
def propagate_electricity(x, y):
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]; random.shuffle(dirs)
    moved_to = False

    # Superconductor check: alloy + cryo nearby
    is_super = False
    for ax, ay, an in neighbors(x, y):
        if an in ALLOY_S and has_neighbor(ax, ay, CRYOGENIC):
            is_super = True; break

    # Priority 1: conductors
    for dx,dy in dirs:
        nx,ny=x+dx,y+dy; n=g(nx,ny)
        if n in CONDUCTIVE and not moved[ny][nx]:
            sw(x,y,nx,ny); moved_to=True; break

    # Priority 2: arc to empty
    if not moved_to:
        arc_chance = 0.4 if is_super else 0.2
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if g(nx,ny)==EMPTY and random.random()<arc_chance:
                sw(x,y,nx,ny); moved_to=True; break

    # Priority 3: discharge effects
    if not moved_to:
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy; n=g(nx,ny)
            # v6: Electricity creates visible arc trail
            if n==EMPTY and random.random()<0.08:
                cgrid[ny][nx]=(150,180,255)
            if n==WATER:
                s(nx,ny,HYDROGEN if random.random()<0.5 else OXYGEN)
                s(x,y,EMPTY); return
            if n==SALTWATER:
                s(nx,ny,CHLORINE if random.random()<0.5 else HYDROGEN)
                s(x,y,EMPTY); return
            if n in (METAL,STEEL,BRONZE,COPPER,GOLD,SILVER) and random.random()<0.03:
                s(nx,ny,MOLTEN_METAL)
            if n==WIRE and random.random()<0.005:
                s(nx,ny,FIRE)
            if n==SAND and random.random()<0.08:
                s(nx,ny,GLASS); s(x,y,EMPTY)
            if n in FLAMMABLES and random.random()<0.2:
                s(nx,ny,FIRE)
            if n in (TNT,DYNAMITE,PROPANE,THERMITE) and random.random()<0.15:
                explode(nx,ny,4); s(x,y,EMPTY); return
            if n==C4:
                explode(nx,ny,6,0.85); s(x,y,EMPTY); return
            if n==PETN:
                explode(nx,ny,7,0.9); s(x,y,EMPTY); return
            if n==GUNPOWDER: s(nx,ny,FIRE)
            if n==FLASH_POWDER:
                for fx in range(-2,3):
                    for fy in range(-2,3):
                        if fx*fx+fy*fy<=4 and ib(nx+fx,ny+fy) and g(nx+fx,ny+fy)==EMPTY and random.random()<0.3:
                            s(nx+fx,ny+fy,STEAM)
                explode(nx,ny,1,0.15); s(x,y,EMPTY); return
            if n==SMOKE_BOMB:
                _smoke(4)(nx,ny,n,x,y,n); s(x,y,EMPTY); return
            if n==BATTERY and random.random()<0.15:
                explode(nx,ny,2,0.3); return
            if n==LED and random.random()<0.3:
                cgrid[ny][nx]=(random.randint(100,255),random.randint(100,255),random.randint(100,255))
            if n==LASER_E and random.random()<0.4:
                ldirs=[(-1,0),(1,0),(0,-1),(0,1)]
                ldx,ldy=random.choice(ldirs)
                for dist in range(1,40):
                    lx,ly=nx+ldx*dist,ny+ldy*dist
                    if not ib(lx,ly): break
                    lt=g(lx,ly)
                    if lt!=EMPTY:
                        if lt in FLAMMABLES and random.random()<0.3: s(lx,ly,FIRE)
                        elif lt in CONDUCTIVE and random.random()<0.02: s(lx,ly,MOLTEN_METAL)
                        elif lt==ICE: s(lx,ly,WATER)
                        break
                    if dist<39: cgrid[ly][lx]=(255,0,0)
            if n==MAGNET: cgrid[ny][nx]=(220,50,50)

    fade = 0.0 if is_super else 0.1
    if not moved_to and random.random()<fade:
        s(x,y,EMPTY)


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE FUNCTIONS — Physics only; reactions handled by ReactionEngine
# ═══════════════════════════════════════════════════════════════════════════════

def update_powder(x, y, e):
    if RX.process(x, y, e, diag=True): return
    try_fall(x, y, e)


def update_liquid(x, y, e):
    if RX.process(x, y, e, diag=True): return
    if can_disp(e, g(x,y+1)):
        sw(x,y,x,y+1)
    else:
        dirs=[-1,1]; random.shuffle(dirs); fell=False
        for dx in dirs:
            if can_disp(e,g(x+dx,y+1)): sw(x,y,x+dx,y+1); fell=True; break
        if not fell:
            sp = {HONEY:2, OIL:3, WINE:3, NITROGLYCERIN:3, INK:3,
                  WATER:5, ACID:5, MERCURY:5, SALTWATER:5, LIQUID_NITROGEN:5,
                  CHLORINE:4, NUCLEAR_WASTE:3, SOAP:4, LYE:4, WAX:2, NAPALM:3, TAR:2, MUD:3,
                  MILK:4, SLIME:3, MOLTEN_GLASS:1, MOLTEN_METAL:1}.get(e, 4)
            try_spread(x, y, e, sp)
    _liquid_post(x, y, e)


def _liquid_post(x, y, e):
    if e == LAVA:
        v = random.randint(0,40)
        cgrid[y][x] = (min(255,207+v//2), min(255,50+v), 20)
        for nx,ny,n in neighbors(x,y):
            if n==SNOW: s(nx,ny,WATER)
            if n==SULFUR and random.random()<0.05:
                s(nx,ny,FIRE)
                if empt(nx,ny-1): s(nx,ny-1,POISON_GAS)
    elif e == MUD:
        if random.random()<0.002: s(x,y,DIRT)
    elif e == MOLTEN_GLASS:
        if random.random()<0.008: s(x,y,GLASS)
    elif e == MOLTEN_METAL:
        for nx,ny,n in neighbors(x,y):
            if n==WIRE and random.random()<0.01: s(nx,ny,MOLTEN_METAL)
        if random.random()<0.005: s(x,y,METAL)
    elif e == MILK:
        if random.random()<0.0005: cgrid[y][x]=(230,220,180)
    elif e == MERCURY:
        n=g(x,y+1)
        if n in LIQUIDS and n!=MERCURY: sw(x,y,x,y+1)
        # v6: Mercury shimmer
        if random.random()<0.03:
            cgrid[y][x]=(180+random.randint(0,20),190+random.randint(0,10),200+random.randint(0,20))
    elif e == PROPANE:
        if random.random()<0.005:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY: s(nx,ny,NATURAL_GAS); break
    elif e == NUCLEAR_WASTE:
        gv=random.randint(0,30); cgrid[y][x]=(50+gv,200+gv//2,50+gv)
        if random.random()<0.001: s(x,y,POISON_GAS)
        # v5: Glow plants (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n==PLANT and random.random()<0.01: cgrid[ny][nx]=(50,255,50)
        # v5: Mutual heating (moved from reaction engine — plasma part)
        for nx,ny,n in neighbors(x,y):
            if n==NUCLEAR_WASTE:
                add_temp(x,y,3); add_temp(nx,ny,3)
                if random.random()<0.001: s(x,y,PLASMA)
                break
    # v6: Mercury shimmer (merged from duplicate block)
    elif e == INK:
        for nx,ny,n in neighbors(x,y):
            if n in (WOOD,PLANT,GRASS,MUSHROOM) and random.random()<0.01:
                cgrid[ny][nx]=(20,15,25)
    elif e == HONEY:
        # v5: Caramel from electricity (moved from reaction engine)
        if has_neighbor(x,y,(ELECTRICITY,)) and random.random()<0.05:
            cgrid[y][x]=(180,120,40)
    elif e == OIL:
        # v5: Oil slick visual on water (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (WATER,SALTWATER) and random.random()<0.01:
                cgrid[ny][nx]=(60,80,30)
    elif e == SOAP:
        if random.random()<0.003: cgrid[y][x]=(220,220,210)
    elif e == WAX:
        if random.random()<0.01: cgrid[y][x]=(240+random.randint(0,10),230+random.randint(0,10),180+random.randint(0,10))


def update_gas(x, y, e):
    if RX.process(x, y, e, diag=False): return
    try_rise(x, y, e)
    _gas_post(x, y, e)


def _gas_post(x, y, e):
    if e == STEAM:
        if random.random()<0.003: s(x,y,WATER)
        # Bug 54: Steam condenses faster near cold surfaces
        cold_near = has_neighbor(x,y,(ICE,LIQUID_NITROGEN,DRY_ICE,STONE))
        if cold_near and random.random()<0.01: s(x,y,WATER)
        if y<=1 and random.random()<0.05: s(x,y,EMPTY)
    elif e == SMOKE:
        if random.random()<0.008: s(x,y,EMPTY)
        if y<=1 and random.random()<0.1: s(x,y,EMPTY)
        # v5: Dissolve into water (acid rain, moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (WATER,SALTWATER) and random.random()<0.002:
                s(x,y,EMPTY); cgrid[ny][nx]=(30,100,30); break
    elif e == NATURAL_GAS:
        if has_neighbor(x,y,(FIRE,LAVA,ELECTRICITY,PLASMA),diag=True) and random.random()<0.5:
            s(x,y,FIRE)
        # v5: Pool heating from nearby gas (moved from reaction engine)
        gas_n = count_neighbors(x,y,(NATURAL_GAS,),diag=True)
        if gas_n >= 3 and random.random()<0.01:
            add_temp(x,y,5)
    elif e == POISON_GAS:
        dissipate = 0.004 if y < GH // 4 else 0.002
        if random.random() < dissipate: s(x,y,EMPTY)
    elif e == CO2:
        # Bug 53: CO2 sinks first (heavier than air), then spreads
        if can_disp(e, g(x,y+1)) and not moved[y][x]:
            sw(x,y,x,y+1)
        elif not moved[y][x]:
            try_spread(x, y, e, 3)
        if random.random()<0.002: s(x,y,EMPTY)
    elif e == NEON:
        if random.random()<0.001: s(x,y,EMPTY)
        # v5: Glow from fire/electricity (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (FIRE,LAVA,PLASMA) and random.random()<0.1:
                cgrid[y][x]=(255,random.randint(50,150),random.randint(100,200))
                break
            if n==ELECTRICITY and random.random()<0.2:
                cgrid[y][x]=(255,random.randint(50,150),random.randint(100,200))
                break
        # v5: Brightness boost from nearby neon
        neon_count = count_neighbors(x,y,(NEON,),diag=True)
        if neon_count > 0:
            brightness = min(255, 150 + neon_count * 20)
            cgrid[y][x]=(brightness, random.randint(50,150), random.randint(100,200))
    elif e == CLOUD:
        # v6: Improved rain cycle — moisture-driven precipitation
        m = get_moist(x, y)
        rain_chance = 0.003 + m * 0.0003  # more moisture = more rain
        if random.random() < rain_chance:
            if empt(x,y+1):
                s(x,y+1,WATER)
            elif random.random() < 0.01:
                s(x,y,FOG)  # oversaturated cloud becomes fog
        # Cloud gains moisture from nearby water/steam
        for nx,ny,n in neighbors(x,y):
            if n in (WATER, SALTWATER, STEAM) and random.random()<0.002:
                add_moist(x,y,5)
    elif e == FOG:
        # v6: Fog disperses faster near heat, settles near cold
        near_heat = has_neighbor(x,y,(FIRE,LAVA,PLASMA,MOLTEN_METAL))
        near_cold = has_neighbor(x,y,(ICE,LIQUID_NITROGEN,DRY_ICE))
        if near_heat and random.random()<0.08: s(x,y,EMPTY); return
        if random.random()<(0.04 if near_heat else 0.02) and can_disp(e,g(x,y+1)): sw(x,y,x,y+1)
        if has_neighbor(x,y,(STONE,)) and random.random()<0.02: s(x,y,WATER)
        if random.random()<0.003: s(x,y,EMPTY)
        # Toxic fog tint from poison gas
        if has_neighbor(x,y,(POISON_GAS,)) and random.random()<0.03:
            cgrid[y][x]=(140,100,160)
    elif e == SPORE:
        below = g(x,y+1)
        if below in SOLIDS: s(x,y,MUSHROOM); return
        if random.random()<0.003: s(x,y,EMPTY)
    elif e == AMMONIA:
        if random.random()<0.002: s(x,y,EMPTY)
    elif e == HELIUM:
        if random.random()<0.001: s(x,y,EMPTY)
        # Helium is lighter than other gases — actively rises faster
        if not moved[y][x] and y > 0:
            above = g(x, y-1)
            if above in GASES and above != HELIUM and random.random() < 0.3:
                sw(x, y, x, y-1)
        # v5: Helium extinguishes fire (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n==FIRE and random.random()<0.05: s(nx,ny,EMPTY)


def update_solid(x, y, e):
    if RX.process(x, y, e, diag=False): return
    _solid_behavior(x, y, e)


def _solid_behavior(x, y, e):
    if e == PLANT:
        if random.random()<0.01:
            v=COLOR_VAR.get(PLANT,20)
            cgrid[y][x]=(30+random.randint(0,v),120+random.randint(0,v),30)
    elif e == MUSHROOM:
        wc = sum(1 for _,_,n in neighbors(x,y) if n in (WATER,SALTWATER,MUD))
        moist_ok = get_moist(x,y) > 20 or wc >= 2
        if moist_ok and random.random()<0.003:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY: s(nx,ny,MUSHROOM); break
    elif e == GRASS:
        if random.random()<0.01:
            cgrid[y][x]=(50+random.randint(0,25),150+random.randint(0,30),20+random.randint(0,10))
    elif e == CRYSTAL:
        # v5: Refraction glow from nearby light sources (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (FIRE, LAVA, PLASMA, ELECTRICITY) and random.random()<0.1:
                cgrid[y][x]=(random.randint(150,255),random.randint(150,255),random.randint(200,255))
                break
            if n == NEON and random.random()<0.08:
                cgrid[y][x]=(random.randint(200,255),random.randint(100,200),random.randint(200,255))
                break
        # Crystal growth from crystal neighbors
        if random.random()<0.001:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY: s(nx,ny,CRYSTAL); break
    elif e == FUSE:
        if has_neighbor(x,y,(FIRE,ELECTRICITY,PLASMA)) and random.random()<0.15:
            s(x,y,FIRE)
    elif e == WOOD:
        if has_neighbor(x,y,(ACID,)) and random.random()<0.005:
            s(x,y,EMPTY)
    elif e == WIRE:
        if has_neighbor(x,y,(LAVA,MOLTEN_METAL,PLASMA)):
            if random.random()<0.05: s(x,y,MOLTEN_METAL)
        # v5: Glow when electrified (moved from reaction engine)
        if has_neighbor(x,y,(ELECTRICITY,)):
            cgrid[y][x]=(255,200,100)
            if random.random()<0.002: s(x,y,FIRE)
    elif e == URANIUM:
        gv=random.randint(0,20); cgrid[y][x]=(80+gv,190+gv//2,80+gv)
        # v5: Heat nearby water (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (WATER,SALTWATER) and random.random()<0.02:
                add_temp(x,y,8)
                if random.random()<0.02: s(nx,ny,STEAM)
    elif e == MOSS:
        # Bug 55: Moss grows on more surface types near water
        moss_surfaces = (STONE, BRICK, WOOD, CACTUS)
        for nx,ny,n in neighbors(x,y):
            if n in moss_surfaces and random.random()<0.002 and has_neighbor(nx,ny,(WATER,)):
                s(nx,ny,MOSS)
            if n==WATER and random.random()<0.01: s(nx,ny,EMPTY)
        # v5: Sunlight glow from fire/neon (moved from reaction engine)
        for nx,ny,n in neighbors(x,y):
            if n in (FIRE,LAVA,PLASMA) and random.random()<0.02:
                cgrid[y][x]=(80+random.randint(0,40),180+random.randint(0,40),80)
            elif n == NEON and random.random()<0.01:
                cgrid[y][x]=(80+random.randint(0,40),160+random.randint(0,40),80)
        if has_neighbor(x,y,(FIRE,LAVA,PLASMA)):
            if random.random()<0.05: s(x,y,EMPTY)
    elif e == ICE:
        if y==0 and random.random()<0.01: s(x,y,WATER)
        for nx,ny,n in neighbors(x,y):
            if n==WATER and random.random()<0.002: s(nx,ny,ICE)
    elif e == CACTUS:
        if has_neighbor(x,y,(SAND,)) and has_neighbor(x,y,(WATER,)):
            if random.random()<0.003:
                for nx,ny,n in neighbors(x,y):
                    if n==EMPTY: s(nx,ny,CACTUS); break
        if has_neighbor(x,y,(WATER,)) and random.random()<0.001:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY: s(nx,ny,WATER); break
        # Cactus also grows upward slowly
        if not moved[y][x] and random.random() < 0.002:
            if empt(x, y-1): s(x, y-1, CACTUS)
    elif e in ALLOY_S:
        _alloy_behavior(x, y, e)


def _alloy_behavior(x, y, e):
    if e == STEEL:
        if has_neighbor(x,y,(LAVA,PLASMA,MOLTEN_METAL)):
            if random.random()<0.005: s(x,y,MOLTEN_METAL)
    elif e == BRONZE:
        if has_neighbor(x,y,(LAVA,PLASMA,MOLTEN_METAL)):
            if random.random()<0.01: s(x,y,MOLTEN_METAL)
    elif e == COPPER:
        if has_neighbor(x,y,(LAVA,PLASMA,MOLTEN_METAL)):
            if random.random()<0.02: s(x,y,MOLTEN_METAL)
        # v5: Patina formation (moved from reaction engine)
        if has_neighbor(x,y,(WATER,SALTWATER,MUD)) and random.random()<0.002:
            cgrid[y][x]=(50+random.randint(0,30),140+random.randint(0,20),80)
    elif e == GOLD:
        if has_neighbor(x,y,(LAVA,PLASMA,MOLTEN_METAL)):
            if random.random()<0.003: s(x,y,MOLTEN_METAL)
        if random.random()<0.01:
            cgrid[y][x]=(255,210+random.randint(0,30),50+random.randint(0,30))
    elif e == SILVER:
        if has_neighbor(x,y,(LAVA,PLASMA,MOLTEN_METAL)):
            if random.random()<0.015: s(x,y,MOLTEN_METAL)
        if has_neighbor(x,y,(SMOKE,)):
            if random.random()<0.002: cgrid[y][x]=(120,120,130)
    elif e == RUST:
        if random.random()<0.001: s(x,y,DUST)
        if has_neighbor(x,y,(FIRE,LAVA)):
            if random.random()<0.002: s(x,y,METAL)


def update_special(x, y, e):
    if e == FIRE:
        # v5: Multi-layer fire color based on temperature and age
        t = get_temp(x, y)
        life_frac = min(1.0, (t - 20) / 160.0)
        if life_frac > 0.7:
            # White-hot core
            cgrid[y][x] = (255, random.randint(200, 255), random.randint(150, 255))
        elif life_frac > 0.3:
            # Yellow-orange body
            cgrid[y][x] = (255, random.randint(100, 200), random.randint(0, 60))
        else:
            # Red dying embers
            cgrid[y][x] = (random.randint(180, 255), random.randint(30, 80), 0)
        add_temp(x, y, -2)  # fire cools as it burns
        # v6: Oxygen-boosted fire spread + better smoke
        has_o2 = any(g(ox,oy)==OXYGEN for ox,oy,_ in neighbors(x,y))
        spread_chance = 0.12 if has_o2 else 0.06  # oxygen doubles spread rate
        smoke_chance = 0.06 if has_o2 else 0.14  # less smoke with oxygen (cleaner burn)
        for nx,ny,n in neighbors(x,y,diag=True):
            if n in FLAMMABLES and random.random()<spread_chance:
                s(nx,ny,FIRE)
            if n==GUNPOWDER: s(nx,ny,FIRE)
            if n in (WATER,SALTWATER):
                s(x,y,STEAM); return
            if n==ICE: s(nx,ny,WATER)
            # v6: Fire preheats nearby metal/conductors
            if n in (METAL,STEEL,BRONZE,COPPER) and random.random()<0.01:
                add_temp(nx,ny,10)
        if random.random()<smoke_chance and empt(x,y-1): s(x,y-1,SMOKE)
        if random.random()<0.05:
            r_fe = random.random()
            if r_fe < 0.3: s(x,y,ASH)
            elif r_fe < 0.7: s(x,y,SMOKE)
            else: s(x,y,CO2)
            return  # Bug 48: don't move after dying
        if random.random()<0.3:
            if empt(x,y-1): sw(x,y,x,y-1)
            else:
                dirs=[-1,1]; random.shuffle(dirs)
                for dx in dirs:
                    if empt(x+dx,y-1): sw(x,y,x+dx,y-1); break

    elif e == CLONE:
        for nx,ny,n in neighbors(x,y):
            if n not in (EMPTY,CLONE,WALL,VOID,-1):
                cdirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(cdirs)
                for ddx,ddy in cdirs:
                    tx,ty = x+ddx, y+ddy
                    if empt(tx,ty): s(tx,ty,n); return

    elif e == VOID:
        # v5: Absorb all non-special neighbors (moved from 7 separate reaction registrations)
        for nx,ny,n in neighbors(x,y):
            if n not in (EMPTY,WALL,VOID,CLONE,-1) and random.random()<0.1:
                s(nx,ny,EMPTY)

    elif e == ELECTRICITY:
        # v5: Bright white-blue core with flickering
        r = random.random()
        if r < 0.3:
            cgrid[y][x] = (220+random.randint(0,35), 230+random.randint(0,25), 255)  # white core
        elif r < 0.7:
            cgrid[y][x] = (100+random.randint(0,80), 160+random.randint(0,60), 255)  # blue
        else:
            cgrid[y][x] = (180+random.randint(0,75), 120+random.randint(0,80), 255)  # purple arc
        add_temp(x, y, 5)
        propagate_electricity(x, y)

    elif e == ANT:
        _ant_ai(x, y)

    elif e == PLASMA:
        # v5: Vivid color cycling plasma with temperature-based hue
        t = get_temp(x, y)
        phase = (t * 3 + random.randint(0, 40)) % 120
        if phase < 40:
            cgrid[y][x] = (200+random.randint(0,55), 80+random.randint(0,40), 220+random.randint(0,35))
        elif phase < 80:
            cgrid[y][x] = (160+random.randint(0,60), 120+random.randint(0,60), 255)
        else:
            cgrid[y][x] = (220+random.randint(0,35), 60+random.randint(0,40), 180+random.randint(0,75))
        add_temp(x, y, -1)
        for nx,ny,n in neighbors(x,y,diag=True):
            if n in (WALL,DIAMOND,EMPTY): continue
            r=random.random()
            if n in (METAL,WIRE,BRICK,STEEL,BRONZE,COPPER,GOLD,SILVER) and r<0.15:
                s(nx,ny,MOLTEN_METAL)
            elif n in (STONE,OBSIDIAN) and r<0.08: s(nx,ny,LAVA)
            elif n in (GLASS,SAND) and r<0.1: s(nx,ny,MOLTEN_GLASS)
            elif n==ICE and r<0.5: s(nx,ny,STEAM)
            elif n in (WATER,SALTWATER,MUD,MILK,HONEY,WINE,SLIME) and r<0.3: s(nx,ny,STEAM)
            elif n in SOLIDS and r<0.1: s(nx,ny,FIRE)
            elif n in (WOOD,PLANT,GRASS,HAY,PAPER) and r<0.15: s(nx,ny,CHARCOAL)
            elif n in (WOOD,PLANT,GRASS,HAY,PAPER) and r<0.15: s(nx,ny,CHARCOAL)
            elif n in LIQUIDS and r<0.05: s(nx,ny,STEAM)
            elif n in CREATURES and r<0.3: s(nx,ny,EMPTY)
            elif n in EXPL_S:
                if r<0.2:
                    if n==THERMITE: explode_themo(nx,ny,3)
                    elif n in (DYNAMITE,PROPANE): explode(nx,ny,5)
                    elif n==PETN: explode(nx,ny,7,0.9)
        if random.random()<0.01: s(x,y,LAVA)
        if random.random()<0.2:
            if empt(x,y-1): sw(x,y,x,y-1)
            else:
                dirs=[-1,1]; random.shuffle(dirs)
                for dx in dirs:
                    if empt(x+dx,y-1): sw(x,y,x+dx,y-1); break


def _ant_ai(x, y):
    dirs=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]
    random.shuffle(dirs)
    # Bug 25: Ants prioritize moving toward food
    food_dirs = []
    for dx,dy in dirs:
        nx,ny=x+dx,y+dy; n=g(nx,ny)
        if n in ORGANIC: food_dirs.append((dx,dy,nx,ny,n))
    if food_dirs and random.random() < 0.6:
        _,_,nx,ny,n = random.choice(food_dirs)
        s(nx,ny,EMPTY)
        if random.random()<0.08:
            for ex,ey,_ in neighbors(x,y):
                if empt(ex,ey): s(ex,ey,ANT); break
        return
    moved_a=False
    for dx,dy in dirs:
        nx,ny=x+dx,y+dy; n=g(nx,ny)
        if n==EMPTY: sw(x,y,nx,ny); moved_a=True; break
        if n in POWDERS and random.random()<0.1: sw(x,y,nx,ny); moved_a=True; break
    if not moved_a:
        for nx,ny,n in neighbors(x,y):
            if n in ORGANIC and random.random()<0.02:
                s(nx,ny,EMPTY)
                if random.random()<0.1:
                    for ex,ey,_ in neighbors(x,y):
                        if empt(ex,ey): s(ex,ey,ANT); break
                break
    if has_neighbor(x,y,(SPIDER,)) and random.random()<0.05: s(x,y,EMPTY)


def update_life(x, y, e):
    if RX.process(x, y, e, diag=False): return
    _creature_ai(x, y, e)


def _creature_ai(x, y, e):
    d4=[(-1,0),(1,0),(0,-1),(0,1)]
    d8=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]
    random.shuffle(d8)

    if e == FISH:
        # v5: Fish school together and flee jellyfish
        if not has_neighbor(x,y,(WATER,SALTWATER)):
            if random.random()<0.15: s(x,y,EMPTY); return  # Bug 23: die faster on land
        # Flee from jellyfish
        jf_near = False
        for jx,jy,jn in neighbors(x,y,diag=True):
            if jn==JELLYFISH:
                jf_near = True
                # Swim away from jellyfish into water
                dx_=x-jx; dy_=y-jy
                tx=x+(1 if dx_>0 else -1 if dx_<0 else random.choice([-1,1]))
                ty=y+(1 if dy_>0 else -1 if dy_<0 else 0)
                tn=g(tx,ty)
                if tn in (WATER,SALTWATER): sw(x,y,tx,ty)
                break
        if not jf_near:
            # Seek worms (fishing!)
            worm_near = False
            for wx,wy,wn in neighbors(x,y,diag=True):
                if wn==WORM:
                    worm_near = True
                    if random.random()<0.1:
                        s(wx,wy,EMPTY)
                        if random.random()<0.03:
                            for fx,fy,_ in neighbors(x,y):
                                if empt(fx,fy) and has_neighbor(fx,fy,(WATER,SALTWATER)):
                                    s(fx,fy,FISH); break
                    break
            if not worm_near:
                # Schooling: prefer to move toward other fish
                for dx,dy in d8:
                    nx,ny=x+dx,y+dy; n=g(nx,ny)
                    if n in (WATER,SALTWATER):
                        # Check if this direction has more fish nearby
                        fish_count = count_neighbors(nx,ny,(FISH,),diag=True)
                        if fish_count > 0 or random.random()<0.3:
                            sw(x,y,nx,ny); break
        for nx,ny,n in neighbors(x,y):
            if n==BACTERIA and random.random()<0.05: s(nx,ny,EMPTY); break
        if has_neighbor(x,y,(JELLYFISH,)) and random.random()<0.03: s(x,y,EMPTY)

    elif e == BIRD:
        # v5: Birds flock together, avoid danger, seek food
        danger = has_neighbor(x,y,(FIRE,LAVA,PLASMA,POISON_GAS),diag=True)
        if danger:
            # Flee fast — move once to safe cell
            for dx,dy in d8:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n==EMPTY and not has_neighbor(nx,ny,(FIRE,LAVA,PLASMA,POISON_GAS)):
                    sw(x,y,nx,ny); break
        else:
            # Flocking: check for nearby birds and align
            flock_dir = [0, 0]
            for bx,by,bn in neighbors(x,y,diag=True):
                if bn==BIRD:
                    flock_dir[0] += (bx-x)
                    flock_dir[1] += (by-y)
            food_found = False
            # Seek food if nearby
            for dx,dy in d8:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n in (FRUIT,WORM,SPIDER,HONEY,BREAD,ANT):
                    if random.random()<0.15:
                        s(nx,ny,EMPTY); food_found = True
                        if random.random()<0.01: _spawn_near(x,y,BIRD)
                        break
            if not food_found:
                moved_b=False
                # Try flock direction first
                if abs(flock_dir[0]) + abs(flock_dir[1]) > 0:
                    fdx = 1 if flock_dir[0]>0 else -1 if flock_dir[0]<0 else 0
                    fdy = 1 if flock_dir[1]>0 else -1 if flock_dir[1]<0 else 0
                    tn=g(x+fdx,y+fdy)
                    if tn==EMPTY or tn in GASES:
                        sw(x,y,x+fdx,y+fdy); moved_b=True
                if not moved_b:
                    for dx,dy in d8:
                        nx,ny=x+dx,y+dy; n=g(nx,ny)
                        if n==EMPTY: sw(x,y,nx,ny); break
                        if n in (STEAM,SMOKE,CO2,NATURAL_GAS,OXYGEN) and random.random()<0.3:
                            sw(x,y,nx,ny); break
                        if n in LIQUIDS: break  # birds avoid liquids
        for nx,ny,n in neighbors(x,y):
            if n==FISH and random.random()<0.01: s(nx,ny,EMPTY); break
        if has_neighbor(x,y,LIQUIDS) and random.random()<0.005: s(x,y,EMPTY)

    elif e == SPIDER:
        # v5: Spiders build webs (create FUSE as web strands) and hunt
        web_count = count_neighbors(x,y,(FUSE,),diag=True)
        if web_count < 4 and random.random()<0.004:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY and not has_neighbor(nx,ny,(SPIDER,)) and has_neighbor(nx,ny,SOLIDS):
                    s(nx,ny,FUSE); break
        for dx,dy in d8:
            nx,ny=x+dx,y+dy; n=g(nx,ny)
            if n==EMPTY and (has_neighbor(nx,ny,SOLIDS) or g(nx,ny+1) in SOLIDS):
                sw(x,y,nx,ny); break
        for nx,ny,n in neighbors(x,y):
            if n==ANT and random.random()<0.08: s(nx,ny,EMPTY); break
            if n==BACTERIA and random.random()<0.03: s(nx,ny,EMPTY); break
            if n==BIRD and random.random()<0.01: s(nx,ny,EMPTY); break
            # Spider catches insects in web
            if n==FUSE:
                for wx,wy,wn in neighbors(nx,ny):
                    if wn == ANT and random.random()<0.1:
                        s(wx,wy,EMPTY); break

    elif e == BACTERIA:
        if has_neighbor(x,y,(WATER,MUD,SALTWATER)) and random.random()<0.015:
            for nx,ny,n in neighbors(x,y):
                if n==EMPTY and random.random()<0.3: s(nx,ny,BACTERIA); break
        if random.random()<0.3:
            for dx,dy in d4:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n in (WATER,MUD,SALTWATER,EMPTY): sw(x,y,nx,ny); break
        for nx,ny,n in neighbors(x,y):
            if n in (BREAD,MEAT,CHEESE,FRUIT) and random.random()<0.008: s(nx,ny,DIRT)
            if n in (WOOD,PLANT) and random.random()<0.001: s(nx,ny,DIRT)

    elif e == TERMITE:
        ate=False
        for nx,ny,n in neighbors(x,y):
            if n==WOOD and random.random()<0.02:
                s(nx,ny,DUST); ate=True
                if random.random()<0.08:
                    for ex,ey,_ in neighbors(x,y):
                        if empt(ex,ey): s(ex,ey,TERMITE); break
                break
            if n==PLANT and random.random()<0.01: s(nx,ny,DIRT); ate=True; break
        if not ate:
            for dx,dy in d8:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n==EMPTY: sw(x,y,nx,ny); break
                if n in POWDERS and random.random()<0.15: sw(x,y,nx,ny); break
        if has_neighbor(x,y,LIQUIDS) and random.random()<0.03: s(x,y,EMPTY)

    elif e == WORM:
        # v4: Worms flee predators and eat organic matter
        predator_near = has_neighbor(x,y,(BIRD,FISH))
        if predator_near and random.random()<0.05:
            for dx,dy in d4:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n in (DIRT,MUD,EMPTY) and not has_neighbor(nx,ny,(BIRD,FISH)):
                    sw(x,y,nx,ny); break
        else:
            for dx,dy in d4:
                nx,ny=x+dx,y+dy; n=g(nx,ny)
                if n in (DIRT,MUD) and random.random()<0.4: sw(x,y,nx,ny); break
                if n==EMPTY: sw(x,y,nx,ny); break
        for nx,ny,n in neighbors(x,y):
            if n in (PLANT,MUSHROOM,HAY) and random.random()<0.005:
                s(nx,ny,DIRT)
                if random.random()<0.02: _spawn_near(x,y,WORM)
                break
        if random.random()<0.005:
            for nx,ny,n in neighbors(x,y):
                if n==DIRT and random.random()<0.3: s(nx,ny,GRASS); break
        if not has_neighbor(x,y,(DIRT,MUD,WATER,PLANT,GRASS)):
            if random.random()<0.005: s(x,y,EMPTY)

    elif e == JELLYFISH:
        in_liquid = has_neighbor(x,y,LIQUIDS)
        if not in_liquid:
            if random.random()<0.01: s(x,y,EMPTY); return
        for dx,dy in d8:
            nx,ny=x+dx,y+dy; n=g(nx,ny)
            if n in LIQUIDS: sw(x,y,nx,ny); break
        if random.random()<0.1:
            for nx,ny,n in neighbors(x,y):
                if n in CREATURES and n!=JELLYFISH and random.random()<0.02:
                    s(nx,ny,EMPTY); break
        if random.random()<0.05:
            cgrid[y][x]=(200+random.randint(0,55),150+random.randint(0,50),255)


def update_explosive(x, y, e):
    if RX.process(x, y, e, diag=False): return
    try_fall(x, y, e)
    if e == PROPANE and random.random() < 0.003:  # Bug 34: propane leaks gas
        for nx,ny,n in neighbors(x,y):
            if n == EMPTY: s(nx,ny,NATURAL_GAS); break


def update_food(x, y, e):
    if RX.process(x, y, e, diag=False): return
    _food_behavior(x, y, e)


def _food_behavior(x, y, e):
    if e == BREAD:
        if (has_neighbor(x,y,(MUSHROOM,)) and random.random()<0.001) or \
           (has_neighbor(x,y,(WATER,MUD,SALTWATER)) and get_moist(x,y)>40 and random.random()<0.001):
            s(x,y,MUSHROOM)
        for nx,ny,n in neighbors(x,y):
            if n in (ANT,TERMITE) and random.random()<0.01: s(x,y,DUST); return
            if n==BACTERIA and random.random()<0.005: s(x,y,DIRT); return

    elif e == MEAT:
        if random.random()<0.0005: s(x,y,DUST)
        for nx,ny,n in neighbors(x,y):
            if n in (ANT,TERMITE,SPIDER) and random.random()<0.008: s(x,y,DUST); return
            if n==BACTERIA and random.random()<0.008: s(x,y,DUST); return
            if n==BIRD and random.random()<0.003: s(x,y,DUST); return
        if has_neighbor(x,y,(ICE,LIQUID_NITROGEN)) and random.random()<0.002:
            cgrid[y][x]=(140,80,80)

    elif e == EGG:
        above = g(x, y-1)
        if above in (STONE, METAL, BRICK, STEEL, OBSIDIAN) and random.random()<0.1: s(x,y,EMPTY); return
        if has_neighbor(x,y,(FIRE,LAVA,MOLTEN_METAL),diag=True) and random.random()<0.01:
            s(x,y,random.choice([BIRD,ANT,SPIDER,WORM])); return
        if has_neighbor(x,y,(STONE,METAL,BRICK,STEEL,OBSIDIAN)):
            below=g(x,y+1)
            if below in SOLIDS and random.random()<0.02: s(x,y,EMPTY)

    elif e == CHEESE:
        if has_neighbor(x,y,(LAVA,MOLTEN_METAL,MOLTEN_GLASS,PLASMA)):
            if random.random()<0.05: cgrid[y][x]=(240,210,80); return  # visual melt only
        for nx,ny,n in neighbors(x,y):
            if n in (ANT,TERMITE) and random.random()<0.005: s(x,y,DUST); return
            if n==BACTERIA and random.random()<0.003: s(x,y,DIRT); return

    elif e == FRUIT:
        for nx,ny,n in neighbors(x,y):
            if n in (ANT,TERMITE,BIRD,SPIDER) and random.random()<0.006: s(x,y,DIRT); return
            if n==BACTERIA and random.random()<0.004: s(x,y,DIRT); return
            if n==PLANT and has_neighbor(x,y,(WATER,)) and random.random()<0.002:
                s(x,y,DIRT)  # fruit consumed as compost

    elif e == HAY:
        if has_neighbor(x,y,(WATER,MUD,SALTWATER)) and random.random()<0.003:
            cgrid[y][x]=(160,140,60)
        if random.random()<0.0003: s(x,y,DIRT)
        for nx,ny,n in neighbors(x,y):
            if n in (ANT,TERMITE) and random.random()<0.005: s(x,y,DUST); return


def update_electronic(x, y, e):
    if RX.process(x, y, e, diag=False): return
    _electronic_behavior(x, y, e)


def _electronic_behavior(x, y, e):
    if e == LED:
        if has_neighbor(x,y,(ELECTRICITY,)):
            r=random.random()
            if r<0.25: cgrid[y][x]=(255,random.randint(30,80),random.randint(30,80))
            elif r<0.5: cgrid[y][x]=(random.randint(30,80),255,random.randint(30,80))
            elif r<0.75: cgrid[y][x]=(random.randint(30,80),random.randint(30,80),255)
            else: cgrid[y][x]=(255,255,random.randint(30,100))
        else:
            if random.random()<0.05: cgrid[y][x]=(0,random.randint(80,150),random.randint(20,60))

    elif e == SENSOR:
        has_adj = any(n!=EMPTY and n!=WALL and n!=SENSOR for _,_,n in neighbors(x,y))
        if has_adj and random.random()<0.03:
            for ex,ey,_ in neighbors(x,y):
                if empt(ex,ey): s(ex,ey,ELECTRICITY); break

    elif e == LASER_E:
        if has_neighbor(x,y,(ELECTRICITY,)):
            cgrid[y][x]=(255,random.randint(0,60),random.randint(0,60))
            ldirs=[(-1,0),(1,0),(0,-1),(0,1)]
            ldx,ldy=random.choice(ldirs)
            for dist in range(1,60):
                lx,ly=x+ldx*dist,y+ldy*dist
                if not ib(lx,ly): break
                lt=g(lx,ly)
                if lt!=EMPTY:
                    if lt==WALL or lt==DIAMOND: break
                    if lt in (GLASS,CRYSTAL):
                        if random.random()<0.3: break
                        continue
                    if lt in FLAMMABLES and random.random()<0.3: s(lx,ly,FIRE)
                    elif lt in CONDUCTIVE and random.random()<0.02: s(lx,ly,MOLTEN_METAL)
                    elif lt==ICE: s(lx,ly,WATER)
                    break
                if dist<59: cgrid[ly][lx]=(255,0,0)
        else:
            if random.random()<0.02: cgrid[y][x]=(180,30,30)

    elif e == MAGNET:
        magnetic = (METAL,MERCURY,STEEL,BRONZE,COPPER,GOLD,SILVER,WIRE,RUST)
        for nx,ny,n in neighbors(x,y):
            if n in magnetic:
                dx_=x-nx; dy_=y-ny
                tx=nx+(1 if dx_>0 else -1 if dx_<0 else 0)
                ty=ny+(1 if dy_>0 else -1 if dy_<0 else 0)
                if empt(tx,ty) and (tx!=x or ty!=y): sw(nx,ny,tx,ty)
        if has_neighbor(x,y,(ELECTRICITY,)):
            cgrid[y][x]=(220,50,50)
            for nx,ny,n in neighbors(x,y,diag=True):
                if n in magnetic:
                    dx_=x-nx; dy_=y-ny
                    tx=nx+(1 if dx_>0 else -1 if dx_<0 else 0)
                    ty=ny+(1 if dy_>0 else -1 if dy_<0 else 0)
                    if empt(tx,ty): sw(nx,ny,tx,ty)

    elif e == GENERATOR:
        has_motion = False
        for nx,ny,n in neighbors(x,y):
            if n in LIQUIDS and n not in (MOLTEN_GLASS,MOLTEN_METAL,HONEY):
                has_motion=True; break
            if n in GASES: has_motion=True; break
            if n in CREATURES: has_motion=True; break
        if has_motion and random.random()<0.04:
            for ex,ey,_ in neighbors(x,y):
                if empt(ex,ey): s(ex,ey,ELECTRICITY); break
        if has_neighbor(x,y,(SALTWATER,)) and random.random()<0.0002:
            s(x,y,RUST)
        elif has_neighbor(x,y,(WATER,)) and random.random()<0.00005:
            s(x,y,RUST)


def update_alloy(x, y, e):
    if RX.process(x, y, e, diag=False): return
    _alloy_behavior(x, y, e)


# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════
# V4: MATERIAL UPDATE
# ═══════════════════════════════════════════════════════════════════
def update_material(x, y, e):
    if e in (SOAP, LYE, WAX, NAPALM, TAR):
        if RX.process(x, y, e, diag=True): return
        update_liquid(x, y, e)
    elif e in (RESIN, ZINC, POTASSIUM, CALCIUM):
        if RX.process(x, y, e, diag=True): return
        if e == RESIN:
            _solid_behavior(x, y, e)
            if not moved[y][x] and random.random() < 0.01: try_fall(x, y, e)
        else: try_fall(x, y, e)
    elif e == PAPER:
        if RX.process(x, y, e, diag=True): return
        if random.random() < 0.01:
            for nx,ny,n in neighbors(x,y):
                if n in GASES and random.random()<0.3:
                    sw(x,y,nx,ny); break
        # Paper should slowly fall if unsupported (gravity)
        elif not moved[y][x] and random.random() < 0.02:
            below = g(x, y+1)
            if below == EMPTY or below in GASES:
                sw(x, y, x, y+1)
    elif e in (FLOUR, COKE, DRY_ICE, IODINE):
        if RX.process(x, y, e, diag=True): return
        try_fall(x, y, e)
        if e == DRY_ICE:
            for nx,ny,n in neighbors(x,y):
                if n == WATER and random.random()<0.04: s(nx,ny,ICE)
            if random.random()<0.02:
                for nx,ny,n in neighbors(x,y):
                    if n==EMPTY and random.random()<0.2:
                        s(nx,ny,CO2); break


# GRID UPDATE
# ═══════════════════════════════════════════════════════════════════════════════
def update_grid():
    for y in range(GH-1, -1, -1):
        xr = range(GW) if (GH-1-y) % 2 == 0 else range(GW-1, -1, -1)
        for x in xr:
            if moved[y][x]: continue
            e = grid[y][x]
            if e == EMPTY:
                decay_state(x, y)
                continue
            decay_state(x, y)
            # Heat sources propagate temperature
            if e in HEAT_SOURCES or e in CRYOGENIC:
                propagate_heat(x, y)
            if is_pow(e):       update_powder(x, y, e)
            elif is_liq(e):     update_liquid(x, y, e)
            elif is_gas(e):     update_gas(x, y, e)
            elif is_sol(e):     update_solid(x, y, e)
            elif e in SPECIALS: update_special(x, y, e)
            elif e in LIFE_S:   update_life(x, y, e)
            elif e in EXPL_S:   update_explosive(x, y, e)
            elif e in FOOD_S:   update_food(x, y, e)
            elif e in ELEC_S:   update_electronic(x, y, e)
            elif e in ALLOY_S:  update_alloy(x, y, e)
            elif e in MATERIALS: update_material(x, y, e)
    for y in range(GH):
        for x in range(GW):
            moved[y][x] = False


# ═══════════════════════════════════════════════════════════════════════════════
# UI
# ═══════════════════════════════════════════════════════════════════════════════
def build_buttons():
    btns=[]; px=GW*CELL+6; bw,bh=28,20; gap=2; cols=8; y=68
    for cn,elems,cc in CATEGORIES:
        btns.append(("label",pygame.Rect(px,y,UI_W-12,16),cn,cc)); y+=18
        for i,eid in enumerate(elems):
            col,row=i%cols,i//cols
            bx,by=px+col*(bw+gap),y+row*(bh+gap)
            btns.append(("btn",pygame.Rect(bx,by,bw,bh),eid,ELEM[eid][0]))
        y+=((len(elems)+cols-1)//cols)*(bh+gap)+6
    return btns,y

def draw_brush(cx,cy,elem,size):
    r=size//2
    for dx in range(-r,r+1):
        for dy in range(-r,r+1):
            if dx*dx+dy*dy<=r*r:
                nx,ny=cx+dx,cy+dy
                if ib(nx,ny):
                    if elem==EMPTY: s(nx,ny,EMPTY)
                    elif grid[ny][nx]==EMPTY: s(nx,ny,elem)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    global grid,cgrid,moved,temp_grid,moist_grid,pressure_grid,cooldown_grid
    pygame.init()
    screen=pygame.display.set_mode((SW,SH))
    spec_count, trait_count, state_count = RX.count_rules()
    pygame.display.set_caption(f"Falling Sand v6 - 121 Elements | {spec_count}+{trait_count}+{state_count} Rules")
    clock=pygame.time.Clock()
    font=pygame.font.SysFont("consolas",15,bold=True)
    sfont=pygame.font.SysFont("consolas",11)
    tfont=pygame.font.SysFont("consolas",18,bold=True)
    selected=SAND; brush_size=5; paused=False; ui_scroll=0
    show_temp=False  # Toggle temperature overlay with T key
    buttons,ui_content_h=build_buttons()
    grid_w_px=GW*CELL; grid_h_px=GH*CELL
    # v5: Pre-allocate numpy arrays for fast rendering
    grid_pixels = np.zeros((grid_w_px, grid_h_px, 3), dtype=np.uint8)
    bg_color = np.array([10, 10, 15], dtype=np.uint8)
# v6: Visual category sets for per-element rendering detail
    VIS_LIQUIDS = frozenset([WATER, SALTWATER, MILK, HONEY, SLIME, SOAP, INK, WINE, LYE, MUD, NUCLEAR_WASTE, CHLORINE, MERCURY])
    VIS_HOT_LIQ = frozenset([LAVA, MOLTEN_METAL, MOLTEN_GLASS])
    VIS_GLASS = frozenset([GLASS, ICE, DIAMOND, CRYSTAL, GLASS_SHARD])
    VIS_METALS = frozenset([METAL, STEEL, BRONZE, COPPER, GOLD, SILVER, RUST, WIRE])
    VIS_ORGANIC = frozenset([WOOD, PLANT, GRASS, CACTUS, HAY, RESIN, PAPER, BREAD, EGG, MOSS, MUSHROOM])
    VIS_MASONRY = frozenset([BRICK, STONE, OBSIDIAN])
    VIS_GASES = frozenset([STEAM, SMOKE, FOG, CLOUD, NATURAL_GAS, POISON_GAS, HELIUM, HYDROGEN, OXYGEN, CO2, NEON, SPORE, AMMONIA])
    # Glow accumulators (low-res, at cell level for performance)
    glow_grid = np.zeros((GW, GH, 3), dtype=np.float32)
    # Brush preview surface (reused each frame)
    brush_surf = pygame.Surface((grid_w_px, grid_h_px), pygame.SRCALPHA)
    grid_surface = screen.subsurface((0, 0, grid_w_px, grid_h_px))
    glow_surface = pygame.Surface((grid_w_px, grid_h_px))
    all_elems_flat=[]
    for _,elems,_ in CATEGORIES: all_elems_flat.extend(elems)
    # Cache glow array for performance (Bug 42: avoid list conversion every frame)
    GLOW_ARR = np.array(list(GLOW_SET), dtype=np.int16)
    tooltip_text=""; tooltip_timer=0
    running=True
    while running:
        fps=clock.get_fps(); clock.tick(60)
        if tooltip_timer>0: tooltip_timer-=1
        else: tooltip_text=""
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: running=False
            elif ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_SPACE: paused=not paused
                elif ev.key==pygame.K_c:
                    grid=[[EMPTY]*GW for _ in range(GH)]
                    cgrid=[[(0,0,0)]*GW for _ in range(GH)]
                    temp_grid=[[AMBIENT_TEMP]*GW for _ in range(GH)]
                    moist_grid=[[AMBIENT_MOIST]*GW for _ in range(GH)]
                    pressure_grid=[[0]*GW for _ in range(GH)]
                    cooldown_grid=[[0]*GW for _ in range(GH)]
                    moved=[[False]*GW for _ in range(GH)]
                    RX._stats = {"specific_hits": 0, "trait_hits": 0, "state_hits": 0}
                elif ev.key==pygame.K_UP: brush_size=min(brush_size+1,30)
                elif ev.key==pygame.K_DOWN: brush_size=max(brush_size-1,1)
                elif ev.key==pygame.K_t: show_temp=not show_temp
                elif pygame.K_1<=ev.key<=pygame.K_9:
                    idx=ev.key-pygame.K_1
                    if idx<len(all_elems_flat): selected=all_elems_flat[idx]
                elif ev.key==pygame.K_0:
                    if 9<len(all_elems_flat): selected=all_elems_flat[9]
            elif ev.type==pygame.MOUSEBUTTONDOWN:
                mx,my=ev.pos
                if ev.button==1:
                    clicked=False
                    for item in buttons:
                        if item[0]=="btn":
                            _,rect,eid,_=item; adj=rect.copy(); adj.y-=ui_scroll
                            if adj.collidepoint(mx,my):
                                selected=eid; tooltip_text=ELEM[eid][0]; tooltip_timer=90
                                clicked=True; break
                    if not clicked and mx<grid_w_px and 0<=my<SH:
                        draw_brush(mx//CELL,my//CELL,selected,brush_size)
                elif ev.button==3 and mx<grid_w_px and 0<=my<SH:
                    draw_brush(mx//CELL,my//CELL,EMPTY,brush_size)
                elif ev.button==4:
                    if mx>=grid_w_px: ui_scroll=max(0,ui_scroll-25)
                    else: brush_size=min(brush_size+1,30)
                elif ev.button==5:
                    if mx>=grid_w_px:
                        ms=max(0,ui_content_h-(SH-68)); ui_scroll=min(ms,ui_scroll+25)
                    else: brush_size=max(brush_size-1,1)
            elif ev.type==pygame.MOUSEMOTION:
                mx,my=ev.pos; mb=pygame.mouse.get_pressed()
                if mx<grid_w_px and 0<=my<SH:
                    if mb[0]: draw_brush(mx//CELL,my//CELL,selected,brush_size)
                    elif mb[2]: draw_brush(mx//CELL,my//CELL,EMPTY,brush_size)
        if not paused: update_grid()
        screen.fill((20,20,25))

        # ── v6: Textured surfarray rendering with per-element detail ─────
        # Build cell-level color array with material feel
        grid_pixels[:] = bg_color  # fill background
        glow_grid[:] = 0  # reset glow
        _bg = (10, 10, 15)  # background color for gas edge blending

        for y2 in range(GH):
            row = grid[y2]
            crow = cgrid[y2]
            for x2 in range(GW):
                if row[x2] != EMPTY:
                    c = crow[x2]
                    e = row[x2]
                    px, py = x2 * CELL, y2 * CELL
                    # Fill base block
                    grid_pixels[px:px+CELL, py:py+CELL] = c

                    # ── Per-element visual detail ──
                    if e in VIS_LIQUIDS:
                        # Liquid: lighter top edge (surface tension), darker bottom
                        grid_pixels[px:px+CELL, py] = (min(255,c[0]+20), min(255,c[1]+20), min(255,c[2]+20))
                        grid_pixels[px:px+CELL, py+CELL-1] = (max(0,c[0]-12), max(0,c[1]-12), max(0,c[2]-12))
                        # Side darkening for depth
                        grid_pixels[px, py:py+CELL] = (max(0,c[0]-6), max(0,c[1]-6), max(0,c[2]-6))
                    elif e in VIS_HOT_LIQ:
                        # Molten materials: bright glowing center
                        grid_pixels[px+1:px+3, py+1:py+3] = (min(255,c[0]+35), min(255,c[1]+25), min(255,c[2]+15))
                        # Hot edge glow
                        grid_pixels[px, py] = (min(255,c[0]+20), min(255,c[1]+15), min(255,c[2]+10))
                    elif e in VIS_GLASS:
                        # Transparent/reflective: specular highlight corner + opposite shadow
                        grid_pixels[px, py] = (min(255,c[0]+55), min(255,c[1]+55), min(255,c[2]+55))
                        grid_pixels[px+1, py] = (min(255,c[0]+30), min(255,c[1]+30), min(255,c[2]+30))
                        grid_pixels[px+CELL-1, py+CELL-1] = (max(0,c[0]-18), max(0,c[1]-18), max(0,c[2]-18))
                        # Inner transparency tint
                        grid_pixels[px+1:px+CELL-1, py+1:py+CELL-1] = (min(255,c[0]+8), min(255,c[1]+8), min(255,c[2]+8))
                    elif e in VIS_METALS:
                        # Metals: subtle horizontal brushed grain + bevel
                        gc = (min(255,c[0]+7), min(255,c[1]+7), min(255,c[2]+7))
                        grid_pixels[px:px+CELL, py] = gc
                        grid_pixels[px:px+CELL, py+2] = gc
                        # Left highlight, right shadow for 3D feel
                        grid_pixels[px, py:py+CELL] = (min(255,c[0]+5), min(255,c[1]+5), min(255,c[2]+5))
                        grid_pixels[px+CELL-1, py:py+CELL] = (max(0,c[0]-8), max(0,c[1]-8), max(0,c[2]-8))
                    elif e in VIS_ORGANIC:
                        # Organic materials: subtle vertical grain/variation
                        vc = (max(0,c[0]-7), min(255,c[1]+5), max(0,c[2]-5))
                        grid_pixels[px, py:py+CELL] = vc
                        grid_pixels[px+2, py:py+CELL] = vc
                    elif e in VIS_MASONRY:
                        # Stone/brick: 3D bevel with mortar-like edges
                        lc = (min(255,c[0]+12), min(255,c[1]+12), min(255,c[2]+12))
                        dc = (max(0,c[0]-20), max(0,c[1]-20), max(0,c[2]-20))
                        grid_pixels[px, py:py+CELL] = lc
                        grid_pixels[px+CELL-1, py:py+CELL] = dc
                        grid_pixels[px:px+CELL, py] = lc
                        grid_pixels[px:px+CELL, py+CELL-1] = dc
                    elif e in VIS_GASES:
                        # Gases: semi-transparent edges blend with background
                        ec = ((c[0]*2+_bg[0])//3, (c[1]*2+_bg[1])//3, (c[2]*2+_bg[2])//3)
                        grid_pixels[px, py] = ec
                        grid_pixels[px+CELL-1, py] = ec
                        grid_pixels[px, py+CELL-1] = ec
                        grid_pixels[px+CELL-1, py+CELL-1] = ec
                    elif e == FIRE:
                        # Fire: bright white-yellow core pixels
                        grid_pixels[px+1, py+1] = (255, 255, min(255, c[2]+120))
                        grid_pixels[px+2, py+2] = (255, min(255, c[1]+60), 0)
                    elif e == ELECTRICITY:
                        # Electricity: white-hot center
                        grid_pixels[px+1:px+3, py+1:py+3] = (220, 235, 255)
                    elif e == PLASMA:
                        # Plasma: vivid inner core
                        grid_pixels[px+1:px+3, py+1:py+3] = (min(255,c[0]+30), min(255,c[1]+30), min(255,c[2]+15))

                    # Accumulate glow for emissive elements
                    if e in GLOW_SET:
                        glow_grid[x2, y2, 0] += c[0] * 0.3
                        glow_grid[x2, y2, 1] += c[1] * 0.3
                        glow_grid[x2, y2, 2] += c[2] * 0.3

        # Apply temperature overlay
        if show_temp:
            for y2 in range(GH):
                for x2 in range(GW):
                    if grid[y2][x2] != EMPTY:
                        t = temp_grid[y2][x2]
                        px, py = x2 * CELL, y2 * CELL
                        if t > 50:
                            heat_frac = min(1.0, (t - 50) / 150.0)
                            r = min(255, int(grid_pixels[px, py, 0] + (255 - grid_pixels[px, py, 0]) * heat_frac * 0.5))
                            gv = max(0, int(grid_pixels[px, py, 1] * (1 - heat_frac * 0.3)))
                            b = max(0, int(grid_pixels[px, py, 2] * (1 - heat_frac * 0.5)))
                            grid_pixels[px:px+CELL, py:py+CELL] = (r, gv, b)
                        elif t < 0:
                            cold_frac = min(1.0, -t / 80.0)
                            rv = max(0, int(grid_pixels[px, py, 0] * (1 - cold_frac * 0.3)))
                            bv = max(0, int(grid_pixels[px, py, 1] * (1 - cold_frac * 0.3)))
                            b = min(255, int(grid_pixels[px, py, 2] + (255 - grid_pixels[px, py, 2]) * cold_frac * 0.5))
                            grid_pixels[px:px+CELL, py:py+CELL] = (rv, bv, b)

        # Blit pixel array to screen (fast C-level blit)
        pygame.surfarray.blit_array(grid_surface, grid_pixels)

        # v5: Glow/bloom pass using numpy (fast)
        # Build a bool grid for glow membership (numpy, O(GW*GH))
        grid_arr = np.array(grid, dtype=np.int16)
        # Bug 42: Cache GLOW_ARR outside loop for performance
        has_glow = np.any(np.isin(grid_arr, GLOW_ARR))

        if has_glow:
            # Two-pass box blur using numpy roll (no Python loops)
            glow = glow_grid
            # Pad edges
            padded = np.pad(glow, ((1,1),(1,1),(0,0)), mode='edge')
            # Box blur pass 1
            blurred = (padded[:-2,1:-1,:] + padded[2:,1:-1,:] +
                       padded[1:-1,:-2,:] + padded[1:-1,2:,:] +
                       padded[1:-1,1:-1,:] * 2) / 6.0
            # Box blur pass 2
            padded2 = np.pad(blurred, ((1,1),(1,1),(0,0)), mode='edge')
            blurred = (padded2[:-2,1:-1,:] + padded2[2:,1:-1,:] +
                       padded2[1:-1,:-2,:] + padded2[1:-1,2:,:] +
                       padded2[1:-1,1:-1,:] * 2) / 6.0

            # Scale and convert to uint8
            intensity = np.max(blurred, axis=2)
            mask = intensity > 8
            if np.any(mask):
                glow_rgb = np.clip(blurred * 0.15, 0, 60).astype(np.uint8)
                # Bug 47: Use pygame.transform.scale for glow (less memory)
                glow_small = pygame.Surface((GW, GH))
                glow_masked = np.where(mask[:,:,np.newaxis], glow_rgb, 0).astype(np.uint8)
                pygame.surfarray.blit_array(glow_small, glow_masked)
                glow_scaled = pygame.transform.scale(glow_small, (grid_w_px, grid_h_px))
                glow_surface.blit(glow_scaled, (0, 0))
                glow_surface.set_colorkey((0, 0, 0))
                screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        mx,my=pygame.mouse.get_pos()
        if mx<grid_w_px:
            gx,gy=mx//CELL,my//CELL; r=brush_size//2
            # v5: Reuse pre-allocated brush surface
            brush_surf.fill((0, 0, 0, 0))
            sel_color=ELEM[selected][1]
            for dx in range(-r,r+1):
                for dy in range(-r,r+1):
                    if dx*dx+dy*dy<=r*r:
                        nx,ny=gx+dx,gy+dy
                        if ib(nx,ny):
                            pygame.draw.rect(brush_surf,(*sel_color,70),(nx*CELL,ny*CELL,CELL,CELL))
            screen.blit(brush_surf,(0,0))
        panel_x=grid_w_px
        pygame.draw.rect(screen,(30,30,38),(panel_x,0,UI_W,SH))
        pygame.draw.line(screen,(55,55,65),(panel_x,0),(panel_x,SH),2)
        screen.blit(tfont.render("FALLING SAND v6",True,(230,230,245)),(panel_x+8,6))
        screen.blit(sfont.render(f"121 Elements | 11 Cats | Textured v6",True,(120,120,140)),(panel_x+8,28))
        screen.blit(sfont.render(f"Brush:{brush_size:2d}  FPS:{fps:4.0f}  {'[TEMP]' if show_temp else ''}",True,(120,120,140)),(panel_x+8,42))
        clip_rect=pygame.Rect(panel_x,62,UI_W,SH-130)
        screen.set_clip(clip_rect)
        for item in buttons:
            if item[0]=="label":
                _,rect,name,color=item; adj_y=rect.y-ui_scroll
                if 62-20<adj_y<SH-130:
                    screen.blit(sfont.render(name,True,color),(rect.x,adj_y))
            else:
                _,rect,eid,ename=item; adj_y=rect.y-ui_scroll
                if 62-25<adj_y<SH-130:
                    is_sel=(eid==selected); bc=ELEM[eid][1]
                    pygame.draw.rect(screen,bc,(rect.x,adj_y,rect.w,rect.h))
                    if is_sel:
                        pygame.draw.rect(screen,(255,255,80),(rect.x-1,adj_y-1,rect.w+2,rect.h+2),2)
                    else:
                        pygame.draw.rect(screen,(60,60,70),(rect.x,adj_y,rect.w,rect.h),1)
                    lbl=sfont.render(ename,True,(255,255,255) if sum(bc)<400 else (0,0,0))
                    screen.blit(lbl,(rect.x+2,adj_y+3))
        screen.set_clip(None)
        by=SH-62
        pygame.draw.line(screen,(55,55,65),(panel_x+4,by),(panel_x+UI_W-4,by))
        sel_name=ELEM[selected][0]; sel_col=ELEM[selected][1]
        pygame.draw.rect(screen,sel_col,(panel_x+8,by+6,22,22))
        pygame.draw.rect(screen,(200,200,200),(panel_x+8,by+6,22,22),1)
        screen.blit(font.render(sel_name,True,(230,230,245)),(panel_x+36,by+8))
        helps=["LMB:Draw  RMB:Erase","Space:Pause C:Clear T:Temp","Scroll:Brush/UI  0-9:Pick"]
        for i,h in enumerate(helps):
            screen.blit(sfont.render(h,True,(100,100,120)),(panel_x+8,by+32+i*13))
        if paused:
            ps=font.render("|| PAUSED",True,(255,80,80))
            screen.blit(ps,(panel_x+UI_W-100,by+8))
        if tooltip_text and tooltip_timer>0:
            alpha=min(255,tooltip_timer*5)
            tip_surf=sfont.render(tooltip_text,True,(255,255,200))
            tip_bg=pygame.Surface((tip_surf.get_width()+8,tip_surf.get_height()+4),pygame.SRCALPHA)
            tip_bg.fill((0,0,0,min(180,alpha)))
            tip_x=max(0,min(SW-tip_surf.get_width(),mx-tip_surf.get_width()//2-4))
            tip_y=max(0,my-25)
            screen.blit(tip_bg,(tip_x,tip_y))
            screen.blit(tip_surf,(tip_x+4,tip_y+2))
        pygame.display.flip()
    pygame.quit(); sys.exit()

if __name__=="__main__":
    main()