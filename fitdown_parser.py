import re
from datetime import datetime

def parse(workout_text):
    total_sets = []
    current_date = None
    current_exercise = None

    # split raw text by on newlines
    for line in workout_text.split("\n"):
        # remove leading and trailing white space
        line = line.strip()
        # skip empty lines
        if not line:
            current_exercise = None
            continue

        # Match workout date
        date_match = re.match(r'^Workout (\w+ \d{1,2}, \d{4})$', line)
        if date_match:
            # save the current date
            date_str = date_match.group(1)
            current_date = datetime.strptime(date_str, "%B %d, %Y").strftime("%m/%d/%Y")
            continue
        
        # Match exercise name
        exercise_match = re.match(r'^(\w[\w\s]+)$', line)
        # If the line matches the exercise name pattern and there's a current date
        if exercise_match and current_date:  
            current_exercise = exercise_match.group(1).lower()
            continue

        # Match sets, repetitions, notes, and single line exercises
        if "@" in line and current_date:
            # Match sets, repetitions, and weight
            set_match = re.match(r'^(\d+(?:x\d+)?)\s*@\s*([\d.]+)\s*(lb|kg)\s*(.*)$', line)
            if set_match and current_exercise:
                sets_reps = set_match.group(1)
                weight = set_match.group(2)
                unit = set_match.group(3)
                notes = set_match.group(4).strip()
                
                # Handle 'x' notation for sets and repetitions
                if 'x' in sets_reps:
                    sets, reps = map(int, sets_reps.split('x'))
                else:
                    sets = 1
                    reps = int(sets_reps)
                
                # Append the extracted information to the total_sets list
                exercise_set = {
                    "date": current_date,
                    "exercise": current_exercise,
                    "reps": reps,
                    "weight": float(weight),
                    "unit": unit,
                    "notes": notes
                }

                total_sets.extend([exercise_set] * int(sets))
            else:
                # Match single line exercises
                single_line_match = re.match(r'^([\d]+(?:x\d+)?\s*@\s*[\d.]+\s*(lb|kg)?)\s*([\w\s]+)$', line)
                if single_line_match:
                    sets_reps_weight = single_line_match.group(1)
                    unit = single_line_match.group(2)
                    exercise = single_line_match.group(3).strip().lower()
                    
                    # Handle 'x' notation for sets and repetitions
                    if 'x' in sets_reps_weight:
                        sets_reps = sets_reps_weight.split('@')[0].strip()
                        sets, reps = map(int, sets_reps.split('x'))
                    else:
                        sets = 1
                        reps = int(sets_reps_weight.split('@')[0].strip())
                    
                    # Extract weight
                    weight = float(sets_reps_weight.split('@')[1].split(unit)[0].strip())
                    
                    # Append the extracted information to the total_sets list
                    exercise_set = {
                        "date": current_date,
                        "exercise": exercise,
                        "reps": reps,
                        "weight": weight,
                        "unit": unit,
                        "notes": ""
                    }
                    total_sets.extend([exercise_set] * int(sets))

    return total_sets

def main():
    import json
    # Path to the example_workout.md file
    # workout_file = "example_workout.md"
    workout_file = "2024-02-26.md"

    # Read the workout file
    with open(workout_file, "r") as file:
        workout_content = file.read()

    # Parse the workout file
    workout_data = parse(workout_content)

    # Print the parsed workout data
    print(json.dumps(workout_data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
