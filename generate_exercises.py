#!/usr/bin/env python3
"""
Generate comprehensive exercises.json from PDF structure
Includes: Warm-Up (Koordination + Coerver), then main exercise categories
"""

import json
from datetime import datetime

def create_exercise(id, category, order, name, description, duration, 
                   setup_equipment=None, setup_space=None, setup_solo=True,
                   technique_points=None, technique_focus=None, 
                   mistakes=None, coaching_tips=None, partner=False, subCategory=None):
    """Helper to create exercise objects"""
    exercise = {
        "id": id,
        "category": category,
        "order": order,
        "name": name,
        "description": description,
        "duration": duration,
        "setup": {
            "equipment": setup_equipment or [],
            "space": setup_space or "Minimal",
            "solo": setup_solo,
            "partner": partner
        },
        "technique": {
            "keyPoints": technique_points or [],
            "focus": technique_focus or ""
        },
        "commonMistakes": mistakes or [],
        "coachingTips": {
            "observation": coaching_tips or "",
            "scaling_easier": "",
            "scaling_harder": "",
            "motivation": ""
        },
        "progressionPath": [],
        "videoLink": {
            "url": None,
            "title": None
        }
    }
    if subCategory:
        exercise["subCategory"] = subCategory
    return exercise

# ============================================
# BUILD MAIN DATA STRUCTURE
# ============================================

exercises_data = {
    "metadata": {
        "version": "2.0",
        "ageGroup": "U11/U12",
        "skillLevel": "competitive",
        "lastUpdated": datetime.now().isoformat(),
        "totalExercises": 0,
        "sources": [
            "Coerver Coaching Method",
            "DFB Trainingsmethodik",
            "UEFA Youth Development",
            "Fußball-Grundlagen im Garten"
        ],
        "structure": "Warm-Up (Koordination + Coerver) → Schwerpunkt-Übungen"
    },
    "categories": {
        "warmup_coordination": {
            "name": "Warm-Up – Koordination (ohne Ball)",
            "description": "Reine Koordinationsübungen – guter allererster Programmpunkt um Puls und Beine zu aktivieren",
            "order": 0,
            "phase": "warmup"
        },
        "warmup_coerver": {
            "name": "Warm-Up – Ballgefühl (Coerver)",
            "description": "Basis-Übungen (täglich) + rotierende Coerver-Sets (1 pro Woche)",
            "order": 1,
            "phase": "warmup"
        },
        "firstTouch": {
            "name": "First Touch (Ballannahme)",
            "description": "Der erste Kontakt entscheidet oft über Zeitgewinn im Spiel",
            "order": 2,
            "phase": "main"
        },
        "ballIntake": {
            "name": "Ballmitnahme",
            "description": "Annahme kombiniert mit sofortiger Richtungsänderung",
            "order": 3,
            "phase": "main"
        },
        "ballControl": {
            "name": "Ballführung",
            "description": "Enger Ballkontakt in Bewegung",
            "order": 4,
            "phase": "main"
        },
        "dribbling": {
            "name": "Dribbling (mit Hütchen)",
            "description": "Klassische Hütchen-Parcours für Ballkontrolle und Finten",
            "order": 5,
            "phase": "main"
        },
        "directionChange": {
            "name": "Richtungswechsel (mit Hütchen)",
            "description": "Simulieren typische Spielsituationen besser als reines Slalomdribbling",
            "order": 6,
            "phase": "main"
        },
        "juggling": {
            "name": "Juggling (Hochhalten)",
            "description": "Schult vor allem Ballgefühl und Koordination",
            "order": 7,
            "phase": "main"
        }
    },
    "exercises": {}
}

# ============================================
# WARM-UP: KOORDINATION (OHNE BALL)
# ============================================

