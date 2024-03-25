import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

from fitdown_parser import parse

def calculate_workouts_per_year(workouts_folder):
    logging.info(f"Calculating workouts per year in {workouts_folder}")
    workouts = os.listdir(workouts_folder)

    # Each workout file has the data of the workout in the filename ex. 2022-01-01.md
    # calculate the number of workouts per year
    workouts_per_year = {}
    for workout in workouts:
        workout_date = workout.split(".")[0]
        workout_date = datetime.strptime(workout_date, "%Y-%m-%d")
        year = workout_date.year

        if year in workouts_per_year:
            workouts_per_year[year] += 1
        else:
            workouts_per_year[year] = 1

    return workouts_per_year


def calculate_workouts_per_month(workouts_folder):
    logging.info(f"Calculating workouts per month in {workouts_folder}")
    workouts = os.listdir(workouts_folder)

    # Each workout file has the data of the workout in the filename ex. 2022-01-01.md
    # calculate the number of workouts per month
    workouts_per_month = {}
    for workout in workouts:
        workout_date = workout.split(".")[0]
        workout_date = datetime.strptime(workout_date, "%Y-%m-%d")
        month = workout_date.month

        if month in workouts_per_month:
            workouts_per_month[month] += 1
        else:
            workouts_per_month[month] = 1

    return workouts_per_month
    

def calculate_workouts_per_week(workouts_folder):
    logging.info(f"Calculating workouts per week in {workouts_folder}")
    workouts = os.listdir(workouts_folder)

    # Each workout file has the data of the workout in the filename ex. 2022-01-01.md
    # calculate the number of workouts per week
    workouts_per_week = {}
    for workout in workouts:
        workout_date = workout.split(".")[0]
        workout_date = datetime.strptime(workout_date, "%Y-%m-%d")
        week = workout_date.isocalendar()[1]

        if week in workouts_per_week:
            workouts_per_week[week] += 1
        else:
            workouts_per_week[week] = 1

    return workouts_per_week


def calculate_streak(workouts_per_week, target_workouts_per_week):
    logging.info(f"Calculating streak of working out {target_workouts_per_week} times a week")
    # calculate my current streak of working out 3 times a week
    # a streak means that I have worked out 3 times a week for a consecutive number of weeks
    previous_week = None  # Track the previous week number
    streak = 0  # Track the streak of consecutive weeks

    # sort the weeks in descending order
    weeks = sorted(workouts_per_week.keys(), reverse=True)

    for week in weeks:
        if (previous_week is None or week == previous_week - 1) and workouts_per_week[week] >= target_workouts_per_week:
            streak += 1
            previous_week = week
        else:
            break

    return streak


def aggregate_exercises(workouts_folder):
    logging.info(f"Aggregating exercises in {workouts_folder}")
    workouts = os.listdir(workouts_folder)
    all_exercises = {}
    for workout in workouts:
        workout_file = os.path.join(workouts_folder, workout)
        logging.info(f"Aggregating exercises in {workout_file}")
        with open(workout_file, "r") as file:
            workout_content = file.read()

        # Parse the workout file
        workout_data = parse(workout_content)

        for item in workout_data:
            exercise = item["exercise"]
            if exercise in all_exercises:
                all_exercises[exercise].append(item)
            else:
                all_exercises[exercise] = [item]

    return all_exercises


def get_personal_best(sets):
    return max([set["poundage"] for set in sets])


def get_sets_by_date(sets):
    sets_by_date = {}
    for set in sets:
        date = set["date"]
        if date in sets_by_date:
            sets_by_date[date].append(set)
        else:
            sets_by_date[date] = [set]

    return sets_by_date


def get_most_recent_highest_weight(sets):
    logging.info(f"Calculating most recent highest weight")
    # sets = sorted(sets, key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"), reverse=True)

    # group the sets by date
    sets_by_date = get_sets_by_date(sets)

    # get the most recent date
    most_recent_date = sorted(sets_by_date.keys(), key=lambda x: datetime.strptime(x, "%m/%d/%Y"), reverse=True)[0]

    # get the highest weight for the most recent date
    most_recent_sets = sets_by_date[most_recent_date]
    highest_weight = max([set["poundage"] for set in most_recent_sets])

    return highest_weight


