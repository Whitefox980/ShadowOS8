# ShadowFox OS8

**ShadowFox OS8** je modularna AI-driven platforma za ofanzivnu bezbednost, fuzzing, strategiju i vizuelnu analizu ranjivosti.

---

## 📦 Struktura Modula

| Modul                 | Opis                                                   |
|----------------------|--------------------------------------------------------|
| `main/runner.py`     | Pokreće generaciju payload-a i scoring (mutation engine) |
| `main/launcher.py`   | Klasični napadni launcher (query-based)                |
| `main/launcher_ai.py`| Smart launcher (query/header/cookie fuzz)              |
| `main/auto_mode.py`  | Glavni operativni režim — sve u jednom                 |

---

## 🧠 AI Sistemi

| Modul                    | Funkcija                                      |
|--------------------------|-----------------------------------------------|
| `tools/ai_advisor.py`    | AI savet na osnovu testiranih payload-a       |
| `tools/black_shadow_advisor.py` | Ofanzivna strategija komandanta         |
| `tools/replay_commander.py`     | Replay HIT-ova za sekundarni napad      |

---

## 📊 Vizuelizacija

| Modul                    | Opis                                          |
|--------------------------|-----------------------------------------------|
| `tools/vizualizacija.py` | Pie chart po tipu ranjivosti                  |
| `tools/radar_chart.py`   | Prosečan score po tipu (radar dijagram)       |

---

## 📁 Misije i Izveštaji

- Svaka misija se automatski pakuje u `missions/mission_<timestamp>/`
- Svi fajlovi su dostupni preko lokalnog browsera (FrontGate)

Pokretanje:

```bash
python3 main/auto_mode.py
