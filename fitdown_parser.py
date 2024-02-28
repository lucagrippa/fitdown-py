import re
from datetime import datetime

def parse(raw_text):
    # Initialize an empty list to store parsed rows
    rows = []
    # Initialize variables for exercise and date
    exercise = None
    date = None

    # Helper function to check if a line contains a specific symbol
    def contains(line, symbol):
        return symbol in line

    # Helper function to parse poundage from a line
    def parse_poundage(line):
        # Use regular expression to find poundage in the format '[number]lb'
        return int(re.search(r'\d+lb', line).group(0).replace("lb", ""))

    # Iterate through each line in the raw text
    for line in raw_text.split("\n"):
        # Remove leading and trailing whitespaces from the line
        line = line.strip()

        # If the line contains '@', parse reps, poundage, and notes
        if contains(line, "@"):
            reps, poundage, multiplier, notes = None, None, None, None
            # Split the line at '@'
            before_at, after_at = map(str.strip, line.split("@"))
            before_at_lower = before_at.lower()

            # Check if 'x' is present in the first part of the line
            if "x" in before_at_lower:
                before_x, after_x = before_at_lower.split("x")
                multiplier = int(before_x)
                reps = int(after_x)
            else:
                # If 'x' is not present, set multiplier to 1 and parse reps
                multiplier = 1
                reps = int(before_at)

            # Find numbers after '@' using regular expression
            numbers_after_at = re.findall(r'\d+', after_at)
            poundage = int(numbers_after_at[0])

            # Create a dictionary representing the row
            row = {"exercise": exercise, "reps": reps, "poundage": poundage}

            # Check if there is text after numbers
            has_text_after_numbers = len(numbers_after_at[0]) < len(after_at)
            if has_text_after_numbers:
                # Extract text after numbers and assign it to 'notes' or 'exercise' field
                text_after_numbers = after_at[len(numbers_after_at[0]):].strip()

                # check if exercise is already assigned
                if exercise:
                    # this is a multi-line exercise
                    # check if the "notes" is just "lb"
                    if text_after_numbers == "lb":
                        # if so, continue to the next line
                        continue
                    row["notes"] = text_after_numbers
                else:
                    # this is a single line exercise
                    row["exercise"] = text_after_numbers

                row["notes" if exercise else "exercise"] = text_after_numbers

            # Assign date to the row if it exists
            if date:
                row["date"] = date

            # Add the row to the list, repeating it 'multiplier' times
            rows.extend([row] * multiplier)
        # If the line contains 'Workout', parse the date
        elif contains(line, "Workout"):
            # Extract the date string and convert it to the desired format
            date_str = line.replace("Workout", "").strip()
            date = datetime.strptime(date_str, "%B %d, %Y").strftime("%m/%d/%Y")
        # If the line contains 'lb', parse poundage
        elif contains(line, "lb"):
            # Create a row with exercise, notes, and poundage
            rows.append({"exercise": exercise, "notes": line, "poundage": parse_poundage(line)})
        # If the line is empty, reset the exercise variable
        elif not line:
            exercise = None
        else:
            # Otherwise, the line represents the exercise name
            exercise = line

    # Return the list of parsed rows
    return rows
