from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        risk_factors = {
            "A.I": sport_to_ai_or_aii(request.form["sport"]),
            "B": float(request.form["b"]),
            "C": float(request.form["c"]),
            "D": float(request.form["d"]),
            "E": float(request.form["e"]),
            "F": float(request.form["f"]),
            "G": float(request.form["g"])
        }
        workouts = generate_workouts(risk_factors)
        return render_template("index.html", workouts=workouts)
    return render_template("index.html")

def generate_workouts(risk_factors):
    workout_list = {
        "A.I": ["1 Mile Run", "3 Mile Run", "Star Drill"],
        "A.II": ["Box Drill", "40 Yard Sprints (2x5 with max rest in between sets)", "300 Meter Shuttle (4 Sets with same rest as time spent running)"],
        "B": ["Romanian Deadlift (RDL) (4x10 with controlled pace)", "Deadlift (4x10 with controlled pace)", "Hamstring Curls (4x10 with controlled pace)"],
        "C": ["Plank (1 min for 3 sets)", "Plank on med ball (1 min for 3 sets)", "Side Plank (1 min for 3 sets)", "Pallof press (30 seconds for 3 sets)", "Dead bugs (3x10 ea side)"],
        "D": ["Drop jump (3x10)", "Single leg drop to 3 second hold (3x8)", "Double leg drop to landing position (3x10)"],
        "E": ["Weighted side lunges (4x10)", "Banded lateral leg extension (4x15)", "Banded good mornings (4x12)"],
        "F": ["Single leg RDL (3x12 with controlled pace)", "Single leg hamstring (3x12 with controlled pace)"],
        "G": ["Single leg bulgarian split squats (3x12)", "Split squats (3x12)"]
    }
    #First, choose 4 random workouts from A.I or A.II based on sport
    workout_list_workouts = workout_list[risk_factors["A.I"]]
    #Error above: UnboundLocalError: cannot access local variable 'workout_list' where it is not associated with a value
    #Working code:
    # workout_list_workouts = workout_list["A.I"]
    #Now, we choose 4 random workouts
    # They can be repeated, so choose 1 four times
    workouts_mylist = []
    for i in range(4):
        workouts_mylist.append(random.choice(workout_list_workouts))

    #Now, we choose 16 workouts from the other factors
    #The lower a factor is on the percentile score, the more likely it is to be chosen
    #Percentiles for the factors: A.I Aerobic activity (Soccer, Lacrosse, Nordic)
    # A.II Aerobic activity (Football, Basketball, Volleyball, Baseball, lacrosse downhill skiing)
    # B Hamstring/Quad Strength Ratio: (1st percentile= .46 ) (25th percentile= .52) (50th percentile= .58) (75th percentile= .64) (99th percentile= .70)
    # C Core stability: Time to stabilization for single leg stand and hold(S) (1st percentile=1.70)(25th percentile=1.45)(50th percentile=1.20)(75th percentile=.95)(99th percentile=0.70)
    # D Landing biomechanics: RSI (1st percentile= 1.00)(25th percentile= 1.63)(50th percentile= 1.99)(75th percentile= 2.55)(99th percentile= 3.48)
    # E Adduction/Abduction Strength Ratio: (1st percentile= 1.43)(25th percentile=1.14)(50th percentile=1.03)(75th percentile=.90)(99th percentile=.63)
    # F Muscular Asymmetries - Hamstring (1st percentile= 25)(25th percentile=18.75)(50th percentile=12.5)(75th percentile=6.25)(99th percentile=0)
    # G Muscular asymmetries - Abductor (1st percentile= 25)(25th percentile=18.75)(50th percentile=12.5)(75th percentile=6.25)(99th percentile=0)

    workouts = workouts_mylist
    percentiles = []
    total_percentile_score = 0
    #calculate percentiles for each factor
    for k, v in risk_factors.items():
        #Ignore A.I
        if k == "A.I":
            continue

        #Calculate percentile
        percentile = calculate_percentile(k,v)
        #Now, get a percentage of 16
        percentiles.append([k, 100-percentile])
        total_percentile_score += 100-percentile

    #Loop over and get the percentage of the total for each
    for k, v in percentiles:
        percent = v/total_percentile_score
        #Get a number from dividing by 16
        number = int(percent*16)
        #Add that many workouts to the list
        wotkout_options = workout_list[k]
        for i in range(number):
            workouts.append(random.choice(wotkout_options))
    print("WORKOUTS: ", workouts)
    return workouts
def calculate_percentile(name, value):
    if name == "B":
        if value <= 0.46:
            return 1
        elif value <= 0.52:
            return 25
        elif value <= 0.58:
            return 50
        elif value <= 0.64:
            return 75
        else:
            return 99
    elif name == "C":
        if value >= 1.70:
            return 1
        elif value >= 1.45:
            return 25
        elif value >= 1.20:
            return 50
        elif value >= 0.95:
            return 75
        else:
            return 99
    elif name == "D":
        if value >= 3.48:
            return 1
        elif value >= 2.55:
            return 25
        elif value >= 1.99:
            return 50
        elif value >= 1.63:
            return 75
        else:
            return 99
    elif name == "E":
        if value >= 1.43:
            return 1
        elif value >= 1.14:
            return 25
        elif value >= 1.03:
            return 50
        elif value >= 0.90:
            return 75
        else:
            return 99
    elif name == "F" or name == "G":
        if value >= 25:
            return 1
        elif value >= 18.75:
            return 25
        elif value >= 12.5:
            return 50
        elif value >= 6.25:
            return 75
        else:
            return 99


def sport_to_ai_or_aii(sport):
    if sport.lower() in ['soccer', 'lacrosse', 'nordic']:
        return 'A.I'
    elif sport.lower() in ['football', 'basketball', 'volleyball', 'baseball', 'lacrosse', 'downhill skiing']:
        return 'A.II'

    generated_workouts = {k: [] for k in workout_list}

    for k, v in workout_percentages.items():
        num_exercises = round(v * 20)
        exercises = random.sample(workout_list[k], len(workout_list[k]))
        for _ in range(num_exercises):
            generated_workouts[k].append(random.choice(exercises))

    return generated_workouts

if __name__ == "__main__":
    app.run(debug=True)