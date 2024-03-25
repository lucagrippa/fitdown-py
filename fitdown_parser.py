import re
from datetime import datetime
from fitdown_parser import parse

def main():
    import json

    # Path to the example_workout.md file
    
    # workout_file = "example_workout.md"
    workout_file = "example_workouts/2024-01-26.md"

    # Read the workout file
    with open(workout_file, "r") as file:
        workout_content = file.read()

    # Parse the workout file
    workout_data = parse(workout_content)

    # Print the parsed workout data
    print(json.dumps(workout_data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
