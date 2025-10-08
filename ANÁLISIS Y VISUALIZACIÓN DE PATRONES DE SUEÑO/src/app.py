from flask import Flask, render_template, request
from utils.dataProcessing import calculateRoutineLevel
import pandas as pd
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/routine", methods=['POST'])
def recommendation():
    # Transformar datos ingresados por el usuario a un DataFrame
    df = pd.DataFrame({
        'Age': [int(request.form['age'])],
        'Gender': [request.form['gender']],
        'Sleep Quality': [int(request.form['sleep_quality'])],
        'Bedtime': [request.form['sleep_time']],
        'Daily Steps': [int(request.form['daily_steps'])],
        'Calories Burned': [int(request.form['calories_burned'])],
        'Physical Activity Level': [request.form['activity_level']],
        'Dietary Habits': [request.form['eating_habits']],
        'Sleep Disorders': [request.form['sleep_disorder']],
        'Medication Usage': [request.form['medication']],
        'Sleep Duration': [float(request.form['sleep_quality'])],
        'Stress Level': [int(request.form['stress_level'])],
        'BMI Category': [request.form['bmi']],
        'Heart Rate': [int(request.form['heart_rate'])],
        'BP_Diastolic': [int(request.form['blood_pressure_diastolic'])],
        'BP_Systolic': [int(request.form['blood_pressure_systolic'])]
    })

    # Leer rutinas
    path = "ANÁLISIS Y VISUALIZACIÓN DE PATRONES DE SUEÑO/data/routines.json"
    with open(path, "r", encoding="utf-8") as f:
        routines = json.load(f)

    # Definir rutina en base a los datos ingresados
    routineLevel = calculateRoutineLevel(df.iloc[0])
    userRoutine = routines[routineLevel]

    return render_template("routine.html", data=userRoutine)


if __name__ == "__main__":
    app.run(debug=True)
