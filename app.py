from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmr(gender, weight, height, age):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender")

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "super active": 1.9
    }
    return bmr * activity_multipliers.get(activity_level.lower(), 1.2)

def calculate_caloric_intake(tdee, weight_loss_rate):
    caloric_deficit = weight_loss_rate * 7700 / 7
    return tdee - caloric_deficit

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        gender = request.form["gender"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        age = int(request.form["age"])
        activity_level = request.form["activity_level"]
        weight_loss_rate = float(request.form["weight_loss_rate"])
        
        try:
            bmr = calculate_bmr(gender, weight, height, age)
            tdee = calculate_tdee(bmr, activity_level)
            caloric_intake = calculate_caloric_intake(tdee, weight_loss_rate)
            result = {
                "bmr": round(bmr, 2),
                "tdee": round(tdee, 2),
                "caloric_intake": round(caloric_intake, 2),
                "weight_loss_rate": weight_loss_rate
            }
        except ValueError as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
