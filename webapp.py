from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

#Load JSON data
DATA_FILE = os.path.join(os.path.dirname(__file__), "astronauts.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

#helper: missions list and normal keys
def get_missions(data):
    missions = []
    for astronauts in data:
        profile = astronaut.get("Profile", {})
        name = profile.get("Name", "Unknown")
        for m in astronaut.get("Mission", []) or []:
            missions.append({
                "astronaut": name,
                "role": m.get("Role", ""),
                "year": m.get("Year") or m.get("Mission.Year") or 0,
                "duration": (m.get("Durations", {}) or {}).get("Mission duration", 0.0),
                "eva": (m.get("Durations", {}) or {}).get("EVA duration", 0.0),
                "vehicles": (m.get("Vehicles", {}) or {})
            })
    return missions

def get_lifetime_stats(data):
    stats = []
    for astronaut in data:
        p = astronaut.get("Profile", {})
        stats.append({
            "astronaut": p.get("Name", "Unknown"),
            "missions": (p.get("Lifetime Statistics", {}) or {}).get("Mission count", 0),
            "duration": (p.get("Lifetime Statistics", {}) or {}).get("Mission duration", 0.0),
            "eva": (p.get("Lifetime Statistics", {}) or {}).get("EVA duration", 0.0),
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
    total_missions = sum(
        len(a.get("Mission", []) or []) for a in data
    )
    stats = get_lifetime_stats(data)
    avg_missions = round(sum(s["missions"] for s in stats) / (len(stats) or 1), 2)
    return render_template(
        "home.html",
        total_astronauts=total_astronauts,
        total_missions=total_missions,
        avg_missions=avg_missions,
        nationality_count=nationality_counts(data)
    )

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
    app.run(degub=True)