from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss": {
        "factor": 22,
        "description": "High-energy fat loss plan with cardio and strength balance",
    },
    "Muscle Gain": {
        "factor": 35,
        "description": "Hypertrophy-focused strength plan for lean mass gain",
    },
    "Beginner": {
        "factor": 26,
        "description": "Entry-level full-body plan for technique and consistency",
    },
}


def calculate_daily_calories(weight_kg, program_name):
    if weight_kg is None or weight_kg <= 0:
        raise ValueError("Weight must be greater than 0 kg.")

    normalized_name = program_name.strip()
    if normalized_name not in PROGRAMS:
        raise ValueError(f"Program '{program_name}' is not supported.")

    return int(float(weight_kg) * PROGRAMS[normalized_name]["factor"])


def get_client_summary(name, age, weight_kg, program_name):
    cleaned_name = (name or "").strip()
    if not cleaned_name:
        raise ValueError("Client name is required.")

    if age is None or age <= 0:
        raise ValueError("Age must be a positive number.")

    calories = calculate_daily_calories(weight_kg, program_name)

    return {
        "name": cleaned_name,
        "age": int(age),
        "weight_kg": float(weight_kg),
        "program": program_name,
        "calories_per_day": calories,
        "description": PROGRAMS[program_name]["description"],
    }


@app.get("/")
def home():
    return jsonify(
        {
            "app": "ACEest Fitness & Gym",
            "status": "ok",
            "programs": list(PROGRAMS.keys()),
        }
    )


@app.get("/programs")
def list_programs():
    return jsonify({"programs": PROGRAMS})


@app.post("/calculate-calories")
def calculate_calories_route():
    payload = request.get_json(silent=True) or {}
    try:
        program = payload.get("program", "")
        weight_kg = float(payload.get("weight_kg", 0))
        calories = calculate_daily_calories(weight_kg, program)
        return jsonify({
            "program": program,
            "weight_kg": weight_kg,
            "calories_per_day": calories,
        })
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/client-summary")
def client_summary_route():
    payload = request.get_json(silent=True) or {}
    try:
        summary = get_client_summary(
            name=payload.get("name", ""),
            age=payload.get("age"),
            weight_kg=payload.get("weight_kg"),
            program_name=payload.get("program", ""),
        )
        return jsonify(summary)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