def get_second_most_recent_highest_weight(sets):
    logging.info(f"Calculating second most recent highest weight")
    # group the sets by date
    sets_by_date = get_sets_by_date(sets)

    # get the most recent date
    second_most_recent_date = sorted(sets_by_date.keys(), key=lambda x: datetime.strptime(x, "%m/%d/%Y"), reverse=True)[1]

    # get the highest weight for the most recent date
    most_recent_sets = sets_by_date[second_most_recent_date]
    highest_weight = max([set["poundage"] for set in most_recent_sets])

    return highest_weight


def get_percentage_difference(most_recent, second_most_recent):
    logging.info(f"Calculating percentage difference between {most_recent} and {second_most_recent}")
    # check for division by zero
    if second_most_recent == 0:
        return 0.0
    
    return ((most_recent - second_most_recent) / second_most_recent) * 100


def calculate_exercise_statistics(all_exercises):
    logging.info(f"Calculating exercise statistics")
    exercise_statistics = {}
    for exercise, sets in all_exercises.items():
        number_of_sets = len(sets)
        personal_best = get_personal_best(sets)
        most_recent = get_most_recent_highest_weight(sets)
        second_most_recent = get_second_most_recent_highest_weight(sets)
        percentage_difference = get_percentage_difference(most_recent, second_most_recent)

        exercise_statistics[exercise] = {
            "number_of_sets": number_of_sets,
            "personal_best": personal_best,
            "most_recent": most_recent,
            "second_most_recent": second_most_recent,
            "percentage_difference": percentage_difference
        }

    return exercise_statistics


def create_month_table(workouts_per_month):
    logging.info(f"Creating markdown table for workouts per month")
    # List of months in order
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Create markdown table
    markdown_table = "| " + " | ".join(months) + " |\n"
    markdown_table += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    markdown_table += "| " + " | ".join(str(workouts_per_month.get(month, '')) for month in range(1, 13)) + " |\n"

    return markdown_table

def create_week_bar_chart(workouts_per_week):
    logging.info(f"Creating bar chart for workouts per week")
    # Create a bar chart of the number of workouts per week
    bar_chart = ""
    # Determine the maximum number of workouts in a week
    max_workouts = 7
    # Define the length of the bar chart
    chart_length = 7

    # Sort the keys (weeks) numerically
    sorted_workouts_per_week = sorted(workouts_per_week.keys())
    for week in sorted_workouts_per_week:
        count = workouts_per_week[week]

        # Calculate the length of the bar for the current week
        bar_length = int((count / max_workouts) * chart_length)
        # Create the bar chart representation
        bar = "#" * bar_length + "-" * (chart_length - bar_length)
        # Write the week number and the bar chart representation to the markdown file
        bar_chart += f"- Week {week}: {bar} ({count} workouts)\n"

    return bar_chart


def write_to_markdown(statistics_file, target_workouts_per_week, workouts_per_week, workouts_per_month, workouts_per_year, streak, exercise_statistics):
    logging.info(f"Writing statistics to markdown file {statistics_file}")
    # Write statistics to markdown file
    with open(statistics_file, 'w') as file:
        file.write("# Workout Statistics\n\n")

        file.write(f"## 🔥 {streak} week(s) streak 🔥 \n\n")

        file.write("## Workouts per Week\n")
        bar_chart = create_week_bar_chart(workouts_per_week)
        file.write(bar_chart)

        # Sort the keys (weeks) numerically
        # sorted_workouts_per_week = sorted(workouts_per_week.keys())
        # for week in sorted_workouts_per_week:
        #     count = workouts_per_week[week]
        #     if count < target_workouts_per_week:
        #         file.write(f"- Week {week}: {count} workouts ❌\n")
        #     else:
        #         file.write(f"- Week {week}: {count} workouts ✅\n")
        file.write("\n")

        file.write("## Workouts per Month\n")
        workouts_per_month_table = create_month_table(workouts_per_month)
        file.write(workouts_per_month_table)

        # for month, count in workouts_per_month.items():
        #     if count < target_workouts_per_week * 4:
        #         file.write(f"- Month {month}: {count} workouts ❌\n")
        #     else:
        #         file.write(f"- Month {month}: {count} workouts ✅\n")
        file.write("\n")

        file.write("## Workouts per Year\n")
        for year, count in workouts_per_year.items():
            if count < target_workouts_per_week * 52:
                file.write(f"- Year {year}: {count} workouts ❌\n")
            else:
                file.write(f"- Year {year}: {count} workouts ✅\n")
        file.write("\n")


        file.write("## Exercise Specific Metrics\n")
        for exercise, stats in exercise_statistics.items():
            file.write(f"\n### {exercise}\n")

            most_recent_weight = f"- Most Recent Weight: {stats['most_recent']} lbs "

            if stats['percentage_difference'] < 0:
                most_recent_weight += f"({'{0:.2f}'.format(stats['percentage_difference'])}% 👎)"
            else:
                most_recent_weight += f"({'{0:.2f}'.format(stats['percentage_difference'])}% 👍)"

            file.write(most_recent_weight + "\n")
            
            file.write(f"- Most Recent Weight: {stats['most_recent']} lbs\n")
            file.write(f"- Number of Sets: {stats['number_of_sets']}\n")
            file.write(f"- Personal Best: {stats['personal_best']} lbs 💪\n")

