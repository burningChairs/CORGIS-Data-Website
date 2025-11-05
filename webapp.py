from flask import Flask, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "astronauts.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


def get_missions(data):
    missions = []
    for astronaut in data:
        profile = astronaut.get("Profile", {})
        name = profile.get("Name", "Unknown")
        raw_missions = astronaut.get("Mission", [])
        if not isinstance(raw_missions, list):
            raw_missions = []

        for m in raw_missions:
            if not isinstance(m, dict):
                continue  # Skip malformed mission entries
            durations = m.get("Durations")
            if not isinstance(durations, dict):
                durations = {}

            missions.append({
                "astronaut": name,
                "role": m.get("Role", ""),
                "year": m.get("Year") if isinstance(m.get("Year"), int) else 0,
                "duration": durations.get("Mission duration", 0.0),
                "eva": durations.get("EVA duration", 0.0),
                "vehicles": m.get("Vehicles", {})
            })
    return missions

def get_lifetime_stats(data):
    stats = []
    for astronaut in data:
        profile = astronaut.get("Profile", {})
        lifetime_stats = profile.get("Lifetime Statistics")
        if not isinstance(lifetime_stats, dict):
            lifetime_stats = {}

        stats.append({
            "astronaut": profile.get("Name", "Unknown"),
            "missions": lifetime_stats.get("Mission count", 0),
            "duration": lifetime_stats.get("Mission duration", 0.0),
            "eva": lifetime_stats.get("EVA duration", 0.0),
        })
    return stats

def nationality_counts(data):
    counts = {}
    for astronaut in data:
        nat = (astronaut.get("Profile", {}) or {}).get("Nationality", "Unknown")
        counts[nat] = counts.get(nat, 0) + 1
    return counts

@app.route("/")
def home():
    total_astronauts = len(data)
    total_missions = sum(len(a.get("Mission", []) or []) for a in data)
    stats = get_lifetime_stats(data)
    avg_missions = round(sum(s["missions"] for s in stats) / (len(stats) or 1), 2)
    nationality_count = nationality_counts(data)
    return render_template("home.html",
                           total_astronauts=total_astronauts,
                           total_missions=total_missions,
                           avg_missions=avg_missions,
                           nationality_count=nationality_count)

@app.route("/page1")
def page1():
    #Astronaut list with profile data
    return render_template("page1.html", astronauts=data)

@app.route("/page2")
def page2():
    missions = get_missions(data)
    #send list of astronauts names for filters
    names = sorted({(a.get("Profile", {}) or {}).get("Name", "Unknown") for a in data})
    return render_template("page2.html", missions=missions, astronauts_names=names)
    
@app.route("/page3")
def page3():
    stats = get_lifetime_stats(data)
    return render_template("page3.html", stats=stats)

@app.route("/page4")
def page4():
    military = [a for a in data if (a.get("Profile", {}) or {}).get("Military", False)]
    return render_template("page4.html", military=military)

@app.route("/page5")
def page5():
    counts = nationality_counts(data)
    return render_template("page5.html", nationality_count=counts)

if __name__ == "__main__":
    app.run(debug=True)