# -*- coding: utf-8 -*-
"""
OPTC Pirate Rumble — Character Database
Data provided by player Đặng Sỹ Tiến (2A202600937)
"""

# ============================================================
# CHARACTER DATABASE
# ============================================================

CHARACTERS = {

    # ========== ENEMY TEAM: World Government / Five Elders ==========

    4571: {
        "id": 4571,
        "name": "Imu - Occupant of the Empty Throne",
        "type": "STR",
        "classes": ["Powerhouse", "Driven"],
        "factions": ["Navy", "World Government", "Five Elders"],
        "ct": 99,
        "special": (
            "First 15s: 100% Ability Bind to 2 lowest HP enemies (15s), Self CT -30%.\n"
            "100% evade Forced Out & Confusion for Navy/WG (40s).\n"
            "Last 85s: 100% Cleanse all debuffs to crew, 80% Ability Bind all enemies (1s).\n"
            "Last 50s: 100% Ability Bind all enemies (5s), Heal 50% HP if HP<50%, 5000 fixed dmg all enemies."
        ),
        "gp_burst": (
            "Trigger: Time count 80.\n"
            "100% Ability Bind all enemies (15s).\n"
            "Removes 30% Special CT all enemies.\n"
            "100% evade Forced Out for Navy/WG (50s)."
        ),
        "ability": (
            "SPD up lv7 to crew.\n"
            "On hit (limit 10): Self CT -5%, Enemy CT -5%.\n"
            "On damaged (limit 10): Self CT -5%, Enemy CT -5%.\n"
            "On heal (limit 10): Self CT -5%, Enemy CT -5%.\n"
            "Crew 1+: Self CT -100%, Five Elders CT -10%.\n"
            "On appear: Self CT -30%, Enemy CT -30%."
        ),
        "leader_skill": (
            "ATK+SPD lv6 → STR, Navy, WG.\n"
            "Special CT lv3 → STR, Navy, WG.\n"
            "HP+RCV lv6 → Powerhouse, Driven.\n"
            "DEF lv4 → Powerhouse, Driven.\n"
            "ATK lv6 → Navy, WG.\n"
            "Special CT lv3 → Navy, WG.\n"
            "Crew 1+: Special CT Down lv4 debuff to all enemies."
        ),
        "leader_buff_filters": {
            "types": ["STR"],
            "classes": ["Powerhouse", "Driven"],
            "factions": ["Navy", "World Government"]
        },
        "tags": {
            "inflicts": ["Ability Bind", "Special CT Remove"],
            "provides": ["Cleanse", "Heal", "Evade Forced Out", "Evade Confusion", "SPD Up"],
            "counters": ["Forced Out", "Confusion"],
            "threats": ["Ability Bind spam (multi-phase)", "CT drain on hit/damaged/heal"]
        }
    },

    4491: {
        "id": 4491,
        "name": "St. Jaygarcia Saturn - Summoning Highest Authority",
        "type": "STR",
        "classes": ["Driven", "Cerebral"],
        "factions": ["Navy", "World Government", "Five Elders"],
        "ct": 30,
        "special": (
            "DEF lv6 → STR, Driven (20s).\n"
            "Reduce Half Stats → STR, Driven (15s).\n"
            "100% Haste to 2 Navy/WG/Zoan-type.\n"
            "12x ATK spread dmg (medium radial).\n"
            "Crew 5+: 15x ATK spread dmg (large radial)."
        ),
        "gp_burst": (
            "Trigger: After receiving damage 12 times.\n"
            "Reduce Half Stats → STR, Driven, Cerebral (15s).\n"
            "100% Half Stats to Powerhouse and Free Spirit (15s).\n"
            "4x + 20x Leader ATK dmg to all enemies."
        ),
        "ability": (
            "HP+RCV+SPD lv7 → STR, Driven, Five Elders.\n"
            "ATK lv5 → Navy, WG, Zoan-type.\n"
            "DEF lv3 → Navy, WG, Zoan-type.\n"
            "On receives Half Stats (limit 2): ATK lv6 to self, DEF Down lv4 to all enemies."
        ),
        "leader_skill": (
            "SPD+RCV lv6 → STR.\n"
            "Special CT lv3 → STR.\n"
            "HP+ATK lv6 → Driven, Cerebral.\n"
            "DEF lv4 → Driven, Cerebral.\n"
            "Last 50s: DEF Down lv5 to all enemies."
        ),
        "leader_buff_filters": {
            "types": ["STR"],
            "classes": ["Driven", "Cerebral"],
            "factions": ["Navy", "World Government"]
        },
        "tags": {
            "inflicts": ["Half Stats", "DEF Down"],
            "provides": ["DEF Up", "Reduce Half Stats", "Haste", "High Spread Damage"],
            "counters": ["Half Stats"],
            "threats": ["Half Stats to Powerhouse/Free Spirit (GP Burst)", "DEF Down lv5 (last 50s)"]
        }
    },

    4453: {
        "id": 4453,
        "name": "St. Marcus Mars - Godhead of Environment",
        "type": "STR",
        "classes": ["Driven", "Shooter"],
        "factions": ["Navy", "World Government", "Five Elders"],
        "ct": 28,
        "special": (
            "3000 fixed dmg to all enemies.\n"
            "Crew 5+: ATK+SPD lv5 to crew (20s), Special CT lv5 to crew (20s).\n"
            "Crew 5+: Special CT Down lv5 debuff to all enemies (20s).\n"
            "Reduces 20% Special CT to Navy/WG.\n"
            "HP<1%: 100% CT reduce to 1 ATK-Style, 100% Haste to 1 ATK-Style."
        ),
        "gp_burst": (
            "Trigger: After dealing damage 16 times.\n"
            "6000 fixed dmg to all enemies.\n"
            "2x Leader ATK dmg to Striker and Powerhouse.\n"
            "Reduces 40% Special CT → STR, Shooter, Driven."
        ),
        "ability": (
            "HP+SPD lv7 → STR, Shooter, Five Elders.\n"
            "DEF lv5 → STR, Shooter, Five Elders.\n"
            "Crew 5+: DEF+Special CT Down lv3 debuff to all enemies.\n"
            "Special CT lv3 → Navy, WG.\n"
            "Reduce On Death."
        ),
        "leader_skill": (
            "RCV lv6 → STR, Five Elders.\n"
            "DEF lv4 → STR, Five Elders.\n"
            "Special CT lv3 → STR, Five Elders.\n"
            "ATK+SPD lv6 → Shooter, Driven.\n"
            "ATK lv4 → Shooter, Driven.\n"
            "HP+RCV lv4 → Navy, WG.\n"
            "DEF lv2 → Navy, WG."
        ),
        "leader_buff_filters": {
            "types": ["STR"],
            "classes": ["Shooter", "Driven"],
            "factions": ["Navy", "World Government", "Five Elders"]
        },
        "tags": {
            "inflicts": ["Special CT Down", "DEF Down"],
            "provides": ["ATK Up", "SPD Up", "Special CT Up", "Haste", "DEF Up"],
            "counters": [],
            "threats": ["Special CT manipulation (drain + debuff)", "Reduce On Death (hard to kill)"]
        }
    },

    # ========== PLAYER BOX ==========

    4560: {
        "id": 4560,
        "name": "Red-Haired Shanks - Emperor and Captain",
        "type": "STR",
        "classes": ["Cerebral", "Slasher", "Free Spirit", "Driven"],
        "factions": ["Red-Haired Pirates", "Four Emperors"],
        "ct": 28,
        "special": (
            "ATK+DEF lv6 → STR, Cerebral, Slasher, Red-Haired Pirates, Four Emperors.\n"
            "DEF Down lv5 to all enemies (5s).\n"
            "2.2x ATK ignoring DEF to Free Spirit.\n"
            "20x ATK spread dmg to all enemies.\n"
            "Crew 2+: Switch self with 1st sub."
        ),
        "gp_burst": (
            "Trigger: Crew uses specials 4 times.\n"
            "70% Action Bind all enemies (10s).\n"
            "100% Special Bind Free Spirit and Driven (20s).\n"
            "100% RCV Bind all enemies (30s).\n"
            "2.5x Leader ATK dmg to all enemies."
        ),
        "ability": (
            "ATK+DEF lv7 → STR, Cerebral, Slasher, Red-Haired Pirates, Four Emperors.\n"
            "Special CT lv3 → STR, Cerebral, Slasher, Red-Haired Pirates, Four Emperors.\n"
            "On defeated (limit 5): Self CT -30%.\n"
            "On hit (limit 3): Removes 20% Special CT to Free Spirit.\n"
            "Crew 2+: On appear, removes 30% Special CT to all enemies."
        ),
        "leader_skill": (
            "HP+SPD lv6 → STR, Four Emperors.\n"
            "Special CT lv3 → STR, Four Emperors.\n"
            "ATK+RCV lv6 → Cerebral, Free Spirit, Four Emperors.\n"
            "DEF lv4 → Cerebral, Free Spirit, Four Emperors.\n"
            "Last 90s: Removes 30% Special CT to Free Spirit and Driven.\n"
            "Last 90s: Reduces 10% Special CT to Cerebral and Free Spirit."
        ),
        "leader_buff_filters": {
            "types": ["STR"],
            "classes": ["Cerebral", "Free Spirit"],
            "factions": ["Four Emperors"]
        },
        "tags": {
            "inflicts": ["DEF Down", "Action Bind", "Special Bind", "RCV Bind", "Special CT Remove"],
            "provides": ["ATK Up", "DEF Up", "Switch"],
            "counters": [],
            "threats": []
        }
    },

    4564: {
        "id": 4564,
        "name": "Buggy the Genius Jester - Emperor and Chairman",
        "type": "INT",
        "classes": ["Slasher", "Cerebral"],
        "factions": ["Cross Guild", "Seven Warlords of the Sea", "Four Emperors"],
        "ct": 28,
        "special": (
            "DEF+Guard lv5 to self (50s).\n"
            "First 30s: ATK+SPD lv5, Special CT lv3 → INT, Slasher, Cerebral, Cross Guild, Seven Warlords, Four Emperors (100s).\n"
            "Last 50s: 1.5x ATK ignoring DEF (large radial).\n"
            "Last 30s: 15x ATK spread dmg (large radial).\n"
            "Crew 2+: Heal 20% HP to ATK-Style.\n"
            "HP<20%: Heal 30% HP to crew, switch with 1st sub."
        ),
        "gp_burst": (
            "Trigger: Time 20.\n"
            "5000 fixed dmg to all enemies.\n"
            "ATK+SPD+DEF+RCV lv5 → Slasher, Cerebral, Four Emperors (100s).\n"
            "Heal 30% HP → Slasher, Cerebral, Four Emperors."
        ),
        "ability": (
            "DEF+HP lv7, Guard lv5 → INT, Slasher, Cerebral, Cross Guild, Seven Warlords, Four Emperors.\n"
            "On Guard (limit 3): ATK+SPD lv3, DEF lv2 → Cross Guild, Seven Warlords, Four Emperors.\n"
            "Apply Revive (20% HP) to self.\n"
            "On appear: Crew CT -10%, Cross Guild/Seven Warlords CT -30%.\n"
            "First 90s: Self CT -50% upon appearance."
        ),
        "leader_skill": (
            "RCV+HP lv6 → INT, Four Emperors.\n"
            "Special CT lv3 → INT, Four Emperors.\n"
            "ATK+SPD lv6 → Slasher, Cerebral, Four Emperors.\n"
            "DEF lv4 → Slasher, Cerebral, Four Emperors.\n"
            "First 50s: DEF+Guard lv6 → INT, Slasher, Cerebral, Four Emperors."
        ),
        "leader_buff_filters": {
            "types": ["INT"],
            "classes": ["Slasher", "Cerebral"],
            "factions": ["Four Emperors"]
        },
        "tags": {
            "inflicts": [],
            "provides": ["DEF Up", "Guard", "ATK Up", "SPD Up", "Heal", "Revive", "Special CT Up"],
            "counters": [],
            "threats": []
        }
    },

    4562: {
        "id": 4562,
        "name": "Blackbeard - Emperor and Commodore",
        "type": "QCK",
        "classes": ["Driven", "Free Spirit"],
        "factions": ["Blackbeard Pirates", "Four Emperors"],
        "ct": 35,
        "special": (
            "SPD lv5 → QCK, Driven, BB Pirates, Four Emperors (20s).\n"
            "Reduces 20% Special CT → QCK, Driven, BB Pirates, Four Emperors.\n"
            "100% Haste to 2 ATK-Style and DBF-Style.\n"
            "20% health cut to all enemies.\n"
            "SPD Down lv5 to all enemies (20s).\n"
            "100% Action Bind 2 highest CT enemies (20s).\n"
            "DEF+Shield lv5 → QCK, Driven, BB Pirates, Four Emperors (20s).\n"
            "20x ATK spread dmg (large forward).\n"
            "5000 fixed dmg to all enemies.\n"
            "ATK lv5 → QCK, Driven, BB Pirates, Four Emperors (20s).\n"
            "2.2x ATK ignoring DEF (large radial)."
        ),
        "gp_burst": (
            "Trigger: After landing 7 Normal attacks.\n"
            "Reduce Action Bind, Special Bind, Paralysis → QCK, Free Spirit, Driven, Four Emperors (20s).\n"
            "100% evade Action Bind, Special Bind, Paralysis → QCK, Free Spirit, Driven, Four Emperors (20s).\n"
            "Shield lv5 → QCK, Free Spirit, Driven, Four Emperors (20s).\n"
            "100% Haste to 3 QCK, Free Spirit, Driven, Four Emperors.\n"
            "1.6x Leader ATK dmg to all enemies."
        ),
        "ability": (
            "SPD+DEF lv7 → QCK, Driven, BB Pirates, Four Emperors.\n"
            "Special CT lv3 → QCK, Driven, BB Pirates, Four Emperors.\n"
            "On receives Paralysis (limit 1): DEF lv5 → QCK, Driven.\n"
            "Crew 4+: ATK Down lv7 to all enemies.\n"
            "Reduce On Death."
        ),
        "leader_skill": (
            "ATK+RCV lv6 → QCK, Four Emperors.\n"
            "Special CT lv3 → QCK, Four Emperors.\n"
            "SPD+HP lv6 → Free Spirit, Driven, Four Emperors.\n"
            "DEF lv4 → Free Spirit, Driven, Four Emperors.\n"
            "ATK+DEF lv6 → QCK, Free Spirit, Driven, Four Emperors.\n"
            "Last 85s: Reduces 40% Special CT to Free Spirit/Driven with <=50% CT."
        ),
        "leader_buff_filters": {
            "types": ["QCK"],
            "classes": ["Free Spirit", "Driven"],
            "factions": ["Four Emperors"]
        },
        "tags": {
            "inflicts": ["SPD Down", "Action Bind", "ATK Down", "Health Cut"],
            "provides": ["SPD Up", "DEF Up", "Shield", "Haste", "ATK Up",
                         "Reduce Action Bind", "Reduce Special Bind", "Reduce Paralysis",
                         "Evade Action Bind", "Evade Special Bind", "Evade Paralysis"],
            "counters": ["Action Bind", "Special Bind", "Paralysis"],
            "threats": []
        }
    },

    4492: {
        "id": 4492,
        "name": "Bartholomew Kuma - Weak-Willed Pacifist",
        "type": "INT",
        "classes": ["Free Spirit", "Cerebral"],
        "factions": [],
        "ct": 40,
        "special": (
            "ATK+DEF lv6 → INT, Free Spirit (30s).\n"
            "100% Half Stats to Driven (20s).\n"
            "3x ATK dmg (large radial).\n"
            "Reduces 30% Special CT to crew.\n"
            "100% Haste to crew.\n"
            "When Bonney on crew: Provoke to self (30s), Counter 3x ATK to self (30s)."
        ),
        "gp_burst": (
            "Trigger: After receiving 30000 damage.\n"
            "100% evade Forced Out → STR, PSY, INT, Free Spirit, Cerebral (20s).\n"
            "800 fixed HP to crew (30s).\n"
            "6000 fixed dmg to all enemies."
        ),
        "ability": (
            "ATK+RCV+DEF lv7 → INT, Free Spirit.\n"
            "When Bonney on crew: Self CT -50% on appearance.\n"
            "On takes damage (limit 12): 1x RCV heal to INT, Free Spirit."
        ),
        "leader_skill": (
            "HP+SPD lv6 → STR, PSY, INT.\n"
            "DEF lv4 → STR, PSY, INT.\n"
            "ATK+RCV lv6 → Free Spirit, Cerebral.\n"
            "Special CT lv3 → Free Spirit, Cerebral.\n"
            "Apply Revive (50% HP) to Free Spirit and Cerebral."
        ),
        "leader_buff_filters": {
            "types": ["STR", "PSY", "INT"],
            "classes": ["Free Spirit", "Cerebral"],
            "factions": []
        },
        "tags": {
            "inflicts": ["Half Stats"],
            "provides": ["ATK Up", "DEF Up", "Haste", "Heal", "Evade Forced Out",
                         "Revive", "Provoke", "Counter"],
            "counters": ["Forced Out", "Driven enemies"],
            "threats": []
        }
    },

    4490: {
        "id": 4490,
        "name": "Luffy & Bonney - Unexpected Partners",
        "type": "INT",
        "classes": ["Free Spirit", "Cerebral"],
        "factions": ["Straw Hat Pirates", "Vegapunk", "Revolutionary Army"],
        "ct": 27,
        "special": (
            "DEF lv5 → Straw Hat Pirates, Vegapunk, Rev Army (20s).\n"
            "Removes 30% Special CT to 3 enemies with highest CT.\n"
            "100% Forced Out to Five Elders (10s).\n"
            "20000 fixed spread dmg (large radial).\n"
            "5x ATK dmg (large radial)."
        ),
        "gp_burst": (
            "Trigger: After dealing damage 16 times.\n"
            "Removes 30% Special CT to all enemies.\n"
            "1.6x Leader ATK dmg to all enemies.\n"
            "Reduces 30% Special CT → PSY, INT, Free Spirit, Cerebral."
        ),
        "ability": (
            "HP+RCV+SPD lv7 → INT, Free Spirit.\n"
            "ATK lv5 → Straw Hat Pirates, Vegapunk, Rev Army.\n"
            "Special CT lv3 → Straw Hat Pirates, Vegapunk, Rev Army.\n"
            "On appear: Reduces 10% Special CT → Straw Hat Pirates, Vegapunk, Rev Army.\n"
            "Last 50s: Removes 30% Special CT to all enemies upon appearance."
        ),
        "leader_skill": (
            "ATK+RCV lv6 → PSY, INT.\n"
            "Special CT lv3 → PSY, INT.\n"
            "HP+SPD lv6 → Free Spirit, Cerebral.\n"
            "DEF lv4 → Free Spirit, Cerebral.\n"
            "HP+DEF lv6 → Straw Hat Pirates, Vegapunk, Rev Army.\n"
            "Enemies 4+: Special CT Down lv5 to all enemies."
        ),
        "leader_buff_filters": {
            "types": ["PSY", "INT"],
            "classes": ["Free Spirit", "Cerebral"],
            "factions": ["Straw Hat Pirates", "Vegapunk", "Revolutionary Army"]
        },
        "tags": {
            "inflicts": ["Forced Out", "Special CT Remove"],
            "provides": ["DEF Up", "ATK Up", "Special CT Reduce"],
            "counters": ["Five Elders"],
            "threats": []
        }
    },

    4537: {
        "id": 4537,
        "name": "Luffy & Broggy - Pirate and Giant Warrior",
        "type": "STR",
        "classes": ["Free Spirit"],
        "factions": ["Giant", "Straw Hat Pirates"],
        "ct": 36,
        "special": (
            "DEF lv5 → STR, Free Spirit, Giant, Straw Hat Pirates (20s).\n"
            "Reduce Half Stats → STR, Free Spirit, Giant, Straw Hat Pirates (20s).\n"
            "10x ATK spread dmg (large forward).\n"
            "10x ATK spread dmg (large sideways).\n"
            "ATK lv12 → crew (5s).\n"
            "100% Haste to 1 ATK-Style highest ATK.\n"
            "During Assault Rumble: Reduces 15% Special CT → Giant, Straw Hat Pirates."
        ),
        "gp_burst": "N/A",
        "ability": (
            "ATK+HP lv6 → STR, Free Spirit, Giant, Straw Hat Pirates.\n"
            "Blow Away lv5 → STR, Free Spirit, Giant, Straw Hat Pirates.\n"
            "Crew 4+: DEF lv5 to crew.\n"
            "Crew 4+: SPD lv6 to crew."
        ),
        "leader_skill": "N/A",
        "leader_buff_filters": {},
        "tags": {
            "inflicts": [],
            "provides": ["DEF Up", "Reduce Half Stats", "ATK Up", "Haste", "Blow Away",
                         "SPD Up"],
            "counters": ["Half Stats"],
            "threats": []
        }
    },

    4558: {
        "id": 4558,
        "name": "Monkey D. Luffy - Emperor and Captain of SHP",
        "type": "DEX",
        "classes": ["Fighter", "Powerhouse"],
        "factions": ["Straw Hat Pirates", "Four Emperors"],
        "ct": 32,
        "special": (
            "2.5x ATK ignoring DEF to 1 ATK-Style.\n"
            "2.5x ATK ignoring DEF to 1 SPT-Style.\n"
            "Crew 4+: Counter 2.5x ATK to crew (30s).\n"
            "Crew 4+: 20x ATK spread dmg to all enemies.\n"
            "100% Paralysis to self (15s)."
        ),
        "gp_burst": (
            "Trigger: After receiving damage 12 times.\n"
            "Heal 50% HP to 3 lowest HP crew.\n"
            "750 fixed HP to crew (15s).\n"
            "Reduces 25% Special CT → DEX, Fighter, Powerhouse, SHP, Four Emperors.\n"
            "100% cleanse ATK and DEF debuffs to all enemies."
        ),
        "ability": (
            "HP+ATK+DEF lv7 → DEX, Fighter, Straw Hat Pirates, Four Emperors.\n"
            "Crew 4+: Special CT lv3 to crew.\n"
            "On hit (limit 10): Critical Hit lv1 → DEX, Fighter.\n"
            "HP<1%: ATK lv10 to self.\n"
            "Reduce On Death."
        ),
        "leader_skill": (
            "HP+RCV lv6 → DEX, Four Emperors.\n"
            "DEF lv4 → DEX, Four Emperors.\n"
            "ATK+SPD lv6 → Fighter, Powerhouse, Four Emperors.\n"
            "Special CT lv3 → Fighter, Powerhouse, Four Emperors.\n"
            "Last 80s: 3x RCV heal to crew.\n"
            "Last 50s: 4x RCV heal to crew.\n"
            "Last 30s: 5x RCV heal to crew."
        ),
        "leader_buff_filters": {
            "types": ["DEX"],
            "classes": ["Fighter", "Powerhouse"],
            "factions": ["Four Emperors"]
        },
        "tags": {
            "inflicts": ["Paralysis (self)"],
            "provides": ["Counter", "Heal", "Cleanse ATK debuff", "Cleanse DEF debuff",
                         "Special CT Reduce", "Critical Hit"],
            "counters": ["ATK Down", "DEF Down"],
            "threats": []
        }
    },

    4137: {
        "id": 4137,
        "name": "Dr. Vegapunk - Grand Dream of the Genius Scientist",
        "type": "INT",
        "classes": ["Cerebral", "Free Spirit"],
        "factions": ["Vegapunk"],
        "ct": 28,
        "special": (
            "Removes 50% Special CT to 1 highest CT enemy.\n"
            "ATK Down lv10 to 2 highest ATK enemies (20s).\n"
            "DEF Down lv10 to 2 highest DEF enemies (20s).\n"
            "40% health cut to 3 highest HP enemies."
        ),
        "gp_burst": (
            "Trigger: When 2 crew defeated.\n"
            "1000 fixed dmg to all enemies."
        ),
        "ability": (
            "HP+DEF lv6 to Cerebral.\n"
            "Special CT lv2 to INT."
        ),
        "leader_skill": (
            "ATK lv3 to crew.\n"
            "HP+SPD lv3 to crew."
        ),
        "leader_buff_filters": {},
        "tags": {
            "inflicts": ["ATK Down", "DEF Down", "Health Cut", "Special CT Remove"],
            "provides": ["HP Up", "DEF Up", "Special CT Up"],
            "counters": [],
            "threats": []
        }
    },

    4133: {
        "id": 4133,
        "name": "Dr. Vegapunk Atlas - PUNK-05",
        "type": "INT",
        "classes": ["Cerebral", "Fighter"],
        "factions": ["Vegapunk"],
        "ct": 33,
        "special": (
            "1.5x ATK to 1 enemy 5 times.\n"
            "Crew 5+: 3.5x ATK to 3 enemies.\n"
            "Crew 5+: 2x ATK ignoring DEF to 1 enemy."
        ),
        "gp_burst": (
            "Trigger: When 2 crew defeated.\n"
            "1000 fixed dmg to all enemies."
        ),
        "ability": (
            "ATK lv5 to INT.\n"
            "SPD+HP lv6 to Cerebral.\n"
            "On hit (limit 5): Special CT lv1 to self."
        ),
        "leader_skill": (
            "ATK lv3 to crew.\n"
            "HP+SPD lv3 to crew."
        ),
        "leader_buff_filters": {},
        "tags": {
            "inflicts": [],
            "provides": ["ATK Up", "SPD Up", "HP Up", "Special CT Up (self)"],
            "counters": [],
            "threats": []
        }
    },

    4082: {
        "id": 4082,
        "name": "Dr. Vegapunk Lilith - PUNK-02",
        "type": "INT",
        "classes": ["Cerebral", "Shooter"],
        "factions": ["Vegapunk"],
        "ct": 26,
        "special": (
            "DOT lv3 to 1 highest HP enemy (20s).\n"
            "ATK+SPD Down lv7 to 1 highest HP enemy (20s).\n"
            "100% Half Stats to 1 highest HP enemy (20s)."
        ),
        "gp_burst": (
            "Trigger: After receiving 55000 damage.\n"
            "ATK Down lv8 to all enemies (20s).\n"
            "DOT lv2 to all enemies (50s).\n"
            "ATK+SPD lv6 to Cerebral and Shooter (30s).\n"
            "Reduces 20% Special CT to crew."
        ),
        "ability": (
            "HP+SPD lv6 to INT.\n"
            "DEF lv5 to INT.\n"
            "Special CT lv2 to Cerebral."
        ),
        "leader_skill": (
            "HP lv2 to INT.\n"
            "ATK+DEF lv4 to INT.\n"
            "Critical Hit+SPD lv3 to Cerebral and Shooter.\n"
            "ATK lv2 to Cerebral and Shooter."
        ),
        "leader_buff_filters": {
            "types": ["INT"],
            "classes": ["Cerebral", "Shooter"],
            "factions": []
        },
        "tags": {
            "inflicts": ["DOT", "ATK Down", "SPD Down", "Half Stats"],
            "provides": ["ATK Up", "SPD Up", "HP Up", "DEF Up", "Special CT Up",
                         "Special CT Reduce"],
            "counters": [],
            "threats": []
        }
    },
}

# ============================================================
# TEAM DEFINITIONS
# ============================================================

ENEMY_TEAMS = {
    "team_imu": {
        "name": "World Government - Five Elders",
        "leader_id": 4571,
        "member_ids": [4491, 4453],
        "description": "Team full STR với Imu leader. Chiến thuật chính: Ability Bind spam + CT manipulation + Half Stats. Cực kỳ tanky với Reduce On Death."
    }
}

PLAYER_BOX = [4560, 4564, 4562, 4492, 4490, 4537, 4558, 4137, 4133, 4082]

# ============================================================
# TYPE MATCHUP TABLE
# ============================================================

TYPE_ADVANTAGE = {
    "STR": {"strong_against": "DEX", "weak_against": "QCK", "neutral": ["PSY", "INT"]},
    "DEX": {"strong_against": "QCK", "weak_against": "STR", "neutral": ["PSY", "INT"]},
    "QCK": {"strong_against": "STR", "weak_against": "DEX", "neutral": ["PSY", "INT"]},
    "PSY": {"strong_against": "INT", "weak_against": "INT", "neutral": ["STR", "DEX", "QCK"]},
    "INT": {"strong_against": "PSY", "weak_against": "PSY", "neutral": ["STR", "DEX", "QCK"]},
}