warmup_coo = [
    ("coo_line_jump_single", "Seitliches Linienspringen – einbeinig",
     "Auf einem Bein seitlich über eine Linie hin- und herspringen. Rechtes und linkes Bein getrennt üben.",
     "60-90 Sekunden pro Bein", ["Linie oder Kreppband"], "Minimal (2-3m)",
     ["Auf einem Bein stehen", "Seitlich über Linie springen", "Rhythmischer Wechsel"], "Einbeinige Balance"),
    
    ("coo_line_jump_both", "Seitliches Linienspringen – beidbeinig",
     "Mit geschlossenen Füßen seitlich über die Linie hin- und herspringen, zügiger Rhythmus.",
     "60-90 Sekunden", ["Linie oder Kreppband"], "Minimal (2-3m)",
     ["Füße geschlossen", "Zügiger Rhythmus", "Explosivität"], "Schnellkraft"),
    
    ("coo_line_jump_forward", "Linienspringen vor/zurück",
     "Beidbeinig vorwärts über die Linie springen, dann rückwärts zurück.",
     "60-90 Sekunden", ["Linie oder Kreppband"], "Minimal (2-3m)",
     ["Schnelle Bodenkontakte", "Gerader Sprung", "Richtungswechsel"], "Schnellkraft"),
    
    ("coo_ladder_one_per_field", "Koordinationsleiter – Ein Kontakt pro Feld",
     "Mit schnellen Schritten durch jedes Feld der Leiter laufen.",
     "60-90 Sekunden", ["Koordinationsleiter"], "Leiter (5-7m lang)",
     ["Schnelle Fußaufsätze", "Ein Fuß pro Feld", "Fokus auf Geschwindigkeit"], "Fußgeschwindigkeit"),
    
    ("coo_ladder_two_per_field", "Koordinationsleiter – Zwei Kontakte pro Feld",
     "Mit zwei Schritten pro Feld durch die Leiter laufen.",
     "60-90 Sekunden", ["Koordinationsleiter"], "Leiter (5-7m lang)",
     ["Zwei Schritte pro Feld", "Gleichmäßiger Rhythmus", "Kontrolle"], "Rhythmusgefühl"),
    
    ("coo_ladder_sidestep", "Koordinationsleiter – Seitwärts (Sidestep)",
     "Seitlich, mit dem Körper quer zur Leiter, durch jedes Feld steigen.",
     "60-90 Sekunden", ["Koordinationsleiter"], "Leiter (5-7m lang)",
     ["Seitliche Bewegung", "Körper quer zur Leiter", "Kontrollierte Schritte"], "Seitliche Beweglichkeit"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in warmup_coo:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "warmup_coordination", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# WARM-UP: COERVER BASIS (TÄGLICH)
# ============================================

basis_exercises = [
    ("coo_basis_toe_taps", "Toe-Taps",
     "Ball abwechselnd mit den Fußspitzen von oben antippen.",
     "40 Sekunden (+ 20 Sek Pause)", ["Fußball"], "Minimal",
     ["Fußspitzen oben", "Abwechselnd rechts-links", "Rhythmisches Tempo"], "Fußspitzen-Kontrolle"),
    
    ("coo_basis_football_dance", "Football Dance",
     "Ball in schnellem Fußwechsel antippen – tänzelnde, rhythmische Bewegung.",
     "40 Sekunden (+ 20 Sek Pause)", ["Fußball"], "Minimal",
     ["Schnelle Wechsel", "Tänzelnde Bewegung", "Rhythmus"], "Fußgeschwindigkeit"),
    
    ("coo_basis_ball_roll", "Ball zwischen den Füßen rollen",
     "Im Stehen den Ball mit Sohle abwechselnd hin- und herrollen.",
     "40 Sekunden (+ 20 Sek Pause)", ["Fußball"], "Minimal",
     ["Sohle kontrolliert", "Abwechselnde Füße", "Rollbewegung"], "Sohlengefühl"),
    
    ("coo_basis_sole_pullpush", "Sohle drauf – Pull-Push",
     "Ball mit der Sohle antippen und sofort wieder wegziehen.",
     "40 Sekunden (+ 20 Sek Pause)", ["Fußball"], "Minimal",
     ["Sohle oben", "Schnelle Bewegung", "Auf der Stelle"], "Sohlen-Reaktion"),
    
    ("coo_basis_inside_outside", "Innenseite-Außenseite-Tipping",
     "Ball auf der Stelle abwechselnd mit Innen- und Außenseite antippen.",
     "40 Sekunden (+ 20 Sek Pause)", ["Fußball"], "Minimal",
     ["Innenseite-Außenseite Wechsel", "Rhythmisch", "Auf der Stelle"], "Fußseitenkontrolle"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in basis_exercises:
    ex = create_exercise(
        ex_id, "warmup_coerver", order, name, desc, duration,
        equipment, space, True, points, focus, subCategory="basis"
    )
    exercises_data["exercises"][ex_id] = ex
    order += 1

# ============================================
# WARM-UP: COERVER ROTATION SETS
# ============================================

coerver_sets = {
    "set1": {
        "title": "Continuous Scissors, Sole Drag, Triple Sole Drag",
        "moves": ["Continuous Scissors", "Sole Drag", "Triple Sole Drag"]
    },
    "set2": {
        "title": "Sole Drag Kombis + The V Inside",
        "moves": ["Sole Drag + Inside Push", "Sole Drag + Outside Push", "The V – Inside"]
    },
    "set3": {
        "title": "The V Outside + Pull-Push Instep",
        "moves": ["The V – Outside", "Pull-Push Instep (rechts)", "Pull-Push Instep (links)", "Triple Pull-Push"]
    },
    "set4": {
        "title": "Rollover, Stop, Inside, Cuts",
        "moves": ["Rollover + Stop + Inside", "Stop + Slide", "Inside Cut", "Outside Push (Messi)"]
    },
    "set5": {
        "title": "Rollover, Stop Instep, The L, Step Over",
        "moves": ["Rollover + Stop Instep", "The L (rechts)", "The L (links)", "Step Over"]
    },
    "set6": {
        "title": "Around Cones – Horizontal & Vertikal",
        "moves": ["Around Two Cones (horizontal)", "Around Two Cones (vertikal)", "Around Four Cones"]
    }
}

order = 6
for set_num, set_data in coerver_sets.items():
    set_order = int(set_num[-1])
    for move_idx, move_name in enumerate(set_data["moves"], 1):
        ex_id = f"coo_set{set_order}_move{move_idx}"
        ex = create_exercise(
            ex_id, "warmup_coerver", order, move_name,
            f"Coerver Set {set_order}: {set_data['title']}",
            "40 Sekunden (+ 20 Sek Pause)",
            ["Fußball", "Optional: Hütchen"],
            "Minimal bis 10x10m",
            True,
            ["Siehe Coerver-Referenz"],
            "Ballkontrolle & Finesse",
            subCategory="rotation"
        )
        exercises_data["exercises"][ex_id] = ex
        order += 1

# ============================================
# FIRST TOUCH (BALLANNAHME)
# ============================================

first_touch = [
    ("ft_wall_reception", "Wandpass-Annahme",
     "Ball gegen eine Wand schießen und sofort kontrolliert annehmen.",
     "10-15 Minuten", ["Fußball", "Wand"], "Wand",
     ["Kontrolle beim Annehmen", "Passhärte variieren", "Verschiedene Annahmeflächen"],
     "First Touch Kontrolle", None),
    
    ("ft_throw_reception", "Hochwurf-Annahme",
     "Ball hochwerfen und mit Innenseite, Spann, Brust, Oberschenkel annehmen.",
     "10-15 Minuten", ["Fußball"], "Freifläche",
     ["Verschiedene Annahmestellen", "Höhen variieren", "Weiche Annahme"],
     "Multi-Surface First Touch", None),
    
    ("ft_partner_pass", "Partnerpässe – Verschiedene Höhen",
     "Partner wirft Ball aus verschiedenen Höhen; Spieler nimmt an.",
     "15 Minuten", ["Fußball"], "Freifläche",
     ["Reaktion", "Anpassung", "Ballkontrolle"],
     "First Touch unter Realitätsbedingungen", [{
        "mistake": "Zu steifer Kontakt",
        "consequence": "Ball springt weg",
        "correction": "Beim Annehmen 'nachgeben'"
    }]),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus, mistakes in first_touch:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "firstTouch", order, name, desc, duration,
        equipment, space, True, points, focus, mistakes
    )
    order += 1

# ============================================
# BALLMITNAHME
# ============================================

ball_intake = [
    ("bi_wall_rotation", "Wand-Mitnahme mit Drehung",
     "Ball an die Wand spielen, mit erstem Kontakt um 90° oder 180° wegdrehen.",
     "10-15 Minuten", ["Fußball", "Wand"], "Wand",
     ["Erste Kontrolle mit Richtung", "90°/180° Drehung", "Flüssige Bewegung"],
     "Mitnahme mit Richtungswechsel"),
    
    ("bi_cone_intake", "Hütchen-Mitnahme",
     "Zugespielten Ball mit erstem Kontakt gezielt in Richtung eines Hütchens mitnehmen.",
     "10-15 Minuten", ["Fußball", "Hütchen (3-4)"], "Freifläche",
     ["Zielgerichtete Mitnahme", "First Touch mit Richtung", "Präzision"],
     "Mitnahme in freien Raum"),
    
    ("bi_pressure_timing", "Mitnahme unter Zeitdruck",
     "Nach Signal (Klatschen/Pfeife) Mitnahme so schnell wie möglich.",
     "10-15 Minuten", ["Fußball"], "Freifläche",
     ["Schnelle Reaktion", "Explosive Mitnahme", "Richtungskontrolle"],
     "Mitnahme unter Spieldruck"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in ball_intake:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "ballIntake", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# BALLFÜHRUNG
# ============================================

ball_control = [
    ("bc_straight_line", "Geradliniges Dribbeln – Parcours",
     "Ball in gerader Linie führen, verschiedene Fußflächen nutzen (Innen, Außen, Spann).",
     "10-15 Minuten", ["Fußball", "Hütchen"], "Freifläche 10-15m",
     ["Enger Ballkontakt", "Fußwechsel", "Kopf oben"],
     "Enger Ballkontakt"),
    
    ("bc_zig_zag", "Zig-Zag-Dribbeln",
     "Zwischen zwei Hütchenreihen dribbeln, Ball unter Kontrolle halten.",
     "10-15 Minuten", ["Fußball", "Hütchen (6-8)"], "Freifläche 10-15m",
     ["Geschwindigkeit variabel", "Ballkontakt eng", "Richtungskontrolle"],
     "Ballführung mit Richtungswechsel"),
    
    ("bc_slalom", "Slalom-Dribbeln",
     "In Slalomlinie um Hütchen dribbeln – maximale Ballkontrolle.",
     "10-15 Minuten", ["Fußball", "Hütchen (5-6)"], "Freifläche 10-15m",
     ["Kurze Ballkontakte", "Hüftbewegung", "Dynamische Positionierung"],
     "Enge Ballkontrolle"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in ball_control:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "ballControl", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# DRIBBLING (MIT HÜTCHEN)
# ============================================

dribbling = [
    ("dr_speed_line", "Sprint-Dribbling – Geradlinie",
     "Ball auf Geschwindigkeit führen über längere Strecke (20-30m).",
     "10-15 Minuten", ["Fußball", "Hütchen"], "Freifläche 20-30m",
     ["Schnelligkeit", "Ballkontakt nicht verlieren", "Kopf oben"],
     "Schnelligkeit mit Ball"),
    
    ("dr_box_drill", "Hütchen-Box-Drill",
     "Um vier Hütchen in Box-Formation dribbeln, verschiedene Geschwindigkeiten.",
     "15-20 Minuten", ["Fußball", "Hütchen (4)"], "Freifläche 10x10m",
     ["Richtungswechsel", "Ballkontrolle", "Beschleunigung"],
     "Dribbling mit Wendungen"),
    
    ("dr_cone_weave", "Slalom zwischen Hütchen",
     "Präzisions-Dribbling durch mehrere in Reihe stehende Hütchen.",
     "10-15 Minuten", ["Fußball", "Hütchen (6-8)"], "Freifläche",
     ["Fußtechnik", "Richtungswechsel", "Ballkontakt"],
     "Präzisions-Dribbling"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in dribbling:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "dribbling", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# RICHTUNGSWECHSEL (MIT HÜTCHEN)
# ============================================

direction_change = [
    ("dc_90_degree", "90°-Wechsel – Hütchen",
     "Auf Hütchen zuspielen, Spieler nimmt an und dreht 90° ab.",
     "15 Minuten", ["Fußball", "Hütchen (4-5)"], "Freifläche 15x15m",
     ["Schnelle Drehung", "First Touch mit Richtung", "Explosivität"],
     "Schnelle Richtungswechsel"),
    
    ("dc_180_turn", "180°-Wende – Ballkontakt",
     "Ball führen, auf Signal schnelle 180°-Drehung ohne Ball zu verlieren.",
     "10-15 Minuten", ["Fußball", "Hütchen"], "Freifläche",
     ["Schnelle Wendung", "Ballkontrolle", "Balance"],
     "Enge Wendungen"),
    
    ("dc_cut_back", "Cut-Back (Rückpass-Simulation)",
     "Dribbeln, dann schneller Rückpass in neuer Richtung.",
     "15 Minuten", ["Fußball", "Hütchen (3-4)"], "Freifläche",
     ["Ballkontrolle", "Passe präzise", "Timing"],
     "Spielrealistische Richtungswechsel"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in direction_change:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "directionChange", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# JUGGLING (HOCHHALTEN)
# ============================================

juggling = [
    ("jgl_sole_to_instep", "Sohle-Spann-Wechsel",
     "Ball mit Sohle antippen, dann mit Spann hochhalten – Wechsel.",
     "5-10 Minuten", ["Fußball"], "Minimal",
     ["Sohlenkontakt", "Spann-Kontrolle", "Rhythmus"],
     "Fußseitenkontrolle"),
    
    ("jgl_alternating_feet", "Abwechselnd beide Füße",
     "Ball abwechselnd mit rechts und links hochhalten.",
     "5-10 Minuten", ["Fußball"], "Minimal",
     ["Abwechselnder Rhythmus", "Balance", "Höhenkontrolle"],
     "Beidbeiniges Hochhalten"),
    
    ("jgl_inside_outside", "Innenseite-Außenseite",
     "Ball nur mit Innen- und Außenseite (kein Spann) hochhalten.",
     "5-10 Minuten", ["Fußball"], "Minimal",
     ["Innen-Außen Wechsel", "Höhenkontrolle", "Rhythmus"],
     "Spezielle Fußseiten-Kontrolle"),
    
    ("jgl_thigh_chest", "Oberschenkel-Brust-Variation",
     "Ball mit Oberschenkel oder Brust miteinbeziehen (nicht nur Fuß).",
     "5-10 Minuten", ["Fußball"], "Minimal",
     ["Multi-Surface Kontrolle", "Balance", "Koordination"],
     "Ganzkörper-Ballkontrolle"),
]

order = 1
for ex_id, name, desc, duration, equipment, space, points, focus in juggling:
    exercises_data["exercises"][ex_id] = create_exercise(
        ex_id, "juggling", order, name, desc, duration,
        equipment, space, True, points, focus
    )
    order += 1

# ============================================
# COUNT & SAVE
# ============================================

exercises_data["metadata"]["totalExercises"] = len(exercises_data["exercises"])

# Pretty print to file
output_path = "exercises.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(exercises_data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(exercises_data['exercises'])} exercises to {output_path}")
print(f"\nStructure:")
print(f"  Warm-Up Koordination: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'warmup_coordination')}")
print(f"  Warm-Up Coerver: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'warmup_coerver')}")
print(f"  First Touch: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'firstTouch')}")
print(f"  Ballmitnahme: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'ballIntake')}")
print(f"  Ballführung: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'ballControl')}")
print(f"  Dribbling: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'dribbling')}")
print(f"  Richtungswechsel: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'directionChange')}")
print(f"  Juggling: {sum(1 for e in exercises_data['exercises'].values() if e['category'] == 'juggling')}")