def calculate_statistics(workouts_folder, target_workouts_per_week, statistics_file):
    logging.info(f"Calculating statistics for workouts in {workouts_folder}")
    workouts_per_week = calculate_workouts_per_week(workouts_folder)
    workouts_per_month = calculate_workouts_per_month(workouts_folder)
    workouts_per_year = calculate_workouts_per_year(workouts_folder)

    # TODO: What happens when a new year starts? The streak should not reset to 0
    streak = calculate_streak(workouts_per_week, target_workouts_per_week)

    all_exercises = aggregate_exercises(workouts_folder)
    exercise_statistics = calculate_exercise_statistics(all_exercises)

    write_to_markdown(statistics_file, target_workouts_per_week, workouts_per_week, workouts_per_month, workouts_per_year, streak, exercise_statistics)
    
def test():
    load_dotenv()  # take environment variables from .env.

    # Path to the folder containing workout markdown files
    workouts_folder = os.getenv("WORKOUTS_FOLDER")

    target_workouts_per_week = 3

    workouts_per_week = calculate_workouts_per_week(workouts_folder)
    print("Workouts per week")
    print(json.dumps(workouts_per_week, indent=4, sort_keys=True))

    workouts_per_month = calculate_workouts_per_month(workouts_folder)
    print("Workouts per month")
    print(json.dumps(workouts_per_month, indent=4, sort_keys=True))

    workouts_per_year = calculate_workouts_per_year(workouts_folder)
    print("Workouts per year")
    print(json.dumps(workouts_per_year, indent=4, sort_keys=True))

    # TODO: What happens when a new year starts? The streak should not reset to 0
    streak = calculate_streak(workouts_per_week, target_workouts_per_week)
    print(f"Streak: {streak} weeks")

    all_exercises = aggregate_exercises(workouts_folder)
    # print(json.dumps(all_exercises, indent=4, sort_keys=True))

    exercise_statistics = calculate_exercise_statistics(all_exercises)
    print(json.dumps(exercise_statistics, indent=4, sort_keys=True))

    statistics_file = "workout_statistics_3.md"
    write_to_markdown(statistics_file, target_workouts_per_week, workouts_per_week, workouts_per_month, workouts_per_year, streak, exercise_statistics)


def main():
    load_dotenv()  # take environment variables from .env.

    # parse command line args to run calculate_statistics function
    import argparse
    parser = argparse.ArgumentParser(description='Calculate workout statistics')
    parser.add_argument('--workouts_folder', type=str, help='Path to the folder containing workout markdown files')
    parser.add_argument('--target_workouts_per_week', type=int, help='Target number of workouts per week')
    parser.add_argument('--statistics_file', type=str, help='Path to the markdown file to write the statistics to')
    args = parser.parse_args()

    calculate_statistics(args.workouts_folder, args.target_workouts_per_week, args.statistics_file)

    # test()



if __name__ == "__main__":
    main()  
