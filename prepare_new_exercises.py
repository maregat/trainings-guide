#!/usr/bin/env python3
"""
Script to prepare 25 new exercises for the athletic training plan.
Preview before saving to exercises.json
"""

import json

# New exercises to be added
new_category = {
    "warmup_fifa11": {
        "name": "Aufwärmen & FIFA 11+ Kids",
        "description": "FIFA 11+ Kids Programme und Aufwärm-Übungen für Verletzungsprävention und Koordination",
        "order": 0,
        "phase": "warmup"
    }
}

# FIFA 11+ Kids Übungen (7)
fifa_exercises = {
    "fifa_lauf_stopp_spiel": {
        "id": "fifa_lauf_stopp_spiel",
        "name": "FIFA 1: Lauf-Stopp-Spiel",
        "category": "warmup_fifa11",
        "description": "Auf Signal plötzlich auf einem Bein stehen und Balance halten (3 Sek). Auf Signal plötzlich auf einem Bein stehen. Niveau 1-5 je nach Schwierigkeit",
        "duration": "3 Sätze à 5 Stopps",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_skating_sprünge": {
        "id": "fifa_skating_sprünge",
        "name": "FIFA 2: Skating-Sprünge",
        "category": "warmup_fifa11",
        "description": "Seitlich-vorwärts von Bein zu Bein springen, weich landen. Nach der Landung kurz stabil stehen.",
        "duration": "2 Sätze à 10 Sprünge (5 pro Bein)",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_einbeinstand_ball": {
        "id": "fifa_einbeinstand_ball",
        "name": "FIFA 3: Einbeinstand mit Ball (Wand)",
        "category": "warmup_fifa11",
        "description": "Auf einem Bein stehen, Ball an die Wand werfen und fangen. Verschiedene Niveau-Varianten. Je Bein 1 Satz.",
        "duration": "Je Bein 20-30 Sekunden",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_liegestütz_variation": {
        "id": "fifa_liegestütz_variation",
        "name": "FIFA 4: Liegestütz-Variation",
        "category": "warmup_fifa11",
        "description": "Hoher Stütz, abwechselnd eine Hand zur Schulter tippen (ersetzt Tunnelübung). Verschiedene Varianten für Level 1-5.",
        "duration": "3 Sätze à 15 Sekunden",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_einbeinsprünge": {
        "id": "fifa_einbeinsprünge",
        "name": "FIFA 5: Einbeinsprünge",
        "category": "warmup_fifa11",
        "description": "Auf einem Bein springen, auf demselben Bein landen und 3 Sekunden halten. Verschiedene Richtungen und Varianten.",
        "duration": "2 Sätze à 5 Sprünge pro Bein",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_spiderman": {
        "id": "fifa_spiderman",
        "name": "FIFA 6: Spiderman",
        "category": "warmup_fifa11",
        "description": "Krebsgang: Bauch nach oben, Hände nach hinten, Füße nach vorn bis zur Streckung. Verschiedene Varianten und Levelsteigerungen.",
        "duration": "3 Sätze à 15 Sekunden (Level 3: 5-10m Krebsgang)",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "fifa_band_pull_apart": {
        "id": "fifa_band_pull_apart",
        "name": "FIFA 7: Band-Pull-Apart",
        "category": "warmup_fifa11",
        "description": "Band mit beiden Händen schulterbreit halten, auseinanderziehen bis Arme seitlich auf Schulterhöhe sind. Schulterblätter zusammenziehen. Ersatz für seitliche Rolle.",
        "duration": "1 Satz à 10-12 Wiederholungen",
        "videoLink": {
            "url": None,
            "title": None
        },
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    }
}

# Kraft & Stabilität - neue Übungen (18)
strength_exercises = {
    "str_hockstand_sprung": {
        "id": "str_hockstand_sprung",
        "name": "Hockstand-Sprung",
        "category": "strength_stability",
        "description": "Aus leichter Hocke nach oben springen, in der Hocke weich landen und 2 Sekunden ruhig stehen. Knie über den Füßen.",
        "duration": "2 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_box_jump": {
        "id": "str_box_jump",
        "name": "Box Jump (Stepper)",
        "category": "strength_stability",
        "description": "Aus leichter Hocke beidbeinig auf den Stepper (20cm) springen, weich landen (Knie über Füßen, leise). Nach dem Springen Füße einzeln herabsteigen (nicht herunterspringen).",
        "duration": "1-2 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_kniebeuge": {
        "id": "str_kniebeuge",
        "name": "Kniebeuge",
        "category": "strength_stability",
        "description": "Füße schulterbreit, Gesäß nach hinten unten, Knie über den Fußspitzen, Brust offen, Arme nach vorn. Tiefe so weit wie sauber möglich.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_ausfallschritt_rückwärts": {
        "id": "str_ausfallschritt_rückwärts",
        "name": "Ausfallschritt rückwärts",
        "category": "strength_stability",
        "description": "Schritt nach hinten, hinteres Knie zum Boden, vorderes Knie über dem Fuß, mit dem vorderen Bein zurückdrücken.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_step_up": {
        "id": "str_step_up",
        "name": "Step-up",
        "category": "strength_stability",
        "description": "Fuß ganz auf die Stufe, ohne Schwung hochdrücken, kontrolliert absenken. Stufe 20-30cm hoch.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_mini_band_seitschritte": {
        "id": "str_mini_band_seitschritte",
        "name": "Mini-Band-Seitschritte",
        "category": "strength_stability",
        "description": "Mini-Band über den Knien tragen, leicht gebeugt, seitlich gehen. Füße parallel, Knie nicht einknicken.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_rumänisches_kreuzheben": {
        "id": "str_rumänisches_kreuzheben",
        "name": "Rumänisches Kreuzheben",
        "category": "strength_stability",
        "description": "Mit Eigengewicht: Gesäß nach hinten schieben, Rücken gerade, Oberkörper kippt vor bis zur Oberschenkelrückseite spannt. Optional einbeinig.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_rudern_band": {
        "id": "str_rudern_band",
        "name": "Rudern mit Band",
        "category": "strength_stability",
        "description": "Band an einer Tür auf Brusthöhe befestigen. Schulterblätter zusammenziehen, Ellbogen am Körper. Aktiviert oberen Rücken.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_dead_bug": {
        "id": "str_dead_bug",
        "name": "Dead Bug",
        "category": "strength_stability",
        "description": "Rückenlage, Arme zur Decke, Knie 90°. Gegenüberliegende Arm und Bein langsam strecken. Unterer Rücken bleibt am Boden.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_einbeinige_kniebeuge_bank": {
        "id": "str_einbeinige_kniebeuge_bank",
        "name": "Einbeinige Kniebeuge zur Bank",
        "category": "strength_stability",
        "description": "Auf einem Bein stehen, Gesäß kontrolliert zur Bank hinten absenken, kurz antippen, aufstehen. Freies Bein vorn.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_laufschule": {
        "id": "str_laufschule",
        "name": "Laufschule",
        "category": "strength_stability",
        "description": "Laufschule Übungen: Skipping (Kniehub), Anfersen, Seitgalopp. Kurz, rhythmisch, hohe Frequenz.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_richtungswechsel_stopp": {
        "id": "str_richtungswechsel_stopp",
        "name": "Richtungswechsel mit Stopp",
        "category": "strength_stability",
        "description": "Zwei Kegel 5m auseinander. Zügig laufen, tief abbremsen, wenden. Knie über dem Fuß, langsam in Woche 1-2.",
        "duration": "4-6 Läufe",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_bird_dog": {
        "id": "str_bird_dog",
        "name": "Bird-Dog",
        "category": "strength_stability",
        "description": "Vierfüßler-Position, gegenüberliegenden Arm und Bein strecken. Becken bleibt ruhig.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    }
}

# Aufwärm-Übungen (4)
warmup_exercises = {
    "str_warm_traben": {
        "id": "str_warm_traben",
        "name": "Locker traben",
        "category": "strength_stability",
        "description": "Lockerer Ausdauerlauf zum Aufwärmen und Pulserhöhung.",
        "duration": "5-10 Minuten",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_beinschwünge": {
        "id": "str_beinschwünge",
        "name": "Beinschwünge",
        "category": "strength_stability",
        "description": "Dynamisches Aufwärmen: Beinschwünge nach vorne, hinten und zur Seite.",
        "duration": "10-15 Wiederholungen pro Bein",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_hüftkreisen": {
        "id": "str_hüftkreisen",
        "name": "Hüftkreisen",
        "category": "strength_stability",
        "description": "Hüfte in großen Kreisen bewegen, beide Richtungen.",
        "duration": "10-15 Wiederholungen pro Richtung",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    },
    "str_hocke": {
        "id": "str_hocke",
        "name": "Hocke (Squat Hold)",
        "category": "strength_stability",
        "description": "In der Hocke halten, dynamisch hin- und herbewegen. Aufwärmen für Beine und Hüfte.",
        "duration": "20-30 Sekunden",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    }
}

# Seilspringen (neue Variante für Athletik-Plan)
seilspringen_exercise = {
    "str_seilspringen": {
        "id": "str_seilspringen",
        "name": "Seilspringen",
        "category": "strength_stability",
        "description": "Kleine Sprünge über den Vorfuß, Knie weich, locker bleiben. Ohne Seil auch als imaginäres Seil möglich.",
        "duration": "2-3 Sätze",
        "videoLink": {"url": None, "title": None},
        "poster": None,
        "published": True,
        "isPartnerExercise": False
    }
}

# Combine all new exercises
all_new_exercises = {
    **fifa_exercises,
    **strength_exercises,
    **warmup_exercises,
    **seilspringen_exercise
}

print("=" * 80)
print("NEUE ÜBUNGEN FÜR ATHLETIK-PLAN: PREVIEW")
print("=" * 80)
print()
print(f"✅ Neue Kategorie: {len(new_category)} Kategorie")
for cat_id, cat_data in new_category.items():
    print(f"   - {cat_id}: {cat_data['name']}")
print()
print(f"✅ Neue Übungen: {len(all_new_exercises)} insgesamt")
print()
print("FIFA 11+ Kids (7):")
for ex_id in fifa_exercises.keys():
    print(f"   - {ex_id}")
print()
print("Kraft & Stabilität (13):")
for ex_id in strength_exercises.keys():
    print(f"   - {ex_id}")
print()
print("Aufwärmen (4):")
for ex_id in warmup_exercises.keys():
    print(f"   - {ex_id}")
print()
print("Sonstiges (1):")
for ex_id in seilspringen_exercise.keys():
    print(f"   - {ex_id}")
print()
print("=" * 80)
print()
print("DETAIL SAMPLE: FIFA 1")
print(json.dumps(fifa_exercises["fifa_lauf_stopp_spiel"], indent=2, ensure_ascii=False))
print()
print("DETAIL SAMPLE: Kraft - Hockstand-Sprung")
print(json.dumps(strength_exercises["str_hockstand_sprung"], indent=2, ensure_ascii=False))
print()
print("=" * 80)
print("✅ Preview complete. All new exercises ready to be added.")
print("=" * 80)

# Save preview as JSON for verification
preview_data = {
    "new_category": new_category,
    "new_exercises": all_new_exercises,
    "summary": {
        "total_new_exercises": len(all_new_exercises),
        "fifa_exercises": len(fifa_exercises),
        "strength_exercises": len(strength_exercises),
        "warmup_exercises": len(warmup_exercises),
        "other_exercises": len(seilspringen_exercise)
    }
}

with open('/tmp/new_exercises_preview.json', 'w', encoding='utf-8') as f:
    json.dump(preview_data, f, indent=2, ensure_ascii=False)

print("\n✅ Preview saved to /tmp/new_exercises_preview.json")
