from flask import Flask, render_template
import json

app = Flask(__name__)

#Load JSON data
with open("astronauts.json", "r") as f:
	data = json.load(f)
	
@app.route("/")
def home():
	return render_template("home.html")

@app.route("/page1")
def page1():
	#List all astronauts
	astronauts = data
	return render_template("page1.html", astronauts=astronauts)
	
@app.route("/page2")
def page2():
	#List missions with astronauts name
	missions = []
	for astronaut in data:
		for mission in astronaut.get("mission", []):
			missions.append({
				"astronaut": astronaut["Profile"]["Name"],
				"role": mission.get("Role", ""),
				"year": mission.get("Year", ""),
				"name": mission.get("Name", "")
			})
	return render_template("page2.html", missions=missions)
	
@app.route("/page3")
def page3():
	#lifetime stats
	stats = []
	for astronaut in data:
		stats.append({
			"astronaut": astronaut["Profile"]["Name"],
			"missions": astronaut["Profile"]["Lifetime Statistics"]["Mission count"],
			"duration": astronaut["Profile"]["Lifetime Statistics"]["Mission duration"],
			"eva": astronaut["Profile"]["Lifetime Statistics"]["EVA duration"]
		})
	return render_template("page3.html", stats=stats)
	
@app.route("/page4")
def page4():
	#military astronauts
	military = [a for a in data if a["Profile"]["Military"]]
	return render_template("page4.html", military=military)
	
@app.route("/page5")
def page5():
    #nationality counts
    nationality_count = {}
    for astronaut in data:
        nat = astronaut["Profile"]["Nationality"]
        nationality_count[nat] = nationality_count.get(nat, 0) + 1
    return render_template("page5.html", nationality_count=nationality_count)
	
if __name__ == "__main__":
	app.run(debug=True)